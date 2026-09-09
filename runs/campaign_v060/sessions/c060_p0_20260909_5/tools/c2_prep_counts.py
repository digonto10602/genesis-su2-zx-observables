#!/usr/bin/env python
"""Gate C2 preparation: classical enumeration evidence for rows V3, V5 and V7.

Session c060_p0_20260909_5, BUILD lane D (preparation only; C2 is NOT gated here).

Writes one JSON per row into <session>/c2_prep/:
    V3_jmax1_counts.json
    V5_static_bridge_counts.json
    V7_ladder_2x3_counts.json
    C2_prep_summary.json

Every number in those files is produced by this script.  Target numbers are
quoted from prompts/gi_cost_campaign_v.0.6.0.md (section 3 validation ladder and
Appendix A) purely as targets to compare against; none of them is used as input.

Run:
    .mamba/envs/su2zx/bin/python \
        runs/campaign_v060/sessions/c060_p0_20260909_5/tools/c2_prep_counts.py
"""
from __future__ import annotations

import json
import platform
import sys
import time
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
SESSION = HERE.parent
REPO = SESSION.parents[3]
OUT = SESSION / "c2_prep"
OUT.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO / "runs" / "section8_v0.5.0_20260907T0628Z" / "src"))

import numpy as np  # noqa: E402

from gi_count import (as_int_report, count_states, ladder_2x3,  # noqa: E402
                      plaquette_1x1)

# ------------------------------------------------------------------ targets
# Quoted from the campaign prompt ONLY as the numbers to compare against.
TARGETS = {
    "V3": {"total": 152, "histogram": {0: 3, 2: 36, 4: 74, 6: 36, 8: 3},
           "source": "prompts/gi_cost_campaign_v.0.6.0.md line 110 (V3), line 228"},
    "V5_static112": {"total": 112, "histogram": {0: 2, 2: 27, 4: 54, 6: 27, 8: 2},
                     "source": "prompts/gi_cost_campaign_v.0.6.0.md line 112 (V5), Appendix A"},
    "V5_static2417": {"total": 2417,
                      "histogram": {0: 4, 2: 119, 4: 597, 6: 977, 8: 597,
                                    10: 119, 12: 4},
                      "source": "prompts/gi_cost_campaign_v.0.6.0.md line 112 (V5), Appendix A"},
    "V7": {"total": 1727,
           "histogram": None,   # the prompt states no ladder histogram
           "source": "prompts/gi_cost_campaign_v.0.6.0.md line 114 (V7), line 228"},
}

METHODS = ("cg", "nullity", "haar")
METHOD_DOC = {
    "cg": "M1 integer Clebsch-Gordan series: singlet multiplicity at each vertex "
          "from the exact integer decomposition of the tensor product of the "
          "incident link irreps, the matter irrep and any static-charge irrep.",
    "nullity": "M2 dense linear algebra: build J^a_total on the explicit "
               "tensor-product carrier space of the vertex and count the exact "
               "zero eigenvalues of sum_a (J^a_total)^2 (|eig| < 1e-9).",
    "haar": "M3 Haar character integral: singlet multiplicity as "
            "(2/pi) int_0^pi sin^2(psi) prod_i chi_{j_i}(psi) d psi with "
            "chi_j(psi) = sin((2j+1)psi)/sin(psi), by 400-node Gauss-Legendre.",
}


def _cmp(res, target):
    ok_total = res["total"] == target["total"]
    if target["histogram"] is None:
        ok_hist = None
    else:
        ok_hist = ({int(k): int(v) for k, v in res["histogram"].items() if v}
                   == {int(k): int(v) for k, v in target["histogram"].items()})
    return {"total_matches_target": ok_total, "histogram_matches_target": ok_hist}


