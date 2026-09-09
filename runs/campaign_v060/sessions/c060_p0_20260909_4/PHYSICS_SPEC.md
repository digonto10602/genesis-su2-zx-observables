# Physics spec — definitions only

Documentation only. This records the frozen definitions; it changes no physics,
no threshold, no observable, no seed derivation, and no acceptance band. The
single source of truth is `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/conventions.py`
(and `src/su2zx/core.py` for the truncated plaquette chain description).

## Model

Lattice units `a = 1`. One square plaquette, open boundaries. From
`conventions.py:8-15`:

```
H = (g2/2) sum_l E_l^2
  + m sum_v (-1)^{x_v+y_v} psi^dag_v psi_v
  + (1/2) sum_l ( eta_l psi^dag_{s(l)} U_l psi_{t(l)} + h.c. )
  - (1/(2 g2)) Tr( U_box + U_box^dag )

U_box = U_l1 U_l2 U_l3^dag U_l4^dag   (counter-clockwise v1->v2->v3->v4->v1)
E^2 = j(j+1) per link.
```

Truncation: primary `jmax = 1/2` (hardcore gluon, 82 gauge-invariant states);
`jmax = 1` built too for the truncation-error statement (152 states).

Two-color staggered fermions, one doublet per vertex. Four Fock states per site:
`n=0` color-singlet vacuum, `n=1` doublet, `n=2` doubly-occupied singlet (baryon).
Staggered vacuum (even sites empty, odd sites full): `N_VAC = (0,2,0,2)`.

## Vertices and links

`VERTICES = ((0,0),(1,0),(1,1),(0,1))` (v1..v4 → indices 0..3).
`LINKS = ((0,1,"x"),(1,2,"y"),(3,2,"x"),(0,3,"y"))` (l1..l4 → 0..3).
Parity `(-1)^{x+y}`: `PARITY = (+1,-1,+1,-1)`.
Staggered phase `eta_x = 1`, `eta_y = (-1)^x` of the source:
`ETA = (+1,-1,+1,+1)`.

## Charge

`charge(v,n) = n - N_VAC[v]`, i.e. `q_v = n_v - n_vac(v)`. With `n_v in {0,1,2}`
and `N_VAC=(0,2,0,2)`, `|q_v|=1` at every vertex forces `n=(1,1,1,1)`, hence total
fermion number `N = 4` and `sum_v q_v = 0` (the R15 correction; see
`SU2QC_CONTRACTS.md`).

## Encoding (L12)

Qubit `3v, 3v+1, 3v+2` hold (first link span, second link span, matter) of vertex
`v`; q0 is the least-significant bit; displayed Qiskit strings read `q11..q0`.
Matter bit is `1` iff `n_v == 2`; link bits are `round(2*j)`. The stretched state
`((0.0,0.5,0.5,0.5),(1,1,0,2),0)` encodes to 3793.

## Channels (as implemented in twin/twin.py)

`q_v = n_v - N_VAC[v]`. Classification order (BBbar → surv → meson → other):

- `P_BBbar`  = indicator of `any_v |q_v| == 2`
- `P_surv`   = indicator of `(q1,q2,q3,q4) == (1,-1,0,0)`
- `P_meson`  = indicator of `all_v |q_v| == 1`
- `P_other`  = remainder within the decodable physical set

`P_stretched` and `P_short` are sub-tallies of `P_surv` (link-spin discriminations
on the same single occupation pattern `(1,1,0,2)`), not additional channels. The
survival selector matches two distinct codewords (2058 and 3793) for that one
occupation pattern — it is not rank-1.

Closure residual, exactly as implemented
(`twin/twin.py:130-143`):

```
residual = (P_surv + P_meson + P_BBbar + P_other)
         - sum_{k decodable and (sum_v n_v == 4 or exists_v |q_v| == 2)} weight[k]
```

Undecodable keys (nonzero weight) are skipped by *both* sides, so the residual
cannot detect them; the R9 demand is UNSATISFIABLE AS WRITTEN (see contracts).

## Observables

From `twin/twin.py`: `P_surv`, `P_meson`, `P_BBbar`, `P_other`, `P_stretched`,
`P_short`, `E2_l1..l4` (per-link Casimir `j(j+1)`), `n_v1..n_v4` (per-vertex
occupation), and `dC = sum_l E2_l - 2.25` (the 9/4 reference of three j=1/2 links
in the stretched string).

## Trotter scheme

Strang (second-order) splitting over the term groups
`D, h0, h1, h2, h3, B` with `B` at full `dt` and every other block at `dt/2`,
in the order `D/2, h0/2, h2/2, h1/2, h3/2, B, h3/2, h1/2, h2/2, h0/2, D/2`
(`circuits/strang_l12.py:165-172`, `dynamics/scan.py:236-247`,
`circuits/strang_l12.py:209-222`).

## Truncated 2+1D caution

The spatial plaquette chain is a truncated 2+1D Hamiltonian system, not pure-gauge
1+1D; the campaign makes no continuum SU(2), physical SU(3) QCD, string tension,
string breaking, hadronization, or quantum-advantage claim (repo rules).

## Bit order

Qiskit strings and displayed bitstrings use `q_(N-1)...q_0`.

## Status

C0 PARTIAL, C1 unamended, C2 NOT STARTED. All noisy simulator numbers EMULATED.
No hardware job has ever been submitted.