# Changed-Language and File-Class Routing

A domain reviewer does not replace language semantics. A Rust firmware reviewer
may understand reset behavior but miss a shell expansion bug in its build wrapper;
a workflow reviewer may understand permissions but miss Python exception behavior
inside an embedded helper. Inventory changed files before dispatch and assign both
the language and domain lenses that carry material risk.

## Build the inventory

For every changed file, generated group, or embedded program, record:

- source language/interpreter and declared supported versions;
- semantic role: production code, firmware/kernel, build/link/package/sign,
  generator, validator, CI policy, test, configuration, or normative documentation;
- consumers and interfaces: arguments, environment, stdin/stdout/stderr, files,
  ABI/wire format, artifact, workflow output, or human procedure;
- whether it is generated or vendored and the reviewed source/generator;
- required domain and language personas; and
- exact deterministic checks and configurations available.

Route by behavior, not filename. A YAML `run: |` block is shell plus CI. Python in
a here-document is Python plus its host language. Markdown containing a release
procedure is a contract. C generated from a reviewed generator may need clean
regeneration and artifact comparison rather than a line-by-line language pass.

For each material row in the inventory, spawn a fresh specialist review context
with exactly one primary persona. Low-risk, mechanically coupled rows may share a
reviewer only when the manifest states both scopes and the reviewer reports each
one separately. Merely launching a process does not count: the pass must finish,
identify the frozen target, and return its coverage artifact.

## Default specialist matrix

| Changed class | Required language/file specialist | Add these domain reviewers when applicable |
| --- | --- | --- |
| Rust | R1 Rust Language Lawyer; R2 for unsafe/FFI/asm | R3–R8 by risk |
| C/C++/headers/native firmware | R17 C/C++ Low-level Language Reviewer | R2 for cross-language ABI, R3–R8 by risk |
| Shell, Make/CMake, linker/package/sign wrappers | R13 Shell and Build Interface Reviewer | R5 firmware, R6 security, R7 architecture, R9 falsifier |
| Executable Python, generators, validators, harnesses | R14 Python Tooling Reviewer | R5/R6/R7/R9 by role |
| GitHub Actions or other CI/YAML/configuration | R15 CI and Declarative Configuration Reviewer | R6 for trust/secrets, R7 for policy, R9 for state transitions |
| Normative Markdown/spec/runbook/procedure | R16 Documentation and Contract Reviewer | Owning technical domain and R10 maintainer |
| Tests/fixtures only | Specialist for the language under test plus R9 | Owning production domain if fixtures encode its contract |
| Generated/vendor output | Review generator/source and verify clean reproduction | Direct output pass only for security, ABI, or generator-blind risks |
| Any other executable language | Appoint a language specialist with authoritative checklist | Mark missing expertise if none is available |

A tiny mechanical change may let one specialist own two closely coupled classes,
but the manifest must name both classes and the reviewer must explicitly accept
both scopes. Do not combine unrelated specialists merely to reduce agent count.

## Escalation rules

Select the High-risk lane when any changed language controls:

- firmware/kernel artifact identity, layout, link, package, signing, or deployment;
- privileged CI permissions, secrets, OIDC, release publication, or required gates;
- parsing of attacker-controlled, hardware, wire, binary, or signed data;
- cross-language ABI, memory ownership, concurrency, or hardware access; or
- destructive recovery/update/runbook steps where an error is hard to reverse.

For High-risk changes, use an independent frontier pass from both approved model
providers on the principal hazard. A deterministic reproducer can confirm a
finding, but it does not establish that all other hazards received independent
coverage.

## Coverage gate

Before adjudication, compare the manifest with the actual review artifacts. A pass
counts only when it records the immutable target, persona, provider/model/version,
files and embedded languages inspected, commands/evidence, and coverage limits.

If an executable or normative class lacks a required specialist and that omission
could hide material correctness, security, firmware, release, or recovery risk:

1. mark the affected scoring category `Unscored`;
2. set the decision to `Provisional — evidence required`;
3. name the missing pass and owner; and
4. do not describe the review as comprehensive.

The exception must be specific, such as “the JSON change is generated from the
reviewed Rust schema and clean regeneration is byte-identical.” “Covered by the
general reviewer” is not an exception.