def run_methods(geom, jmax, label):
    out = {}
    for m in METHODS:
        t0 = time.perf_counter()
        res = as_int_report(count_states(geom, jmax, m))
        res["wall_seconds"] = round(time.perf_counter() - t0, 3)
        res["method_doc"] = METHOD_DOC[m]
        out[m] = res
        print(f"  [{label}] {m:8s} total={res['total']:6d} "
              f"hist={res['histogram']} ({res['wall_seconds']}s)")
    totals = {m: out[m]["total"] for m in METHODS}
    hists = {m: out[m]["histogram"] for m in METHODS}
    out["methods_agree"] = bool(len(set(totals.values())) == 1
                                and all(h == hists[METHODS[0]]
                                        for h in hists.values()))
    return out


# ============================================================ V3: jmax = 1
def row_V3():
    print("V3: j_max = 1 single plaquette")
    rec = {"row": "V3",
           "statement": "j_max = 1 single plaquette: 152 gauge-invariant states, "
                        "fermion-number sectors (3, 36, 74, 36, 3).",
           "target": TARGETS["V3"],
           "independent_enumeration": {},
           "route_implementations": {}}

    ind = run_methods(plaquette_1x1(), 1.0, "V3")
    rec["independent_enumeration"] = ind
    ref = ind["cg"]

    # --- route A (spin-network), read-only import from the frozen v0.5.0 tree
    from su2qc.ham import route_spinnet as route1
    t0 = time.perf_counter()
    labels1 = route1.enumerate_basis(1.0)
    tA_basis = time.perf_counter() - t0
    hA = {}
    for _js, ns, _tag in labels1:
        hA[sum(ns)] = hA.get(sum(ns), 0) + 1
    t0 = time.perf_counter()
    H1, _basis1 = route1.build_hamiltonian(1.0, 0.1, 1.0)[:2]
    tA_ham = time.perf_counter() - t0
    dense = H1.toarray()
    herm = float(np.max(np.abs(dense - dense.conj().T)))
    rec["route_implementations"]["route_A_spinnet"] = {
        "module": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_spinnet.py",
        "call": "enumerate_basis(1.0) / build_hamiltonian(1.0, 0.1, 1.0)",
        "total": len(labels1),
        "histogram": {int(k): int(hA[k]) for k in sorted(hA)},
        "hamiltonian_shape": list(H1.shape),
        "hermiticity_max_abs_asymmetry": herm,
        "wall_seconds_basis": round(tA_basis, 3),
        "wall_seconds_hamiltonian": round(tA_ham, 3),
        "duplicate_labels": len(labels1) - len(set(labels1)),
    }
    print("  [V3] route_A   total=%d hist=%s"
          % (len(labels1),
             rec["route_implementations"]["route_A_spinnet"]["histogram"]))

    # --- route B (Gauss-law kernel).  Expensive at jmax = 1 (redundant space
    #     14^4 * 256 ~ 9.8e6); timed and recorded, never truncated silently.
    from su2qc.ham import route_gausskernel as route2
    t0 = time.perf_counter()
    labels2, P2 = route2._basis(1.0)
    tB = time.perf_counter() - t0
    hB = {}
    for _js, ns, _tag in labels2:
        hB[sum(ns)] = hB.get(sum(ns), 0) + 1
    ortho = float(np.max(np.abs((P2.conj().T @ P2).toarray()
                                - np.eye(len(labels2)))))
    rec["route_implementations"]["route_B_gausskernel"] = {
        "module": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_gausskernel.py",
        "call": "_basis(1.0)  (equivalently kernel_dimension(1.0))",
        "total": len(labels2),
        "histogram": {int(k): int(hB[k]) for k in sorted(hB)},
        "projector_orthonormality_max_abs_dev": ortho,
        "projector_orthonormality_threshold": 1.0e-12,
        "projector_orthonormality_pass": bool(ortho < 1.0e-12),
        "wall_seconds": round(tB, 3),
        "note": "route B builds only the kernel at j_max = 1; the projected H "
                "is route-A-only per its module docstring.",
    }
    print("  [V3] route_B   total=%d hist=%s (%.1fs)"
          % (len(labels2),
             rec["route_implementations"]["route_B_gausskernel"]["histogram"], tB))

    rec["route_label_set_identical"] = bool(set(labels1) == set(labels2))
    rec["route_label_order_identical"] = bool(list(labels1) == list(labels2))

    rA = rec["route_implementations"]["route_A_spinnet"]
    rB = rec["route_implementations"]["route_B_gausskernel"]
    rec["agreement"] = {
        "independent_vs_route_A": bool(ref["total"] == rA["total"]
                                       and ref["histogram"] == rA["histogram"]),
        "independent_vs_route_B": bool(ref["total"] == rB["total"]
                                       and ref["histogram"] == rB["histogram"]),
        "route_A_vs_route_B": bool(rA["total"] == rB["total"]
                                   and rA["histogram"] == rB["histogram"]),
    }
    rec["vs_target"] = _cmp(ref, TARGETS["V3"])
    rec["verdict"] = ("ALL METHODS AGREE WITH TARGET"
                      if (all(rec["agreement"].values())
                          and rec["vs_target"]["total_matches_target"]
                          and rec["vs_target"]["histogram_matches_target"]
                          and ind["methods_agree"])
                      else "DISAGREEMENT - see fields")
    return rec


