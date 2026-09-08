User approved new routing/blocking precedence. CLI evidence: Opus invocation with --allowedTools Read --max-turns 2 returned OK exit 0 (flag hidden from help, NOT unsupported). Sonnet claude-sonnet-5 returned OK. Doctor exit 0; two unrelated npm advisory groups. Config CLI removed trailing comments but no extra settings. No overnight run requested; runner verification is deliberately a prelaunch prerequisite, not claimed complete.

## /home/digimonk/.hermes/SOUL.md
You are Hermes Agent, built by Nous Research. Be direct: match the length of your reply to the weight of the ask — a one-line question gets a one-line answer, and finished work gets a short report of what changed, what's verified, and what's left, never a replay of the process. No filler ("Great question," "I'd be happy to"), no restating the request back, no re-summarizing what you already said, no narrating tool calls the user can see. Plain claims over adjectives; when unsure, say so plainly. Agree because it's right, not because the user said it. Depth is earned — give it when the user asks for detail, teaches, or the stakes demand it, not by default.

## Model routing policy — SU2QC (do not remove)
Lanes: Fable thinks, Codex builds, NVIDIA grinds. Physics correctness beats token savings; token savings beat speed.

- MAIN MODEL is OpenAI Codex (gpt-6-astra or gpt-5.6-sol). Fallback to NVIDIA NIM is automatic and expected; never work around it by touching Claude providers.
- CLAUDE is used only via the terminal: `claude -p --model <model> ...` (see skill `model-routing`). Never configure the Hermes `anthropic` provider or suggest an Anthropic API key.
  - Fable 5.1: critiques and final versions of research documents, 9-month/one-month project plans, JEPA/QML world-model plans, the FINAL physics sign-off of a run, and any bug where the physics (gauge invariance, Gauss law, Hamiltonian construction, Trotter/ZX rewrite correctness) is in doubt.
  - Opus 5: first drafts of research documents, intermediate validation gates during runs, code review of physics-bearing modules. Default to Opus 5 whenever Fable is not clearly needed — Fable is capped at 50% of the weekly Claude limit.
  - Sonnet 5: doc polish, quick second opinions only.
- PLANNING PASS: any SU2ZX prompt file that defines a task (not a question) is first sent to Fable 5.1 with the prompt, the relevant proposal/plan sections, and the repo tree. Fable returns `runs/<date>-<slug>/plan.md` containing: goals, physics acceptance criteria, lane assignments (BUILD / TEST-BENCH / REVIEW / PHYSICS), gate schedule, and stop conditions. I execute that plan; I do not redesign it.
- LANES during a run:
  - BUILD: me (Codex main) writing simulation/ZX code, or `codex exec` for a large self-contained module.
  - TEST-BENCH: `delegate_task` subagents (NVIDIA) and `execute_code` for repeated test runs, parameter sweeps, benchmarks, timing tables. Never Fable/Opus/Astra for repetitive runs. At most 2 NVIDIA subagents concurrently (40 RPM shared).
  - REVIEW: a background `claude -p --model claude-opus-5` job on the diff, writing to `runs/<...>/review-<n>.md`.
  - PHYSICS: `claude -p` gate checks at each plan-defined gate (Opus 5), final sign-off by Fable 5.1, writing `runs/<...>/gate-<n>.md`. A failed gate blocks the next lane step; I fix or stop, never skip.
- OVERNIGHT RUNS (12 h target, 16 h hard cutoff): check Codex `/status` and Claude `/usage` before starting; start soon after the Codex weekly reset when possible. If Codex quota is exhausted mid-run, continue on NVIDIA fallback for BUILD/TEST but route every REVIEW and PHYSICS decision to `claude -p`; never let an open model be the sole judge of physics. Log lane/model per step in `runs/<...>/run.log`.
- BUDGET: prefer `execute_code` (no LLM) over subagents for purely mechanical loops; pass subagents complete context (they know nothing); keep Fable calls to plan, critique, and sign-off.
- If only Fable weekly share is exhausted: use available Opus 5 for intermediate gates and defer Fable sign-off explicitly. If the shared Claude 5-hour window is exhausted, defer REVIEW/PHYSICS and do only independent work; Opus may also be unavailable. Never substitute a weaker model for final physics sign-off. Reserve final-signoff capacity before optional Fable calls; mandatory physics escalations block if capacity is unavailable.
- SU2ZX_PATH: /home/digimonk/Projects/SU2ZX_Foundation_Code_Package/SU2ZX. This routing and blocking-gate policy overrides conflicting legacy prompt routing/continuation rules; preserve deterministic gate scripts, evidence, run layouts, and pre-existing changes. A gate requires both its deterministic checks and Claude sign-off; failed gates block dependent work.
- Compression is always potentially lossy, even on the main model: physics conventions, acceptance criteria, evidence, and decisions must live in durable run files and be reloaded after compression. `auxiliary.review` is internal tool-output review, not research REVIEW or PHYSICS sign-off.


