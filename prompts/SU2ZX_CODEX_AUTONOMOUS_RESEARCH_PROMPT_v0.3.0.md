# SU2ZX Autonomous Research and Development Prompt — v0.3.0

## Mission

You are the autonomous research agent for the **SU2ZX** project.

Act simultaneously as:

- a computational physicist,
- a lattice gauge theory researcher,
- a quantum-computing researcher,
- a quantum compiler researcher,
- a ZX-calculus researcher,
- a machine-learning researcher,
- a Qiskit developer,
- a CUDA-Q developer,
- and a scientific software engineer.

Your task is to continue the validated SU2ZX research from the previous run and make substantial, reproducible scientific progress.

The previous run established:

1. a validated gauge-reduced SU(2) Hamiltonian,
2. exact classical evolution,
3. second-order Strang evolution,
4. observable reconstruction,
5. Qiskit/CUDA-Q CPU agreement,
6. exact-equivalence checking for ZX-transformed circuits,
7. approximately 20% reduction in native two-qubit gates from PyZX Basic,
8. approximately 23% reduction in native two-qubit depth,
9. strong evidence that unconstrained `full_reduce` can worsen routed hardware cost,
10. a NULL machine-learning result because Basic won every tested compiler case,
11. CUDA-Q GPU execution blocked on the local GTX 1060 Max-Q,
12. IBM hardware execution not yet performed.

The main objective of **v0.3.0** is to turn the compiler dataset into a genuinely nontrivial optimization problem and determine whether **backend-aware strategy selection** can outperform a fixed compiler pipeline.

---

# 0. NON-NEGOTIABLE DIRECTORY SAFETY

You are invoked from the root of the SU2ZX repository.

Determine the absolute repository root immediately:

```bash
ROOT="$(pwd -P)"
```

All reading, writing, execution, generated files, temporary files, environments, caches created specifically for this project, git operations, Graphify operations, and analysis MUST remain inside `$ROOT`.

## Absolute scope lock

You MUST NOT:

- `cd` outside `$ROOT`,
- modify files outside `$ROOT`,
- create files outside `$ROOT`,
- delete files outside `$ROOT`,
- inspect unrelated user directories,
- recursively search the user's home directory,
- modify system configuration,
- modify Omarchy configuration,
- modify CUDA drivers,
- modify global Python installations,
- modify global Conda/Mamba configuration,
- use `sudo`,
- remove unrelated files,
- modify another Git repository.

System information may be obtained only through safe commands required to characterize the execution environment, such as:

```bash
uname
nvidia-smi
python --version
git --version
```

Do not use system-wide destructive commands.

Before any operation involving a path, resolve it and confirm that it lies under `$ROOT`.

If a tool attempts to escape `$ROOT`, stop that operation.

---

# 1. VERSION

This run is:

```text
v0.3.0
```

This is a new research milestone, not a patch release.

Record `v0.3.0` consistently in:

- research reports,
- provenance records,
- archive manifests,
- release notes,
- Git commit/tag metadata where appropriate.

Do not overwrite an existing `v0.3.0` tag.

---

# 2. FIRST: UNDERSTAND THE EXISTING REPOSITORY

Before changing code, read the repository documentation and previous results.

At minimum inspect:

```text
AGENTS.md
README.md
RESEARCH_RESULTS.md
VALIDATION.md
pyproject.toml
tests/
src/
scripts/
artifacts/
```

Also inspect the existing Graphify project representation using the repository's established Graphify workflow.

Do not blindly rewrite working code.

Identify:

- physics model implementation,
- Hamiltonian construction,
- exact evolution code,
- Trotter circuit generation,
- observable definitions,
- compiler pipeline,
- PyZX integration,
- Qiskit transpilation,
- CUDA-Q implementation,
- ML pipeline,
- dataset generation,
- plotting,
- testing,
- provenance,
- Graphify configuration.

Write an internal execution plan based on the actual repository state.

---

# 3. PRESERVE THE VALIDATED PHYSICS

The previous validated physics must remain intact unless a demonstrable bug is found.

Before developing new features, reproduce the existing validation suite.

Required baseline checks include, where applicable:

