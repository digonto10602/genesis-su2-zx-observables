# Conventions reconciliation: frozen-matter 2x2 block vs monograph H~1

Measured (route 1 = route 2 to machine precision, g2 = 1.3, m -> 1e9):

- Diagonal: E(|0000>) = 0, E(|½½½½>) = 1.5 g2  (electric (g2/2)(3/4)·4),
  matching the monograph electric splitting after the H~ = 2H/g² rescale:
  H~ diag splitting 3 = 2·(1.5 g2)/g2.  Max deviation 3e-11 (O(1/m) residual).
- Off-diagonal: H_01 = -1/g2 exactly (offdiag·g2 = -1.000000000000).

Monograph (repo src/su2zx/core.py, n=1): H~1 = 1.5 I - 1.5 Z - 2x X with
x = 2/g^4 and H = (g2/2) H~, giving H_offdiag^mono = -(g2/2)(2x) = -2/g².

Reconciliation factor: H_offdiag^patch = (1/2) · H_offdiag^mono.

Root cause (normalization, not error): the monograph's one-plaquette magnetic
normalization corresponds to the pure-gauge model where the plaquette operator
in the 2-state basis {all-j=0, all-j=½} has matrix element 2 for
-(1/(2g²))Tr(U□+U□†) — i.e. Tr(U□)+Tr(U□†) contributes 2·2/... with its group
integral normalization; the with-matter patch's dressed-vertex singlet
normalization (each corner tensor unit-norm, metric 1/sqrt(2j+1) per vertex)
yields ⟨½½½½|Tr U□|0000⟩ = 1, hence half the monograph value. Both are
internally consistent conventions; the physical content (spectra of each
model) is unchanged. The patch value is FIXED by gauge invariance of route 2
([G,H]=0 exactly with the Wigner-D insertion sqrt((2j+1)/(2j'+1))·CG·CG),
so the patch normalization is the physically correct KS one; the monograph's
H~1 x-normalization absorbs the factor into its definition of x.

Consequence for comparisons: map monograph results onto the patch's frozen-
matter block via x_eff = x/2 (equivalently g²_eff relation), documented here
once; no code changes.