# ==================================================== V5: static-charge bridge
def row_V5():
    print("V5: static-charge bridges")
    rec = {"row": "V5",
           "statement": "Two static fundamental (j = 1/2) background charges "
                        "entering G^a_v as +B^a_v; count the Gauss-law kernel.",
           "gauss_law_reading": (
               "A static fundamental charge at vertex v contributes one extra "
               "j = 1/2 representation to the SU(2) invariance condition at v. "
               "The gauge-invariant dimension is therefore the product over "
               "vertices of the singlet multiplicity of "
               "(x)_{l incident on v} V_{j_l} (x) V_{matter(n_v)} (x) V_{1/2}, "
               "summed over all link-spin and matter configurations. No coupling, "
               "convention or basis definition is altered."),
           "cases": {}}

    g1 = plaquette_1x1(static_charges=(0, 2))
    c1 = run_methods(g1, 0.5, "V5/112")
    rec["cases"]["static112_1x1"] = {
        "geometry_note": "frozen 1x1 plaquette; static charges at v0=(0,0) "
                         "(bottom-left) and v2=(1,1) (top-right), as Appendix A "
                         "of the campaign prompt specifies.",
        "jmax": 0.5,
        "results": c1,
        "target": TARGETS["V5_static112"],
        "vs_target": _cmp(c1["cg"], TARGETS["V5_static112"]),
    }

    g2 = ladder_2x3(static_charges=(0, 5))
    c2 = run_methods(g2, 0.5, "V5/2417")
    rec["cases"]["static2417_2x3"] = {
        "geometry_note": "2x3 ladder, 6 vertices / 7 links / 2 plaquettes; "
                         "v = 3*row + col, (x,y) = (col,row); static charges at "
                         "v0=(0,0) and v5=(2,1), the two diagonally opposite far "
                         "corners.",
        "jmax": 0.5,
        "results": c2,
        "target": TARGETS["V5_static2417"],
        "vs_target": _cmp(c2["cg"], TARGETS["V5_static2417"]),
    }

    # --- ambiguity audit: which placements of two static charges reproduce the
    #     targets?  Reported for transparency, not used to pick a convention.
    print("  [V5] placement audit")
    aud = {}
    for name, geo, jm, tgt in (("1x1", plaquette_1x1, 0.5, 112),
                               ("2x3", ladder_2x3, 0.5, 2417)):
        n_v = geo().n_v
        rows = []
        for pair in combinations(range(n_v), 2):
            r = as_int_report(count_states(geo(static_charges=pair), jm, "cg"))
            rows.append({"charges_at": list(pair),
                         "coords": [list(geo().vertices[p]) for p in pair],
                         "total": r["total"],
                         "histogram": r["histogram"],
                         "equals_target": bool(r["total"] == tgt)})
        aud[name] = {"target_total": tgt, "placements": rows}
    rec["placement_audit"] = aud
    rec["verdict"] = ("BOTH CASES MATCH TARGET"
                      if all(rec["cases"][k]["vs_target"]["total_matches_target"]
                             and rec["cases"][k]["vs_target"]["histogram_matches_target"]
                             and rec["cases"][k]["results"]["methods_agree"]
                             for k in rec["cases"])
                      else "DISAGREEMENT - see fields")
    return rec