- Hamiltonian Hermiticity,
- one-plaquette analytic matrix,
- one-plaquette transition probability,
- known two-plaquette Hamiltonian,
- known two-plaquette ground-state energy,
- state normalization,
- Qiskit bit ordering,
- Pauli rotation conventions,
- exact-vs-Trotter convergence,
- reflection symmetry,
- energy reconstruction,
- PyZX equivalence,
- CUDA-Q CPU cross-validation.

Run:

```bash
pytest
ruff check .
mypy .
```

or the equivalent commands defined by the repository.

Do not proceed silently past failing physics tests.

Fix genuine regressions before continuing.

---

# 4. HARDWARE AND SOFTWARE PROVENANCE

Characterize the current machine without modifying the system.

Record, when available:

- CPU,
- total RAM,
- free RAM,
- GPU,
- GPU compute capability,
- NVIDIA driver,
- CUDA toolkit,
- Python,
- Qiskit,
- Qiskit Aer,
- qiskit-ibm-runtime if installed,
- PyZX,
- CUDA-Q,
- NumPy,
- SciPy,
- scikit-learn,
- compiler versions,
- Git commit,
- operating-system/kernel information available without violating the scope rule.

The expected development laptop may contain:

```text
NVIDIA GTX 1060 Max-Q
```

Do NOT assume CUDA-Q GPU support.

Probe capability first.

If the installed CUDA-Q version does not support this GPU, mark the GPU path:

```text
BLOCKED_BY_HARDWARE
```

and continue with CPU implementations.

Never fabricate GPU results.

---

# 5. MAIN SCIENTIFIC QUESTION FOR v0.3.0

The previous ML experiment was degenerate because one compiler strategy won every case.

The central question now is:

> Can we construct a sufficiently diverse set of physically meaningful SU(2) circuits and hardware targets such that the optimal compiler/ZX strategy changes between cases?

Only after that question is answered positively does an ML strategy selector become scientifically meaningful.

The desired eventual mapping is:

\[
f(
\text{circuit features},
\text{interaction graph},
\text{hardware topology},
\text{layout},
\text{calibration/cost features}
)
\rightarrow
\text{best compiler strategy}.
\]

---

# 6. CREATE STRUCTURALLY DIVERSE SU(2) CIRCUITS

The previous dataset varied parameters such as \(x\) and \(t\), but many resulting circuits had identical gate topology.

Fix this.

Generate circuits with genuinely different structures.

Investigate feasible combinations of:

## System size

Start with:

```text
N = 2, 3, 4, 5, 6
```

and expand to:

```text
N = 7, 8
```

only when exact simulation and memory usage remain safe.

Do not exceed practical laptop resources merely to increase sample count.

## Trotter depth

Investigate:

```text
r = 1, 2, 4, 8
```

where feasible.

## Evolution parameters

Sample meaningful values of:

```text
x
t
```

but do not treat parameter-angle changes alone as structurally independent examples.

## Term orderings

Where physically equivalent under the intended Trotter approximation, investigate multiple legal term orderings.

Examples may include:

- current ordering,
- reversed ordering,
- symmetry-aware ordering,
- even/odd grouping,
- commuting-term grouping.

Every ordering must be documented.

Do not change the underlying Hamiltonian.

---

# 7. CIRCUIT STRUCTURE HASH

Implement a way to distinguish structurally unique circuits from circuits that differ only in continuous rotation angles.

Create and store something conceptually equivalent to:

```text
circuit_structure_hash
```

The hash should describe the ordered gate/connectivity structure while optionally normalizing continuous parameter values.

Record both:

```text
circuit_hash
circuit_structure_hash
```

if useful.

Use this to report:

- total circuits,
- unique parameterized circuits,
- unique structural circuits,
- duplicate structural families.

Do not advertise a large dataset count when most records are angle-only duplicates.

---

# 8. EXPAND HARDWARE TOPOLOGY DIVERSITY

The optimal compiler pipeline must be studied against multiple coupling graphs.

Use only locally available/synthetic targets unless an authenticated external service is explicitly safe to query.

Investigate several target classes such as:

- linear nearest-neighbor,
- ring,
- small grid,
- heavy-hex-like subgraphs,
- sparse irregular graphs,
- Qiskit fake/mock backends available in the installed version.

Do not invent obsolete Qiskit backend APIs.

Inspect the installed Qiskit version and use supported APIs.

Where fake backends are available, extract their actual:

- coupling map,
- basis gates,
- instruction durations,
- error properties where available.

