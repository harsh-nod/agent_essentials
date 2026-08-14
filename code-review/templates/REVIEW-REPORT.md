# Consolidated PR Review

## Decision

- Decision: Approve | Approve with follow-ups | Request changes | Provisional — evidence required
- Overall score: `<0-100 | Unscored>`
- Raw weighted score: `<value | Unscored>`
- Applied cap: `<none or rule and value>`
- Findings: `<N Major, N Minor, N Nit, N questions>`
- Review target: `<BASE_SHA>...<HEAD_SHA>`
- Review lane/date:
- Required human approvals/status:

One-sentence rationale: `<the most important reason for the decision>`

## Blocking findings

List confirmed Majors only, ordered by potential impact. If none, write `None`.

### F-001: `<imperative, specific title>`

- Severity: Major
- Confidence: high
- Category:
- Location: `path/to/file.rs:line`
- Affected configurations:
- Invariant:
- Trigger:
- Impact:
- Evidence:
- Reasoning:
- Minimal safe direction:
- Regression test:
- Verification/challenger result:

## Non-blocking findings

List confirmed Minors, then at most five grouped Nits. Use the same fields as above
except the severity. Do not include low-confidence speculation.

## Questions and evidence required

| Question/unknown | Why it matters | Required evidence/owner | Blocks final score? |
| --- | --- | --- | --- |
| | | | |

## Scorecard

Use `N/A` only when truly inapplicable and `Unscored` when evidence is missing.

| Category | Weight | Score 0–10 | Weighted points | Rationale/evidence |
| --- | ---: | ---: | ---: | --- |
| Functional correctness | 20 | | | |
| Rust soundness and FFI | 15 | | | |
| Concurrency and memory ordering | 12 | | | |
| Hardware, GPU, and firmware correctness | 15 | | | |
| Security and resilience | 10 | | | |
| Architecture and compatibility | 10 | | | |
| Performance and resource use | 8 | | | |
| Testing and verifiability | 5 | | | |
| Maintainability and documentation | 5 | | | |

Calculation:

```text
raw_overall = 100 * sum(weight * score / 10) / sum(applicable weights)
overall = min(raw_overall, applicable caps)
```

Applied caps and gates:

- [ ] No confirmed Major.
- [ ] No catastrophic-impact Major cap (39).
- [ ] No two-Major cap (49).
- [ ] No other-Major cap (69).
- [ ] All required deterministic checks pass, or check-failure cap (59) applied.
- [ ] No material category is Unscored.
- [ ] Required human/code-owner/security/hardware approvals complete.

## Coverage

### Reviewers

| Persona | Product/model/effort | Scope | Result | Coverage limits |
| --- | --- | --- | --- | --- |
| | | | | |

### Checks and evidence

| Check | Exact command/configuration | Target/hardware | Result/artifact |
| --- | --- | --- | --- |
| | | | |

### Reviewed boundaries

- Safe-Rust behavior and errors:
- Unsafe/FFI/assembly:
- Concurrency/async/interrupts:
- GPU kernel/host launch:
- Firmware/MMIO/DMA/state/update:
- Security/trust/isolation:
- Architecture/API/compatibility:
- Performance/resources:
- Tests/operations/documentation:

### Not covered

- Untested target/feature/hardware:
- Missing specification/context:
- Tool/model limitation:
- Residual risk and owner:

## Follow-up and re-review plan

- Required fixes:
- Required targeted tests/evidence:
- Re-review scope:
- Accepted risks, owner, issue, compensating control, expiry:
- Deferred improvements and issue:

## Private adjudication audit appendix

Remove this section from the public PR report unless unresolved evidence affects the
decision. Retain it in the review-eval record.

| Candidate | Origin | Final status | Severity change | Rationale/evidence |
| --- | --- | --- | --- | --- |
| | | confirmed/downgraded/question/rejected | | |
