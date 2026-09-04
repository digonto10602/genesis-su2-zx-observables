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

## 4. Environment policy: Omarchy/GTX 1060 Max-Q, local-first testing, and at most one Mamba environment

The target computer is a laptop running **Omarchy OS (Arch Linux based)** with an **NVIDIA GeForce GTX 1060 Max-Q**. Treat the GPU as a Pascal-generation, compute-capability-6.1 device unless runtime probing reports otherwise. Current CUDA-Q and cuQuantum releases may require a newer GPU architecture, so do not assume that their GPU backends will run and do not force an unsupported installation. The mandatory research path is local CPU execution; compatible GPU tests are an additional validation path.

1. Before installing anything, record the exact OS (`/etc/os-release` and Omarchy version when available), kernel, CPU, RAM, Python, `mamba --version`, and GPU details in `artifacts/environment.md`. Probe with `nvidia-smi` and, when supported, record GPU name, compute capability, VRAM, driver, reported CUDA compatibility, and active processes. Also record `nvcc --version` when available. Do not assume Ubuntu package names or use `apt`; Omarchy is Arch based.
2. Run the complete small local CPU/reference test suite first: imports and tiny calculations for Python, NumPy, SciPy, Matplotlib, pandas, scikit-learn, Qiskit, Qiskit Aer, PyZX, and pytest, followed by the analytic `N=1,2` and exact/Trotter `N=5` physics checks. These tests must proceed even if every NVIDIA-specific component is unavailable.
3. Use a capability-aware accelerator ladder:
   - test the NVIDIA driver with `nvidia-smi`;
   - if a compatible CUDA runtime is already available inside the selected environment, run a minimal one-qubit or vector-operation CUDA smoke test and record the actual device used;
   - test CUDA-Q's CPU target locally (for example `qpp-cpu`, if exposed by the installed release) before trying any GPU target;
   - attempt CUDA-Q `nvidia`, `tensornet`, `tensornet-mps`, and direct cuTensorNet only when the installed versions' documented minimum compute capability and the probed GTX 1060 Max-Q capability are compatible;
   - verify actual GPU use rather than accepting an import, target-selection message, or silent CPU fallback as a GPU pass.
4. If the current CUDA-Q/cuQuantum release requires a newer compute capability than the GTX 1060 Max-Q provides, record `BLOCKED - UNSUPPORTED GPU ARCHITECTURE` with the detected capability and documented requirement. Continue with CUDA-Q CPU execution where supported and with SciPy/Qiskit CPU references. Do not install arbitrary old CUDA-Q, CUDA, cuQuantum, or NVIDIA-driver versions merely to make Pascal work; only use an older combination if it is already present, locally compatible, and its exact versions and limitations are recorded.
5. If the current environment passes every required CPU test, reuse it. Do not create another environment.
6. Otherwise create or reuse exactly one fixed Mamba prefix:

   `ROOT/.mamba/envs/su2zx`

   Set `MAMBA_ROOT_PREFIX=ROOT/.mamba`. Never create an environment with a per-run or per-prompt name. If the fixed prefix already exists, update/reuse it rather than creating another.
7. Use Python 3.11 unless an existing verified environment is retained. Upgrade pip to at least 24 before installing CUDA-Q.
8. Install the local project editable and only its declared dependencies. Prefer currently supported packages and inspect official documentation if an API has changed.
9. Current NVIDIA guidance uses the `cudaq` Python package. Check for and avoid conflicting legacy CUDA-Q distributions before installation. Attempt cuQuantum only after CUDA/driver/compute-capability compatibility checks.
10. Do not install system packages with `sudo`, do not run an Omarchy/Arch system upgrade, and do not modify shell startup files, the NVIDIA driver, or system CUDA. Keep project environment metadata and caches inside `ROOT`.
11. If GPU installation or execution fails, preserve the complete error log, continue with exact CPU/Qiskit simulations and locally supported CUDA-Q CPU tests, and mark each unavailable CUDA-Q GPU/cuTensorNet route as `BLOCKED`, not `PASS`.

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

Run this phase **locally on the Omarchy laptop first**. The GTX 1060 Max-Q is optional acceleration, not a prerequisite. Probe its exact compute capability and VRAM, and never substitute results from a different GPU while labeling them local.

1. Cross-check `N=1,2,5` using CUDA-Q's CPU target, when supported, against SciPy/Qiskit before attempting GPU execution.
2. Run a minimal CUDA-Q `nvidia` smoke test on the GTX 1060 Max-Q only if the installed CUDA-Q release officially supports the detected compute capability. If it succeeds, cross-check the same `N=1,2,5` cases and record the target, device name, versions, runtime, and numerical error. If it is unsupported or fails, record the precise blocker and retain the CPU cross-checks as the completed local result.
3. Check exact `tensornet` and approximate `tensornet-mps` targets only when their CUDA-Q/cuQuantum versions support the detected GPU.
4. Test direct cuTensorNet `CircuitToEinsum` only if the installed Qiskit/cuQuantum versions and detected GPU architecture are compatible. If not, document the API/version/hardware blocker; do not imply that `tensornet` remains available unless its own smoke test passed.
5. For MPS, run separate processes for
   \[
   \chi=32,64,128,256
   \]
   on representative `N=5,10,20,40` cases that fit the **probed** VRAM/RAM. Start with the smallest `N` and bond dimension, increase one step at a time, and skip unsafe sizes rather than exhausting laptop memory.
6. Record occupations, energy, survival, mirror symmetry, runtime, peak RAM/VRAM, and final-doubling change.
7. Call MPS converged only when every primary observable changes by less than `1e-3` under the final feasible bond-dimension doubling.
8. Record exact-backend agreement at `1e-8` where applicable.

A GTX 1060 Max-Q, CUDA-Q GPU, or tensor-network blocker must not stop CPU physics, compiler studies, observable generation, plotting, reporting, or GitHub publication. Clearly separate `LOCAL CPU PASS`, `LOCAL GPU PASS`, and `BLOCKED/NOT RUN` statuses.

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
- detected Omarchy, GTX 1060 Max-Q, driver, compute-capability, and VRAM summary, plus which local CPU/GPU paths actually ran;
- a one-paragraph conclusion stating whether the compiler-resource, hardware-physics, and AI-selector hypotheses passed, failed, were null, or were not run.

The run is complete only when the research artifacts and explanatory Markdown report exist, mandatory CPU gates have been evaluated honestly, and the new public repository has been verified—or when the sole GitHub-authentication blocker has been documented without risking the wrong account.
