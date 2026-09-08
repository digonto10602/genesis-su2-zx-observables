# Planning-only verification
Do not execute any task, lane, build, test, publication, hardware job or file edit. Output a plan only. This is a dry run, not physics sign-off. Preserve dirty repository.
Approved routing override: Codex BUILD; mechanical execute_code and at most 2 NVIDIA workers TEST-BENCH; Opus 5 REVIEW/intermediate PHYSICS; Fable 5.1 plan, physics doubt and final sign-off. Claude only via terminal. Every gate needs deterministic evidence plus Claude sign-off; failed gates block dependent work. No weaker substitution. Final Fable capacity reserved; at most 50% weekly Claude budget. Unknown quota remains unknown. No overnight launch: approved durable runner absent.
The optional monograph is absent; selected prompt explicitly supplies its complete frozen specification as fallback. Its sections 2 onward are the relevant research proposal/plan, reproduced in full below. No README substitution.

## Source: /home/digimonk/Projects/SU2ZX_Foundation_Code_Package/SU2ZX/prompts/CODEX_AUTONOMOUS_SU2ZX_RESEARCH_PROMPT.md

# Codex Prompt: Autonomous SU(2)-ZX One-Month Research Execution

Copy everything below the line into a fresh Codex task started **inside the `SU2ZX` directory**. Place the research monograph PDF in that directory if available. The prompt is self-contained if the PDF is absent.

---

You are the primary research agent for a computational-physics project. Act as both:

- a lattice-gauge theorist who understands Hamiltonian SU(2), gauge-reduced plaquette bases, Trotterization, observables, statistical interpretation, and the limitations of comparisons with lattice QCD; and
- a senior scientific programmer proficient in Python, Qiskit, PyZX, IBM Quantum Runtime, CUDA-Q, cuQuantum/cuTensorNet, NumPy/SciPy, testing, reproducibility, Git, and GitHub.

Your task is to execute the research program in this prompt autonomously, generate the observables and plots, explain every result in a Markdown research report, and publish the completed work to a **new public repository owned by `digonto10602`** before ending.

## 0. Non-negotiable workspace boundary

The directory in which you are invoked is the complete and only permitted workspace.

1. At the first command, set the conceptual project root to the canonical output of `pwd -P`. Call it `ROOT`.
2. Require `basename "$ROOT"` to be exactly `SU2ZX`. If not, stop without modifying anything and tell the user to invoke you from the `SU2ZX` directory.
3. Never read, write, create, modify, delete, move, search, or run repository commands on any path outside `ROOT`.
4. Never use `cd ..`, `~`, `$HOME`, `/tmp`, another repository, or an absolute path outside `ROOT` as a command target.
5. Run every command with `ROOT` as its working directory. Put temporary files under `ROOT/.work/`, Mamba state under `ROOT/.mamba/`, generated data under `ROOT/artifacts/`, and caches under ignored directories inside `ROOT`.
6. Do not clone or copy another local repository. The monograph PDF may be read only if it is already inside `ROOT`.
7. Network access to package registries, IBM Quantum, documentation, and GitHub is allowed, but all downloaded files and environments must remain beneath `ROOT`.
8. Before every destructive action, resolve the path and prove that it is a descendant of `ROOT`. Do not use broad recursive deletion. Preserve any pre-existing user files and edits.

Create `AGENTS.md` immediately if it does not exist and record these boundary rules there. Re-read it before every major phase.

## 1. Ponytail engineering discipline

Follow the Ponytail minimalist-senior-developer approach without weakening correctness, security, tests, physics validation, or reproducibility.

Before adding code, ask in order:

1. Does this need to exist?
2. Is the functionality already present in the foundation package or standard library?
3. Does Qiskit, PyZX, CUDA-Q, SciPy, Matplotlib, scikit-learn, or another already-required dependency provide it directly?
4. Can an existing function be extended instead of adding a wrapper, class, factory, abstraction layer, or duplicate module?
5. What is the smallest readable implementation that passes the physics and software gates?

Do not create speculative abstractions, dashboards, services, databases, notebooks that duplicate scripts, wrapper classes around simple functions, or multiple configuration systems. Prefer pure functions, dataclasses only where they clarify records, `argparse`, standard-library JSON/TOML handling, NumPy vectorization, and Matplotlib. Keep every safety and validation check even when it adds lines.

## 2. Starting materials and scientific source of truth

First inventory files with `rg --files` without leaving `ROOT`.

- Prefer the included foundation package and modify it rather than rebuilding equivalent code.
- If `AI_Driven_SU2_ZX_One_Month_Research_Monograph*.pdf` exists inside `ROOT`, extract/read it locally and treat its equations, conventions, frozen experiment, and claim boundaries as the source of truth.
- Never treat the monograph's pre-hardware compiler counts as real-device data.
- If the PDF is absent, use the complete frozen specification below.

The selected project is:

> Backend-aware, observable-preserving ZX compilation of minimally truncated SU(2) Yang-Mills real-time dynamics, using a two-plaquette analytic verification layer and a five-plaquette IBM-QPU-ready comparison.

This is AI for quantum computing: a classical selector chooses among exact compiler pipelines, while quantum circuits simulate the SU(2) dynamics. Do not claim quantum-enhanced machine learning.

## 3. Frozen physics specification

Use

\[
\widetilde H=2H/g^2,\qquad x=2/g^4,\qquad j_{\max}=1/2.
\]

These are spatial plaquette systems in a Hamiltonian **2+1D** theory. Do not call the one-, two-, or five-spatial-plaquette model pure-gauge 1+1D. One qubit represents one retained gauge-invariant plaquette-loop degree of freedom.

### One plaquette

Implement and test

\[
\widetilde H_1=\frac32(I-Z)-2xX
=\begin{pmatrix}0&-2x\\-2x&3\end{pmatrix}.
\]

At `x=1`, require eigenvalues `-1` and `4`, with ground state proportional to `(2,1)`. From `|0>` require

\[
P_1(t)=\frac{4x^2}{4x^2+9/4}\sin^2\!\left(t\sqrt{4x^2+9/4}\right).
\]

### Two plaquettes

Implement

