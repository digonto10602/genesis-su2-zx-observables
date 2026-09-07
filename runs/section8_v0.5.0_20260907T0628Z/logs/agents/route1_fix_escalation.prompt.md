# Route 1 rebuild per solutions/0.5.0.md (G1 escalation implementation)

You are a fresh builder implementing EXACTLY the fix plan of
`../../solutions/0.5.0.md` (read it first — it is at the repo root:
/home/digimonk/Projects/SU2ZX_Foundation_Code_Package/SU2ZX/solutions/0.5.0.md).
You are started inside the run directory RUN (CWD). Interpreter:
../../.mamba/envs/su2zx/bin/python (numpy/scipy/pytest; NO sympy).

You own ONLY: src/su2qc/ham/route_spinnet.py and tests/test_route_spinnet.py.
You must NOT read, import, or copy from src/su2qc/ham/route_gausskernel.py
(independence of the two routes is a hard audit requirement). You MUST read
src/su2qc/conventions.py (frozen) and follow solutions/0.5.0.md §3.

Summary of what to build (details in the solution file):
- Keep the existing gauge-invariant basis enumeration (82 states at jmax=0.5,
  152 at jmax=1.0, labels ((j1..j4),(n1..n4),0)) — that part of the current
  route_spinnet.py is correct and verified. Keep the diagonal terms (electric +
  mass) — verified correct.
- REPLACE the hopping and magnetic matrix elements with locally computed
  analytic vertex-tensor contractions:
  * Per-vertex singlet tensors T (closed-form CG; c0<c1 mode order; unit norm;
    fixed documented phase): j_a=j_b, n∈{0,2}: link-link singlet
    T0[ma,mb] = (-1)^(j-ma) δ_{ma,-mb}/sqrt(2j+1); |j_a-j_b|=1/2, n=1:
    three-rep singlet via CG(j_a, ma; 1/2, s | j_b, mb) pattern.
  * Hopping ψ†_{s,α} U^{αβ} ψ_{t,β} on link l: amplitude = contraction of the
    initial and final vertex tensors at s and t with the link Wigner insertion
    sqrt((2j+1)/(2j'+1)) CG(j,m;1/2,α|j',m') on both link-end m-indices, times
    the eta_l/2 prefactor, times the JW inter-site sign prod_{s<w<t}(-1)^{n_w}
    (site order v1<v2<v3<v4) and consistent intra-site fermion ordering.
  * Plaquette: product of four one-vertex contractions with TWO link insertions
    per vertex (color indices summed around the loop, U_2 and U_3 daggered per
    conventions.PLAQUETTE_SEQUENCE), matter untouched; coefficient
    -(1/(2 g2)); then +h.c. (assemble TrU_box and add adjoint; do not
    double-count).
- Preserve the public API exactly as it exists now (build_hamiltonian,
  build_hamiltonian_no_magnetic, observable/projector helpers used by
  tests/test_route_spinnet.py and src/su2qc/ham/compare.py — check compare.py's
  imports and keep them working, but DO NOT edit compare.py).
- CG closed forms for the 1/2 insertion are in the solution file §... (use:
  CG(j,m;1/2,+1/2|j+1/2,m+1/2)=sqrt((j+m+1)/(2j+1));
  CG(j,m;1/2,-1/2|j+1/2,m-1/2)=sqrt((j-m+1)/(2j+1));
  CG(j,m;1/2,+1/2|j-1/2,m+1/2)=-sqrt((j-m)/(2j+1));
  CG(j,m;1/2,-1/2|j-1/2,m-1/2)=sqrt((j+m)/(2j+1))).
  Generic-j CG for the singlet tensors: only these plus the (-1)^{j-m} metric
  are needed.

Acceptance (run all, print results):
1. cd RUN && ../../.mamba/envs/su2zx/bin/python -m pytest tests/test_route_spinnet.py -q  → green
   (update ONLY tests that hardcoded the old wrong uniform amplitudes; keep all
   counting/hermiticity/sector/degeneracy tests).
2. ../../.mamba/envs/su2zx/bin/python - <<'PY'
import sys; sys.path.insert(0,'src')
from su2qc.ham import compare
rows = compare.spectra_comparison()
print(rows); assert max(r['max_rel_dev'] for r in rows) <= 1e-12
dev,_ = compare.time_series_comparison(); print('ts dev', dev); assert dev <= 1e-10
print('G1 route agreement OK')
PY
   Note: importing compare triggers the other route's build (~60 s first time;
   its cache makes later calls fast). You may not READ route_gausskernel.py but
   running compare.py (which imports it) is required — treat it as a black box.
3. Hermiticity ≤ 1e-13, [H,N]=0 ≤ 1e-13 at (g2,m)=(1.3,0.27), jmax=0.5 and 1.0.

If after your best effort the spectra still disagree, print the per-term
diagnostic (diagonal dev, hopping-only spectra dev, magnetic-only spectra dev,
unique |element| values of each) and stop — do NOT fudge factors to force
agreement.

When done print a JSON summary: {files, spectra_max_rel_dev, ts_dev,
tests_pass, notes}.