# ================================================================ V7: 2x3 ladder
def row_V7():
    print("V7: 2x3 ladder at j_max = 1/2")
    g = ladder_2x3()
    res = run_methods(g, 0.5, "V7")
    rec = {"row": "V7",
           "statement": "2x3 ladder, j_max = 1/2, OURS (no static charges): "
                        "1,727 gauge-invariant states, by three independent methods.",
           "geometry_note": "6 vertices, 7 links, 2 plaquettes; v = 3*row + col, "
                            "(x,y) = (col,row); horizontal links left->right, "
                            "rungs bottom->top, matching the 1x1 link orientation "
                            "convention. The 3x2 reading is the same graph up to "
                            "relabelling and gives the same counts.",
           "jmax": 0.5,
           "three_methods": res,
           "target": TARGETS["V7"],
           "vs_target": _cmp(res["cg"], TARGETS["V7"]),
           "note_on_routes": "Neither frozen v0.5.0 route implements a 2x3 "
                             "geometry (both are hard-coded to the single "
                             "plaquette), so no route number exists for this row "
                             "yet. The 1x1 cross-check below shows the same three "
                             "methods reproduce both routes where they do exist."}

    from su2qc.ham import route_spinnet as route1
    from su2qc.ham import route_gausskernel as route2
    lab1 = route1.enumerate_basis(0.5)
    lab2, _P = route2._basis(0.5)
    ref = run_methods(plaquette_1x1(), 0.5, "V7/xcheck-1x1")
    totals = {len(lab1), len(lab2), 82, *[ref[m]["total"] for m in METHODS]}
    rec["cross_check_1x1_jmax_half"] = {
        "route_A_total": len(lab1),
        "route_B_total": len(lab2),
        "three_methods": {m: ref[m]["total"] for m in METHODS},
        "conventions_EXPECTED_DIM_half": 82,
        "all_equal": bool(len(totals) == 1),
    }
    rec["verdict"] = ("THREE METHODS AGREE WITH TARGET"
                      if (res["methods_agree"]
                          and rec["vs_target"]["total_matches_target"])
                      else "DISAGREEMENT - see fields")
    return rec


def main():
    t0 = time.perf_counter()
    meta = {
        "session": "c060_p0_20260909_5",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "generator": str(Path(__file__).resolve().relative_to(REPO)),
        "python": sys.version.split()[0],
        "numpy": np.__version__,
        "platform": platform.platform(),
        "read_only_sources": [
            "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/conventions.py",
            "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_spinnet.py",
            "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_gausskernel.py",
        ],
        "disclaimer": "Preparation evidence for gate C2. This session does not "
                      "gate C2 and issues no gate verdict.",
    }
    written = []
    for fname, fn in (("V3_jmax1_counts.json", row_V3),
                      ("V5_static_bridge_counts.json", row_V5),
                      ("V7_ladder_2x3_counts.json", row_V7)):
        rec = fn()
        rec["meta"] = meta
        p = OUT / fname
        p.write_text(json.dumps(rec, indent=2, sort_keys=False) + "\n")
        written.append((fname, rec.get("verdict")))
        print("  -> %s" % p.relative_to(REPO))

    summary = {"meta": meta,
               "rows": {f.split("_")[0]: {"file": f, "verdict": v}
                        for f, v in written},
               "total_wall_seconds": round(time.perf_counter() - t0, 2)}
    p = OUT / "C2_prep_summary.json"
    p.write_text(json.dumps(summary, indent=2) + "\n")
    print("  -> %s" % p.relative_to(REPO))
    print("done in %ss" % summary["total_wall_seconds"])


if __name__ == "__main__":
    main()