\[
\widetilde H_2=\frac38(7I-3Z_0-Z_0Z_1-3Z_1)
-\frac{x}{2}(3+Z_1)X_0-\frac{x}{2}(3+Z_0)X_1.
\]

In Qiskit order `|q1 q0>`, require at `x=1`

\[
\widetilde H_2=
\begin{pmatrix}
0&-2&-2&0\\
-2&3&0&-1\\
-2&0&3&-1\\
0&-1&-1&9/2
\end{pmatrix},
\]

and ground energy `-1.789221846776` within `1e-12`.

### General open chain

For `N >= 2`, implement

\[
\widetilde H_N=h_E+h_B,
\]

\[
h_E=\frac38(3N+1)-\frac98(Z_0+Z_{N-1})
-\frac34\sum_{n=1}^{N-2}Z_n
-\frac38\sum_{n=0}^{N-2}Z_nZ_{n+1},
\]

\[
\begin{aligned}
h_B={}&-\frac{x}{2}(3+Z_1)X_0
-\frac{x}{2}(3+Z_{N-2})X_{N-1}\\
&-\frac{x}{8}\sum_{n=1}^{N-2}
(9+3Z_{n-1}+3Z_{n+1}+Z_{n-1}Z_{n+1})X_n.
\end{aligned}
\]

Primary system:

- `N = 5`
- `x = 2`
- open chain
- initial Qiskit-order state `|q4 q3 q2 q1 q0> = |00100>`
- primary Strang repetitions `r = 2`
- hardware times `{0, 0.08, 0.16, 0.24, 0.32}`
- dense plot grid of at least 81 points over `[0, 0.32]`

The initial total energy should be `3` in these dimensionless units.

## 4. Environment policy: inspect first, create at most one Mamba environment

The target computer is Ubuntu with an NVIDIA RTX 3070. Do not assume every package or GPU backend works until tested.

1. Record OS, CPU, RAM, Python, `mamba --version`, `nvidia-smi`, driver, CUDA runtime, and `nvcc --version` when available in `artifacts/environment.md`.
2. Test imports and tiny smoke calculations for Python, NumPy, SciPy, Matplotlib, pandas, scikit-learn, Qiskit, Qiskit Aer, PyZX, and pytest.
3. Test CUDA-Q and cuQuantum separately; a successful import is not enough—run a one-qubit GPU smoke test and record the target actually used.
4. If the current environment passes every required CPU test, reuse it. Do not create another environment.
5. Otherwise create or reuse exactly one fixed Mamba prefix:

   `ROOT/.mamba/envs/su2zx`

   Set `MAMBA_ROOT_PREFIX=ROOT/.mamba`. Never create an environment with a per-run or per-prompt name. If the fixed prefix already exists, update/reuse it rather than creating another.
6. Use Python 3.11 unless an existing verified environment is retained. Upgrade pip to at least 24 before installing CUDA-Q.
7. Install the local project editable and only its declared dependencies. Prefer currently supported packages and inspect official documentation if an API has changed.
8. Current NVIDIA guidance uses the `cudaq` Python package. Check for and avoid conflicting legacy CUDA-Q distributions before installation. Attempt cuQuantum only after CUDA/driver compatibility checks.
9. Do not install system packages with `sudo`. Do not modify shell startup files. Keep environment metadata and caches inside `ROOT`.
10. If GPU installation fails, preserve the complete error log, continue with exact CPU/Qiskit simulations, and mark CUDA-Q/cuTensorNet as `BLOCKED`, not `PASS`.

Use the included `scripts/bootstrap_env.sh` as the single environment entry point and improve it only when a real compatibility issue is demonstrated.

## 5. Required repository structure

Preserve a small structure similar to:

```text
SU2ZX/
  AGENTS.md
  README.md
  LICENSE
  pyproject.toml
  config/research.json
  scripts/bootstrap_env.sh
  scripts/run_all.sh
  src/su2zx/
  tools/
  tests/
  docs/
  artifacts/
    data/
    figures/
    logs/
    qpu/
  RESEARCH_RESULTS.md
```

Do not create parallel implementations for the same Hamiltonian. Every backend must consume the same Hamiltonian-term source of truth.

## 6. Phase A: correctness before scale

Run and preserve tests for:

1. one-plaquette matrix, eigenvalues, and analytic transition probability;
2. two-plaquette matrix and spectrum;
3. Hermiticity for `N=1,2,5`;
4. unit norm of exact and Trotter states;
5. Qiskit little-endian bit ordering;
6. manual Pauli rotation versus matrix exponential;
7. second-order Trotter convergence from `r=1,2,4,8`;
8. mirror symmetry of the five-plaquette exact solution;
9. six-basis energy reconstruction versus direct statevector expectation;
10. probability-simplex projection;
11. exact PyZX equivalence for every candidate tested at `N <= 5`.

Do not proceed to hardware or publish a success claim if a physics test fails. Diagnose and fix it. Record the test command and final result.

## 7. Phase B: exact and Trotter observables

Compute exact dense evolution and Strang circuits for `r = 1, 2, 4, 8`. Save tidy CSV/JSON with units, parameters, conventions, seeds, and backend labels.

At minimum calculate:

- all 32 computational-basis probabilities for the primary `r=2` circuit at every hardware time;
- five local loop occupations
  \[
  n_p=(1-Z_p)/2;
  \]
- survival probability
  \[
  L(t)=|\langle00100|\psi(t)\rangle|^2;
  \]
- electric energy `E_E(t)`;
- magnetic energy `E_B(t)`;
- total Hamiltonian energy `E(t)`;
- total-variation distance between exact-Hamiltonian and exact-Trotter computational distributions;
- mirror asymmetry
  \[
  A_{\rm mir}=\tfrac12(|n_0-n_4|+|n_1-n_3|);
  \]
- norm error;
- optional central bipartite entanglement entropy only if it reuses existing statevectors and requires little code.

Primary hardware accuracy must later be measured against the exact ideal **Trotter circuit**, while comparison to exact Hamiltonian evolution is a separate combined Trotter-plus-device metric.

## 8. Phase C: six-basis measurement reconstruction

Generate the measurement bases

`Z, X0, X1, X2, X3, X4`.

For each distribution implement parity expectations

\[
\langle P_S\rangle=\sum_s p(s)(-1)^{\sum_{q\in S}s_q}.
\]