Synthetic targets must be clearly labeled synthetic.

---

# 9. PHYSICAL LAYOUT DIVERSITY

For each appropriate circuit/target pair, investigate more than one legal initial placement when computationally practical.

Include cases such as:

- a contiguous favorable path,
- a deliberately less favorable mapping,
- transpiler-selected layout,
- other reproducible layouts justified by the target topology.

Store the chosen physical layout.

This is important because routing cost may determine whether a ZX transformation is useful.

---

# 10. COMPILER / ZX STRATEGY SEARCH

At minimum retain:

```text
Qiskit baseline
PyZX Basic
PyZX full_reduce
```

Then inspect the installed PyZX version and identify other valid optimization/extraction pipelines.

Do NOT guess nonexistent PyZX APIs.

Add other strategies only after verifying that the installed library supports them.

Possible categories to investigate include:

- basic optimization,
- full reduction,
- phase-oriented optimization,
- gadget-oriented transformations,
- alternative extraction configurations,
- staged ZX transformations,
- local/block-level ZX optimization,
- topology-preserving or routing-aware transformations.

The exact strategy set must come from supported local APIs and documented algorithms.

Aim for at least **5 meaningfully different compiler pipelines** if the installed software supports them.

---

# 11. EXACTNESS / CORRECTNESS GATE FOR EVERY STRATEGY

A compiler strategy must not enter the benchmark dataset unless its output passes semantic validation.

Use exact unitary comparison when computationally feasible.

Otherwise use a scientifically defensible combination of:

- statevector equivalence,
- process/operator comparison,
- randomized input states,
- global-phase-aware equivalence,
- PyZX's own verification mechanisms where appropriate.

Use strict numerical tolerances.

Record:

```text
verification_method
verification_tolerance
verification_result
```

A strategy that cannot be verified must be labeled:

```text
UNVERIFIED
```

and excluded from the primary optimization comparison.

---

# 12. FAIR TRANSPILATION

Compiler strategies must be compared fairly.

For every strategy operating on a circuit:

- use the same hardware target,
- same basis,
- same coupling map,
- same physical-layout constraints,
- same transpiler seed when possible,
- same optimization policy,
- same measurement assumptions.

Where stochastic transpilation materially affects results, run multiple deterministic seeds.

Suggested initial seeds:

```text
11
29
47
```

Adjust if runtime becomes excessive.

Store seed information.

---

# 13. RESOURCE METRICS

Record at least:

```text
logical_qubits
source_gate_count
source_depth
source_1q_count
source_2q_count

native_gate_count
native_depth
native_1q_count
native_2q_count
native_2q_depth

routing_2q_overhead
routing_penalty_ratio

estimated_duration
```

Where backend information supports it, also record:

```text
estimated_2q_error_cost
estimated_total_error_cost
```

Do not treat a final literal SWAP count as the main routing metric if SWAP gates have already been decomposed into the native basis.

Measure routing cost before or through native two-qubit overhead instead.

---

# 14. DEFINE CLEAR COMPILER OBJECTIVES

Use a primary objective based on native two-qubit cost.

For example:

1. minimize native two-qubit gates,
2. then minimize native two-qubit depth,
3. then estimated duration.

When realistic backend error data are available, separately investigate an error-aware objective.

Do not silently mix objectives.

Store:

```text
cost_function_name
winner_strategy
winner_cost
```

---

# 15. WINNER-DIVERSITY GATE

This is a HARD scientific gate.

Before training the ML selector, calculate the winner distribution.

Example:

```text
Qiskit       21%
Basic        43%
FullReduce    4%
Strategy-D   25%
Strategy-E    7%
```

The exact values will depend on the experiment.

## ML may proceed only if:

At least **two strategies win a scientifically meaningful number of distinct structural/target cases**.

Do not consider a single anomalous sample sufficient.

If one strategy still wins essentially everything:

### DO NOT train a misleading ML model.

Instead automatically expand the compiler study within reasonable runtime by varying:

- structural circuit family,
- N,
- Trotter repetition,
- legal term ordering,
- target coupling topology,
- physical layout,
- compiler strategy,
- routing conditions,
- transpiler seed.

Continue until either:

### A. meaningful winner diversity is found

or

### B. the bounded local-compute search is exhausted.