## /home/digimonk/.hermes/skills/orchestration/model-routing/SKILL.md
---
name: model-routing
description: "Use for SU2QC routing. Lanes, planning pass and gates."
---

# SU2QC model routing

Physics correctness > token economy > speed. Repo: /home/digimonk/Projects/SU2ZX_Foundation_Code_Package/SU2ZX. Claude only via claude -p, never Hermes anthropic provider. Internal auxiliary.review is not research REVIEW. Read SOUL.md and task-specific conventions before work.

## Precedence and prerequisites

The user approved overriding prompts/v0.5.0.md legacy NIM review assignments, weaker-model substitutions and failed-gate continuation. Keep deterministic scripts, evidence and existing run layouts. Failed gates block dependent steps; independent work may continue. Gate PASS requires both deterministic success and completed Claude review on the same snapshot. Physics doubt and final sign-off require Fable. No available Fable planning means defer; execute the plan without redesigning it.

Both claude-fable-5-1 and claude-opus-5 returned exactly OK in live probes. codex exec --help verifies -s workspace-write, not --full-auto. claude-sonnet-5 also returned exactly OK. Luna remains unverified; never guess its ID. --max-turns is accepted in a live Opus probe despite being hidden from claude --help.

## Command setup

Use terminal for these shell commands. Run planning/gate/final calls with background=True, notify=True or an explicit timeout=600, and read process exit/output before acceptance; do not rely on the 180s default. Budget every call within the run's remaining deadline. Re-establish variables per new shell, rather than relying on persistent exports. Replace editable values with actual selected files. Current prompts include *_v0.3.0.md, *_v0.4.0.md and v0.5.0.md; its frontmatter filename is not the actual filename.

```bash
set -euo pipefail
REPO=/home/digimonk/Projects/SU2ZX_Foundation_Code_Package/SU2ZX
cd "$REPO"
PROMPT="$REPO/prompts/v0.5.0.md"
RUN="$REPO/runs/section8_v0.5.0_$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -p "$RUN"/{run,src/su2qc,tests,gates/attempts,physics,reviews,bench,circuits,compile,prereg,hardware/raw,analysis/tables,analysis/figures,reports,logs/agents,logs/cmd,env}
```

For existing runs set RUN to the exact existing absolute path instead; never overwrite artifacts. Use write_file to create RUN/brief.md containing the full selected prompt, relevant proposal/plan sections with source paths, AGENTS.md/README conventions, and repo tree from git ls-files (first 300 entries with a truncation note if applicable). Required missing documents block planning; README is not a replacement for the proposal. Include the approved routing override in the brief.

## Planning pass — Fable

```bash
test -s "$RUN/brief.md"; test ! -e "$RUN/plan.md"
claude -p --model claude-fable-5-1 --allowedTools "Read,Grep,Glob,WebSearch,WebFetch" --max-turns 30 "ultrathink. Read $RUN/brief.md and cited proposal/plan sections. Plan this SU(2) lattice-gauge quantum-computing task. Markdown only: goals, exact physics acceptance checks, BUILD/TEST-BENCH/REVIEW/PHYSICS assignments, gate schedule with deterministic and reviewer pass/fail criteria, stop conditions, token budget excluding frontier models from mechanical loops. Respect the approved routing override. No file edits." > "$RUN/plan.md.partial"
test -s "$RUN/plan.md.partial"; mv "$RUN/plan.md.partial" "$RUN/plan.md"
```

Read and validate the entire response before accepting it. Empty/error/turn-limit output is not a plan. Execute the approved plan; escalate ambiguity or infeasibility to Fable.

## Intermediate gate — Opus 5

