# v0.6.2 preflight environment

T0: 2026-09-08T20:49:08+00:00; hard cutoff: 2026-09-09T08:49:08+00:00.
Baseline: 723d083d939a355da1a88880e38b7f08c0c2029a.
Interpreter: repository-local .mamba/envs/su2zx/bin/python, Python 3.11.16.
NumPy 2.4.6; SciPy 1.17.1; Qiskit 2.5.2; Aer 0.17.2.
Live l12.encode(((0.,.5,.5,.5),(1,1,0,2),0)) returned 3793.
Recorded campaign hashes all match; exact values in preflight.json. conventions.py and 00_conventions.md have distinct hashes, correctly identified there.

## Live quota observations

Claude Code 2.1.263, interactive /usage:
- Current session: 10% used, resets 3pm America/Denver.
- Current week all models: 27% used, resets Sep 12, 3am America/Denver.
- Current week Fable: 51% used, resets Sep 12, 3am America/Denver.
These meters are independent, not an additive usage breakdown. No inference of billed token shares is made. The Fable meter is already beyond the configured 50% budget ceiling; capacity under that ceiling for mandatory planning plus final sign-off cannot be established. Defer mandatory Fable calls, rather than substitute Opus or consume uncertain reserve.

Codex 0.153.4, interactive /status:
- 5-hour limit: 82% left, resets 15:00.
- Weekly limit: 97% left, resets 10:00 on Sep 15.
- CLI default reported gpt-5.6-luna; no BUILD launched and no model reconfiguration performed. Main orchestration model is gpt-6-astra per session metadata, billing unverified.

Both quota TUIs closed after inspection. No CLI updates, installs, credentials inspection, QPU calls, pushes or research model calls performed.
