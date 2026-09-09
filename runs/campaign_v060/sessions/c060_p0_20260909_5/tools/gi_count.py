"""Independent classical enumeration of SU(2) Kogut-Susskind gauge-invariant
state counts, written from the frozen conventions only.

Session: c060_p0_20260909_5 (BUILD lane D, preparation for gate C2).

Nothing here imports the su2qc Hamiltonian routes; this module is the
*independent* leg used to cross-check them.  It reproduces the counting rule
that the conventions file fixes, and nothing else:

  * Each link l carries an SU(2) irrep j_l, j_l in {0, 1/2, ..., jmax}.
  * Each vertex v carries a two-colour staggered fermion site with Fock states
    n_v in {0, 1, 2}.  Under the vertex SU(2) the n_v = 0 and n_v = 2 states are
    singlets (one state each) and the n_v = 1 states form one doublet (j = 1/2).
  * A static fundamental background charge at a vertex is one extra j = 1/2
    register entering G^a_v as +B^a_v.
  * Gauss's law: the physical space is the SU(2)-invariant subspace.  Because
    G^a_v acts only on the magnetic indices living at v (the link-end index of
    every link incident on v, the matter multiplet at v, and the static charge
    register at v), the invariant subspace factorises over vertices at fixed
    (j-configuration, n-configuration):

        dim = sum_{j cfg} sum_{n cfg} prod_v  mult_0( (x) reps at v )

    where mult_0(R) is the multiplicity of the trivial irrep in the tensor
    product R.  For a 2-valent vertex with no static charge this reproduces
    exactly the rule hard-coded in route_spinnet.enumerate_basis:
      j_a == j_b        -> n_v in {0, 2}
      |j_a - j_b| == 1/2 -> n_v = 1
      anything else      -> forbidden.

Three independent implementations of mult_0 are provided:

  M1 `mult_cg`      integer Clebsch-Gordan series (exact integer arithmetic)
  M2 `mult_nullity` numerical nullity of sum_a (J^a_total)^2 on the explicit
                    tensor-product carrier space (dense linear algebra)
  M3 `mult_haar`    Haar character integral over SU(2),
                    (2/pi) int_0^pi sin^2(t) prod_i chi_{j_i}(t) dt,
                    by Gauss-Legendre quadrature (analysis, not algebra)

Geometries are declared explicitly; no geometry is read from a document.
"""
from __future__ import annotations

from functools import lru_cache
from itertools import product

import numpy as np

# --------------------------------------------------------------- M1: CG series


@lru_cache(maxsize=None)
def _cg_series(reps: tuple) -> tuple:
    """Decompose the tensor product of `reps` (a tuple of 2j integers) into a
    tuple `mult` with mult[2j] = multiplicity of irrep j.  Exact integers."""
    acc = {0: 1}
    for two_j in reps:
        nxt: dict[int, int] = {}
        for two_a, c in acc.items():
            lo, hi = abs(two_a - two_j), two_a + two_j
            for two_c in range(lo, hi + 1, 2):
                nxt[two_c] = nxt.get(two_c, 0) + c
        acc = nxt
    top = max(acc) if acc else 0
    return tuple(acc.get(k, 0) for k in range(top + 1))


def mult_cg(reps) -> int:
    """M1: multiplicity of the SU(2) singlet in (x)_i V_{j_i}."""
    reps = tuple(sorted(int(round(2 * j)) for j in reps))
    if not reps:
        return 1
    return _cg_series(reps)[0]


# ------------------------------------------------------------ M2: dense nullity


def _spin_ops(two_j: int):
    j = two_j / 2.0
    m = np.arange(j, -j - 1, -1.0)          # descending
    d = len(m)
    jz = np.diag(m).astype(complex)
    jp = np.zeros((d, d), complex)
    for i in range(1, d):
        mm = m[i]
        jp[i - 1, i] = np.sqrt(j * (j + 1) - mm * (mm + 1))
    jx = (jp + jp.conj().T) / 2.0
    jy = (jp - jp.conj().T) / (2.0j)
    return jx, jy, jz


def mult_nullity(reps, tol: float = 1e-9) -> int:
    """M2: nullity of J^2 = sum_a (sum_i J^a_i)^2 on the explicit product space."""
    twos = [int(round(2 * j)) for j in reps]
    if not twos:
        return 1
    dims = [t + 1 for t in twos]
    ops = [_spin_ops(t) for t in twos]
    D = int(np.prod(dims))
    tot = [np.zeros((D, D), complex) for _ in range(3)]
    for i, dim_i in enumerate(dims):
        left = int(np.prod(dims[:i])) if i else 1
        right = int(np.prod(dims[i + 1:])) if i + 1 < len(dims) else 1
        for a in range(3):
            tot[a] += np.kron(np.kron(np.eye(left), ops[i][a]), np.eye(right))
    j2 = sum(A @ A for A in tot)
    w = np.linalg.eigvalsh((j2 + j2.conj().T) / 2.0)
    return int(np.sum(np.abs(w) < tol))


# ------------------------------------------------------------- M3: Haar integral

# Class angle psi in [0, pi]: g ~ diag(e^{i psi}, e^{-i psi}) up to conjugation.
# Haar measure on class functions: d mu = (2/pi) sin^2(psi) d psi, normalised to 1.
# Character: chi_j(psi) = sin((2j+1) psi) / sin(psi).
_GL_N = 400
_GL_X, _GL_W = np.polynomial.legendre.leggauss(_GL_N)
_PSI = 0.5 * np.pi * (_GL_X + 1.0)
_HAAR_W = (2.0 / np.pi) * (0.5 * np.pi) * _GL_W * np.sin(_PSI) ** 2