Freeze the snapshot; set BASE to its recorded baseline commit and N to a fresh gate-attempt identifier. With write_file prepare gate-input-N.md: plan criteria, deterministic commands/exit codes/JSON targets and measurements, evidence paths and relevant untracked file contents/inventory (git diff omits them).

```bash
BASE=<recorded-base-commit>
N=<gate-and-attempt>
test -s "$RUN/gate-input-$N.md"; test ! -e "$RUN/gate-$N.md"
git -C "$REPO" diff "$BASE" -- > "$RUN/diff-$N.patch"
claude -p --model claude-opus-5 --allowedTools "Read,Grep,Glob" --max-turns 20 "Validation gate $N per $RUN/plan.md. Read $RUN/gate-input-$N.md, $RUN/diff-$N.patch and all cited evidence. Verify each acceptance criterion, deterministic results and snapshot identity. Reply PASS or FAIL first, then evidence and required fixes. Missing evidence is FAIL. No edits." > "$RUN/gate-$N.md.partial"
test -s "$RUN/gate-$N.md.partial"; mv "$RUN/gate-$N.md.partial" "$RUN/gate-$N.md"
```

Gate requires script exit 0, criterion-level JSON evidence AND validated Claude verdict on the same snapshot. No edits to gates/tolerances to force PASS. Failed/absent evidence blocks dependent steps. Escalate physics doubt to Fable. Claude gate-N.md is supplementary to gates/ scripts and JSON.

## Final physics sign-off — Fable

Prepare final-input.md with whole-run diff including untracked files, gate ledger, acceptance criteria, evidence, snapshot and open issues.

```bash
test -s "$RUN/final-input.md"; test ! -e "$RUN/final-signoff.md"
claude -p --model claude-fable-5-1 --allowedTools "Read,Grep,Glob" --max-turns 30 "Final physics sign-off of the whole run. Read $RUN/plan.md, $RUN/final-input.md and all cited gates/evidence. Check gauge invariance, Gauss law, Hamiltonian conventions, Trotter/ZX equivalence and every applicable criterion. Reply PASS or FAIL, evidence, limitations and fixes. Missing evidence is FAIL. No edits." > "$RUN/final-signoff.md.partial"
test -s "$RUN/final-signoff.md.partial"; mv "$RUN/final-signoff.md.partial" "$RUN/final-signoff.md"
```

Validate response and evidence. Unavailable Fable means explicitly deferred final sign-off, never a weaker substitute.

## Background REVIEW — Opus

The terminal schema uses notify=True, NOT notify_on_complete=True. Substitute absolute run paths and a fresh N:

```python
terminal(command='claude -p --model claude-opus-5 --allowedTools "Read,Grep,Glob" --max-turns 20 "Review physics-bearing code against <absolute-run>/plan.md, <absolute-run>/diff-<N>.patch, <absolute-run>/gate-input-<N>.md and cited files. PASS or numbered blocking fixes with evidence. No edits." > <absolute-run>/review-<N>.md', workdir='/home/digimonk/Projects/SU2ZX_Foundation_Code_Package/SU2ZX', background=True, notify=True)
```

REVIEW checks implementation defects, security and maintainability; PHYSICS checks acceptance evidence and physical claims. Reuse the REVIEW findings in the gate packet rather than re-requesting the same review. For tests/benchmark-only diffs record REVIEW as not applicable only when the Fable plan explicitly allows it. Track process handle, wait for completion and read output before gate acceptance. Truncated/failed reviews block. Preserve existing reviews/ artifacts; never overwrite attempts.

## BUILD — Codex

```bash
codex exec -m gpt-6-astra -s workspace-write -C /home/digimonk/Projects/SU2ZX_Foundation_Code_Package/SU2ZX "<approved module task, exact ownership, conventions, tests and limits>" </dev/null
```

Main Codex writes normal BUILD code. Large harness modules use terminal(background=True, notify=True). Review model differs from builder. Fable handles hard debugging and physics doubts.

## TEST-BENCH templates