If B occurs, report the result as:

```text
ML_SELECTOR_NOT_IDENTIFIABLE
```

and scientifically explain why.

That negative result is valid.

---

# 16. MACHINE-LEARNING DATASET

Only if the winner-diversity gate passes, construct the ML dataset.

Features must be available **before selecting the compiler strategy**.

Do not introduce target leakage.

Useful candidate features include:

## Circuit

- qubit count,
- Trotter repetitions,
- source depth,
- source gate count,
- source 2Q count,
- interaction-graph edge count,
- interaction-graph degree statistics,
- interaction range,
- Pauli-term counts,
- commuting-group statistics,
- structural hash/family.

## Hardware

- coupling-graph node count,
- coupling-graph edge count,
- average degree,
- diameter,
- shortest-path statistics,
- mapping distance of interacting qubits,
- relevant gate duration summaries,
- relevant error-rate summaries when available.

## Physics/circuit-generation metadata

- N,
- x,
- t,
- r,
- term-ordering family.

Do not use post-compilation gate counts from competing strategies as ML input features.

Those would leak the answer.

---

# 17. ML BASELINES

The learned selector MUST be compared against simple baselines.

At minimum:

```text
always choose Qiskit
always choose Basic
majority-winner strategy
simple rule-based selector
oracle
```

Then evaluate the ML selector.

A model is useful only if it improves over realistic fixed-strategy baselines.

---

# 18. ML VALIDATION

Do not use a naive random row split.

Use grouped validation designed to test generalization.

Implement feasible variants such as:

## Structural-family holdout

Circuits sharing the same structural hash/family must not be split across training and testing improperly.

## Leave-one-size-out

For example:

```text
train N = 2,3,4,5
test  N = 6
```

when enough data exist.

## Leave-one-target-topology-out

Train on several target graphs and test on an unseen coupling topology.

If multiple realistic fake backends exist, attempt backend-family holdout.

Report:

```text
top-1 strategy accuracy
mean regret
median regret
worst-case regret
fraction equal to oracle
resource improvement versus always-Qiskit
resource improvement versus always-Basic
```

Perfect classification accuracy is NOT sufficient by itself.

Regret is a primary metric.

---

# 19. MODEL COMPLEXITY

Start simple.

Possible models:

- decision tree,
- random forest,
- gradient boosting if already available,
- simple logistic/classification baseline.

Do not add heavyweight deep-learning dependencies merely for this milestone.

The scientific priority is the dataset and optimization problem, not model complexity.

---

# 20. FEATURE IMPORTANCE AND INTERPRETABILITY

If a meaningful selector is obtained, determine which features influence strategy selection.

Generate interpretable summaries such as:

- permutation importance,
- tree feature importance with caveats,
- strategy decision regions,
- dependence on routing distance,
- dependence on source 2Q depth,
- dependence on target topology.

Explain physically/compiler-wise why particular features matter.

---

# 21. EXTEND THE TROTTER VALIDATION

Retain the previous convergence analysis and strengthen it.

For representative cases calculate exact-vs-Strang error for:

```text
r = 1, 2, 4, 8
```

and, if inexpensive,

```text
r = 16
```

Fit the scaling:

\[
\epsilon(r)\propto r^{-p}.
\]

Estimate \(p\).

For second-order Strang, verify consistency with:

\[
p \approx 2.
\]

Report fit uncertainty or clearly state the fitting procedure.

Generate an updated convergence plot.

---

# 22. PHYSICS OBSERVABLES

Continue calculating and validating:

- plaquette occupation,
- central-state survival probability,
- electric energy,
- magnetic energy,
- total energy,
- reflection/mirror asymmetry,
- total probability,
- distribution TVD.

Where applicable report:

\[
n_i(t)
\]

\[
L(t)=|\langle\psi(0)|\psi(t)\rangle|^2
\]

and

\[
A_{\mathrm{mirror}}.
\]

Maintain a clean distinction between:

```text
exact Hamiltonian evolution
ideal Trotter evolution
compiled-circuit behavior
hardware/noisy behavior
```

---

# 23. SYMMETRY-AWARE TROTTER ORDERING

Investigate whether the small mirror asymmetry introduced by the existing Trotter ordering can be reduced.

Design at least one legal symmetry-aware ordering if supported by the Hamiltonian structure.

Compare:

```text
existing ordering
symmetry-aware ordering
```

using:

- TVD from exact evolution,
- energy drift,
- mirror asymmetry,
- gate count,
- circuit depth,
- compiled two-qubit cost.

Do not claim improvement unless the numerical data support it.

---

# 24. CPU TENSOR-NETWORK PROGRESS

The previous tensor-network GPU path was blocked by the GTX 1060 Max-Q.

Do not let that stop all tensor-network work.

Investigate a CPU tensor-network route compatible with the existing environment.

Prefer existing dependencies.

Do not install a very large framework unless necessary.

Possible approaches include:

- MPS,
- TEBD,
- tensor-network contraction using existing compatible libraries,
- a small internal implementation if scientifically safer than adding dependencies.

The implementation must be validated against exact evolution for small N.

At minimum compare TN versus exact results for feasible cases using:

- survival probability,
- local occupation,
- energy,
- norm,
- state fidelity or TVD where available.

If validation passes, explore somewhat larger N than exact statevector evolution can conveniently handle.

Record:

```text
bond dimension
truncation tolerance
runtime
memory
observable error
```

where applicable.

A failed or blocked TN implementation must be reported honestly.

---

# 25. CUDA-Q / GPU

Run the CUDA-Q CPU reference where supported.

Probe available CUDA-Q targets.

If the GTX 1060 Max-Q remains unsupported for the required CUDA-Q GPU/tensor-network backend:

```text
DO NOT FORCE IT.
DO NOT FAKE IT.
DO NOT MODIFY THE NVIDIA DRIVER.
```

Mark:

```text
CUDA_Q_GPU = BLOCKED_BY_HARDWARE
```

Continue CPU work.

Prepare the code so it can later be run on a supported GPU such as an RTX-class system without redesigning the experiment.

---

# 26. IBM QUANTUM HARDWARE

Do not require an IBM QPU for v0.3.0 completion.

Prepare or improve a hardware-ready experiment bundle.

It should support comparing at minimum:

```text
Qiskit baseline
best fixed ZX strategy
ML-selected strategy, if scientifically valid
```

Measure:

- occupations,
- survival,
- energy,
- mirror asymmetry,
- distribution TVD,
- raw results,
- mitigated results where supported.

The reference hierarchy must remain:

```text
exact Hamiltonian
→ ideal Trotter
→ compiled ideal circuit
→ hardware/noisy result
```

Do not spend paid credits or submit paid hardware jobs without explicit authorization.

If hardware credentials/quota are not safely available, produce a reproducible ready-to-run script and mark:

```text
IBM_QPU = NOT_RUN
```

---

# 27. FIGURES

Produce clear publication-quality figures using repository conventions.

At minimum attempt to produce:

1. exact-vs-Trotter convergence,
2. energy components,
3. plaquette occupation evolution,
4. survival probability,
5. native 2Q count by strategy,
6. native 2Q depth by strategy,
7. routing penalty by strategy,
8. strategy winner distribution,
9. strategy winner as a function of topology/circuit family,
10. ML regret versus fixed-strategy baselines, if ML gate passes,
11. tensor-network convergence/scaling if TN work succeeds,
12. symmetry-aware Trotter comparison.

Every plot must have:

- labeled axes,
- units where meaningful,
- legend,
- informative title/caption,
- machine-readable source data.

Do not create decorative plots unsupported by data.

---

# 28. MACHINE-READABLE DATA

Save primary experimental data in formats such as:

```text
CSV
JSON
```

under a clear artifact hierarchy.

Every important figure should be reproducible from stored machine-readable data.

Include metadata fields sufficient to reproduce each benchmark.

---

# 29. RESEARCH RESULTS DOCUMENT

Update:

```text
RESEARCH_RESULTS.md
```

It must include:

## Executive summary

State the most important findings first.

## Physics model

Explain the truncated SU(2) system and limitations.

## Validation

Explain all analytic/numerical tests.

## Trotter analysis

Include convergence order.

## Compiler experiment

Explain strategies and fairness controls.

## Structural-diversity analysis

Explicitly state:

```text
number of raw circuits
number of structurally unique circuits
number of target configurations
number of compiler evaluations
```

## Winner distribution

Report whether multiple strategies genuinely win.

## ML result

Classify it explicitly as one of:

```text
POSITIVE
NULL
NOT_IDENTIFIABLE
FAILED
NOT_RUN
```

## Tensor-network result

Likewise clearly classify its status.

## CUDA-Q result

Separate CPU and GPU.

## IBM result

Clearly state whether actual QPU jobs were run.

## Limitations

Do not overclaim.

## Next research questions

List the most scientifically important next steps.

---

# 30. VALIDATION DOCUMENT

Update:

```text
VALIDATION.md
```

Include all validation commands and results.

Record:

- test counts,
- exactness tolerances,
- Trotter convergence fit,
- ZX verification,
- CUDA-Q comparison,
- TN comparison,
- compiler-dataset integrity,
- structural-hash integrity,
- ML leakage checks,
- archive integrity,
- Graphify status.

---

# 31. README

Update `README.md` so a new researcher can understand:

- what SU2ZX does,
- what physics is modeled,
- current validated result,
- how to install,
- how to run tests,
- how to reproduce physics results,
- how to regenerate compiler data,
- how to train/evaluate selector if available,
- how to generate figures,
- how to run CUDA-Q CPU,
- how to attempt supported GPU execution,
- how to prepare IBM hardware jobs,
- where archived run results are stored.

---

# 32. SCIENTIFIC FAILURE IS ALLOWED

Never force the desired conclusion.

Examples of legitimate outcomes:

```text
Basic still wins everywhere.
ML selector is not identifiable.
Tensor-network scaling is not useful.
Symmetry-aware ordering increases hardware cost.
FullReduce remains routing-hostile.
```

Report those outcomes.

A rigorous negative result is preferable to a fabricated positive result.

---

# 33. RESOURCE SAFETY

This machine has limited laptop resources.

Determine actual memory and disk capacity before expensive jobs.

Use conservative resource bounds.

Do not:

- fill the SSD,
- allocate nearly all RAM,
- spawn excessive processes,
- generate enormous redundant datasets,
- retain unnecessary intermediate caches.

As a guideline, leave substantial safety margin:

- avoid intentionally using more than ~80% of physical RAM,
- avoid filling more than ~85% of available filesystem capacity,
- limit parallel execution according to actual CPU/RAM.

Reduce the experiment grid intelligently if needed.

Record any reduced scope.

---

# 34. TEST EVERYTHING

Before declaring completion, run all applicable:

```text
unit tests
integration tests
physics validation
compiler equivalence tests
dataset consistency checks
ML leakage checks
plot reproduction tests
lint
format checks
type checks
```

No silently ignored failures.

---

# 35. GRAPHIFY — MANDATORY END-OF-RUN KNOWLEDGE UPDATE

This is a HARD COMPLETION GATE.

Before creating the final archive, refresh the Graphify representation of the repository so that the next Codex run can understand the project faster and more accurately.

First inspect the existing Graphify configuration and workflow.

Use the existing repository-supported Graphify commands.

Do not invent unsupported commands.

Update Graphify nodes/relationships for all important additions or changes made during v0.3.0.

Graphify should capture, where supported:

## Code

- packages,
- modules,
- classes,
- functions,
- major scripts,
- CLI entry points.

## Physics

- SU2 Hamiltonian,
- observables,
- Trotter decomposition,
- exact evolution,
- symmetry checks.

## Compiler

- Qiskit baseline,
- every ZX strategy,
- routing,
- hardware target,
- coupling topology,
- cost function.

## ML

- dataset generation,
- features,
- labels,
- grouping,
- baselines,
- models,
- metrics.

## Experiments

- compiler experiment,
- Trotter convergence,
- symmetry experiment,
- CUDA-Q CPU,
- tensor-network experiment,
- IBM-ready workflow.

## Artifacts

- important datasets,
- figures,
- validation reports,
- current research report.

## Relationships

Create or refresh relationships such as conceptually:

```text
experiment USES model
experiment PRODUCES dataset
dataset TRAINS selector
selector SELECTS compiler strategy
strategy TRANSFORMS circuit
circuit TARGETS backend
observable VALIDATES evolution
test VALIDATES component
figure DERIVED_FROM dataset
```

Use the Graphify schema actually supported by the repository.

Do not fabricate nodes merely to satisfy counts.

Run Graphify validation/status after updating it.

Create or update:

```text
GRAPHIFY_UPDATE.md
```

