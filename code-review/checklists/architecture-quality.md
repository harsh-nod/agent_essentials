# Architecture, Code Quality, and Operability Checklist

Use this across all PRs. Architecture comments must connect to a concrete invariant,
compatibility risk, operational failure, testing obstacle, or ownership cost. “I
would design it differently” is not a finding.

## Intent, scope, and reviewability

- [ ] PR context states the problem, user/system outcome, constraints, non-goals,
      alternatives considered, and observable success criteria.
- [ ] Diff matches the stated intent; unrelated refactors, formatting, generated
      output, dependency churn, and behavior changes are separated or explained.
- [ ] Size and coupling permit a reviewer to form a complete change model. If not,
      split by independently valid behavior rather than arbitrary files.
- [ ] New assumptions and invariants are visible in types, APIs, assertions, tests,
      specifications, or durable comments near the owning code.
- [ ] Repository instructions, design records, protocol/hardware specs, and runbooks
      are updated when the change makes them stale.

## Responsibility and dependency structure

- [ ] The component that owns data and lifecycle also owns validation and invariant
      enforcement, or the boundary clearly defines who does.
- [ ] Dependency direction follows the intended layering; low-level mechanisms do
      not depend on high-level policy or vendor/product details without reason.
- [ ] Hardware-generation and backend differences are contained behind explicit
      capability/strategy boundaries rather than scattered conditionals.
- [ ] Cross-cutting concerns (security, logging, retries, feature detection,
      synchronization) have one source of policy and do not drift across callers.
- [ ] Abstractions reduce duplicated invariants or enable required variation; they
      are not speculative wrappers with one use and no stable concept.
- [ ] Shared utilities do not become a dumping ground that couples otherwise
      independent crates/subsystems.
- [ ] Dependency cycles, global registries/singletons, callbacks, and hidden side
      effects do not obscure ownership, ordering, or test isolation.

## Data and state models

- [ ] Types make invalid states hard to construct and distinguish identifiers,
      addresses, sizes, units, versions, permissions, and lifecycle states.
- [ ] State machines enumerate transitions, owners, guards, side effects, timeout,
      idempotency, rollback/recovery, and terminal states.
- [ ] Mutation is localized and atomic at the level the external contract observes;
      partial state has defined visibility and cleanup.
- [ ] Cached/derived/duplicated state has a source of truth and invalidation model.
- [ ] Persistence/wire/hardware structures are separated from convenient in-memory
      structures when their evolution, validity, or layout differs.
- [ ] Resource ownership spans async, FFI, DMA, callbacks, cancellation, reset, and
      destruction without “someone else keeps it alive” assumptions.

## Interfaces and compatibility

- [ ] Public Rust API, C ABI, kernel/firmware packet, register use, file/storage
      format, config, CLI, logs/metrics, and error codes are treated as contracts.
- [ ] Breaking and behavioral changes are identified, versioned, migrated, or
      provided a compatibility path; “internal” is verified against real consumers.
- [ ] Mixed-version behavior supports staged rollout and rollback, including old/new
      host, firmware, library, driver, and persisted state combinations.
- [ ] Capability negotiation is explicit and fails safely for absent/unknown values.
- [ ] Defaults remain safe and compatible; a new option does not silently alter
      unrelated callers or targets.
- [ ] Deprecation names the replacement, migration, telemetry/usage evidence,
      timeline, and removal condition.
- [ ] Error types/codes retain actionable semantics and do not collapse distinct
      retry, reset, unsupported, invalid, and security failures.

## Failure containment and recovery

- [ ] Failure boundaries prevent one request, process, VM/tenant, device, engine, or
      optional feature from corrupting or indefinitely blocking the rest.
- [ ] Timeouts, retries, circuit breaking, reset, fallback, and degradation are
      bounded and coordinated; they do not amplify into storms.
- [ ] Operations are idempotent where retried or have durable deduplication/commit
      semantics.
- [ ] Partial initialization/commit/update has a recoverable state and safe reverse
      cleanup; rollback itself is tested.
- [ ] Process/device restart and crash recovery reconstruct or reject stale state
      deliberately.
- [ ] Fail-open versus fail-closed behavior follows the explicit safety/security and
      availability priorities.

## Performance and capacity architecture

- [ ] Algorithmic complexity and worst-case resource use are acceptable, including
      attacker-controlled or pathological inputs.
- [ ] Allocation, copy, serialization, synchronization, launch, and host/device
      transfer boundaries are intentional and measured where material.
- [ ] Backpressure, queue bounds, admission, cancellation, and quotas exist at the
      component that can enforce them.
- [ ] Caches define ownership, key completeness, invalidation, eviction, memory
      budget, error behavior, and observability.
- [ ] Batching, async work, parallelism, and pooling preserve fairness, ordering,
      tail latency, isolation, and teardown.
