# Command reference: edit placeholders and supply required briefs before running.
set -euo pipefail
REPO=/home/digimonk/Projects/SU2ZX_Foundation_Code_Package/SU2ZX
cd "$REPO"
PROMPT="$REPO/prompts/v0.5.0.md"
RUN="$REPO/runs/section8_v0.5.0_$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -p "$RUN"/{run,src/su2qc,tests,gates/attempts,physics,reviews,bench,circuits,compile,prereg,hardware/raw,analysis/tables,analysis/figures,reports,logs/agents,logs/cmd,env}


test -s "$RUN/brief.md"; test ! -e "$RUN/plan.md"
claude -p --model claude-fable-5-1 --allowedTools "Read,Grep,Glob,WebSearch,WebFetch" --max-turns 30 "ultrathink. Read $RUN/brief.md and cited proposal/plan sections. Plan this SU(2) lattice-gauge quantum-computing task. Markdown only: goals, exact physics acceptance checks, BUILD/TEST-BENCH/REVIEW/PHYSICS assignments, gate schedule with deterministic and reviewer pass/fail criteria, stop conditions, token budget excluding frontier models from mechanical loops. Respect the approved routing override. No file edits." > "$RUN/plan.md.partial"
test -s "$RUN/plan.md.partial"; mv "$RUN/plan.md.partial" "$RUN/plan.md"


BASE=<recorded-base-commit>
N=<gate-and-attempt>
test -s "$RUN/gate-input-$N.md"; test ! -e "$RUN/gate-$N.md"
git -C "$REPO" diff "$BASE" -- > "$RUN/diff-$N.patch"
claude -p --model claude-opus-5 --allowedTools "Read,Grep,Glob" --max-turns 20 "Validation gate $N per $RUN/plan.md. Read $RUN/gate-input-$N.md, $RUN/diff-$N.patch and all cited evidence. Verify each acceptance criterion, deterministic results and snapshot identity. Reply PASS or FAIL first, then evidence and required fixes. Missing evidence is FAIL. No edits." > "$RUN/gate-$N.md.partial"
test -s "$RUN/gate-$N.md.partial"; mv "$RUN/gate-$N.md.partial" "$RUN/gate-$N.md"


test -s "$RUN/final-input.md"; test ! -e "$RUN/final-signoff.md"
claude -p --model claude-fable-5-1 --allowedTools "Read,Grep,Glob" --max-turns 30 "Final physics sign-off of the whole run. Read $RUN/plan.md, $RUN/final-input.md and all cited gates/evidence. Check gauge invariance, Gauss law, Hamiltonian conventions, Trotter/ZX equivalence and every applicable criterion. Reply PASS or FAIL, evidence, limitations and fixes. Missing evidence is FAIL. No edits." > "$RUN/final-signoff.md.partial"
test -s "$RUN/final-signoff.md.partial"; mv "$RUN/final-signoff.md.partial" "$RUN/final-signoff.md"


codex exec -m gpt-6-astra -s workspace-write -C /home/digimonk/Projects/SU2ZX_Foundation_Code_Package/SU2ZX "<approved module task, exact ownership, conventions, tests and limits>" </dev/null