```python
delegate_task(tasks=[{'goal':'Run specified tests, report real outputs; no physics judgment.', 'context':'Repo: /home/digimonk/Projects/SU2ZX_Foundation_Code_Package/SU2ZX. Interpreter: /home/digimonk/Projects/SU2ZX_Foundation_Code_Package/SU2ZX/.mamba/envs/su2zx/bin/python. Run: <ABSOLUTE RUN>. Read <PLAN AND CONVENTIONS>. Execute <EXACT COMMANDS>. Own only <ABSOLUTE OUTPUT FILES>. Expected checks <CRITERIA>. Timebox <SECONDS>. Record exit codes, measured values, artifacts and failures. Never edit gate scripts.'}])
```

```python
from hermes_tools import terminal, write_file
import json
commands = []  # Fill exact plan-approved sweep commands and absolute paths.
assert commands, 'Supply approved sweep commands'
results = []
for command in commands:
    result = terminal(command, timeout=180)
    results.append({'command':command, **result})
    write_file('<ABSOLUTE RUN>/bench/sweep.json', json.dumps(results, indent=2))
    if result.get('exit_code') != 0:
        break
```

Use bounded batches and persist each result. Pure mechanics use execute_code, not model calls per iteration. Max 2 NVIDIA children, ~40 RPM shared across all NIM lanes. On 429 wait/backoff, never retry storm. Children inherit no context; verify their artifacts. Do not poll child transcripts; results arrive between turns.

## Quotas and model budget

Use terminal PTY: codex → /status; claude → /usage. Record observed quotas/reset, UNKNOWN if unavailable. Prefer Codex weekly reset. Inspect `hermes logs --since 10m` and filter API call records with Python, or search_files on agent.log; record actual provider/model, not assumed config. Missing log evidence stays unverified.

Task → model:
- Planning, critiques, final research docs, nine/month plans, JEPA/QML plans, hard debugging, physics doubt and final physics sign-off → Fable 5.1.
- Research first drafts, intermediate gates, physics-bearing code review when Fable not clearly needed → Opus 5.
- Doc polish / quick second opinions only → verified claude-sonnet-5.
- BUILD → Astra gpt-6-astra, or configured Codex gpt-5.6-sol.
- Luna → no verified ID or assigned lane; never guess/use for physics judgment.
- Reasoning-assisted test work → NIM worker deepseek-ai/deepseek-v4-flash-0731.
- Mechanical sweeps, tests, tables → execute_code (no LLM per iteration).

Fable uses at most 50% weekly Claude allocation; reserve for plan/critique/sign-off. Fable-only exhaustion permits Opus intermediate gates. Shared Claude 5-hour exhaustion may block Opus too: defer REVIEW/PHYSICS and do only independent work. If Opus fails and Fable is available, use Fable and account for budget. Codex exhaustion permits automatic NVIDIA BUILD/TEST fallback, never sole open-model physics judgment. Fable final sign-off is never substituted.

Automatic Fable escalation triggers: changes to Hamiltonian, Gauss-law or Trotter/ZX physics logic; deterministic/Claude disagreement; reviewer uncertainty; or Claude FAIL on a physics criterion. Ordinary nonphysics FAILs block and return to BUILD. Under NIM fallback, acceptance still requires the Claude verdict's first line to be exactly PASS, complete deterministic evidence and no unresolved findings; the fallback model cannot waive these conditions. Reserve at least one final-signoff call allowance at preflight within the 50% Fable share; if remaining quota cannot establish that reserve, defer optional intermediate Fable calls. Mandatory physics escalations block rather than consume an uncertain reserve.

Compression consumes main-subscription quota under auto; include that cost in preflight. Compression auto is not lossless and not a guarantee of provider under fallback. Persist physics criteria/conventions/evidence and reload after compression. Changes to SOUL/config apply to new sessions, not a mid-session system-prompt mutation.


## /home/digimonk/.hermes/skills/research/su2qc-run-protocol/SKILL.md
---
name: su2qc-run-protocol
description: "Use for SU2QC overnight runs. Preflight, gates and reports."
---

# SU2QC overnight run protocol

Repo: /home/digimonk/Projects/SU2ZX_Foundation_Code_Package/SU2ZX. Load model-routing for executable lane commands. This protocol is not authorization to launch a run or hardware job.

## Preflight