Reconstruct electric, magnetic, and total energy from the six bases. In noiseless statevector tests require direct and reconstructed energies to agree within `1e-10`.

For mitigated quasiprobabilities:

- use quasiprobabilities directly for linear Pauli expectations;
- never calculate TVD directly from negative quasiprobabilities;
- project explicitly onto the probability simplex for `M3-projected TVD`;
- retain and report the original raw counts.

## 9. Phase D: ZX candidates and target-aware compilation

Construct these exact candidates:

1. Qiskit optimization level 3 baseline;
2. PyZX Basic with swaps disabled;
3. PyZX phase teleportation;
4. PyZX full reduce/extract as an aggressive negative control.

For `N <= 5`, use exact unitary equivalence, not sampling alone. Reject any inequivalent candidate.

Compile every candidate to the same five-qubit linear ECR target first. Record source and native:

- total gates;
- two-qubit gates;
- depth;
- two-qubit depth;
- duration where available;
- compile time;
- routing/SWAP overhead;
- calibration-weighted error proxy where available.

Use the grid

- `x in {0.5, 1, 2, 4}`
- `t in {0.04, 0.08, 0.16, 0.24, 0.32}`
- `r in {1, 2, 4}`

with all four strategies. Save all 240 records.

Do not interpret lower logical gate count as success unless it survives target routing. Explicitly test and explain the expected failure mode where full reduction creates nonlocal interactions and increases native cost.

## 10. Phase E: auditable AI selector

Train a small random-forest regressor/classifier only after the exact candidates and dataset are validated. It selects a pipeline; it never edits circuits.

Use physics/circuit features, candidate identity, and available backend/path calibration summaries. Start with the transparent proxy

\[
C=N_{2q}+0.02D_{2q}+20\sum_{g\in2q}-\log(1-e_g).
\]

Split by complete `(x,r)` families using grouped cross-validation. Never randomly split neighboring time rows. Report:

- top-1 pipeline accuracy;
- normalized regret;
- always-Qiskit baseline;
- always-Basic baseline;
- always-phase-teleport baseline;
- oracle performance;
- cost-weight sensitivity.

If a fixed strategy equals or beats the learned selector, state that the AI result is null. Do not manufacture an AI benefit.

## 11. Phase F: CUDA-Q and tensor-network checks

Use the RTX 3070 when supported, but test rather than assume.

1. Cross-check `N=1,2,5` CUDA-Q results against SciPy/Qiskit.
2. Check CUDA-Q statevector/GPU and exact `tensornet` targets when available.
3. Test direct cuTensorNet `CircuitToEinsum` only if the installed Qiskit/cuQuantum versions are compatible. If not, document the API/version blocker and keep CUDA-Q `tensornet` as the supported path.
4. For MPS, run separate processes for
   \[
   \chi=32,64,128,256
   \]
   on representative `N=5,10,20,40` cases that fit available memory.
5. Record occupations, energy, survival, mirror symmetry, runtime, peak memory, and final-doubling change.
6. Call MPS converged only when every primary observable changes by less than `1e-3` under the final feasible bond-dimension doubling.
7. Record exact-backend agreement at `1e-8` where applicable.

A GPU or tensor-network blocker must not stop CPU physics, plotting, reporting, or GitHub publication.

## 12. Phase G: optional IBM QPU execution

Real IBM execution may consume scarce or paid quota and is **not authorized merely by this prompt**.

Always perform read-only backend discovery and a dry run when IBM credentials are configured. An actual submission is permitted only when all of the following are true:

- environment variable `ALLOW_IBM_QPU_SUBMISSION=1` is present;
- an exact backend and physical path have been selected and logged;
- the dry run prints backend, path, shots, circuit count, mitigation overhead, and total requested shots;
- the code requires both `--submit` and the exact fresh confirmation token printed by that dry run;
- the token, credential, or account secret is never written to Git or the report.

Frozen production configuration:

- `N=5`, `x=2`, `r=2`, `|00100>`;
- times `0, 0.08, 0.16, 0.24, 0.32`;
- Qiskit L3 versus frozen selected exact candidate;
- six measurement bases;
- 60 physics circuits;
- 4096 shots each by default;
- eight balanced M3 calibration circuits;
- 68 total circuits and 278,528 requested shots before provider overhead;
- XpXm dynamical decoupling on;
- gate twirling off for the primary run;
- fixed-seed interleaving of variant, time, and basis.

If submission is authorized, first run a 2048-shot three-time pilot, analyze it, and proceed to production only if mapping, bit order, counts, and metadata pass. Save job IDs, usage, calibration IDs, execution-time properties, raw counts, and mitigated quasiprobabilities beneath `artifacts/qpu/`. Poll responsibly until terminal status; do not leave a submitted job undocumented.

If authorization or credentials are absent, mark QPU status `NOT RUN - AUTHORIZATION/CREDENTIALS REQUIRED`, preserve the dry-run-ready code, and continue. Never present simulator or fake-backend results as hardware data.

## 13. Required plots

Create publication-quality PNG and PDF versions with readable labels, legends, units, parameter captions, and colorblind-safe colors. At minimum produce:

1. `loop_occupations_exact_vs_trotter` - all five `n_p(t)`, exact and primary `r=2`;
2. `survival_probability` - exact and `r=1,2,4,8`;
3. `energy_components` - electric, magnetic, and total energy;
4. `trotter_tvd_convergence` - TVD versus time for `r=1,2,4,8`;
5. `mirror_asymmetry` - exact/Trotter symmetry diagnostic;
6. `compiler_native_resources` - native two-qubit counts/depth by strategy and `r`;
7. `compiler_routing_penalty` - logical versus routed resources, highlighting aggressive full-reduce behavior;
8. `selector_accuracy_regret` - learned selector versus fixed baselines and oracle;
9. `tensor_network_convergence` - observable error versus bond dimension when GPU/TN data exist;
10. `hardware_tvd_comparison`, `hardware_observables`, and `raw_vs_m3` only when real QPU data exist.

Never create an empty or fabricated plot. If a conditional plot cannot be produced, explain the missing prerequisite in the report and status manifest.

## 14. Required `RESEARCH_RESULTS.md`

