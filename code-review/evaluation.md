# Review-System Evaluation Protocol

No code-review process can prove that it catches all bugs. Treat coverage as an
empirical property of a particular prompt, persona, model version, repository,
tool access, and test environment—not as a permanent capability claim.

## Evaluation corpus

Maintain a private, versioned corpus containing:

- confirmed historical escaped bugs and review findings;
- fixed counterparts and clean look-alikes that must not be reported;
- seeded one-defect-at-a-time mutations with a reachable trigger;
- multi-file integration failures across language boundaries;
- unsafe/FFI, concurrency, GPU, firmware, security, architecture, performance,
  build/release, CI, Python, shell, C/C++, and documentation-contract cases; and
- missing-context cases whose correct result is a question or provisional review.

For every case, hide the expected location, mechanism, severity, and decisive
evidence from the reviewer. Record which personas are expected to find it and
which personas should abstain.

Whenever a novel failure is found—such as a consumer capturing diagnostic stdout
as a filename—add both the buggy case and a corrected counterexample. The eval
must prove that the responsible reviewer finds the mechanism from the diff rather
than parroting a bug description.

## Measurements

Track by persona, model/provider/version/effort, language, and risk lane:

- Major and Minor recall, with escaped severity weighted explicitly;
- Major precision, confirmation rate, and unsupported-claim rate;
- unique confirmed findings contributed beyond other reviewers;
- correct abstention on clean and missing-context cases;
- severity/category accuracy, duplicates, and actionable regression tests;
- time, tool calls, cost, and human adjudication effort; and
- failures caused by unavailable specs, targets, hardware, or provider access.

Report confidence intervals or case counts beside percentages. Ten easy cases do
not establish reliable firmware recall.

## Release gate for framework or model changes

Before changing a prompt, model alias, roster, or automatic-comment policy:

1. freeze a representative holdout set;
2. run the old and proposed configurations independently;
3. require no unacceptable Major-recall or Major-precision regression;
4. inspect unique findings and false positives, not only an aggregate score;
5. canary the change on read-only live reviews; and
6. record the exact configuration and decision.

Re-run after model/version changes, quarterly, and after every escaped Major. Do
not tune prompts on the final holdout or publish automatic approvals based only on
agent silence.

## Live-review audit

Each consolidated report retains the immutable SHA, changed-language manifest,
actual reviewer execution manifest, raw candidates, challenge dispositions,
commands, and coverage gaps. Periodically sample “no finding” reviews and compare
post-merge bugs to the manifest. The useful question is not “did agents review
it?” but “which hazard was independently exercised, with what evidence?”
