# Rust and GPU Code Review Playbook

This playbook is a repeatable, evidence-first process for agent-assisted review of
Rust changes ranging from ordinary libraries to unsafe runtimes, GPU kernels, and
GPU firmware. Real PRs also change C/C++, shell, Python, CI configuration, and
normative Markdown, so the roster includes file-language specialists for those
surfaces. It covers correctness, soundness, hardware behavior, build and release
integration, security, architecture, performance, tests, maintainability, and
documentation.

The default is a hybrid Codex and Claude review. Independent specialists search
for different failure classes, a challenger tries to falsify consequential
findings, and one collaborative adjudicator publishes a single report. Agents are
additional reviewers; tests, branch protection, code owners, and qualified human
approval remain authoritative.

## Start here

1. The author fills in [PR context](templates/PR-CONTEXT.md).
2. The review lead selects a lane and roster using
   [the operating model](operating-model.md).
3. The lead maps every changed file to a semantic role and language using the
   [language-routing rules](language-routing.md); no executable or normative file
   class is silently left without an owner.
4. Each reviewer receives the common [reviewer prompt](prompts/reviewer.md), its
   assigned role from [personas and models](personas-and-models.md), the PR
   context, the exact diff, and the relevant checklists.
5. Reviewers work independently and emit findings using the required schema.
6. The lead runs the [adjudicator prompt](prompts/adjudicator.md) to verify,
   deduplicate, calibrate severity, score the PR, and fill in the
   [review report](templates/REVIEW-REPORT.md).

For a first rollout, use the Standard lane on ten representative historical PRs
before allowing agent comments to post automatically.

## Documents

| Document | Purpose |
| --- | --- |
| [Operating model](operating-model.md) | Risk intake, review lanes, independence, verification, and collation |
| [Language routing](language-routing.md) | Changed-file inventory, specialist triggers, and coverage gates |
| [Personas and models](personas-and-models.md) | Reviewer personalities, collaborative/adversarial stance, and Codex/Claude pairing |
| [Severity and scoring](severity-and-scoring.md) | Major/minor/nit definitions, confidence, category scores, overall score, and merge gates |
| [Rust checklist](checklists/rust.md) | Safe and unsafe Rust, FFI, atomics, `no_std`, build, dependencies, and verification |
| [GPU-kernel checklist](checklists/gpu-kernels.md) | Execution, indexing, memory, synchronization, numerics, launches, and performance |
| [GPU-firmware checklist](checklists/gpu-firmware.md) | MMIO, DMA, interrupts, state transitions, security, recovery, and silicon variation |
| [Architecture and quality checklist](checklists/architecture-quality.md) | Design, compatibility, operations, maintainability, tests, and documentation |
| [C and C++ checklist](checklists/c-cpp.md) | Language UB, lifetime, ABI, preprocessing, build modes, and low-level interfaces |
| [Shell and build checklist](checklists/shell-build.md) | Shell semantics and build/link/package/sign tool contracts |
| [Python tooling checklist](checklists/python.md) | Python scripts, parsers, subprocesses, files, and deterministic tooling |
| [CI and configuration checklist](checklists/ci-configuration.md) | YAML/workflows, triggers, trust, permissions, matrices, and required checks |
| [Documentation checklist](checklists/documentation.md) | Normative Markdown, commands, contracts, examples, links, and safe publication |
| [Reviewer prompt](prompts/reviewer.md) | Common evidence contract and machine-readable finding format |
| [Adjudicator prompt](prompts/adjudicator.md) | Cross-check, conflict resolution, scoring, and final-report procedure |
| [PR context template](templates/PR-CONTEXT.md) | Inputs the agents and human reviewers need |
| [Review report template](templates/REVIEW-REPORT.md) | One consolidated, actionable output |
| [Codex rules example](templates/AGENTS.example.md) | Durable repository rules for Codex review |
| [Claude rules example](templates/REVIEW.example.md) | Managed Claude Code Review behavior and severity rules |
| [Sources](sources.md) | Primary references and time-sensitive tooling notes |
| [Evaluation protocol](evaluation.md) | Recall/precision measurement, seeded defects, escapes, and model-drift checks |

## Non-negotiable principles

- Review the change against an explicit base and immutable commit SHA. Do not
  review an unspecified working tree and call it a PR review.
- Give reviewers repository context and relevant specifications, not only a diff.
- Keep the initial bug-hunting passes independent to reduce anchoring and correlated
  misses. Collaboration happens during challenge and adjudication.
- Require a mechanism, reachable trigger, impact, and location for every bug claim.
  A plausible story without evidence is a question, not a finding.
- Never decide truth by majority vote. Resolve disagreement with code, a focused
  test, an authoritative specification, or a clearly stated unresolved assumption.
- Verify every Major before publication. Prefer a different model provider or a
  deterministic reproducer for the verification pass.
- Report one root cause once. List multiple affected sites under it.
- Do not spend agent attention restating deterministic formatter, compiler, or
  linter output. Attach that output separately and use agents for judgment.
- Score only the PR's readiness and risk. Do not score the author.
- A numerical score never cancels a confirmed Major or a required human approval.
- A clean review is not proof that no bugs exist. Report what languages,
  configurations, tools, hardware, and specifications were not covered.

## Recommended review lanes

| Lane | Use when | Typical roster | Target behavior |
| --- | --- | --- | --- |
| Quick | Docs, comments, tests only, or a tiny low-risk safe-Rust change | Correctness/Falsifier + Maintainer | Two independent passes; no automatic approval |
| Standard | Normal library, service, driver, or kernel changes | Lead + Rust + Falsifier + Architecture + one domain specialist | Broad review with verification of all Major and disputed Minor findings |
| High-risk | `unsafe`, FFI, atomics, MMIO, DMA, firmware update/boot, synchronization, cryptography, privilege, new kernel, or new hardware target | Full applicable roster from [personas](personas-and-models.md) | Two-provider coverage, independent passes, challenger, and human domain owner |

Escalate one lane for large diffs, missing tests, unfamiliar hardware, incident
remediation, or changes whose rollback is difficult. Split a PR before review when
the agents cannot build a coherent change model; extra reviewers do not repair an
unreviewable diff.
