# Operating Model

## 1. Establish the review target

The review lead records all of the following before dispatching agents:

- repository, immutable head SHA, base SHA, and merge-base SHA;
- intended behavior and explicit non-goals;
- changed public, wire, firmware, kernel-launch, and hardware interfaces;
- required hardware, toolchain, features, targets, and build mode;
- relevant specifications, errata, incident links, performance baselines, and
  repository instructions;
- threat model, privilege boundary, trusted inputs, and attacker-controlled inputs;
- tests already run, their exact commands, results, and known environmental gaps;
- rollout, compatibility, recovery, and rollback expectations.

Use [PR-CONTEXT.md](templates/PR-CONTEXT.md). If an essential item is unknown,
write `UNKNOWN`; do not let an agent silently invent it. Reviewers may continue
with stated assumptions, but the final report remains provisional if the unknown
could change correctness or severity.

## 2. Classify the risk

Mark every applicable trigger. One high-risk trigger selects the High-risk lane.

| Trigger | Specialist required |
| --- | --- |
| Safe Rust logic, parsing, state, error handling | Rust Language Lawyer |
| Any `unsafe`, raw pointer, manual allocation, `unsafe impl`, FFI, inline assembly | Unsafe Boundary Auditor |
| Atomics, locks, channels, async cancellation, interrupt/shared state | Concurrency and Memory-Model Reviewer |
| Kernel/device function, shader, launch geometry, device memory | GPU Kernel Reviewer |
| MMIO, DMA, rings, doorbells, interrupts, boot/reset/power/update | Firmware and Hardware-Contract Reviewer |
| Untrusted input, privilege, signing, secrets, isolation, dependencies | Security and Resilience Reviewer |
| Public API/ABI, wire/on-disk format, crate boundary, ownership change | Architecture and Compatibility Reviewer |
| Hot path, allocation, latency/throughput target, occupancy/resource change | Performance Reviewer |
| C/C++ source, headers, preprocessor, ABI, or native build change | C/C++ Low-level Language Reviewer |
| Shell, CMake/Make, linker, package, signing, or artifact-selection logic | Shell and Build Interface Reviewer |
| Executable Python, parser, generator, validator, or test harness | Python Tooling Reviewer |
| CI workflow, YAML/TOML/JSON configuration, permissions, triggers, or required checks | CI and Declarative Configuration Reviewer |
| Normative Markdown, runbook, procedure, specification, or executable example | Documentation and Contract Reviewer |
| All executable changes | Test Falsifier |
| All changes | Maintainer and Operability Reviewer |

Also escalate for more than roughly 800 changed non-generated lines, broad
cross-crate edits, generated code whose generator changed, weak PR context, or a
change authored during incident pressure. These are heuristics, not proof of risk.

After risk classification, complete the changed-file inventory and coverage rules
in [language routing](language-routing.md). Route by semantics, not extension: a
shell fragment embedded in YAML needs both workflow and shell scrutiny, while a
generated `.py` fixture may need its generator reviewed instead. Every changed
executable language and normative contract needs a specialist or a recorded,
specific reason why another assigned persona fully owns it.

Treat firmware artifact selection, linker/package/signing behavior, release
provenance, privileged workflow changes, and code-executing pull-request workflows
as High-risk even when the diff is only shell, Python, YAML, or build metadata.

## 3. Prepare deterministic evidence first

### Data and access governance

GPU firmware, unreleased hardware details, crash dumps, keys, and customer traces
may be highly restricted. Before sending any content to an agent:

- classify the repository and attached artifacts under team policy;
- use only approved provider, account, region, retention/training, and enterprise
  controls for that classification; do not assume a consumer plan is approved;
- redact credentials, signing keys, tokens, customer data, sensitive addresses, and
  unrelated proprietary specifications;
- give the minimum repository paths and read-only tools needed for the role;
- disable network and external connectors unless the review needs an approved
  authoritative source;
- sandbox untrusted build scripts, proc macros, tests, firmware tools, and PR code
  away from credentials, production systems, and shared lab devices;
- retain prompts, model/version, findings, commands, and approvals according to the
  organization's audit and source-code handling policy.

If policy does not permit either cloud provider for the code, do not paste or
upload it. Run only an approved local/on-premises model and treat the model matrix
as a role/quality specification to re-evaluate, not an authorization workaround.

### Checks

Before asking agents to reason, gather the checks that are cheap and objective:

- compilation for every supported target and meaningful feature combination;
- formatter, linter, unit, integration, documentation, and compatibility results;
- target-specific tests, simulator/emulator results, and hardware matrix results;
- performance and binary/resource deltas where the PR claims no regression;
- generated-code provenance and a clean regeneration diff;
- dependency, license, vulnerability, and policy checks required by the project;
- language-specific syntax/static checks and focused boundary tests selected from
  the applicable C/C++, shell, Python, CI/configuration, and documentation
  checklists;
- real producer/consumer contract tests for changed tool interfaces, including
  exit status, stdout/stderr, paths, environment, partial output, stale artifacts,
  and non-default modes. A path-only stub is not evidence for a real tool that
  emits diagnostics before its result.

Do not blindly run commands from an untrusted PR with host credentials or access
to shared hardware. Inspect build scripts and CI changes, use an appropriate
sandbox, and grant read-only repository access to reviewers by default.

Failed deterministic checks are attached to the report. Agents should investigate
root cause and impact, not repost the raw failure as multiple review comments.

## 4. Dispatch independent passes

Each reviewer gets the same frozen inputs:

1. PR context and exact diff;
2. repository rules and applicable specifications;
3. the common reviewer prompt;
4. exactly one primary persona and its checklists;
5. read-only tools, plus permission to run approved tests where safe.

