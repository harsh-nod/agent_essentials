# Example `AGENTS.md` Code Review Rules for Codex

Copy and tailor the section below into the applicable repository `AGENTS.md`.
Keep root rules repository-wide and put hardware- or crate-specific rules in a
nested `AGENTS.md` near the governed code. Replace placeholders with real
invariants, owner/spec paths, and safe alternatives. Delete rules that merely
repeat CI or routinely create noise.

---

## Code Review Rules

Review the merge-base diff and relevant surrounding code. Remain read-only during
review. Report only issues introduced or materially worsened by the change.

### Finding quality

- Use only Major, Minor, and Nit. Keep confidence separate.
- A finding must cite a changed location and state the violated invariant,
  reachable trigger, impact, evidence, minimal safe direction, and regression test.
- Treat an unsupported hypothesis as a question, not a finding.
- Deduplicate by root cause. Report at most five Nits and group repeats.
- Do not report formatting, lint, generated output, or other issues already
  enforced by CI.

### What is Major in this repository

Request changes for a reachable PR-introduced issue that can cause Rust unsoundness,
security/isolation failure, silent corruption, wrong GPU result, device/firmware
hang or brick, deadlock, unauthorized firmware execution/downgrade, unrecoverable
state, broad compatibility break, or violation of a documented hard resource or
watchdog limit.

### Repository invariants

- `<public API/wire/firmware contract>` must remain backward compatible with
  `<consumer/version window>`. The safe path for a change is `<version/negotiation
  or migration mechanism>`. See `<checked-in spec path>`.
- All `unsafe` abstractions under `<path>` must document and test `<soundness
  invariant>`. Safe callers must not be able to violate it.
- Before publishing `<descriptor/ring ownership field>`, make all descriptor and
  payload writes visible with `<required platform primitive>`. After observing
  device completion, establish `<required visibility>` before reading or reusing.
- GPU kernels under `<path>` must handle sizes not divisible by tile/workgroup/wave
  width and must match `<reference implementation>` within `<error contract>`.
- Firmware update must preserve an authentic bootable image after reset or power
  loss at every commit step and enforce `<anti-rollback policy>`.
- Do not log `<secrets/sensitive addresses/customer data>`; use `<safe diagnostic
  fields>` instead.

### Required review triggers

- Any change to `unsafe`, FFI, inline assembly, atomics, MMIO, DMA, interrupts,
  kernel barriers/atomics, boot/update/recovery, or signing requires a focused
  specialist pass and human owner review.
- Any public API/ABI/protocol/layout change requires mixed-version analysis.
- Any performance claim must include representative baseline and changed results,
  hardware/toolchain, input distribution, and variance.

### Skip or raise the bar

- Skip vendored and generated files when their reviewed generator/source is in the
  same change; verify clean regeneration instead.
- On test fixtures intentionally containing malformed code/data, report only if the
  fixture no longer tests its stated behavior or creates a real execution risk.
- On docs and comments, report behavior/contract inaccuracies; leave pure wording
  preferences as Nits.

---

Validate every new rule with one violating PR, one safe counterexample, and one
unrelated PR. Keep a rule only when it changes consequential review behavior.
