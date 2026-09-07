# Role -> model routing (updated as children return)
Orchestrator: hermes claude-fable-5 (this session)
Builders: hermes delegate_task children (inherit claude-fable-5); codex CLI 0.153.4 available for spot builds
Reviewers (code+physics): delegate_task children, instructed independent derive-first
Escalation: claude-fable-5-1 requested; fallback = delegate_task max effort
Gatekeeper: deterministic python scripts (no LLM)
Scribe: orchestrator
NOTE: per-role provider pinning via delegate_task is not exposed in this Hermes version;
delegate_task children run on nvidia/nemotron-3.5-lightning-30b-a3b (observed). Independence is enforced by fresh context + disjoint
file ownership + predict-before-compute, and recorded honestly here.