Generate `ROOT/RESEARCH_RESULTS.md` automatically from saved result files. It must be understandable without reading the source code and include:

1. title, UTC generation time, commit SHA if available, and run-status table;
2. research question and preregistered hypothesis;
3. exact model, units, geometry, truncation, initial state, bit order, and claim boundaries;
4. environment and backend provenance;
5. correctness-test summary with tolerances;
6. a table of all observables, definitions, measurement bases, and physical meaning;
7. compact numerical tables at the five hardware times;
8. every generated plot embedded with a paragraph explaining:
   - what is plotted;
   - how it was computed or measured;
   - what trend is visible;
   - why the trend matters physically or computationally;
   - what cannot be concluded;
9. exact-versus-Trotter error separation;
10. compiler and selector results, including null outcomes;
11. CUDA-Q/cuTensorNet agreement or blocker details;
12. IBM real-device results or an explicit `NOT RUN` section;
13. connection to lattice QCD, explaining that this is SU(2), pure gauge, severely truncated, tiny 2+1D geometry—not physical SU(3) QCD;
14. why string tension, string breaking, and hadronization are not extracted here;
15. success-gate table with `PASS`, `FAIL`, `NULL`, `BLOCKED`, or `NOT RUN` backed by file paths;
16. limitations, reproducibility commands, and the next 90-day research path.

The report must distinguish calculated results from expectations and literature values. Never invent measurements, job IDs, uncertainties, compiler counts, or GPU timings.

## 15. Reproducibility and quality gates

Before publication:

1. Run the full CPU test suite from the selected Mamba/current environment.
2. Run formatting/lint checks configured by the repository.
3. Run the complete CPU pipeline from a clean generated-output directory inside `ROOT`.
4. Confirm that the report can be regenerated from commands in `README.md`.
5. Confirm every report link and embedded figure exists.
6. Confirm CSV row counts, JSON validity, state normalization, and finite numeric values.
7. Record package versions, random seeds, commands, and failures.
8. Run a secret scan over tracked files. Do not track `.env`, IBM tokens, GitHub tokens, Mamba environments, caches, raw credentials, or provider configuration.
9. Keep raw data immutable after first successful write. Derived files may be regenerated.
10. If a nonoptional physics gate remains broken, report the failure prominently; do not relabel the run successful.

Preregistered research gates:

- exact/noiseless observable mismatch `< 1e-10`;
- median native two-qubit reduction at least `15%` and two-qubit-depth reduction at least `10%` for a resource success;
- hardware paired TVD delta selected-minus-Qiskit negative for raw and M3-projected treatments when hardware exists;
- selector regret below every fixed baseline for an AI-success claim.

## 16. Git and public GitHub publication - explicitly authorized

The user explicitly authorizes one new public research repository under the GitHub account `digonto10602` and authorizes pushing the files produced by this project. This authorization does not include publishing secrets or modifying any other repository.

Use the preferred repository name:

`genesis-su2-zx-observables`

Near the beginning, verify read-only GitHub state:

```bash
gh auth status
gh api user --jq .login
```

The login must equal `digonto10602`. Never create or push to a different owner. Do not create the remote until the local work and secret scan are ready.

If the preferred name already exists, do not overwrite, delete, force-push, or reuse it. Select a new deterministic public name such as `genesis-su2-zx-observables-YYYYMMDD`, adding `-2`, `-3`, and so on until unused. Record the selected name in the report.

Initialize only the current `ROOT` as a Git repository with branch `main`. Make meaningful local checkpoint commits after physics validation, observable generation, compiler/AI work, and final reporting. Never rewrite or reset user history.

Before the final push:

- ensure generated scientific CSV/JSON and figures are tracked;
- exclude `.mamba/`, `.work/`, caches, local credentials, and oversized transient data;
- include `README.md`, `RESEARCH_RESULTS.md`, source, tests, config, environment specification, license, and citations;
- inspect `git diff --check`, tests, and `git status`;
- scan tracked content for secrets;
- make the final commit.

Then create and push:

```bash
gh repo create "digonto10602/$REPO_NAME" \
  --public \
  --source=. \
  --remote=origin \
  --push
```

Do not declare completion until all of these pass:

```bash
git status --short
git rev-parse HEAD
git ls-remote origin refs/heads/main
gh repo view "digonto10602/$REPO_NAME" \
  --json url,visibility,defaultBranchRef
```

Require:

- clean local status;
- remote `main` SHA equals local `HEAD`;
- repository visibility is `PUBLIC`;
- the returned owner/repository is the newly selected repository.

If GitHub authentication is missing or belongs to another account, complete and commit all local research work, create `PUBLISH_BLOCKER.md` with the exact safe commands the user must run, and stop without pushing to the wrong account. This is the only allowed publication blocker.

## 17. Work style and stopping condition

Execute the month-long roadmap as ordered computational phases in this run; do not sleep for calendar days. Give concise progress updates during long work. Resolve ordinary package, API, plotting, test, and compiler failures independently. Consult current official documentation when APIs have changed.

Before stopping, provide:

- the public GitHub URL;
- local and remote commit SHA;
- test summary;
- paths to `RESEARCH_RESULTS.md`, data, and figures;
- QPU/GPU/TN status;
- a one-paragraph conclusion stating whether the compiler-resource, hardware-physics, and AI-selector hypotheses passed, failed, were null, or were not run.

The run is complete only when the research artifacts and explanatory Markdown report exist, mandatory CPU gates have been evaluated honestly, and the new public repository has been verified—or when the sole GitHub-authentication blocker has been documented without risking the wrong account.

## Source: /home/digimonk/Projects/SU2ZX_Foundation_Code_Package/SU2ZX/AGENTS.md

# SU2ZX Agent Rules

## Scope lock

- Treat the canonical current directory as the repository root.
- Its basename must be `SU2ZX` when the package is used for research execution.
- Never read, write, search, delete, or run Git operations outside that root.
- Use `.work/` for temporary files, `.mamba/` for the single reusable Mamba prefix, and `artifacts/` for generated research outputs.
- Do not use `cd ..`, `~`, `$HOME`, `/tmp`, or another repository as a command target.
- Preserve pre-existing user files and uncommitted changes.

## Ponytail discipline