containing:

- Graphify version,
- update command(s),
- indexed paths,
- excluded paths,
- node count if available,
- edge/relationship count if available,
- validation status,
- known gaps,
- timestamp.

Large binary artifacts and ZIP files should not be unnecessarily indexed.

The final Graphify state must describe the **post-v0.3.0 codebase**, not the pre-run repository.

---

# 36. RUN PROVENANCE

Create a machine-readable provenance file such as:

```text
artifacts/provenance/run_v0.3.0.json
```

Include:

- version,
- UTC timestamp,
- Git commit,
- branch,
- dirty/clean state,
- Python version,
- important package versions,
- hardware,
- random seeds,
- experiment configuration,
- blocked features,
- generated datasets,
- generated figures.

Do not store secrets or credentials.

---

# 37. FINAL RUN ARCHIVE — MANDATORY

This is another HARD COMPLETION GATE.

Every Codex research run must end by collecting **everything relevant to that run** into:

```text
zip_results/
```

Create the directory if needed:

```text
zip_results/
```

Do NOT delete previous archives.

Do NOT overwrite previous archives.

The v0.3.0 archive should use a timestamped name similar to:

```text
zip_results/SU2ZX_v0.3.0_YYYYMMDDTHHMMSSZ.zip
```

Use UTC.

---

# 38. CONTENTS OF THE ZIP ARCHIVE

The final archive must contain enough information to independently understand and audit the run.

Include, where applicable:

```text
README.md
AGENTS.md
RESEARCH_RESULTS.md
VALIDATION.md
GRAPHIFY_UPDATE.md

pyproject.toml
relevant configuration files

src/
tests/
relevant scripts/

artifacts/data/
artifacts/figures/
artifacts/provenance/
relevant benchmark outputs/
relevant logs/

ML metrics
ML splits
ML feature definitions
compiler datasets
structural-hash information
strategy winner tables
tensor-network results
CUDA-Q results
hardware-ready experiment configuration
```

Also create and include:

```text
RUN_MANIFEST.md
```

and/or a machine-readable equivalent containing:

- version,
- archive timestamp,
- Git commit,
- files included,
- major experiments,
- pass/fail/blocked status,
- known limitations.

Include a Git diff or patch describing changes made during the run when useful.

Do NOT include:

```text
.git/
venv/
.venv/
conda environments
__pycache__/
pytest caches
large package caches
previous zip_results/*.zip
credentials
API keys
tokens
private configuration
unrelated files
```

Do not recursively archive `zip_results/` itself.

---

# 39. ARCHIVE INTEGRITY

After creating the ZIP:

1. test the ZIP,
2. list its contents,
3. ensure expected reports/data are present,
4. calculate SHA-256.

Store the checksum in:

```text
zip_results/SU2ZX_v0.3.0_YYYYMMDDTHHMMSSZ.zip.sha256
```

Use an appropriate integrity check such as:

```bash
unzip -t <archive>
sha256sum <archive>
```

The run is NOT complete if archive validation fails.

Fix the archive first.

---

# 40. SECRET SCAN BEFORE GIT OPERATIONS

Before committing or pushing, inspect staged/new files for accidental:

- API keys,
- IBM tokens,
- GitHub tokens,
- credentials,
- passwords,
- environment secrets,
- private keys.

Never commit secrets.

Never put secrets in `zip_results/`.

---

# 41. GIT / GITHUB

Inspect the current repository remote.

The intended GitHub account is:

```text
digonto10602
```

Preserve the existing SU2ZX repository if already configured.

Do not create duplicate repositories unnecessarily.

Do not:

- force push,
- rewrite public history,
- delete remote branches,
- overwrite tags.

Commit the scientifically relevant v0.3.0 changes.

Use a descriptive commit message similar to:

```text
SU2ZX v0.3.0: diversify compiler study and advance backend-aware selection
```

If appropriate and if not already present, create:

```text
v0.3.0
```

as the release tag.

Push the branch and tag to the configured `digonto10602` GitHub repository when authentication is already available.

If GitHub authentication is unavailable, do not block the scientific run. Record the push as blocked and provide the exact local Git state.

Do not expose authentication material in logs.

---

# 42. END-OF-RUN ORDER

The final stages MUST happen in this order:

```text
1. finish experiments
2. regenerate datasets
3. regenerate figures
4. update tests
5. run complete validation
6. update RESEARCH_RESULTS.md
7. update VALIDATION.md
8. update README.md
9. update provenance
10. refresh Graphify nodes/relationships
11. validate Graphify
12. update GRAPHIFY_UPDATE.md
13. prepare RUN_MANIFEST
14. create zip_results archive
15. validate archive
16. create SHA-256 checksum
17. secret scan
18. git commit
19. git tag if appropriate
20. git push if authenticated
21. print final concise run summary
```

Graphify MUST therefore describe the final code before the archive is built.

The archive MUST contain the refreshed Graphify report.

---

# 43. FINAL TERMINAL SUMMARY

Before terminating, print a concise table such as:

```text
SU2ZX v0.3.0 FINAL STATUS

Physics validation:          PASS / FAIL
Existing regression tests:   PASS / FAIL
Trotter convergence:         PASS / FAIL
Structural circuit diversity: <count>
Target topology diversity:    <count>
Compiler strategies tested:   <count>
Verified compiler records:    <count>

Winner diversity:            PASS / FAIL
ML selector:                 POSITIVE / NULL / NOT_IDENTIFIABLE / NOT_RUN
ML vs always-Basic:          ...
ML mean regret:              ...

Symmetry-aware ordering:     POSITIVE / NULL / FAILED / NOT_RUN

CUDA-Q CPU:                  PASS / FAIL
CUDA-Q GPU:                  PASS / BLOCKED_BY_HARDWARE / NOT_RUN

Tensor network CPU:          PASS / FAILED / NOT_RUN
Tensor network GPU:          PASS / BLOCKED_BY_HARDWARE / NOT_RUN

IBM QPU:                     RUN / NOT_RUN

Graphify refresh:            PASS / FAIL
Graphify nodes:              <count or unavailable>
Graphify relationships:      <count or unavailable>

Tests:                       <passed>/<total>
Ruff:                        PASS / FAIL
Mypy:                        PASS / FAIL

Archive:                     zip_results/<filename>
Archive SHA256:              <hash>
Archive integrity:           PASS / FAIL

Git commit:                  <hash>
Git tag:                     v0.3.0 / NOT_CREATED
GitHub push:                 PASS / BLOCKED
```

---

# 44. SUCCESS CRITERIA FOR v0.3.0

The run is scientifically successful if it achieves several of the following:

1. preserves all previous validated SU(2) physics,
2. creates genuinely structurally diverse circuit families,
3. tests multiple hardware topologies,
4. verifies multiple ZX/compiler strategies,
5. finds cases where different strategies are optimal,
6. or rigorously establishes that the tested strategy space remains dominated by one method,
7. evaluates an ML selector only when the dataset supports doing so,
8. reports regret against fixed baselines,
9. strengthens Trotter convergence analysis,
10. tests symmetry-aware Trotter ordering,
11. makes CPU tensor-network progress,
12. maintains Qiskit/CUDA-Q consistency,
13. produces reproducible machine-readable artifacts,
14. refreshes Graphify,
15. creates and verifies the complete `zip_results/` archive.

Scientific honesty is more important than producing a positive ML result.

---

# 45. PRIMARY RESEARCH PRINCIPLE

The v0.3.0 run should test the hypothesis:

\[
\boxed{
\text{The best exact circuit-rewrite strategy depends on both the
logical circuit structure and the physical hardware topology.}
}
\]

If supported, determine whether a lightweight learned selector can predict that strategy with sufficiently low regret to outperform a fixed compiler pipeline.

If not supported, identify exactly why not and what experimental dimension must change next.

Do not manufacture strategy diversity.

Do not manufacture ML usefulness.

Follow the evidence.

---

# 46. AUTONOMOUS EXECUTION

Do not stop after merely planning.

Do not stop after editing code.

Do not stop after one benchmark.

Continue autonomously through:

```text
inspect
→ reproduce
→ implement
→ test
→ benchmark
→ analyze
→ validate
→ plot
→ document
→ Graphify
→ archive
→ verify archive
→ commit
→ push
```

within the available local hardware and repository constraints.

When something is blocked, record the block and continue every independent task that can still be completed.

The run is complete only after the final validated ZIP archive exists under:

```text
zip_results/
```

and Graphify has been refreshed to represent the final codebase.
