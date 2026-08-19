# Documentation and Contract Review Checklist

Use for Markdown, specifications, runbooks, plans, READMEs, examples, release notes,
and comments that people or tools rely on. Pure prose polish is not a correctness
review; normative procedures and safety contracts are executable interfaces.

## Classify the document

- [ ] Identify audience, owner, normative versus descriptive status, supported
      versions/hardware, source of truth, last verification date, and expiry.
- [ ] Distinguish implemented/verified behavior from proposal, plan, assumption,
      example, workaround, and unavailable evidence.
- [ ] The document does not override or duplicate an authoritative specification
      without version, rationale, and synchronization mechanism.
- [ ] Generated documentation names its source and is reproducible; reviewers focus
      on source correctness plus a clean generated diff.

## Technical accuracy and contracts

- [ ] Flag, environment, command, API, type, register, packet, file, job, artifact,
      state, metric, and error names exactly match current code and interfaces.
- [ ] Units, ranges, defaults, paths, permissions, prerequisites, versions, targets,
      feature combinations, and expected outputs are complete and unambiguous.
- [ ] Safety/unsafe, concurrency, ownership, lifetime, ordering, security, hardware,
      recovery, and compatibility invariants are explicit enough to act on.
- [ ] Diagrams and sequences match actual actors, direction, states, errors,
      rollback, and trust/privilege boundaries.
- [ ] Links and anchors resolve to stable authoritative targets; version-specific
      claims do not use an unversioned moving page without reason.
- [ ] Proof counts and verification tables distinguish executable refinement,
      structural datatype lemmas, assumptions, and unverified adapters; aggregate
      counts do not imply behavioral coverage they do not provide.

## Commands, examples, and procedures

- [ ] Commands and code blocks identify shell/language, starting directory,
      required environment/credentials, target, expected output, and cleanup.
- [ ] Snippets run or compile in a clean supported environment, or are clearly
      marked pseudocode with non-copyable placeholders.
- [ ] The documented pre-push command covers newly introduced target and feature
      bodies, or explicitly states which configurations are compiled only in CI.
- [ ] Examples cover important error/rollback behavior and do not normalize an
      insecure, deprecated, destructive, or unsupported shortcut.
- [ ] Multi-step procedures define checkpoints, idempotency, partial failure,
      rollback/recovery, evidence to retain, and stop/escalation conditions.
- [ ] Destructive commands resolve a narrow target and include proportionate
      backup/recovery guidance; no example relies on broad roots or empty variables.

## Security, confidentiality, and operations

- [ ] No real secrets, credentials, internal tokens, customer data, sensitive
      addresses, unreleased identifiers, or unsafe diagnostic dumps are published.
- [ ] Authentication, authorization, signing, anti-rollback, trust, and threat-model
      claims match enforced behavior and do not imply guarantees absent from code.
- [ ] Runbooks collect actionable, bounded, non-destructive evidence before reset
      and identify safe mitigation, owner, escalation, and recovery verification.
- [ ] Copy/paste operations use least privilege and cannot expose credentials via
      command history, process arguments, logs, or artifacts.

## Maintainability and verification

- [ ] Terminology and abbreviations follow repository/domain conventions; a rename
      updates definitions and all normative uses without inventing false scope.
- [ ] Tables, references, headings, anchors, lists, and fences render correctly;
      local links and referenced files exist with case-sensitive paths.
- [ ] Documentation tests, link checks, schema/example extraction, and snippet tests
      run where feasible; manual verification records environment and date.
- [ ] The change updates nearby docs and runbooks made stale by the code, without
      requiring unrelated prose churn.
- [ ] Findings cite concrete wrong behavior, unsafe action, broken contract, or
      material ambiguity. Subjective wording stays optional and Nits are grouped.
