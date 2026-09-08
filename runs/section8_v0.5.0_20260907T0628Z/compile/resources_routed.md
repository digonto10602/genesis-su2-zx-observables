# Routed resources (FakeTorino, CZ-native), L12 structured synthesis

Window g2=4.0, m=0.75, dt=0.8333, r_max=3. seed_transpiler=7, opt level 3.

| pipeline | step CZ | step 2q-depth | full r=3 CZ | full r=3 2q-depth | pre-route equiv | routed equiv (r=3) |
|---|---:|---:|---:|---:|---|---|
| qiskit_L3 | 3976 | 3300 | 12142 | 9695 | 0.0e+00 | 3.5060843117662444e-13 |
| pyzx_basic_TP | 4603 | 3990 | 13914 | 12042 | 1.0e+00 | n/a |
| pyzx_full_reduce | 4778 | 3737 | 16025 | 12575 | 2.9e-13 | n/a |

Budget (prompt): ~250 CZ/step, ~1000 CZ/circuit, 2q depth < ~200 (+10% slack).
Per-r routed CZ (qiskit_L3): r=0: 0, r=1: 4025, r=2: 8031, r=3: 12142
