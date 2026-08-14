# Severity, Confidence, and PR Scoring

Severity describes impact and urgency. Confidence describes evidence quality.
Category scores describe the reviewed PR's readiness. Keep these dimensions
separate: a catastrophic but uncertain scenario is not a confirmed Major, and a
high-confidence typo is not important.

## Severity

Use only `Major`, `Minor`, and `Nit` in published findings.

### Major — request changes

The PR can cause a material production failure, unsoundness, security boundary
violation, data corruption, device hang/brick, deadlock, incorrect result, broad
compatibility break, unrecoverable state, or violation of a hard resource/SLO
contract. It has a reachable trigger under supported or security-relevant
conditions and no adequate existing mitigation.

Examples:

- safe Rust can trigger undefined behavior through an unsafe abstraction;
- a divergent GPU barrier can hang a workgroup for a supported shape;
- a device-scope release is used for a host consumer that requires system scope;
- DMA ownership is published before descriptor contents are visible;
- firmware update can accept an unauthorized downgrade or cannot recover from a
  power loss required by the product contract;
- a public ABI or protocol changes without compatibility/migration;
- a normal input produces a wrong kernel result or out-of-bounds access;
- a documented latency, memory, code-size, or watchdog budget is exceeded enough
  to break operation.

A Major must include a concrete mechanism, trigger, impact, and verification.
“Might race,” “could be insecure,” or “architecture is bad” is not sufficient.

### Minor — fix or explicitly accept

The PR has a real, localized defect or material quality gap with bounded impact,
an uncommon/non-default trigger, straightforward recovery, or a meaningful test,
diagnostic, maintainability, or performance omission. It should be fixed in the
PR unless an owner explicitly accepts and tracks it.

Examples:

- a supported but uncommon feature combination does not compile;
- an error path leaks a bounded resource but recovery/reset works;
- a new state transition lacks a targeted regression test;
- diagnostics omit information required to distinguish two actionable failures;
- a measurable regression is below a hard budget but lacks a justified tradeoff;
- an internal interface creates concrete coupling likely to cause near-term
  duplication or inconsistent policy.

### Nit — optional polish

A low-impact readability, consistency, documentation, naming, or local cleanup
suggestion. It does not change current correctness, safety, compatibility,
security, or required operational behavior.

Cap published Nits at five and group repetitions. Formatting and other checks
already enforced by CI should not become agent comments.

## Severity decision test

Apply in order:

1. Is there a specific PR-introduced invariant violation or quality gap? If no,
   omit it or ask a question.
2. Is the trigger reachable on a supported path, adversarial boundary, required
   recovery path, or documented compatibility configuration? If unknown, state
   the missing evidence; do not publish as confirmed.
3. Can the impact be material, broad, silent, unsafe, security-relevant,
   unrecoverable, or contract-breaking? If yes, `Major`.
4. Is the impact real but bounded, rare, recoverable, or primarily a verification,
   maintainability, diagnostic, or non-contractual performance gap? `Minor`.
5. Is it optional polish only? `Nit`.

Likelihood is evaluated over the product lifetime and attacker capability, not
only the reviewer's ability to reproduce it today. A rare power-loss or wraparound
case may be Major when eventual occurrence or adversarial triggering is credible.

## Confidence

| Level | Required support | Publication rule |
| --- | --- | --- |
| High | Reproducer/tool/trace, authoritative spec plus direct code path, or a complete invariant/execution proof | Publish after source spot-check; Major still gets challenge review |
| Medium | Direct code path with one stated assumption or strong but incomplete target evidence | Publish Minor after adjudication; Major requires independent confirmation or is presented as a question |
| Low | Plausible hypothesis, naming inference, uncertain hardware behavior, missing context | Do not publish inline; put in questions/follow-ups with a validation step |

Model agreement raises confidence only when the second review is independent and
adds evidence. Repeating the same reasoning does not.

## Scoring categories

Score each applicable category from 0 to 10 after findings are verified and
deduplicated. `N/A` is allowed only when the category truly does not apply; unknown
coverage is `Unscored`, not `N/A`.