Before adding code, prefer in order: no new code, standard library, an existing project function, an installed dependency's native API, then the smallest readable implementation. Avoid wrappers, factories, duplicate backends, speculative abstractions, dashboards, and redundant notebooks. Never remove validation, security, physics tests, or reproducibility controls for brevity.

## Physics gates

- `src/su2zx/core.py` is the single Hamiltonian and convention source of truth.
- Qiskit strings and displayed bitstrings use `q_(N-1)...q_0`.
- The spatial plaquette chain is a truncated 2+1D Hamiltonian system, not pure-gauge 1+1D.
- Never claim continuum SU(2), physical SU(3) QCD, string tension, string breaking, hadronization, or quantum advantage from this model.
- Never accept a compressed circuit without equivalence validation.
- Never present simulator output as QPU data.

## External actions

- The user authorizes creation of one new public repository under `digonto10602` and pushing this project after tests and a secret scan.
- Never publish credentials, tokens, `.env`, provider configuration, `.mamba/`, or caches.
- IBM QPU submission requires `ALLOW_IBM_QPU_SUBMISSION=1`, `--submit`, and the exact fresh dry-run token. GitHub authorization does not authorize QPU usage.

## Completion

Generate `RESEARCH_RESULTS.md`, CSV/JSON data, plots, test results, and an honest status table. Publish only after local validation. If GitHub authentication is unavailable or is not `digonto10602`, write `PUBLISH_BLOCKER.md` and do not push to another account.

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Graphify is installed in the repository-local Mamba prefix. Invoke it as `.mamba/bin/graphify`.

When the user types `/graphify`, use the installed graphify skill or instructions before doing anything else.