def _chi(two_j: int, psi: np.ndarray) -> np.ndarray:
    """chi_j(psi) = sin((2j+1) psi) / sin(psi)."""
    return np.sin((two_j + 1) * psi) / np.sin(psi)


def mult_haar(reps) -> float:
    """M3: (2/pi) int_0^pi sin^2(psi) prod_i chi_{j_i}(psi) d psi, numerically."""
    twos = [int(round(2 * j)) for j in reps]
    integrand = np.ones_like(_PSI)
    for t in twos:
        integrand = integrand * _chi(t, _PSI)
    return float(np.sum(_HAAR_W * integrand))


MULT_METHODS = {"cg": mult_cg, "nullity": mult_nullity, "haar": mult_haar}


# ------------------------------------------------------------------- geometry


class Geometry:
    """A lattice patch: vertices with coordinates, links as (source, target)."""

    def __init__(self, name, vertices, links, static_charges=()):
        self.name = name
        self.vertices = tuple(vertices)            # (x, y) per vertex index
        self.links = tuple(tuple(l) for l in links)
        self.static = tuple(sorted(static_charges))
        self.n_v = len(self.vertices)
        self.n_l = len(self.links)
        self.incident = tuple(
            tuple(l for l, (s, t) in enumerate(self.links) if s == v or t == v)
            for v in range(self.n_v)
        )

    @property
    def n_vac(self):
        """Staggered vacuum occupation: even sites empty, odd sites full."""
        return tuple(0 if (x + y) % 2 == 0 else 2 for (x, y) in self.vertices)

    def describe(self):
        return {
            "name": self.name,
            "vertices": [list(v) for v in self.vertices],
            "links": [list(l) for l in self.links],
            "static_charges_at": list(self.static),
            "valence": [len(i) for i in self.incident],
            "staggered_vacuum": list(self.n_vac),
        }


def plaquette_1x1(static_charges=()):
    """The frozen single plaquette of su2qc.conventions.

    VERTICES = ((0,0),(1,0),(1,1),(0,1)); LINKS = (0->1, 1->2, 3->2, 0->3).
    """
    return Geometry("1x1", ((0, 0), (1, 0), (1, 1), (0, 1)),
                    ((0, 1), (1, 2), (3, 2), (0, 3)), static_charges)


def ladder_2x3(static_charges=()):
    """2 rows x 3 columns of vertices: 6 vertices, 7 links, 2 plaquettes.

    Vertex index v = 3*row + col, coordinates (x, y) = (col, row):
        v3(0,1) --l5-- v4(1,1) --l6-- v5(2,1)
         |              |              |
        l2             l3             l4
         |              |              |
        v0(0,0) --l0-- v1(1,0) --l1-- v2(2,0)
    Link orientation: horizontal left->right, vertical bottom->top, matching the
    1x1 convention (l1: v1->v2 in x, l4: v1->v4 in y).
    """
    verts = tuple((c, r) for r in range(2) for c in range(3))
    links = ((0, 1), (1, 2),           # bottom row, x
             (0, 3), (1, 4), (2, 5),   # rungs, y
             (3, 4), (4, 5))           # top row, x
    return Geometry("2x3", verts, links, static_charges)


# ------------------------------------------------------------------ the count


def count_states(geom: Geometry, jmax: float, method: str = "cg",
                 tol: float = 1e-6):
    """Enumerate the gauge-invariant dimension and its fermion-number histogram.

    Returns dict with total, histogram {N: dim}, and bookkeeping.
    """
    mult = MULT_METHODS[method]
    js = [k / 2.0 for k in range(int(round(2 * jmax)) + 1)]
    matter_rep = {0: 0.0, 1: 0.5, 2: 0.0}
    hist: dict[int, float] = {}
    total = 0.0
    n_link_cfg = 0
    for jcfg in product(js, repeat=geom.n_l):
        # per-vertex, per-n multiplicity, computed once for this link config
        vmult = []
        dead = False
        for v in range(geom.n_v):
            base = [jcfg[l] for l in geom.incident[v]]
            if v in geom.static:
                base.append(0.5)
            row = {}
            for n in (0, 1, 2):
                m = mult(base + [matter_rep[n]])
                row[n] = m
            if all(abs(m) < tol for m in row.values()):
                dead = True
                break
            vmult.append(row)
        if dead:
            continue
        n_link_cfg += 1
        for ncfg in product((0, 1, 2), repeat=geom.n_v):
            w = 1.0
            for v, n in enumerate(ncfg):
                w *= vmult[v][n]
                if abs(w) < tol:
                    break
            if abs(w) < tol:
                continue
            N = sum(ncfg)
            hist[N] = hist.get(N, 0.0) + w
            total += w
    return {
        "geometry": geom.describe(),
        "jmax": jmax,
        "method": method,
        "total": total,
        "histogram": {int(k): hist[k] for k in sorted(hist)},
        "link_configs_with_a_live_vertex_set": n_link_cfg,
    }


def as_int_report(res, tol=1e-6):
    """Round a count result to integers, recording the worst rounding error."""
    vals = [res["total"]] + list(res["histogram"].values())
    err = max(abs(v - round(v)) for v in vals) if vals else 0.0
    out = dict(res)
    out["total"] = int(round(res["total"]))
    out["histogram"] = {k: int(round(v)) for k, v in res["histogram"].items()}
    out["max_rounding_error"] = err
    out["integer_within_tol"] = bool(err < tol)
    return out