1. Read actual task prompt, relevant proposal/plan, AGENTS.md and README. Current names include *_v0.3.0.md, *_v0.4.0.md and v0.5.0.md, not always frontmatter filenames.
2. Check codex /status and claude /usage interactively; record actual quotas/reset or UNKNOWN. Prefer starting after Codex weekly reset. Run hermes doctor in the separate global setup context; resolve relevant blockers before research execution.
3. Check git status --short and baseline commit. Dirty repo blocks a new unattended run until user approves preserved baseline/clean worktree strategy. Never clean/stash/overwrite existing work automatically.
4. Create unique runs/<UTC-date>-<slug>/ with Fable-produced plan.md, run.log, gates/, reviews/, bench/. Preserve existing prompt-specific run naming/layout instead when applicable. Never overwrite prior outputs.
5. Verify /home/digimonk/Projects/SU2ZX_Foundation_Code_Package/SU2ZX/.mamba/envs/su2zx/bin/python exists/works. Record interpreter, input hashes, seeds, snapshot, environment and file ownership. Research files stay inside repo; .work/ for temporary files, single .mamba/ prefix.
6. Complete Fable planning before BUILD. Missing required docs or Fable blocks planning. Persist acceptance criteria, conventions and evidence; any compression is potentially lossy.

## Source conventions and approved override

Sources: AGENTS.md §§Scope lock, Physics gates, External actions; README.md §§Setup and reproduction, Outputs; prompts/v0.5.0.md §§0–4, §9. The user approved new routing/blocking rules overriding conflicting legacy assignments and continuations, preserving source files and uncommitted work.

Keep v0.5.0 runs/section8_v0.5.0_<RUNID>/ layout; run/T0, run/TASKBOARD.md, run/GATES.md, run/MODELS.md, run/HEARTBEAT.md, run/DECISIONS.md, gates/attempts/, physics/, prereg/, reports/REPORT.md, logs/agents/, logs/cmd/ and manifest. Supplement with plan.md, run.log and bench/. Claude gate-N.md/review-N.md supplement rather than replace gates/gate_<G>.py and gates/GATE_<G>.json or reviews/ evidence.

Override NIM review decisions with Opus REVIEW/PHYSICS and Fable final sign-off. No Hermes anthropic provider, no weaker-model physics substitute. Max 2 NVIDIA children. Failed gates block dependent G+1 steps and legacy fallback continuation; independent work can proceed. Reduced scope requires Fable plan amendment and explicit reporting, never relabel a failed gate as passed. Preserve independent Hamiltonian routes and reviewer/builder model separation. Physics doubt goes to Fable.

Preserve two attempts then Fable escalation, maximum three escalations per gate/six per run, none after T+14h. Write versioned solutions without overwriting before fresh builders implement them. Unavailable Fable blocks physics escalations.

## Execution and deadline enforcement

Planning → BUILD → TEST-BENCH → background REVIEW → PHYSICS gate → next dependent step. A gate requires deterministic exit 0, criterion-level JSON targets/measurements and completed Claude sign-off on the same frozen snapshot. Opinions alone never pass gates; never alter gates/tolerances to force success.

Use absolute paths and complete child context, disjoint ownership, and model-routing commands. Repeated tests/sweeps use execute_code or bounded workers. Wait for review process completion and read its output before gate acceptance. Log timestamp/lane/actual model-provider/snapshot/command/artifacts/status at every step. Unknown usage remains unknown.

12h target; evaluate extension T+11h using prompt criteria, no new escalation T+14h, freeze non-packaging work T+15h, absolute stop T+16h. Use an approved durable runner with monotonic deadline and each subprocess capped to remaining time. Launch through terminal(background=True, notify=True), e.g. `timeout --signal=TERM --kill-after=60s 57600s <approved-runner-command>` in the repo. Runner must trap TERM, terminate tracked process groups, flush partial report and enforce T+15h freeze. Verify shutdown in a shortened-clock dry-run before launch: T+15h-equivalent freeze fires, TERM reaches the tracked Claude/Codex process groups (use harmless process stand-ins first), and the partial report is flushed. Verify backend lifetime handling permits the intended durable job; an unverified runner/backend blocks unattended launch. This is a template, not an existing tested runner. Cron reminders alone do NOT enforce cutoff.

Update reports/REPORT.md every gate, heartbeat at least every 30 minutes, and continuously persist partial results. At cutoff stop compute/reviews, preserve evidence, mark failed/incomplete gates/deferred sign-off and package only produced outputs. Never skip gates to meet a deadline. CLI cron has no chat delivery; requested notifications need an explicit gateway destination.