Rules:
- For codebase questions, first run `.mamba/bin/graphify query "<question>"` when graphify-out/graph.json exists. Use `.mamba/bin/graphify path "<A>" "<B>"` for relationships and `.mamba/bin/graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- Dirty graphify-out/ files are expected after hooks or incremental updates; dirty graph files are not a reason to skip graphify. Only skip graphify if the task is about stale or incorrect graph output, or the user explicitly says not to use it.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `.mamba/bin/graphify update .` to keep the graph current (AST-only, no API cost).

## Source: /home/digimonk/Projects/SU2ZX_Foundation_Code_Package/SU2ZX/README.md

# SU2ZX v0.4.0

Reproducible research on exact compiler selection and real-time evolution of a gauge-reduced, j_max=1/2 SU(2) plaquette chain in a truncated 2+1D Hamiltonian geometry. `src/su2zx/core.py` defines the Hamiltonian and q_(N-1)...q_0 convention.

v0.4.0 demonstrates direct-observable CPU MPS scaling through N=32. Basic/Teleport winners survive the sampled fixed-target seeds; ML is NULL on prospective generalization, and symmetry-aware ordering has MIXED physics effects. See [RESEARCH_RESULTS.md](RESEARCH_RESULTS.md) and [VALIDATION.md](VALIDATION.md).

No continuum physics, physical SU(3) QCD, string tension, string breaking, hadronization or quantum advantage is established. Synthetic compilation and simulator outputs are never labeled QPU data.

The [completion audit](docs/V040_COMPLETION_AUDIT.md) maps the v0.4.0 prompt to evidence.
The [code logic and test report](docs/CODE_LOGIC_AND_TESTS.md) explains the complete
workflow, benchmarks, test coverage and limitations; the
[function inventory](docs/CODE_FUNCTION_INVENTORY.md) lists actual callables and assertions.

## Setup and reproduction

Run from the SU2ZX repository root. All working files remain inside it.

```bash
bash scripts/bootstrap_env.sh
bash scripts/run_v040.sh
```

Use the existing single `.mamba/` installation; the interpreter is `.mamba/envs/su2zx/bin/python`. `scripts/run_all.sh` retains the historical v0.3.0 reproduction pipeline and overwrites legacy reports; use run_v040.sh for the current milestone.

## Individual stages

```bash
export TMPDIR="$PWD/.work/tmp" MPLCONFIGDIR="$PWD/.work/matplotlib"
export XDG_CACHE_HOME="$PWD/.work/cache" OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=2
.mamba/envs/su2zx/bin/python -m pytest
# Historical physics / six-strategy benchmark (use separate output for preservation):
.mamba/envs/su2zx/bin/python -m su2zx.study --config config/research.json --output .work/baseline
.mamba/envs/su2zx/bin/python -m su2zx.compiler_study --config config/research.json --output .work/baseline
# Fixed-target robustness, paired data, grouped ML and frozen-rule prospective test:
.mamba/envs/su2zx/bin/python -m su2zx.robust_study
# Re-analyze saved data without recompilation:
.mamba/envs/su2zx/bin/python -m su2zx.robust_study --stage analyze
# Symmetry physics/compiler grid, full/asymptotic fits and Pareto table:
.mamba/envs/su2zx/bin/python -m su2zx.scaling_study physics
# Direct-observable MPS validation then bounded no-statevector scaling:
.mamba/envs/su2zx/bin/python -m su2zx.scaling_study tn
.mamba/envs/su2zx/bin/python tools/validate_v040.py controls
.mamba/envs/su2zx/bin/python tools/validate_v040.py hardware
.mamba/envs/su2zx/bin/python tools/cudaq_reference.py --target qpp-cpu --plaquettes 5
.mamba/envs/su2zx/bin/python tools/plot_v040.py
.mamba/envs/su2zx/bin/python tools/validate_v040.py audit
.mamba/envs/su2zx/bin/python tools/report_v040.py
```

The frozen design is `config/research_v040.json`, checked against `artifacts/data/v040/frozen_design.json`. Preserve these for reproduction; a new research design needs a new timestamped freeze and a fresh holdout. Five routing seeds reuse calibration seed 7. All primary comparisons exclude any pair with a failed output. Randomized routed equivalence is explicitly distinguished from exact logical unitary validation.

## IBM and optional GPU

```bash
.mamba/envs/su2zx/bin/python -m su2zx.qpu --comparison   --backend BACKEND --physical-path q0,q1,q2,q3,q4
.mamba/envs/su2zx/bin/python -m su2zx.qpu_analysis artifacts/qpu/ibm_su2_run.json
```

The IBM command defaults to a dry run. Live submission requires ALLOW_IBM_QPU_SUBMISSION=1, --submit and the exact fresh --confirm token. Approval is one use, configuration/manifest bound, and expires after 15 minutes. The four-way current/symmetry × Basic/Teleport workflow measures occupations, survival, energy, mirror asymmetry and TVD, with raw/M3 analysis and separate exact/Trotter references. The saved QPY bundle uses a synthetic target; regenerate on the chosen real backend. This release submitted zero QPU jobs.

CUDA-Q CPU works. The detected GTX 1060 Max-Q (compute capability 6.1) blocks GPU execution. Existing CUDA-Q scripts accept supported targets on a future compatible GPU; do not alter drivers or force unsupported targets.

## Outputs, Graphify and archives

Data, figures/source mappings, logs and provenance live under artifacts/. Historical v0.3.0 outputs remain preserved alongside v040/. Sixteen current figures have both PNG and PDF outputs.

```bash
.mamba/bin/graphify query "direct MPS robustness pairwise selector symmetry"
.mamba/bin/graphify update .
# After final reports and Graphify validation:
.mamba/envs/su2zx/bin/python tools/archive_v040.py
```

The archive helper requires a passing Graphify validation record, scans the curated file set for secrets, creates a new UTC timestamped ZIP in zip_results/, tests that exact ZIP, verifies its expected contents and writes SHA256 plus an integrity receipt. It excludes environments, caches, credentials and prior archives. Never overwrite prior archives. Archive details are in RUN_MANIFEST.md and GRAPHIFY_UPDATE.md.

## Repository tracked tree (first 300 entries; truncated if more)
.gitignore
.graphifyignore
AGENTS.md
CITATION.cff
GRAPHIFY_UPDATE.md
LICENSE
README.md
RELEASE_NOTES_v0.3.0.md
RELEASE_NOTES_v0.4.0.md
RESEARCH_RESULTS.md
RUN_MANIFEST.md
VALIDATION.md
artifacts/cudaq_reference_N1.json
artifacts/cudaq_reference_N2.json
artifacts/cudaq_reference_N5.json
artifacts/data/accelerator_status.json
artifacts/data/basis_probabilities.csv
artifacts/data/compiler_dataset.csv
artifacts/data/compiler_seed_sensitivity.csv
artifacts/data/compiler_winners.csv
artifacts/data/measurement_reconstruction.csv
artifacts/data/ml_feature_definitions.json
artifacts/data/ml_group_assignments.csv
artifacts/data/physics_observables.csv
artifacts/data/physics_summary.json
artifacts/data/publication.json
artifacts/data/selector_summary.json
artifacts/data/symmetry_ordering.csv
artifacts/data/tensor_network_cpu.csv
artifacts/data/tensor_network_summary.json
artifacts/data/trotter_convergence.csv
artifacts/data/v040/compiler_control_results.csv
artifacts/data/v040/compiler_design.json
artifacts/data/v040/compiler_layout_topology_sensitivity.csv
artifacts/data/v040/compiler_raw_results.csv
artifacts/data/v040/compiler_seed_robustness.csv
artifacts/data/v040/compiler_strict_winners.csv
artifacts/data/v040/compiler_structural_results.csv
artifacts/data/v040/cudaq_N1.json
artifacts/data/v040/cudaq_N2.json
artifacts/data/v040/cudaq_N5.json
artifacts/data/v040/frozen_design.json
artifacts/data/v040/hardware_ready.json
artifacts/data/v040/hardware_ready.qpy
artifacts/data/v040/pairwise_basic_teleport.csv
artifacts/data/v040/pairwise_feature_importance.csv
artifacts/data/v040/pairwise_features.json
artifacts/data/v040/pairwise_ml_groups.csv
artifacts/data/v040/pairwise_ml_predictions.csv
artifacts/data/v040/pairwise_ml_results.csv
artifacts/data/v040/pairwise_ml_summary.json
artifacts/data/v040/physics_compiler_frontier.csv
artifacts/data/v040/prospective_logistic_coefficients.csv
artifacts/data/v040/prospective_tree_rules.txt
artifacts/data/v040/seed_reproduction.json
artifacts/data/v040/symmetry_compiler_results.csv
artifacts/data/v040/symmetry_compiler_summary.json
artifacts/data/v040/symmetry_summary.json
artifacts/data/v040/symmetry_trotter_results.csv
artifacts/data/v040/tn_all_runs.csv
artifacts/data/v040/tn_observable_validation.csv
artifacts/data/v040/tn_observables.csv
artifacts/data/v040/tn_scaling.csv
artifacts/data/v040/tn_summary.json
artifacts/data/v040/trotter_fits.csv
artifacts/environment-pip-freeze.txt
artifacts/environment.md
artifacts/figures/compiler_native_resources.pdf
artifacts/figures/compiler_native_resources.png
artifacts/figures/compiler_routing_penalty.pdf
artifacts/figures/compiler_routing_penalty.png
artifacts/figures/energy_components.pdf
artifacts/figures/energy_components.png
artifacts/figures/loop_occupations_exact_vs_trotter.pdf
artifacts/figures/loop_occupations_exact_vs_trotter.png
artifacts/figures/mirror_asymmetry.pdf
artifacts/figures/mirror_asymmetry.png
artifacts/figures/selector_accuracy_regret.pdf
artifacts/figures/selector_accuracy_regret.png
artifacts/figures/strategy_winner_by_topology.pdf
artifacts/figures/strategy_winner_by_topology.png
artifacts/figures/strategy_winner_distribution.pdf
artifacts/figures/strategy_winner_distribution.png
artifacts/figures/survival_probability.pdf
artifacts/figures/survival_probability.png
artifacts/figures/symmetry_aware_ordering.pdf
artifacts/figures/symmetry_aware_ordering.png
artifacts/figures/tensor_network_convergence.pdf
artifacts/figures/tensor_network_convergence.png
artifacts/figures/trotter_tvd_convergence.pdf
artifacts/figures/trotter_tvd_convergence.png
artifacts/figures/v040/delta_distribution.pdf
artifacts/figures/v040/delta_distribution.png
artifacts/figures/v040/figure_sources.json
artifacts/figures/v040/physics_compiler_frontier.pdf
artifacts/figures/v040/physics_compiler_frontier.png
artifacts/figures/v040/selector_confusion.pdf
artifacts/figures/v040/selector_confusion.png
artifacts/figures/v040/selector_regret.pdf
artifacts/figures/v040/selector_regret.png
artifacts/figures/v040/symmetry_energy_drift.pdf
artifacts/figures/v040/symmetry_energy_drift.png
artifacts/figures/v040/symmetry_mirror_asymmetry.pdf
artifacts/figures/v040/symmetry_mirror_asymmetry.png
artifacts/figures/v040/symmetry_native_depth.pdf
artifacts/figures/v040/symmetry_native_depth.png
artifacts/figures/v040/symmetry_source_depth.pdf
artifacts/figures/v040/symmetry_source_depth.png
artifacts/figures/v040/symmetry_tvd.pdf
artifacts/figures/v040/symmetry_tvd.png
artifacts/figures/v040/tn_mps_tensor_bytes.pdf
artifacts/figures/v040/tn_mps_tensor_bytes.png
artifacts/figures/v040/tn_observable_error.pdf
artifacts/figures/v040/tn_observable_error.png
artifacts/figures/v040/tn_observed_max_bond.pdf
artifacts/figures/v040/tn_observed_max_bond.png
artifacts/figures/v040/tn_runtime_seconds.pdf
artifacts/figures/v040/tn_runtime_seconds.png
artifacts/figures/v040/trotter_convergence.pdf
artifacts/figures/v040/trotter_convergence.png
artifacts/figures/v040/winner_fraction_seed.pdf
artifacts/figures/v040/winner_fraction_seed.png
artifacts/figures/v040/winner_robustness.pdf
artifacts/figures/v040/winner_robustness.png
artifacts/logs/archive_integrity.log
artifacts/logs/archive_integrity_final.log
artifacts/logs/compiler.log
artifacts/logs/compiler_v0.3.0.log
artifacts/logs/cudaq.log
artifacts/logs/data_integrity.log
artifacts/logs/mypy.log
artifacts/logs/pytest.log
artifacts/logs/report.log
artifacts/logs/ruff.log
artifacts/logs/secret_scan.log
artifacts/logs/secret_scan_final.log
artifacts/logs/study.log
artifacts/logs/v040/archive_integrity.json
artifacts/logs/v040/baseline_mypy.log
artifacts/logs/v040/baseline_physics.log
artifacts/logs/v040/baseline_pytest.log
artifacts/logs/v040/baseline_ruff.log
artifacts/logs/v040/completion/controls.log
artifacts/logs/v040/completion/data_integrity.log
artifacts/logs/v040/completion/format.log
artifacts/logs/v040/completion/graph_refresh.log
artifacts/logs/v040/completion/graph_update.log
artifacts/logs/v040/completion/mypy.log
artifacts/logs/v040/completion/pairwise_ml.log
artifacts/logs/v040/completion/plots.log
artifacts/logs/v040/completion/pytest.log
artifacts/logs/v040/completion/pytest.xml
artifacts/logs/v040/completion/ruff.log
artifacts/logs/v040/completion/tn.log
artifacts/logs/v040/controls.log
artifacts/logs/v040/cudaq.log
artifacts/logs/v040/data_integrity.log
artifacts/logs/v040/format.log
artifacts/logs/v040/format_applied.log
artifacts/logs/v040/graph_diagnostic.json
artifacts/logs/v040/graph_merge.log
artifacts/logs/v040/graph_query.log
artifacts/logs/v040/graph_update.log
artifacts/logs/v040/graph_validation.json
artifacts/logs/v040/hardware.log
artifacts/logs/v040/mypy.log
artifacts/logs/v040/new_guards.log
artifacts/logs/v040/pairwise_ml.log
artifacts/logs/v040/plots.log
artifacts/logs/v040/pytest.log
artifacts/logs/v040/report.log
artifacts/logs/v040/robust_study.log
artifacts/logs/v040/ruff.log
artifacts/logs/v040/secret_scan.json
artifacts/logs/v040/symmetry.log
artifacts/logs/v040/tn.log
artifacts/provenance/completion_v040.json
artifacts/provenance/graph_semantic_v040.json
artifacts/provenance/publication_v040.json
artifacts/provenance/run_v0.3.0.json
artifacts/provenance/run_v0.4.0.json
config/research.json
config/research_v040.json
docs/CODE_FUNCTION_INVENTORY.md
docs/CODE_LOGIC_AND_TESTS.md
docs/REFERENCES.md
docs/V040_COMPLETION_AUDIT.md
prompts/CODEX_AUTONOMOUS_SU2ZX_RESEARCH_PROMPT.md
prompts/CODEX_AUTONOMOUS_SU2ZX_RESEARCH_PROMPT_Laptop.md
prompts/SU2ZX_CODEX_AUTONOMOUS_RESEARCH_PROMPT_v0.3.0.md
prompts/SU2ZX_CODEX_AUTONOMOUS_RESEARCH_PROMPT_v0.4.0.md
prompts/v0.5.0.md
pyproject.toml
runs/section8_v0.5.0_20260907T0628Z/OUTPUT_CONTRACT.json
runs/section8_v0.5.0_20260907T0628Z/analysis/figures/exact_casimir.png
runs/section8_v0.5.0_20260907T0628Z/analysis/figures/exact_channels.png
runs/section8_v0.5.0_20260907T0628Z/analysis/figures/exact_density.png
runs/section8_v0.5.0_20260907T0628Z/analysis/tables/exact_mass_scan.csv
runs/section8_v0.5.0_20260907T0628Z/analysis/tables/exact_timeseries.csv
runs/section8_v0.5.0_20260907T0628Z/bin_clock.sh
runs/section8_v0.5.0_20260907T0628Z/circuits/l12_r0.qasm
runs/section8_v0.5.0_20260907T0628Z/circuits/l12_r1.qasm
runs/section8_v0.5.0_20260907T0628Z/circuits/l12_r2.qasm
runs/section8_v0.5.0_20260907T0628Z/circuits/l12_r3.qasm
runs/section8_v0.5.0_20260907T0628Z/circuits/resources_logical.md
runs/section8_v0.5.0_20260907T0628Z/circuits/trotter_scaling.json
runs/section8_v0.5.0_20260907T0628Z/env/requirements.lock.txt
runs/section8_v0.5.0_20260907T0628Z/gates/GATE_G0.json
runs/section8_v0.5.0_20260907T0628Z/gates/GATE_G1.json
runs/section8_v0.5.0_20260907T0628Z/gates/GATE_G2.json
runs/section8_v0.5.0_20260907T0628Z/gates/GATE_G3.json
runs/section8_v0.5.0_20260907T0628Z/gates/attempts/G1_attempt1.md
runs/section8_v0.5.0_20260907T0628Z/gates/attempts/G1_attempt2.md
runs/section8_v0.5.0_20260907T0628Z/gates/gate_G0.py
runs/section8_v0.5.0_20260907T0628Z/gates/gate_G1.py
runs/section8_v0.5.0_20260907T0628Z/gates/gate_G2.py
runs/section8_v0.5.0_20260907T0628Z/gates/gate_G3.py
runs/section8_v0.5.0_20260907T0628Z/logs/agents/l12_builder.out.md
runs/section8_v0.5.0_20260907T0628Z/logs/agents/l12_builder.prompt.md
runs/section8_v0.5.0_20260907T0628Z/logs/agents/route1_fix_escalation.out.md
runs/section8_v0.5.0_20260907T0628Z/logs/agents/route1_fix_escalation.prompt.md
runs/section8_v0.5.0_20260907T0628Z/logs/agents/route2_attempt2.out.md
runs/section8_v0.5.0_20260907T0628Z/logs/agents/route2_attempt2.prompt.md
runs/section8_v0.5.0_20260907T0628Z/logs/cmd/run_g2.log
runs/section8_v0.5.0_20260907T0628Z/logs/cmd/test_l12.log
runs/section8_v0.5.0_20260907T0628Z/physics/DISCREPANCIES.md
runs/section8_v0.5.0_20260907T0628Z/physics/conventions_reconciliation.md
runs/section8_v0.5.0_20260907T0628Z/physics/predictions_G1.json
runs/section8_v0.5.0_20260907T0628Z/physics/predictions_G1.md
runs/section8_v0.5.0_20260907T0628Z/physics/predictions_G2.md
runs/section8_v0.5.0_20260907T0628Z/physics/resonance.json
runs/section8_v0.5.0_20260907T0628Z/physics/signoff_G1.json
runs/section8_v0.5.0_20260907T0628Z/physics/signoff_G1.md
runs/section8_v0.5.0_20260907T0628Z/physics/signoff_G2.json
runs/section8_v0.5.0_20260907T0628Z/physics/signoff_G2.md
runs/section8_v0.5.0_20260907T0628Z/physics/truncation_error.json
runs/section8_v0.5.0_20260907T0628Z/physics/truncation_error.md
runs/section8_v0.5.0_20260907T0628Z/physics/window.json
runs/section8_v0.5.0_20260907T0628Z/reports/REPORT.md
runs/section8_v0.5.0_20260907T0628Z/reports/SUMMARY.md
runs/section8_v0.5.0_20260907T0628Z/reviews/p1_route_spinnet_1.md
runs/section8_v0.5.0_20260907T0628Z/run/CONFIG_ENV.md
runs/section8_v0.5.0_20260907T0628Z/run/DECISIONS.md
runs/section8_v0.5.0_20260907T0628Z/run/GATES.md
runs/section8_v0.5.0_20260907T0628Z/run/HEARTBEAT.md
runs/section8_v0.5.0_20260907T0628Z/run/INVENTORY.md
runs/section8_v0.5.0_20260907T0628Z/run/MODELS.md
runs/section8_v0.5.0_20260907T0628Z/run/PLAN.md
runs/section8_v0.5.0_20260907T0628Z/run/PROMPT_HASH
runs/section8_v0.5.0_20260907T0628Z/run/T0
runs/section8_v0.5.0_20260907T0628Z/run/TASKBOARD.md
runs/section8_v0.5.0_20260907T0628Z/src/su2qc/__init__.py
runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/__init__.py
runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/export_l12.py
runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/strang_l12.py
runs/section8_v0.5.0_20260907T0628Z/src/su2qc/conventions.py
runs/section8_v0.5.0_20260907T0628Z/src/su2qc/dynamics/__init__.py
runs/section8_v0.5.0_20260907T0628Z/src/su2qc/dynamics/engine.py
runs/section8_v0.5.0_20260907T0628Z/src/su2qc/dynamics/run_g2.py
runs/section8_v0.5.0_20260907T0628Z/src/su2qc/dynamics/scan.py
runs/section8_v0.5.0_20260907T0628Z/src/su2qc/encodings/__init__.py
runs/section8_v0.5.0_20260907T0628Z/src/su2qc/encodings/l12.py
runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/__init__.py
runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/compare.py
runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/limits.py
runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_gausskernel.py
runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_spinnet.py
runs/section8_v0.5.0_20260907T0628Z/tests/conftest.py
runs/section8_v0.5.0_20260907T0628Z/tests/pytest.ini
runs/section8_v0.5.0_20260907T0628Z/tests/test_dynamics.py
runs/section8_v0.5.0_20260907T0628Z/tests/test_l12.py
runs/section8_v0.5.0_20260907T0628Z/tests/test_route_gausskernel.py
runs/section8_v0.5.0_20260907T0628Z/tests/test_route_spinnet.py
scripts/bootstrap_env.sh
scripts/run_all.sh
scripts/run_v040.sh
solutions/0.5.0.md
src/su2zx/__init__.py
src/su2zx/compiler_study.py
src/su2zx/core.py
src/su2zx/paths.py
src/su2zx/qpu.py
src/su2zx/qpu_analysis.py
src/su2zx/report.py
src/su2zx/robust_study.py
src/su2zx/scaling_study.py
src/su2zx/study.py
src/su2zx/tn_study.py
tests/test_compiler.py
tests/test_core.py
tests/test_qpu.py
tests/test_study.py
tests/test_tn.py
tests/test_v040.py
tools/archive_v040.py
tools/cudaq_reference.py
tools/cutensornet_reference.py
tools/function_inventory.py
tools/plot_v040.py
tools/provenance.py
Total tracked entries: 304