- [ ] Optimization complexity is justified by a representative baseline and can be
      disabled/fallen back for debugging and unsupported hardware where needed.

## Security architecture

- [ ] Trust boundaries and attacker-controlled fields are explicit, and validation
      occurs before address, allocation, dispatch, privilege, or state use.
- [ ] Least privilege applies to processes, devices, DMA mappings, keys, debug
      facilities, build systems, dependencies, and agent/CI credentials.
- [ ] Authentication, authorization, integrity, freshness/anti-replay, isolation,
      and recovery are owned by the right layer and cannot be bypassed by fallback.
- [ ] Sensitive data has an explicit lifetime, storage, logging, dump, zeroization,
      and cross-tenant policy.
- [ ] Security decisions are auditable without leaking secrets; failures are
      rate-limited and recoverable.

## Maintainability and local code quality

- [ ] Naming reflects domain meaning, units, ownership, and state rather than
      implementation accidents.
- [ ] Functions/modules have one coherent responsibility and expose the minimum
      state needed to enforce invariants.
- [ ] Control flow makes success, failure, cleanup, and exceptional hardware paths
      visible; deeply nested cleverness is simplified where it hides behavior.
- [ ] Comments explain why, contract, hardware workaround, safety proof, memory
      order, numerical choice, or removal condition—not syntax.
- [ ] `unsafe`, fences, volatile accesses, magic constants, register sequences,
      algorithms, and performance tricks cite the owning spec/invariant.
- [ ] Duplicated logic cannot drift, while deduplication does not erase meaningful
      target differences.
- [ ] Errors add actionable context once, preserve structured causes, and avoid
      secrets, uncontrolled volume, or formatting/allocation in constrained paths.
- [ ] Dead code, stale flags, TODOs without owners, temporary compatibility paths,
      and workarounds have removal criteria/tracking where material.
- [ ] Dependencies and features have clear value and do not expand build, security,
      binary, licensing, or platform burden gratuitously.

## Test architecture and verifiability

- [ ] Each material requirement/invariant maps to a test, proof, runtime assertion,
      monitoring signal, or explicitly documented manual/hardware validation.
- [ ] Tests exercise public behavior and independent oracles rather than duplicating
      private implementation steps.
- [ ] Unit tests isolate algorithms; integration tests cover boundaries; property,
      differential, fuzz, model, fault, simulator, and HIL tests cover the risks
      each is suited to.
- [ ] Failure, cancellation, retry, timeout, reset, partial state, compatibility,
      and recovery paths receive first-class tests.
- [ ] Target/feature/hardware matrix reflects real supported combinations and has
      explicit owners for gaps.
- [ ] Tests are deterministic or control/report seeds, schedules, clocks, devices,
      tolerances, warm-up, and environmental dependencies.
- [ ] Performance tests use representative inputs, stable measurement, variance,
      and meaningful regression thresholds.
- [ ] Generated artifacts are reproducible and CI verifies regeneration when
      practical.

## Operability and rollout

- [ ] Logs, metrics, traces, dumps, and health/status expose the state and causal
      identifiers needed to detect and diagnose new failure modes.
- [ ] Telemetry is bounded, privacy/security safe, target-appropriate, and robust
      during overload, interrupts, OOM, and device failure.
- [ ] Config is validated, documented, observable, safely defaulted, and supports
      staged rollout/rollback without version skew surprises.
- [ ] Feature flags have owner, expiry, both-path tests, and behavior after rollback.
- [ ] Deployment/update order, compatibility window, data/firmware migration,
      rollback, and recovery steps are explicit.
- [ ] Alerts and runbooks identify symptom, likely cause, evidence to collect, safe
      mitigation, escalation, and conditions requiring device isolation/replacement.
- [ ] Support/debug tooling understands new states, versions, errors, and artifacts.

## Documentation

- [ ] Public API docs state invariants, units, ranges, threading/async, safety,
      errors/panics, side effects, lifetime/ownership, and examples.
- [ ] Unsafe APIs have a `Safety` contract sufficient for an independent caller;
      safe wrappers explain how they uphold it.
- [ ] Hardware and protocol code cites exact spec/errata revision and preserves
      context that cannot be inferred from code.
- [ ] Architecture/design docs show changed components, state/sequence, trust and
      failure boundaries, and compatibility/rollout decisions.
- [ ] User/operator docs and changelog/migration notes reflect externally observable
      behavior.

## Proportionate feedback

- Mark a concern `Major` only when the architecture creates a concrete material
  failure, unsafe boundary, compatibility break, unrecoverable migration, or hard
  operational/resource violation in this PR.
- Mark a bounded design or verification gap `Minor` when it has a specific cost and
  feasible fix or acceptance decision.
- Mark optional clarity/local cleanup `Nit`, cap Nits, and group repetitions.
- Offer one minimal safe direction, not a speculative rewrite, unless the current
  structure cannot meet the required invariants.
