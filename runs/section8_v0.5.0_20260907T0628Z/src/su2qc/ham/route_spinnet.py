"""Route 1: analytic spin-network / dressed-site Hamiltonian for SU(2) single plaquette
with dynamical two-color staggered fermions.

Basis: ((j1,j2,j3,j4), (n1,n2,n3,n4), tag) where:
  j_l in {0, 1/2} (jmax=0.5) or {0, 1/2, 1} (jmax=1) as floats
  n_v in {0,1,2} with gauge-invariant constraints per vertex
  tag = 0 (always for 2-valent vertices)

Gauge invariance at each 2-valent vertex with incident link spins (j_a, j_b) and matter n_v:
  - if j_a == j_b:     n_v in {0, 2}  (vacuum or baryon)
  - if |j_a - j_b| == 1/2: n_v = 1  (doublet)
  - if |j_a - j_b| == 1:     NOT allowed (projected out, only jmax=1)

Hamiltonian: H = H_elec + H_mass + H_hop + H_mag

eta = (+1, -1, +1, +1) per link l1..l4.
Staggered vacuum: n_vac = (0,2,0,2).  Vertices v1..v4 at (0,0),(1,0),(1,1),(0,1).
Links: l1:v1->v2, l2:v2->v3, l3:v4->v3, l4:v1->v4.
Plaquette: U_box = U_l1 U_l2 U_l3^dag U_l4^dag (counter-clockwise v1->v2->v3->v4->v1).
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from scipy.sparse import csr_matrix, lil_matrix
from scipy.linalg import eigh

# ---- conventions ----
SRC = Path(__file__).resolve().parents[2]  # .../su2qc
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
import su2qc.conventions as cv

# Shortcuts
ETA   = cv.ETA          # (+1, -1, +1, +1)
PARITY = cv.PARITY      # (+1, -1, +1, -1)
LINKS  = cv.LINKS       # ((0,1,"x"), (1,2,"y"), (3,2,"x"), (0,3,"y"))
VERTICES = cv.VERTICES  # ((0,0),(1,0),(1,1),(0,1))
N_VERTICES = cv.N_VERTICES
N_VAC  = cv.N_VAC       # (0, 2, 0, 2)

# Link source/target (python indices 0..3)
LINK_ST = [(l[0], l[1]) for l in LINKS]  # (source, target)


def _cg_half(j: float, m: float, s: int, jp: float, mp: float) -> float:
    """Closed-form CG(j,m;1/2,s/2|jp,mp), with no symbolic dependency."""
    if abs(mp - (m + 0.5*s)) > 1e-12:
        return 0.0
    if abs(jp - (j + 0.5)) < 1e-12:
        return np.sqrt(max(0.0, (j + (m if s == 1 else -m) + 1.0) / (2.0*j + 1.0)))
    if abs(jp - (j - 0.5)) < 1e-12 and j > 0:
        return (-np.sqrt(max(0.0, (j - m) / (2.0*j + 1.0)))
                if s == 1 else np.sqrt(max(0.0, (j + m) / (2.0*j + 1.0))))
    return 0.0


def _mvalues(j: float) -> tuple[float, ...]:
    return tuple(-j + k for k in range(int(round(2.0*j)) + 1))


def _vertex_state(ja: float, jb: float, n: int) -> np.ndarray:
    """Unit-norm invariant vertex state as an array (da, db, 4).

    All three indices are state-type (each transforms with +J); the tensor is
    the unique singlet of V_ja x V_jb x V_matter(n):
      n=0/2 (needs ja==jb): metric tensor (-1)^(ja-ma) delta_{ma,-mb}/sqrt(2ja+1)
        with fermion Fock f=0 (n=0) or f=3 (n=2);
      n=1 (needs |ja-jb|=1/2): T[ma,mb,c] = (-1)^(ja+ma) *
        CG(jb, mb; 1/2, s_c | ja, -ma), s_c=+1 for c=0, -1 for c=1;
        Fock f = 1 (c=0 occupied) or 2 (c=1 occupied); unit-normalized.
    Fock basis: f = n_c0 + 2 n_c1.
    """
    ma, mb = _mvalues(ja), _mvalues(jb)
    out = np.zeros((len(ma), len(mb), 4), dtype=float)
    if n in (0, 2):
        if abs(ja - jb) > 1e-12:
            return out
        f = 0 if n == 0 else 3
        for a, x in enumerate(ma):
            for b, y in enumerate(mb):
                if abs(x + y) < 1e-12:
                    out[a, b, f] = (-1.0) ** int(round(ja - x)) / np.sqrt(2.0*ja + 1.0)
        return out
    if n != 1 or abs(abs(ja - jb) - 0.5) > 1e-12:
        return out
    for a, x in enumerate(ma):
        for b, y in enumerate(mb):
            for c, s in enumerate((1, -1)):
                out[a, b, 1 if c == 0 else 2] = \
                    ((-1.0) ** int(round(ja + x))) * _cg_half(jb, y, s, ja, -x)
    norm = np.sqrt(np.sum(out * out))
    if norm > 0.0:
        out /= norm
    return out


# 4-dim site-Fock operators (f = n_c0 + 2 n_c1); bare sigma^+/- and Z per color.
def _sigma_plus(c: int) -> np.ndarray:
    out = np.zeros((4, 4))
    for f in range(4):
        if not f & (1 << c):
            out[f | (1 << c), f] = 1.0
    return out


def _sigma_minus(c: int) -> np.ndarray:
    return _sigma_plus(c).T


def _zc(c: int) -> np.ndarray:
    return np.diag([(-1.0) ** ((f >> c) & 1) for f in range(4)])


# Link-end insertion matrices (convention fixed by the Gauss law of the
# redundant KS formulation: the L (source) color index is conjugated).
# alpha color c: c=0 <-> spin +1/2, c=1 <-> spin -1/2.
def _end_insertion(j: float, jp: float, c: int, end: str,
                   dagger: bool = False) -> np.ndarray:
    """Matrix (2jp+1)x(2j+1) taking the link-end m index from j to jp.

    L end (source vertex): entry[m',m] = sign_c * CG(j,m;1/2,-s_c|jp,m')
    R end (target vertex): entry[m',m] = CG(j,m;1/2,+s_c|jp,m')
    with s_c = +1 for c=0, -1 for c=1; sign_c = +1 for c=0, -1 for c=1.
    The sqrt((2j+1)/(2j'+1)) Wigner prefactor is NOT included here; it is
    applied once per link in the amplitude assembly.
    dagger=True returns the conjugate-transposed insertion of the reverse
    transition (for U^dagger links).
    """
    if dagger:
        return _end_insertion(jp, j, c, end, False).T
    mj, mjp = _mvalues(j), _mvalues(jp)
    out = np.zeros((len(mjp), len(mj)))
    s = 1 if c == 0 else -1
    for b, m in enumerate(mj):
        for a, mp in enumerate(mjp):
            if end == "L":
                out[a, b] = (1.0 if c == 0 else -1.0) * _cg_half(j, m, -s, jp, mp)
            else:
                out[a, b] = _cg_half(j, m, s, jp, mp)
    return out


_VLINKS = ((3, 0), (0, 1), (1, 2), (2, 3))  # vertex v -> (link_a, link_b)
# which rotor index of link l lives at vertex v: "L" if v is source else "R"
_VEND = tuple(tuple("L" if LINK_ST[l][0] == v else "R" for l in _VLINKS[v])
              for v in range(4))


def _vertex_overlap2(ja, jb, n_old, ja2, jb2, n_new,
                     ins_a=None, ins_b=None, fop=None) -> float:
    """<T'(ja2,jb2,n_new)| (ins_a x ins_b x fop) |T(ja,jb,n_old)>."""
    T = _vertex_state(ja, jb, n_old)
    T2 = _vertex_state(ja2, jb2, n_new)
    A = ins_a if ins_a is not None else np.eye(len(_mvalues(ja)))
    B = ins_b if ins_b is not None else np.eye(len(_mvalues(jb)))
    F = fop if fop is not None else np.eye(4)
    out = np.einsum("abf,ax,by,fg,xyg->", T2, A, B, F, T)
    return float(out)


def _fermion_sign(source: int, target: int, n: tuple[int, int, int, int]) -> float:
    """Parity of the middle sites for psi^dag_source ... psi_target (v-ordered)."""
    s, t = source, target
    lo, hi = (s, t) if s < t else (t, s)
    return (-1.0) ** sum(n[k] for k in range(lo + 1, hi))



def _check_vertex_gauge_invariant(n_vals: tuple[int, int, int, int],
                                   j_tuple: tuple[float, float, float, float]) -> bool:
    """Check whether a full matter assignment satisfies all 4 vertex gauge-invariants.

    For vertex v with incident link spins (j_a, j_b):
      - j_a == j_b     => n_v in {0, 2}
      - |j_a - j_b| == 1/2 => n_v = 1
      - |j_a - j_b| == 1   => forbidden (projected out)
    """
    j1, j2, j3, j4 = j_tuple
    n1, n2, n3, n4 = n_vals

    # v1: links l4, l1  -> j4, j1
    ja, jb = j4, j1
    if ja == jb:
        if n1 not in (0, 2):
            return False
    elif abs(ja - jb) == 0.5:
        if n1 != 1:
            return False
    elif abs(ja - jb) == 1.0:
        return False
    else:
        return False

    # v2: links l1, l2  -> j1, j2
    ja, jb = j1, j2
    if ja == jb:
        if n2 not in (0, 2):
            return False
    elif abs(ja - jb) == 0.5:
        if n2 != 1:
            return False
    elif abs(ja - jb) == 1.0:
        return False

    # v3: links l2, l3  -> j2, j3
    ja, jb = j2, j3
    if ja == jb:
        if n3 not in (0, 2):
            return False
    elif abs(ja - jb) == 0.5:
        if n3 != 1:
            return False
    elif abs(ja - jb) == 1.0:
        return False

    # v4: links l3, l4  -> j3, j4
    ja, jb = j3, j4
    if ja == jb:
        if n4 not in (0, 2):
            return False
    elif abs(ja - jb) == 0.5:
        if n4 != 1:
            return False
    elif abs(ja - jb) == 1.0:
        return False

    return True


def enumerate_basis(jmax: float) -> list[tuple]:
    """Return list of basis labels ((j1,j2,j3,j4), (n1,n2,n3,n4), 0) for the given jmax.

    The basis is constructed by iterating all allowed link spins and then, for each,
    all matter assignments that satisfy the 4 vertex constraints.
    """
    if jmax == 0.5:
        j_vals = [0.0, 0.5]
    elif jmax == 1.0:
        j_vals = [0.0, 0.5, 1.0]
    else:
        raise ValueError(f"Unsupported jmax={jmax}; use 0.5 or 1.0")

    basis = []
    for j1 in j_vals:
        for j2 in j_vals:
            for j3 in j_vals:
                for j4 in j_vals:
                    jt = (j1, j2, j3, j4)
                    # Determine allowed n values for each vertex
                    # v1: n1 allowed if j4==j1 -> {0,2}; |j4-j1|==1/2 -> n1=1
                    if j4 == j1:
                        n1_opts = [0, 2]
                    elif abs(j4 - j1) == 0.5:
                        n1_opts = [1]
                    elif abs(j4 - j1) == 1.0:
                        n1_opts = []
                    else:
                        n1_opts = []

                    if n1_opts == []:
                        continue

                    if j1 == j2:
                        n2_opts = [0, 2]
                    elif abs(j1 - j2) == 0.5:
                        n2_opts = [1]
                    elif abs(j1 - j2) == 1.0:
                        n2_opts = []
                    else:
                        n2_opts = []

                    if n2_opts == []:
                        continue

                    if j2 == j3:
                        n3_opts = [0, 2]
                    elif abs(j2 - j3) == 0.5:
                        n3_opts = [1]
                    elif abs(j2 - j3) == 1.0:
                        n3_opts = []
                    else:
                        n3_opts = []

                    if n3_opts == []:
                        continue

                    if j3 == j4:
                        n4_opts = [0, 2]
                    elif abs(j3 - j4) == 0.5:
                        n4_opts = [1]
                    elif abs(j3 - j4) == 1.0:
                        n4_opts = []
                    else:
                        n4_opts = []

                    if n4_opts == []:
                        continue

                    for n1 in n1_opts:
                        for n2 in n2_opts:
                            for n3 in n3_opts:
                                for n4 in n4_opts:
                                    # Verify gauge invariance
                                    if not _check_vertex_gauge_invariant((n1, n2, n3, n4), jt):
                                        continue
                                    label = ((j1, j2, j3, j4), (n1, n2, n3, n4), 0)
                                    basis.append(label)
    return basis


# ---- Hamiltonian building blocks ----

def _electric_diag(j_tuple: tuple[float, float, float, float], g2: float) -> float:
    """Electric term: (g2/2) * sum_l j_l(j_l+1).  Diagonal in the basis."""
    return g2 / 2.0 * sum(cv.casimir(j) for j in j_tuple)


def _mass_diag(n_tuple: tuple[int, int, int, int], m: float) -> float:
    """Mass term: m * sum_v parity_v n_v.  Diagonal in the basis."""
    return m * sum(PARITY[v] * n_tuple[v] for v in range(4))


# ---- hopping operator ----

def _hopping_matrix_element(
    j_from: tuple[float, float, float, float],
    n_from: tuple[int, int, int, int],
    link_idx: int,
    j_to: tuple[float, float, float, float],
    n_to: tuple[int, int, int, int],
) -> complex:
    """Matrix element <to| (1/2) eta_l psi^dag_s U_l psi_t |from> for one link.

    Only the forward direction (n_s + 1, n_t - 1) is computed; the caller adds
    the h.c. partner into the transposed entry.
    """
    s, t = LINK_ST[link_idx]  # source, target

    dn_s = n_to[s] - n_from[s]
    dn_t = n_to[t] - n_from[t]
    if not (dn_s == 1 and dn_t == -1):
        return 0.0
    j, jp = j_from[link_idx], j_to[link_idx]
    if abs(abs(j - jp) - 0.5) > 1e-12:
        return 0.0
    pref = np.sqrt((2.0*j + 1.0) / (2.0*jp + 1.0))

    side_s = "above" if s < t else "below"
    side_t = "below" if s < t else "above"
    amp = 0.0
    for ca in range(2):        # color created at s (L end of the link)
        for cb in range(2):    # color annihilated at t (R end)
            Fs = _site_create(ca, side_s)
            Ft = _site_annihilate(cb, side_t)
            insL = _end_insertion(j, jp, ca, "L")
            insR = _end_insertion(j, jp, cb, "R")
            ov_s = _vertex_overlap_at(s, j_from, n_from, j_to, n_to,
                                      {link_idx: insL}, Fs)
            ov_t = _vertex_overlap_at(t, j_from, n_from, j_to, n_to,
                                      {link_idx: insR}, Ft)
            amp += ov_s * ov_t
    return complex(0.5 * ETA[link_idx] * _fermion_sign(s, t, n_from)
                   * pref * amp)


def _site_create(c: int, side: str) -> np.ndarray:
    """Site creation op for color c with the JW Z-string on the given side."""
    op = _sigma_plus(c)
    ks = range(c + 1, 2) if side == "above" else range(0, c)
    for k in ks:
        op = op @ _zc(k)
    return op


def _site_annihilate(c: int, side: str) -> np.ndarray:
    return _site_create(c, side).T


def _vertex_overlap_at(v, j_from, n_from, j_to, n_to, ins_by_link, fop=None):
    la, lb = _VLINKS[v]
    return _vertex_overlap2(j_from[la], j_from[lb], n_from[v],
                            j_to[la], j_to[lb], n_to[v],
                            ins_by_link.get(la), ins_by_link.get(lb), fop)


def _magnetic_matrix_element(j_from, n, j_to) -> complex:
    """<to| Tr(U_l1 U_l2 U_l3^dag U_l4^dag) |from> by four local contractions.

    Color loop: sum_{abcd} U0^{ab} U1^{bc} (U2^dag)^{cd} (U3^dag)^{da}; per
    vertex the two incident link-end insertions carry the loop colors:
      v1: l4(L,a,dag), l1(L,a) | v2: l1(R,b), l2(L,b)
      v3: l2(R,c), l3(R,c,dag) | v4: l3(L,d,dag), l4(R,d,dag)
    Wigner prefactor per link: sqrt((2j+1)/(2j'+1)) for plain links,
    sqrt((2j'+1)/(2j+1)) for daggered links.
    """
    pref = 1.0
    for l in range(4):
        j, jp = j_from[l], j_to[l]
        if abs(abs(j - jp) - 0.5) > 1e-12:
            return 0.0
        if l in (2, 3):
            pref *= np.sqrt((2.0*jp + 1.0) / (2.0*j + 1.0))
        else:
            pref *= np.sqrt((2.0*j + 1.0) / (2.0*jp + 1.0))
    total = 0.0
    for a in range(2):
        for b in range(2):
            for c in range(2):
                for d in range(2):
                    specs = (
                        (0, {3: (a, "L", True), 0: (a, "L", False)}),
                        (1, {0: (b, "R", False), 1: (b, "L", False)}),
                        (2, {1: (c, "R", False), 2: (c, "R", True)}),
                        (3, {2: (d, "L", True), 3: (d, "R", True)}),
                    )
                    product = 1.0
                    for v, spec in specs:
                        ins = {l: _end_insertion(j_from[l], j_to[l], col, end,
                                                 dag)
                               for l, (col, end, dag) in spec.items()}
                        product *= _vertex_overlap_at(v, j_from, n, j_to, n,
                                                      ins)
                        if product == 0.0:
                            break
                    total += product
    return complex(pref * total)


def build_hamiltonian(g2: float, m: float, jmax: float) -> tuple[csr_matrix, list]:
    """Build the full route-1 Hamiltonian for the single plaquette.

    Returns (H_sparse, basis) where basis is the list of labels in the same order
    as the matrix rows/cols.

    Physics:
      H = H_elec + H_mass + H_hop + H_mag
      H_elec = (g2/2) sum_l j_l(j_l+1)                     (diagonal)
      H_mass = m sum_v parity_v n_v                          (diagonal, parity=+ - + -)
      H_hop  = (1/2) sum_l ( eta_l psi^dag_{s(l)} U_l psi_{t(l)} + h.c. )  (off-diagonal)
      H_mag  = -(1/(2g2)) Tr(U_box + U_box^dag)            (off-diagonal)
    """
    basis = enumerate_basis(jmax)
    dim = len(basis)

    # Map label -> row index for O(1) lookups
    label_to_idx = {lab: i for i, lab in enumerate(basis)}

    # Sparse matrix in LIL format for easy insertion
    H = lil_matrix((dim, dim), dtype=complex)

    # ----- Electric term (diagonal) -----
    for i, (j_tuple, n_tuple, _) in enumerate(basis):
        H[i, i] = _electric_diag(j_tuple, g2)

    # ----- Mass term (diagonal) -----
    for i, (j_tuple, n_tuple, _) in enumerate(basis):
        H[i, i] += _mass_diag(n_tuple, m)

    # ----- Hopping term (off-diagonal) -----
    for i, (j_from, n_from, _) in enumerate(basis):
        for link_idx in range(4):
            s, t = LINK_ST[link_idx]

            # Direction A: psi^dag_s U_l psi_t  (n_s+1, n_t-1, j_l -> j_l +- 1/2)
            nA = list(n_from)
            nA[s] += 1
            nA[t] -= 1
            if 0 <= nA[s] <= 2 and 0 <= nA[t] <= 2:
                for dj in (0.5, -0.5):
                    jA = list(j_from)
                    jA[link_idx] += dj
                    if not (-1e-12 <= jA[link_idx] <= jmax + 1e-12):
                        continue
                    labelA = (tuple(jA), tuple(nA), 0)
                    if labelA in label_to_idx:
                        me = _hopping_matrix_element(j_from, n_from, link_idx,
                                                      tuple(jA), tuple(nA))
                        j_idx = label_to_idx[labelA]
                        H[j_idx, i] += complex(me, 0.0)
                        H[i, j_idx] += np.conjugate(complex(me, 0.0))  # Hermitian

    # ----- Magnetic term (off-diagonal) -----
    # -(1/(2g2)) Tr(U_box + U_box^dag)
    # Flips all four links simultaneously between configurations where every link changes by ±1/2.
    # Matrix element is a product of vertex factors depending on (j_a, j_b, matter state) at each corner.
    # Matter is untouched (diagonal in n).

    for i, (j_from, n_from, _) in enumerate(basis):
        # Enumerate the 16 possible flip sign patterns for the 4 links
        for flip_signs in [(1, 1, 1, 1), (1, 1, 1, -1), (1, 1, -1, 1), (1, 1, -1, -1),
                          (1, -1, 1, 1), (1, -1, 1, -1), (1, -1, -1, 1), (1, -1, -1, -1),
                          (-1, 1, 1, 1), (-1, 1, 1, -1), (-1, 1, -1, 1), (-1, 1, -1, -1),
                          (-1, -1, 1, 1), (-1, -1, 1, -1), (-1, -1, -1, 1), (-1, -1, -1, -1)]:
            j_flipped = list(j_from)
            valid = True
            for li in range(4):
                j_new = j_from[li] + flip_signs[li] * 0.5
                if j_new < 0 or j_new > jmax + 1e-12:
                    valid = False
                    break
                j_flipped[li] = j_new

            if not valid:
                continue

            label_flipped = (tuple(j_flipped), n_from, 0)
            if label_flipped in label_to_idx:
                j_idx = label_to_idx[label_flipped]
                if j_idx <= i:
                    continue
                me = -(1.0 / (2.0 * g2)) * (
                    _magnetic_matrix_element(j_from, n_from, tuple(j_flipped))
                    + np.conjugate(_magnetic_matrix_element(
                        tuple(j_flipped), n_from, j_from)))
                H[i, j_idx] += np.conjugate(me)
                H[j_idx, i] += me

    # Convert to CSR for efficient operations
    H = H.tocsr()

    # Hermiticity check: H should equal H^\dagger
    # (We already enforced it by adding both i,j and j,i)

    return H, basis


def build_hamiltonian_no_magnetic(g2: float, m: float, jmax: float) -> tuple[csr_matrix, list]:
    """Build the Hamiltonian without the magnetic term (electric + mass + hopping only).

    Same basis ordering as build_hamiltonian, useful for limit checks.
    """
    basis = enumerate_basis(jmax)
    dim = len(basis)

    label_to_idx = {lab: i for i, lab in enumerate(basis)}
    j_labels = np.array([lab[0] for lab in basis], dtype=object)
    n_labels = np.array([lab[1] for lab in basis], dtype=object)

    H = lil_matrix((dim, dim), dtype=complex)

    # Electric diagonal
    for i, (j_tuple, n_tuple, _) in enumerate(basis):
        H[i, i] = _electric_diag(j_tuple, g2)

    # Mass diagonal
    for i, (j_tuple, n_tuple, _) in enumerate(basis):
        H[i, i] += _mass_diag(n_tuple, m)

    # Hopping off-diagonal (same logic as in build_hamiltonian)
    for i, (j_from, n_from, _) in enumerate(basis):
        for link_idx in range(4):
            s, t = LINK_ST[link_idx]

            # Direction A: psi^dag_s U_l psi_t  (n_s+1, n_t-1, j_l -> j_l +- 1/2)
            nA = list(n_from)
            nA[s] += 1
            nA[t] -= 1
            if 0 <= nA[s] <= 2 and 0 <= nA[t] <= 2:
                for dj in (0.5, -0.5):
                    jA = list(j_from)
                    jA[link_idx] += dj
                    if not (-1e-12 <= jA[link_idx] <= jmax + 1e-12):
                        continue
                    labelA = (tuple(jA), tuple(nA), 0)
                    if labelA in label_to_idx:
                        me = _hopping_matrix_element(j_from, n_from, link_idx,
                                                      tuple(jA), tuple(nA))
                        j_idx = label_to_idx[labelA]
                        H[j_idx, i] += complex(me, 0.0)
                        H[i, j_idx] += np.conjugate(complex(me, 0.0))

    H = H.tocsr()
    return H, basis


# ---- observables ----

def number_op(v: int):
    """Return the number operator n_v for vertex v (diagonal in the basis).

    The returned function takes (dim, basis) and returns a CSR matrix.
    """
    def _no(dim_: int, basis_: list):
        H = lil_matrix((dim_, dim_), dtype=complex)
        for i, (j_tuple, n_tuple, _) in enumerate(basis_):
            H[i, i] = float(n_tuple[v])
        return H.tocsr()
    return _no


def total_number():
    """Return the total fermion number sum_v n_v (diagonal in the basis)."""
    def _no(dim_: int, basis_: list):
        H = lil_matrix((dim_, dim_), dtype=complex)
        for i, (j_tuple, n_tuple, _) in enumerate(basis_):
            H[i, i] = float(sum(n_tuple))
        return H.tocsr()
    return _no


def casimir_link(l: int):
    """Return the electric casimir operator j_l(j_l+1) for link l (diagonal in the basis)."""
    def _no(dim_: int, basis_: list):
        H = lil_matrix((dim_, dim_), dtype=complex)
        for i, (j_tuple, n_tuple, _) in enumerate(basis_):
            H[i, i] = cv.casimir(j_tuple[l])
        return H.tocsr()
    return _no


# ---- projectors ------

def _charge_projector(charge_tuple: tuple[int, int, int, int],
                      basis: list, dim: int) -> csr_matrix:
    """Projector onto states with given local charges q_v = n_v - n_vac(v).

    Args:
        charge_tuple: (q_v1, q_v2, q_v3, q_v4) where q_v = n_v - n_vac(v)
        basis: list of basis labels
        dim: dimension of the basis
    """
    H = lil_matrix((dim, dim), dtype=complex)
    for i, (j_tuple, n_tuple, _) in enumerate(basis):
        q = tuple(int(n_tuple[v] - N_VAC[v]) for v in range(4))
        if q == charge_tuple:
            H[i, i] = 1.0
    return H.tocsr()


def P_stretched(g2: float, m: float, jmax: float) -> csr_matrix:
    """Projector onto states with q = (+1, -1, 0, 0)."""
    basis = enumerate_basis(jmax)
    dim = len(basis)
    return _charge_projector((1, -1, 0, 0), basis, dim)


def P_short(g2: float, m: float, jmax: float) -> csr_matrix:
    """Projector onto states with q = (+1, -1, 0, 0) — the short sector."""
    basis = enumerate_basis(jmax)
    dim = len(basis)
    return _charge_projector((1, -1, 0, 0), basis, dim)


def P_surv(g2: float, m: float, jmax: float) -> csr_matrix:
    """Projector onto states with q = (+1, -1, 0, 0) (surviving stretched string)."""
    basis = enumerate_basis(jmax)
    dim = len(basis)
    return _charge_projector((1, -1, 0, 0), basis, dim)


def P_meson(g2: float, m: float, jmax: float) -> csr_matrix:
    """Projector onto states with |q_v| = 1 for all v."""
    basis = enumerate_basis(jmax)
    dim = len(basis)
    H = lil_matrix((dim, dim), dtype=complex)
    for i, (j_tuple, n_tuple, _) in enumerate(basis):
        q = tuple(int(n_tuple[v] - N_VAC[v]) for v in range(4))
        if all(abs(qq) == 1 for qq in q):
            H[i, i] = 1.0
    return H.tocsr()


def P_BBbar(g2: float, m: float, jmax: float) -> csr_matrix:
    """Projector onto any state with |q_v| = 2 for some v (takes precedence)."""
    basis = enumerate_basis(jmax)
    dim = len(basis)
    H = lil_matrix((dim, dim), dtype=complex)
    for i, (j_tuple, n_tuple, _) in enumerate(basis):
        q = tuple(int(n_tuple[v] - N_VAC[v]) for v in range(4))
        if any(abs(qq) == 2 for qq in q):
            H[i, i] = 1.0
    return H.tocsr()


# ---- charge from conventions ----
def charge(v: int, n: int) -> int:
    """Local charge relative to the staggered vacuum: q_v = n_v - n_vac(v)."""
    return n - N_VAC[v]


# ---- debugging / validation ----

def validate_dimensions(jmax: float = 0.5) -> dict:
    """Validate that the basis dimension and sector counts match expectations."""
    basis = enumerate_basis(jmax)
    dim = len(basis)

    # Sector dims: count states by total fermion number N = sum n_v
    sector_dims = {0: 0, 2: 0, 4: 0, 6: 0, 8: 0}
    for _, n_tuple, _ in basis:
        N = sum(n_tuple)
        if N in sector_dims:
            sector_dims[N] += 1

    expected_dim = {0.5: 82, 1.0: 152}[jmax]
    expected_sectors = {0.5: {0: 2, 2: 20, 4: 38, 6: 20, 8: 2}, 1.0: None}[jmax]

    result = {
        "jmax": jmax,
        "dim": dim,
        "expected_dim": expected_dim,
        "dim_match": dim == expected_dim,
        "sector_dims": sector_dims,
        "expected_sectors": expected_sectors,
    }
    if expected_sectors:
        for N in range(0, 9, 2):
            result[f"sector_N{N}_match"] = sector_dims.get(N, 0) == expected_sectors.get(N, 0)

    return result


def validate_hermiticity(H: csr_matrix, atol: float = 1e-13) -> dict:
    """Check that H is Hermitian within tolerance."""
    H_arr = H.toarray()
    diff = np.max(np.abs(H_arr - H_arr.T.conj()))
    return {
        "hermitian": diff <= atol,
        "max_diff": float(diff),
    }


def validate_commutator(H: csr_matrix, N_op: csr_matrix, atol: float = 1e-13) -> dict:
    """Check [H, N] = 0 within tolerance."""
    H_arr = H.toarray()
    N_arr = N_op.toarray()
    comm = H_arr @ N_arr - N_arr @ H_arr
    max_comm = np.max(np.abs(comm))
    return {
        "[H,N]": max_comm <= atol,
        "max_comm": float(max_comm),
    }


def pure_electric_check(g2_big: float = 1e6) -> dict:
    """Spectrum at g2 -> inf, m = 0: electric levels with k-degeneracies.

    From limits.py pure_electric_check.
    """
    from su2qc import conventions as cv
    from su2qc.ham.route_spinnet import build_hamiltonian as bh
    H, basis = bh(g2_big, 0.0, 0.5)[:2]
    evals = np.sort(eigh(H.toarray(), eigvals_only=True))
    unit = g2_big / 2.0 * 0.75
    ks = np.rint(evals / unit).astype(int)
    got = [int(np.sum(ks == k)) for k in range(5)]
    rel = np.max(np.abs(evals - ks * unit)) / unit
    ok = got == [16, 16, 18, 16, 16] and rel <= 1e-8 * g2_big / 1e6 * 100
    return {"degeneracies": got, "rel_dev": float(rel), "ok": bool(ok)}


if __name__ == "__main__":
    # Quick validation
    print("=== Validating jmax=0.5 basis ===")
    r = validate_dimensions(0.5)
    print(f"dim={r['dim']} (expected 82): {'OK' if r['dim_match'] else 'FAIL'}")
    for k in [0, 2, 4, 6, 8]:
        print(f"  N={k}: got={r['sector_dims'][k]} expected={r['expected_sectors'][k]} {'OK' if r[f'sector_N{k}_match'] else 'FAIL'}")

    print("\n=== Validating jmax=1.0 basis ===")
    r = validate_dimensions(1.0)
    print(f"dim={r['dim']} (expected 152): {'OK' if r['dim_match'] else 'FAIL'}")

    print("\n=== Hermiticity check (jmax=0.5) ===")
    H, basis = build_hamiltonian(1.0, 0.0, 0.5)
    hcheck = validate_hermiticity(H)
    print(f"Hermitian: {hcheck['hermitian']}, max_diff={hcheck['max_diff']}")

    print("\n=== Pure electric check ===")
    pe = pure_electric_check()
    print(f"degeneracies={pe['degeneracies']} expected=[16,16,18,16,16] ok={pe['ok']}")