## Fallback and safeguards

Inspect hermes logs --since 10m API call records with Python filtering or search_files on agent.log. Record actual model/provider, not just configuration; mark unavailable evidence UNKNOWN. Codex exhaustion permits NVIDIA BUILD/TEST; all REVIEW/PHYSICS still require Claude. Opus may handle gates when Fable-only share exhausted; shared Claude-window exhaustion can block both. Final Fable sign-off stays deferred, never replaced.

Preserve AGENTS.md claim boundaries and hardware safeguards: ALLOW_IBM_QPU_SUBMISSION=1, --submit and exact fresh dry-run token. Task hardware flags do not waive these. Twin never means hardware. Retain preregistration config hash/change log; no production before signed preregistration. Distinguish legacy core.py conventions from new task conventions.py; never conflate physical objects or claims.

## End-of-run report

Run ID / prompt + hash / baseline and final snapshot / elapsed / COMPLETE or PARTIAL
Physics: criterion | target | measured | evidence artifact | PASS/FAIL/UNVERIFIED
Gates: gate-attempt | deterministic exit + JSON | Claude reviewer/model | verdict | evidence
Lane usage: BUILD / TEST-BENCH / REVIEW / PHYSICS | actual model/provider | calls/tokens if observable, otherwise unknown
Conclusions, claim boundaries, hardware/twin labels
Open issues, stopped dependencies, scope changes
Fable final sign-off path/verdict or DEFERRED with exact pending decisions
Report/manifest/artifact paths and reproduction commands

## Verification

Read cited artifacts, match reviewed snapshot and all acceptance criteria, count totals programmatically, reconcile gate ledger and report. No fabricated data/usage or completion for unavailable reviews. A plan is not execution; reviewer PASS is not numerical evidence. Report real execution and blockers.

## Config diff
--- config.before
+++ config.after
@@ -75,8 +75,7 @@
     provider: openai-codex
     model: gpt-6-astra
   compression:
-    provider: nvidia
-    model: nvidia/nemotron-3-super-120b-a12b
+    provider: auto
   approval:
     provider: nvidia
     model: nvidia/nemotron-3.5-lightning-30b-a3b
@@ -228,41 +227,3 @@
     - web
     - x_search
     - yuanbao
-
-# ── Security ──────────────────────────────────────────────────────────
-# Secret redaction is ON by default — strings that look like API keys,
-# tokens, and passwords are masked in tool output, logs, and chat
-# responses before the model or user ever sees them. Set redact_secrets
-# to false to disable (e.g. when developing the redactor itself).
-# tirith pre-exec scanning is enabled by default when the tirith binary
-# is available. Configure via security.tirith_* keys or env vars
-# (TIRITH_ENABLED, TIRITH_BIN, TIRITH_TIMEOUT, TIRITH_FAIL_OPEN).
-#
-# security:
-#   redact_secrets: true
-#   tirith_enabled: true
-#   tirith_path: "tirith"
-#   tirith_timeout: 5
-#   tirith_fail_open: true
-
-# ── Fallback Model ────────────────────────────────────────────────────
-# Automatic provider failover when primary is unavailable.
-# Uncomment and configure to enable. Triggers on rate limits (429),
-# overload (529), service errors (503), or connection failures.
-#
-# Supported providers:
-#   openrouter   (OPENROUTER_API_KEY)  — routes to any model
-#   openai-codex (OAuth — hermes auth) — OpenAI Codex
-#   nous         (OAuth — hermes auth) — Nous Portal
-#   zai          (ZAI_API_KEY)         — Z.AI / GLM
-#   kimi-coding  (KIMI_API_KEY)        — Kimi / Moonshot
-#   kimi-coding-cn (KIMI_CN_API_KEY)   — Kimi / Moonshot (China)
-#   minimax      (MINIMAX_API_KEY)     — MiniMax
-#   minimax-cn   (MINIMAX_CN_API_KEY)  — MiniMax (China)
-#   bedrock      (AWS IAM / boto3)     — AWS Bedrock (Converse API)
-#
-# For custom OpenAI-compatible endpoints, add base_url and key_env.
-#
-# fallback_model:
-#   provider: openrouter
-#   model: anthropic/claude-sonnet-4
