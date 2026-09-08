# Frozen v0.5.0 conventions carried into campaign v0.6.1

Source: runs/section8_v0.5.0_20260907T0628Z/src/su2qc/conventions.py
SHA-256: fb3b7525b1a1d69bcb30ace986465880b972cc9fb23a417af5a9ca78ebade306

This file is the campaign pointer to the frozen convention source. Phase 2 extends it with the four-coefficient API, static-charge labels, and the 2x3 geometry. Until then, the v0.5.0 source file is authoritative.

R5 mapping: the frozen v0.5.0 window is g^2=4, m=0.75, dt=0.8333333333333334, r_max=3. In code units the coefficients are (cE,cM,cH,cB)=(2,0.75,0.5,0.125), with g_E=g^2/2=2 and mu=3/8. P-S uses (2,0.75,0.04,0.04), with t={2.5,6.25}.