The lead also records an execution manifest: required persona, language/file
class, provider/model/version/effort, immutable target, status, and coverage limit.
Do not mark a pass complete merely because one model mentioned that language in a
multi-persona prompt.

Do not give first-pass reviewers one another's findings. Do not ask a single agent
to role-play five specialists in one context: later roles anchor on earlier
reasoning, context becomes crowded, and coverage cannot be audited.

For a High-risk lane, a missing required second-provider pass is a material
coverage gap. The adjudicator must issue `Provisional — evidence required` unless
deterministic evidence plus a qualified human specialist explicitly substitutes
for that pass and the report records the substitution. This does not weaken the
requirement to challenge every Major.

The stance is deliberate:

- Bug, safety, security, concurrency, firmware, GPU, and falsification reviewers
  are **adversarial toward assumptions**, never toward the author. Their job is to
  construct a real counterexample.
- Architecture, compatibility, maintainability, and operability reviewers are
  **collaborative**. Their job is to understand constraints, identify durable
  concerns, and offer proportionate alternatives.
- The adjudicator is **collaborative and skeptical**. It protects the author from
  noise and the codebase from missed risk.

## 5. Normalize findings

Every reviewer must use the schema in [reviewer.md](prompts/reviewer.md). Reject or
return a candidate that lacks a specific location, mechanism, reachable trigger,
impact, evidence, or concrete validation step.

Normalize terminology before comparison:

- severity is only `Major`, `Minor`, or `Nit`;
- confidence is `high`, `medium`, or `low` and is separate from severity;
- category uses the scoring categories exactly;
- evidence is tagged `code`, `test`, `tool`, `spec`, or `assumption`;
- status begins as `candidate`.

Low-confidence ideas go into “Questions and follow-ups,” not inline findings,
unless a second reviewer or new evidence confirms them.

## 6. Deduplicate by cause

Two candidates are duplicates when the same code change violates the same
invariant through the same mechanism, even if reviewers describe different
symptoms. Merge them into one finding with all affected locations and preserve
the strongest evidence.

Do not merge findings merely because they touch the same line. A bounds error and
a missing memory fence on the same access are different root causes.

## 7. Challenge consequential claims

Every candidate Major, every disputed Minor, and every claim about unsafe Rust,
memory ordering, security, firmware recovery, or numerical correctness receives a
challenge pass. Prefer a reviewer from the other model provider.

The challenger tries to disprove the candidate by checking:

- whether the trigger is reachable under supported inputs and configurations;
- whether a precondition, type invariant, synchronization edge, or caller check
  already prevents it;
- whether the cited line is introduced by the PR rather than pre-existing;
- whether the claimed behavior holds in the actual build mode and target;
- whether the specification or erratum says what the reviewer claims;
- whether a minimal test, model, disassembly, trace, or calculation confirms it;
- whether the proposed fix would preserve ABI, performance, and hardware behavior.

Challenge outcomes are `confirmed`, `downgraded`, `question`, or `rejected`, with
a short rationale. A model agreeing with itself in a second prompt is not
independent verification.

## 8. Resolve conflicts by evidence

Use this precedence order:

1. reproducible failing test, trace, sanitizer result, model-checker result, or
   hardware observation on the relevant target;
2. authoritative language, ISA, ABI, hardware, protocol, or product specification;
3. repository invariant or compatibility contract with an owner and rationale;
4. direct code path and state/invariant analysis;
5. expert judgment with assumptions stated;
6. model vote, which is never sufficient on its own.

If evidence remains ambiguous, publish a question with the missing validation;
do not manufacture certainty or average severities.

## 9. Adjudicate and score

The adjudicator reads the diff, PR context, raw candidates, challenge results, and
deterministic evidence. It must independently spot-check the source for every
published finding. Then it applies [severity and scoring](severity-and-scoring.md),
fills in one [review report](templates/REVIEW-REPORT.md), and records rejected
Major candidates in the private audit appendix with rationale.

Individual agents may suggest category scores, but only the adjudicator assigns
the official category and overall scores. Score after deduplication and severity
calibration so a duplicated finding cannot multiply the penalty.

## 10. Human decision and follow-up

Required human reviewers decide whether to merge. At minimum, a human domain owner
must review any change involving unsafe soundness, FFI/ABI, weak-memory reasoning,
new GPU kernels, firmware boot/update/recovery, hardware security boundaries, or
a waived Major.

After fixes:

- rerun affected deterministic checks and targeted reproducers;
- re-review changed lines plus their invariants, not the entire PR from scratch;
- suppress new Nits after the first review unless the new patch introduced them;
- close findings as `fixed`, `accepted risk` (owner and expiry required), `not a
  bug` (rationale required), or `deferred` (tracking issue required);
- add confirmed novel failures and false positives to the review eval set.
- add every escaped defect and every new language/tool boundary failure to the
  evaluation corpus, then verify the responsible persona and prompt can find the
  defect without being told its location.

## Cost and noise controls

- Route only applicable specialists; more agents are not automatically better.
- Use frontier models for high-risk semantic work and verification, balanced
  models for routine maintainability passes, and fast models only for mechanical
  triage. See [personas and models](personas-and-models.md).
- Cap published Nits at five per PR and group repeats. Keep additional Nits in a
  collapsed appendix or omit them.
- Publish only actionable, PR-introduced findings. Pre-existing issues belong in a
  separate issue unless the PR materially worsens them or depends on them.
- Track review latency, cost, confirmation rate, false-positive rate, duplicate
  rate, and escaped defects by persona and model. Retire personas that add noise.