| Category | Weight | What the score covers |
| --- | ---: | --- |
| Functional correctness | 20 | Intended behavior, edge cases, errors, resource lifetime, target/feature behavior |
| Rust soundness and FFI | 15 | Unsafe invariants, aliasing/validity/lifetime/layout, ABI, unwind, asm |
| Concurrency and memory ordering | 12 | Races, atomics/scopes, locks, progress, interrupts, host/device visibility |
| Hardware, GPU, and firmware correctness | 15 | Indexing, launch/ABI, MMIO, DMA, registers, state/reset/power, silicon variation |
| Security and resilience | 10 | Trust boundaries, validation, privilege/isolation, update/recovery, supply chain |
| Architecture and compatibility | 10 | Ownership/boundaries, state model, API/ABI/protocol evolution, rollout/rollback |
| Performance and resource use | 8 | Complexity, latency/throughput, occupancy, bandwidth, memory/stack/code/power budgets |
| Testing and verifiability | 5 | Regression, property/differential/fault tests, target matrix, observability of claims |
| Maintainability and documentation | 5 | Clarity, invariants, diagnostics, comments, dependency burden, runbooks |

For a docs-only PR, for example, Rust soundness and hardware categories may be
`N/A` and the remaining weights are renormalized. For an unsafe GPU firmware PR,
all categories apply.

## Category anchors

Use these anchors, interpolating only when evidence supports it:

| Score | Meaning |
| ---: | --- |
| 10 | Exceptional: requirements and invariants are explicit; implementation is convincing; targeted evidence covers important failure modes; no confirmed findings |
| 8 | Strong: correct and well-supported with small bounded gaps or Nits only |
| 6 | Acceptable with work: one or more confirmed Minors or meaningful evidence gaps, but design is recoverable and no confirmed Major |
| 4 | Weak: several Minors, a large verification gap, or a Major that is localized and straightforward to fix |
| 2 | Unsafe to merge: confirmed Major affects core behavior or the design obscures critical invariants |
| 0 | Catastrophic/unreviewable: demonstrated unsoundness, security compromise, corruption, bricking, or no credible basis to judge the category |

Suggested deductions can improve consistency but do not replace judgment:

- Major: normally 4–10 points in each directly affected category;
- Minor: normally 1–3 points;
- Nit: normally 0–0.5 points, capped at 1 total per category;
- duplicated symptoms count once at the root cause;
- one finding may affect multiple categories, but explain each effect rather than
  multiplying a mechanical penalty.

Start from the anchor that describes the evidence, then check that deductions and
findings tell a consistent story. Do not give 10 merely because no agent found a
bug when coverage or tests were weak.

## Overall score

For applicable categories `i`, with category score `s_i` from 0–10 and weight
`w_i`, compute:

```text
raw_overall = 100 * sum(w_i * s_i / 10) / sum(w_i)
overall = min(raw_overall, all_applicable_caps)
```

Round once to the nearest integer at the end. The report must show category
scores, weights, rationales, `N/A` categories, caps, and the formula result.

## Non-averaging caps and gates

Apply the lowest relevant cap:

| Condition | Overall cap | Decision |
| --- | ---: | --- |
| Confirmed Major with potential unsoundness, security compromise, silent corruption, device brick/hang, unrecoverable firmware, or deadlock | 39 | Request changes; qualified human owner required |
| Two or more independent confirmed Majors | 49 | Request changes |
| Any other confirmed Major | 69 | Request changes |
| A required deterministic check fails because of the PR | 59 | Request changes unless failure is itself the already-counted stronger cap |
| Material requirement, hardware contract, or applicable category cannot be evaluated | No final score | Provisional review; obtain evidence |

No score or reviewer count can approve a PR with a confirmed Major. A waived Major
remains visible; record the accountable owner, rationale, compensating control,
tracking issue, and expiry. Waiver does not increase the score.

## Readiness bands

| Overall | Label | Default interpretation |
| ---: | --- | --- |
| 90–100 | Excellent | Approve if there are no Majors and required human/CI gates pass |
| 80–89 | Strong | Approve or approve with small follow-ups; Minors must be resolved or explicitly accepted |
| 70–79 | Needs work | Request focused changes or missing evidence before merge |
| 50–69 | High risk | Request changes; substantial gaps or a Major cap |
| 0–49 | Unsafe/unready | Do not merge; fundamental correctness, safety, security, hardware, or reviewability problem |

The band is an input to human judgment, not a merge bot by itself.

## Example

An unsafe kernel PR receives scores `8, 7, 8, 6, 9, 8, 6, 7, 8`. All categories
apply. The weighted raw score is:

```text
(20*8 + 15*7 + 12*8 + 15*6 + 10*9 + 10*8 + 8*6 + 5*7 + 5*8) / 10
= 74.4 -> 74
```

If the hardware score of 6 includes a confirmed wrong-result Major, the overall
score remains 69 because the Major cap overrides the raw 74. If that finding can
silently corrupt results, the stronger cap makes it 39. The PR is request-changes
in either case.
