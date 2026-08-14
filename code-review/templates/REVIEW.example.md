# Example `REVIEW.md` for Managed Claude Code Review

This is a template for the managed GitHub Code Review pipeline described in the
current Claude Code documentation. Put a tailored copy at the repository root.
Its instructions are injected directly into review agents, so include essential
rules here rather than relying on imports. The local/background `/code-review`
flow may use different instruction sources; verify current product behavior before
assuming this file applies there.

---

# Review instructions

Review only issues introduced or materially worsened by this PR. Use the exact PR
diff plus relevant full-codebase context. Do not modify code.

## Severity

Use these labels in titles and summaries:

- **Major**: a reachable issue can cause Rust unsoundness, material security or
  isolation failure, silent corruption, incorrect GPU results, device/firmware
  hang or brick, deadlock, unauthorized firmware execution/downgrade,
  unrecoverable state, broad compatibility break, or violation of a hard runtime,
  resource, or watchdog contract. A Major needs a concrete trigger and evidence.
- **Minor**: a real localized defect or material test, diagnostic, architecture,
  maintainability, compatibility, or non-contractual performance gap with bounded
  impact or straightforward recovery.
- **Nit**: optional polish only. Report at most five Nits per review and group
  repeated instances. If the PR has only Nits, lead with “No blocking issues.”

Confidence is separate from severity. Publish a Major only with high confidence
after verification. Put low-confidence hypotheses in the summary as questions,
not inline findings.

## Evidence bar

Every finding must include:

- the smallest changed line that causes the issue;
- the invariant being violated;
- a minimal supported input, state, schedule, hardware, or version that triggers it;
- observable impact and affected configurations;
- direct code plus a test/tool/specification citation or a complete causal argument;
- the smallest validation that would settle any remaining assumption;
- a minimal safe direction and focused regression test.

Try to disprove each candidate before posting it. Check callers, validation,
synchronization edges, configuration, feature/target restrictions, and tests. Do
not decide based on multiple agents agreeing. Deduplicate by root cause.

## Always check

- Safe Rust: ranges/conversions, debug-release differences, errors/panics, partial
  cleanup, cancellation, target/features, and API behavior.
- Unsafe/FFI/assembly: validity, alignment, initialization, provenance/aliasing,
  lifetime/drop/unwind, `Send`/`Sync`, layout/ABI, allocator ownership, and clobbers.
- Concurrency: actors, happens-before, atomic order/scope, volatile versus atomic,
  lock/progress/wakeup, interrupts, wraparound/ABA, host-device visibility.
- GPU kernels: index overflow/bounds, partial tiles, divergent barriers, active
  masks/wave width, memory races/scope, async lifetime, ABI, numerical error, and
  launch/device capability.
- Firmware/hardware: exact register semantics, MMIO/I/O barriers, DMA visibility
  and ownership, ring wrap, interrupt acknowledgement, reset/power/update at every
  intermediate step, version/stepping/errata, authenticity and recovery.
- Architecture/quality: invariant ownership, dependency direction, state model,
  API/ABI/protocol compatibility, failure containment, rollback, observability,
  representative tests, and measured performance/resource claims.

## Repository-specific invariants

- `<contract>` must remain compatible across `<version window>`. Use `<safe change
  path>` and see `<spec path>`.
- `<unsafe boundary>` is sound only while `<invariant>`; all safe constructors and
  error/drop paths must preserve it.
- `<DMA/ring protocol>` transfers ownership only after `<required visibility and
  barrier>` and reuses memory only after `<completion visibility>`.
- `<kernel family>` must support `<shape/layout/dtype matrix>` and match `<oracle>`
  within `<numerical error contract>`.
- `<firmware update path>` must authenticate `<signed region>`, enforce
  `<anti-rollback rule>`, and recover after power loss at every commit step.

## Do not report

- formatting, lint, compiler, spelling, license-header, or other failures already
  enforced by CI;
- vendored/lock/generated output when the generator/source is reviewed and clean
  regeneration is verified;
- purely speculative future abstraction requests without a concrete PR consequence;
- pre-existing issues the PR does not worsen, except as a clearly separated
  rollout dependency;
- performance guesses without measurement or a precise contract/resource argument.

## Summary

Start with `N Major, N Minor, N Nit, N questions`. If there is a Major, name the
highest-impact failure and affected target. State review coverage and missing
hardware/specification/evidence. Do not approve or block the PR automatically;
existing branch protections and required human reviewers remain authoritative.

---

Keep this file focused. Put general project context in `CLAUDE.md` and deterministic
style checks in CI.
