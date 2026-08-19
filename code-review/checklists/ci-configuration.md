# CI, Workflow, and Declarative Configuration Checklist

Use for GitHub Actions and equivalent CI, YAML/TOML/JSON configuration, policy
files, matrices, and scripts embedded in configuration. Confirm repository/admin
settings through read-only APIs when they affect enforcement; do not infer them.

## Parsing and effective configuration

- [ ] Validate syntax and the platform schema; YAML booleans, numbers, anchors,
      duplicate keys, quoting, expression interpolation, and indentation preserve
      the intended types and structure.
- [ ] Inspect the effective merged/inherited configuration, reusable workflows,
      composite actions, defaults, environment protection, repository rules, and
      organization policy—not only the edited fragment.
- [ ] Embedded shell/PowerShell/Python is reviewed under its language semantics,
      including two-stage interpolation by YAML, expressions, and the interpreter.
- [ ] Defaults and missing/unknown values fail safely; configuration precedence and
      environment-specific overrides cannot silently select another behavior.

## Events, identity, and invalidation

- [ ] Every state change that must recompute policy has a trigger: synchronize,
      reopen, base advance, review submit/edit/dismiss, label, merge queue, schedule,
      manual rerun, or external event as applicable.
- [ ] `paths`/`paths-ignore`, branches, activity types, conditions, and skip behavior
      cannot leave a required check absent or a previous green result stale.
- [ ] The workflow identifies immutable head SHA, base SHA, merge result, workflow
      source, and artifact provenance correctly for each event type.
- [ ] Base advancement, force-push, rerun, cancellation, and merge queue cannot
      merge a tree that was never evaluated by the decisive policy/checker.
- [ ] Status/check names remain stable and unique; skipped jobs and matrix summaries
      cannot satisfy required checks without evaluating required configurations.

## Trust, permissions, and untrusted code

- [ ] Event choice (`pull_request`, target-context variants, workflow chaining, etc.)
      matches the threat model for forks and same-repository branches.
- [ ] Token, contents, checks, PR, packages, deployments, OIDC, and environment
      permissions are explicit and least-privileged at workflow/job scope.
- [ ] Untrusted code, branch-controlled actions/scripts/config, artifact names,
      cache keys, outputs, or PR metadata cannot reach secrets or write authority.
- [ ] Actions and reusable workflows are pinned to reviewed immutable revisions;
      dependency update and provenance policy covers transitive behavior.
- [ ] Secret values are masked and never passed through unsafe command construction,
      outputs, artifacts, caches, summaries, or attacker-controlled logs.

## Jobs, matrices, artifacts, and gates

- [ ] Matrix dimensions cover supported targets/features/hardware and exclusions are
      deliberate; fail-fast and continue-on-error do not hide a required failure.
- [ ] When a PR adds target/feature-specific source, compare the documented local
      validation command with CI. Either the documented command compiles the new
      body or the documentation clearly identifies the CI-only prerequisite and
      the delayed-feedback risk.
- [ ] `needs`, conditions, output propagation, retries, timeouts, and cancellation
      preserve failure and do not run release/deploy/sign after an upstream failure.
- [ ] Concurrency groups prevent conflicting publication without letting an attacker
      cancel trusted work or retain an obsolete green state.
- [ ] Caches are performance-only unless integrity is verified; keys include every
      input needed to prevent incompatible or attacker-poisoned reuse.
- [ ] Artifacts carry source SHA, configuration, producer, hash/attestation, and
      retention; consumers reject missing, mixed, stale, or ambiguous artifacts.
- [ ] Required status checks, strict/up-to-date policy, approvals, stale-review
      dismissal, and merge-queue behavior collectively enforce the stated gate.
      File changes alone cannot prove repository-admin configuration.
- [ ] A branch-controlled policy checker cannot silently disappear with its own
      invocation and tests. Prefer a trusted-base checker or an independently
      enforced digest/manifest, and make an unexpected test-count drop visible.

## Configuration lifecycle

- [ ] New flags/settings have a schema, exact allowed values, safe default, owner,
      documentation, both-path tests, rollout/rollback plan, and removal condition.
- [ ] Renames update every producer, consumer, example, cache key, environment,
      workflow input/output, dashboard, and compatibility alias as required.
- [ ] Invalid, conflicting, absent, duplicated, and future unknown values fail with
      actionable diagnostics rather than silently choosing a backend.
- [ ] Environment/tenant/region/hardware overrides cannot weaken security or select
      an unsupported artifact without explicit capability validation.

## Verification

- [ ] Run schema/lint/action validation plus tests that evaluate expressions and
      the effective configuration for every relevant event.
- [ ] Simulate event transitions, not only static files: new commit, base advance,
      review dismissal, path-only change, skipped job, retry, cancellation, and
      merge queue.
- [ ] Inspect live repository rules/settings when enforcement is claimed and record
      exact read-only evidence and date; distinguish code fixes from admin changes.
- [ ] Trace each changed source body to the job that compiles, executes, or proves
      it. A green host test plus a target compile is not behavioral coverage of a
      duplicated target state machine.
- [ ] Test embedded scripts separately and end-to-end with realistic outputs,
      artifacts, permissions, and failure states.
- [ ] Exercise the exact checker CLI that CI invokes, including exit status,
      stdout/stderr, missing and malformed inputs, encoding errors, and diagnostic
      stability. Direct helper calls are not a substitute for the process contract.
- [ ] Pair adversarial semantic mutations with cosmetic controls in comments,
      strings, whitespace, and unrelated code. A source scanner that rejects prose
      or valid unrelated syntax is a gate defect even when it catches the seeded bug.
- [ ] For artifact-equality claims, reproduce both sides in the same recorded
      producer environment. Treat relative byte equality separately from an
      absolute size/digest that may depend on archive tools or metadata.
