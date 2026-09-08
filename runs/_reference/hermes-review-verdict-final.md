Verification is complete. Everything I could check live matches the document.

**PASS.** No remaining concrete contradictions or invalid commands.

What I verified against the live install:

- **claude CLI:** `-p`, `--model`, `--allowedTools` (comma-separated is documented) exist. `--max-turns` is absent from help, as the document states. The Opus probe evidence is accepted as given.
- **Hermes terminal tool:** the schema advertises `background`, `timeout` (default 180, foreground cap 600, over-cap promotes to background), `workdir`, `pty` (background only), and `notify` as bool or pattern list. The document's `terminal(..., background=True, notify=True)` call is valid. One nit: `notify_on_complete` is still accepted as a legacy alias, so "NOT notify_on_complete" is overstated but harmless.
- **execute_code stubs:** `from hermes_tools import terminal, write_file` is valid. The sandbox `terminal(command, timeout=..., workdir=...)` returns a dict with `output` and `exit_code`. The sweep template is correct.
- **delegate_task:** `tasks=[{'goal':..., 'context':...}]` is the canonical shape. Placeholder rejection applies only to `goal`, which the template keeps concrete.
- **hermes logs --since 10m** and **hermes doctor** both exist in the installed CLI source.
- **Config:** the live config has `auxiliary.compression.provider: auto` exactly as the diff shows. Deployed SOUL.md and both SKILL.md files are byte-identical to the review text.
- **Paths:** the repo, `prompts/v0.5.0.md`, AGENTS.md, README.md and the mamba interpreter all exist.

Two items I could not re-run in this sandbox and am relying on the document's prior live evidence for:

- `codex exec -s workspace-write -m -C` flags. The command needed approval here.
- Contents of the Hermes `.env` and `auth.json`. This matters because the aux "auto" chain can reach native Anthropic, but only when the anthropic provider is explicitly configured. Source comment: "Claude Code credentials must not silently become aux fallback." Since the policy forbids configuring that provider, the chain cannot reach Anthropic as long as no `ANTHROPIC_API_KEY` or anthropic auth entry exists. Confirm that at preflight.

Overnight runner remains untested, and the document correctly gates launch on that dry run.
