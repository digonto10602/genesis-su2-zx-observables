"""FROZEN conventions for the SU(2) single-plaquette patch with dynamical matter.

Frozen at G0 of run section8_v0.5.0_20260907T0628Z. DO NOT EDIT.
Both Hamiltonian routes, all encodings, circuits, and analysis import from here
and ONLY from here. Any objection goes to physics/conventions_objection_*.md.

Model (Section 5.1 of the v0.5.0 prompt):
  Lattice units a = 1. One square plaquette, open boundaries.
  H = (g^2/2) sum_l E_l^2
    + m sum_v (-1)^{x_v+y_v} psi\dagger_v psi_v
    + (1/2) sum_l ( eta_l psi\dagger_{s(l)} U_l psi_{t(l)} + h.c. )
    - (1/(2 g^2)) Tr( U_box + U_box\dagger )
  U_box = U_l1 U_l2 U_l3\dagger U_l4\dagger   (counter-clockwise v1->v2->v3->v4->v1)
  E^2 = j(j+1) per link. Truncation j in {0, 1/2} (hardcore gluon); j_max = 1
  is built too for the truncation-error statement.
"""

# ---------------------------------------------------------------- vertices
# index -> (x, y). Vertex numbering v1..v4 maps to python indices 0..3.
VERTICES = ((0, 0), (1, 0), (1, 1), (0, 1))  # v1, v2, v3, v4
N_VERTICES = 4

def parity(v: int) -> int:
    """(-1)^{x+y} for vertex index v in 0..3.  v1,v3 even (+1); v2,v4 odd (-1)."""
    x, y = VERTICES[v]
    return 1 if (x + y) % 2 == 0 else -1

PARITY = tuple(parity(v) for v in range(4))          # (+1, -1, +1, -1)

# ---------------------------------------------------------------- links
# index -> (source_vertex, target_vertex, direction). Link numbering l1..l4
# maps to python indices 0..3.  l1: v1->v2 (x, y=0); l2: v2->v3 (y, x=1);
# l3: v4->v3 (x, y=1); l4: v1->v4 (y, x=0).
LINKS = ((0, 1, "x"), (1, 2, "y"), (3, 2, "x"), (0, 3, "y"))
N_LINKS = 4

def eta(l: int) -> int:
    """Staggered phase of link l: eta_x = 1, eta_y = (-1)^x  (x of the source)."""
    s, _t, d = LINKS[l]
    if d == "x":
        return 1
    return 1 if VERTICES[s][0] % 2 == 0 else -1

ETA = tuple(eta(l) for l in range(4))                # (+1, -1, +1, +1)

# Plaquette orientation: U_box = U_0 U_1 U_2^dag U_3^dag (python link indices).
PLAQUETTE_SEQUENCE = ((0, +1), (1, +1), (2, -1), (3, -1))  # (link, +1=U / -1=Udag)

# ---------------------------------------------------------------- matter
# Two-color staggered fermions, one doublet per vertex. 4 Fock states per site:
# n=0 color-singlet vacuum, n=1 doublet, n=2 doubly-occupied singlet (baryon).
# Staggered vacuum: even sites empty, odd sites full: n_vac = (0, 2, 0, 2).
N_VAC = (0, 2, 0, 2)

def charge(v: int, n: int) -> int:
    """Local charge relative to the staggered vacuum: q_v = n_v - n_vac(v)."""
    return n - N_VAC[v]

# Jordan-Wigner mode order for route 2 (redundant Kogut-Susskind space).
# Mode index 0..7 = (v1,c1),(v1,c2),(v2,c1),(v2,c2),(v3,c1),(v3,c2),(v4,c1),(v4,c2)
JW_ORDER = tuple((v, c) for v in range(4) for c in range(2))

# ---------------------------------------------------------------- truncation
JMAX_HALF = 0.5   # primary truncation, 82 gauge-invariant states
JMAX_ONE = 1.0    # for the truncation-error statement, 152 states

def casimir(j: float) -> float:
    """SU(2) quadratic Casimir j(j+1)."""
    return j * (j + 1.0)

# Expected gauge-invariant dimensions (verified independently by both routes).
EXPECTED_DIM = {JMAX_HALF: 82, JMAX_ONE: 152}
# Fermion-number sector dims at jmax=1/2, N = 0,2,4,6,8:
EXPECTED_SECTOR_DIMS = {0: 2, 2: 20, 4: 38, 6: 20, 8: 2}

# ---------------------------------------------------------------- couplings
def coupling_electric(g2: float) -> float:
    """Coefficient of sum_l E_l^2."""
    return g2 / 2.0

def coupling_magnetic(g2: float) -> float:
    """Coefficient of -Tr(U_box + U_box^dag) (i.e. H_B = -c * Tr(...))."""
    return 1.0 / (2.0 * g2)

HOPPING_PREFACTOR = 0.5   # (1/2) sum_l ( eta_l psi^dag_s U psi_t + h.c. )

# Tree-level resonance (a=1): removing one j=1/2 link releases (g^2/2)(3/4);
# equals pair cost 2m at m* = 3 g^2 / 16.
def tree_level_resonance(g2: float) -> float:
    return 3.0 * g2 / 16.0

# ---------------------------------------------------------------- bit orders
# Qiskit strings and displayed bitstrings use q_(N-1)...q_0 (repo-wide rule).
QISKIT_BIT_ORDER = "q_(N-1)...q_0"

# Canonical basis-label form shared by both routes and compare.py:
# a state is labeled ((j1,j2,j3,j4), (n1,n2,n3,n4), intertwiner_tag) where
# j are half-integers as floats, n in {0,1,2}; intertwiner_tag disambiguates
# nothing at 2-valent vertices (always 0) but is kept for forward compat.
LABEL_DOC = "((j_l1..j_l4), (n_v1..n_v4), tag)"
