# GPU Firmware and Hardware-Boundary Review Checklist

This checklist covers firmware itself and host/driver Rust that talks to GPU
firmware or hardware. The authoritative register, protocol, ISA, platform, and
silicon-errata documents for the exact product override all generic guidance.
When the agent cannot access them, it must mark the hardware claim unverified.

## Define the hardware contract

- [ ] Record device family, IP block, silicon steppings, board/platform variants,
      firmware/host versions, privilege level, and relevant errata revisions.
- [ ] Identify every changed register, packet, descriptor, ring, mailbox, shared
      buffer, interrupt, DMA mapping, command, and state transition.
- [ ] Record address widths/spaces, access sizes/alignment, byte/bit order, reset
      values, reserved bits, and ownership for every boundary structure.
- [ ] Record timing/deadline/watchdog, memory/stack/code/power, boot, update,
      recovery, and compatibility requirements.
- [ ] Draw the actors and trust boundaries: host process, kernel/driver, firmware,
      GPU engines, security processor, DMA/IOMMU, peer devices, and attacker inputs.

## MMIO and register access

- [ ] Access uses the platform's correct MMIO primitives, width, alignment,
      privilege, address mapping, and endianness.
- [ ] Volatile access prevents compiler elision where required, but is not mistaken
      for atomicity, mutual exclusion, cache maintenance, or hardware ordering.
- [ ] Required compiler, CPU, I/O, DMA, and device barriers are present at the right
      side of accesses; a generic Rust atomic fence may not order MMIO or DMA.
- [ ] Posted writes are flushed/read back where the hardware contract requires
      completion before a dependent action.
- [ ] Read-to-clear, write-one-to-clear/set, toggle, sticky, self-clearing, latch,
      shadowed, and destructive-read registers are handled explicitly.
- [ ] Read-modify-write does not corrupt reserved bits, acknowledge unrelated
      events, or race hardware updates; masks preserve mandated values.
- [ ] Reset values are not assumed after warm/partial/function-level reset when
      the register retains or has undefined state.
- [ ] Poll loops use the correct completion bit/polarity, tolerate transitional
      values, have bounded timeouts, and issue required barriers/delays.
- [ ] Register sequences remain atomic with respect to other cores, tasks,
      interrupts, firmware, and power/reset transitions.
- [ ] Debug reads/logging do not themselves change device state or timing.

## DMA, memory, and ownership

- [ ] DMA addresses, IOVA/physical/virtual distinctions, masks, address width,
      aperture, segment boundaries, alignment, and length units are correct.
- [ ] IOMMU mappings and permissions cover exactly the intended buffers and device;
      mapping lifetime extends through confirmed hardware completion.
- [ ] Integer arithmetic for address + offset + length cannot wrap before bounds
      and authorization checks.
- [ ] Descriptor/ring/buffer memory has required physical contiguity, cache-line
      alignment, padding, and non-overlap; false sharing does not corrupt ownership.
- [ ] Cache clean/flush before device reads and invalidate before CPU reads occur
      where the platform is non-coherent; coherent memory still gets required
      ordering barriers.
- [ ] Producer fills descriptor/data, makes it visible, transfers ownership, and
      rings the doorbell in the specified order.
- [ ] Consumer observes ownership/completion, establishes visibility, consumes, and
      only then reuses/unmaps/frees the storage.
- [ ] Device writes cannot target secrets, code, page tables, other tenants, stale
      mappings, or memory outside the validated request.
- [ ] Scatter/gather counts, chain/next pointers, terminators, cycles, overlapping
      entries, per-entry lengths, and maximum total length are validated.
- [ ] Partial DMA, errors, cancellation, reset, timeout, and surprise removal do not
      permit early reuse or leave permanent mappings/ownership ambiguity.
- [ ] CPU references do not claim immutability/exclusivity while DMA or firmware can
      mutate the same allocation; unsafe Rust invariants cover external mutation.

## Rings, queues, mailboxes, and commands

- [ ] Head/tail/index/phase arithmetic is correct for empty, one element, full,
      wraparound, counter overflow, and producer/consumer width differences.
- [ ] Full and empty states are distinguishable; capacity/reserved-slot convention
      agrees on both sides.
- [ ] Ownership/phase/generation bits prevent ABA and stale completion after reset
      or descriptor reuse.
- [ ] Packet opcode, version, size, flags, reserved fields, checksum/MAC, and payload
      are validated before dispatch or pointer use.
- [ ] Unknown commands/fields/versions fail safely and allow compatible extension
      where the protocol requires it.
- [ ] Partial/truncated/oversized/misaligned commands and malicious chains cannot
      read beyond buffers, loop forever, exhaust resources, or confuse state.
- [ ] Doorbell batching/coalescing cannot lose a notification or leave work idle;
      barriers order descriptors before notification.
- [ ] Backpressure and quotas prevent unbounded queue, memory, log, retry, or
      interrupt growth.
- [ ] Reset/teardown invalidates stale queue entries and synchronizes all actors
      before reinitialization.

## Interrupts, concurrency, and time

- [ ] Interrupt cause is read and acknowledged in the hardware-specified order;
      shared/spurious/masked/coalesced/level/edge behavior is handled.
- [ ] No event is lost between reading status, clearing it, unmasking, and checking
      for new work; shared status updates do not clear another source.
- [ ] Interrupt handlers perform only bounded, allowed operations and defer blocking
      or heavy work to an appropriate context.
- [ ] Locks and critical sections work across cores, task/interrupt context, nested
      interrupts, callbacks, and reset paths; lock order is acyclic.
- [ ] Atomics have supported width/alignment/order/scope and interact correctly with
      device memory rather than only CPU threads.
- [ ] Polling, event, and interrupt paths cannot both consume or complete one request
      without a single ownership transition.
- [ ] Time units, clock source/frequency, rounding, counter width, signedness,
      wraparound comparison, and suspend/power-clock effects are correct.
- [ ] Timeouts distinguish slow, lost, reset, and malicious devices; recovery is
      bounded and cannot create a retry/reset storm.
- [ ] Watchdog feeding proves progress rather than merely activity and cannot hide
      a stuck state indefinitely.

## Boot, reset, power, and lifecycle state machines

- [ ] Every state and transition has an owner, entry invariant, exit invariant,
      timeout, observable status, and recovery path.
- [ ] Cold boot, warm boot, partial reset, function/engine reset, suspend/resume,
      low-power entry/exit, hotplug/surprise removal, and crash recovery are covered.
- [ ] Initialization and teardown are idempotent or explicitly reject repeats;
      partial initialization unwinds in safe reverse order.
- [ ] Dependencies (clocks, rails, resets, memory, engines, security state) are
      enabled/disabled in the specified order with required stabilization delays.
- [ ] No operation races a power/reset transition or touches inaccessible state;
      in-flight work is quiesced, aborted, or reconstructed by contract.
- [ ] Reset does not silently erase evidence/ownership needed to safely reclaim DMA,
      locks, queues, or caller requests.
- [ ] Recovery has a bounded escalation ladder and avoids reset loops, permanent
      device disablement, or system-wide failure for a recoverable engine fault.
- [ ] Boot and recovery failure behavior is fail-safe for the product, with a
      diagnosable reason and supported repair path.

## Firmware update, authenticity, and anti-rollback

- [ ] Firmware is authenticated before execution using the intended root of trust,
      algorithm, key, signed region/metadata, and verification policy.
- [ ] Version/rollback policy prevents unauthorized downgrade while preserving an
      explicitly authorized recovery route.
- [ ] Lengths, offsets, load addresses, sections, compression, hashes, signatures,
      and manifest relationships are validated before copy/decompression/execution.
- [ ] Verification cannot be bypassed by integer wrap, alternate boot/recovery path,
      debug/manufacturing mode, partial image, mixed components, or TOCTOU.
- [ ] Power loss/reset at every update step leaves either the old or new authentic
      image bootable, or enters a tested authenticated recovery mode.
- [ ] A/B selection, commit markers, monotonic counters, retries, and bad-image
      quarantine are atomic and wear-aware where relevant.
- [ ] Key material and verification secrets are not logged, DMA-exposed, left in
      reusable buffers, or accessible at the wrong privilege.
- [ ] Update error reporting is actionable without leaking security-sensitive
      details or allowing an unprivileged denial-of-service loop.

## Security, isolation, and resilience

- [ ] Treat host/guest command streams, descriptors, firmware images, shared memory,
      device responses, and timing as untrusted according to the threat model.
- [ ] Validate before use at the component that owns the hardware invariant; do not
      rely solely on an upstream actor across a trust boundary.
- [ ] Privileged registers/opcodes/memory/engines are inaccessible to untrusted
      clients; tenant/context IDs cannot be forged, confused, or reused stale.
- [ ] DMA/IOMMU, memory protection, context-switch save/restore, scrub/zeroization,
      and reset maintain process/VM/tenant isolation.
- [ ] Debug, trace, JTAG, manufacturing, test, fault-injection, and recovery features
      are disabled or authorized appropriately in production lifecycle states.
- [ ] Secrets and sensitive addresses/data do not leak through logs, crash dumps,
      telemetry, residual memory/registers, timing, or cross-context caches where in
      scope.
- [ ] Malformed input cannot cause unbounded loops, allocation, interrupt storms,
      reset storms, watchdog starvation, queue blockage, or thermal/power abuse.
- [ ] Protect, detect, and recover controls exist for destructive firmware changes;
      recovery artifacts and paths are themselves authenticated.
- [ ] Security failures fail closed without making legitimate recovery impossible.

## Rust and constrained-runtime concerns

- [ ] Unsafe wrappers express MMIO/DMA/interrupt invariants without exposing safe
      references that hardware can invalidate or mutate concurrently.
- [ ] `read_volatile`/`write_volatile` types match register width/layout and are not
      used on ordinary shared memory as a concurrency primitive.
- [ ] `Send`/`Sync` implementations account for device instance, core/interrupt
      context, mapping lifetime, thread affinity, and reset.
- [ ] Panic/OOM/allocation behavior is defined; critical paths do not unexpectedly
      allocate, recurse, format heavily, or unwind.
- [ ] Stack, heap, static, code, log, and per-request resources fit worst-case
      budgets, including error and interrupt nesting.
- [ ] Integer/pointer conversions and packed descriptors meet Rust validity,
      provenance, alignment, initialization, and lifetime requirements.
- [ ] Compiler/linker scripts place code/data/metadata at correct addresses and keep
      boot/signature sections from unintended optimization or mutation.

## Compatibility and silicon variation

- [ ] Old host/new firmware, new host/old firmware, staged rollout, rollback, and
      partially upgraded multi-component systems are defined and tested.
- [ ] Capability/version negotiation precedes use; absence, unknown values, and
      lying/malicious peers have safe behavior.
- [ ] Protocol structure growth uses explicit sizes/versions/reserved fields and
      avoids interpreting uninitialized padding.
- [ ] Stepping/fuse/board differences and errata workarounds are detected narrowly,
      documented with source and removal condition, and tested on affected and
      unaffected hardware.
- [ ] Feature fallback preserves correctness and reports loss of capability; it does
      not silently run an incompatible sequence.
- [ ] Public telemetry/error/status identifiers and dump formats remain consumable
      by existing tools or have a migration path.

## Observability and diagnostics

- [ ] Failures report device/context, operation/state, status/register snapshot,
      firmware/host versions, and recovery action without secrets or unsafe reads.
- [ ] Logs are bounded/rate-limited and safe in interrupt/failure contexts; one bad
      device cannot exhaust system resources.
- [ ] Tracing preserves causal identifiers across submission, firmware processing,
      interrupt, completion, timeout, and reset.
- [ ] Health counters distinguish transient, corrected, degraded, reset, update,
      authentication, and permanent failure.
- [ ] Diagnostics do not alter destructive registers, acknowledge events, expose
      another tenant, or make timing failures disappear.

## Verification and fault injection

- [ ] Unit/property/fuzz tests cover packet/descriptor parsing, ring wrap/full/empty,
      arithmetic, state-machine transitions, and invalid/reserved values.
- [ ] Model or schedule tests cover producer/consumer ownership, barriers, interrupts,
      cancellation, reset, and timeout races.
- [ ] Simulator/emulator tests cover registers and state but are not mistaken for
      proof of cache, timing, electrical, interrupt, or silicon behavior.
- [ ] Hardware-in-the-loop covers all materially different steppings/platforms and
      records firmware, driver, compiler, clocks, and configuration.
- [ ] Inject malformed commands, DMA faults, IOMMU denial, partial completion,
      interrupt loss/storm, stuck bits, slow/no response, watchdog, and engine reset.
- [ ] Cut power/reset at each boot/update/commit step and prove authentic recovery.
- [ ] Stress counter/ring wrap with accelerated initialization near boundaries,
      not a test that would require years to wrap naturally.
- [ ] Measure worst-case stack/heap/code size, interrupt latency, watchdog margin,
      queue depth, throughput, power, and recovery time against hard budgets.
- [ ] Preserve traces and minimized fault scenarios as regression fixtures.
- [ ] Obtain a human hardware/security owner sign-off for unmodelled contract claims.

## Automatic Major triggers when confirmed

- unsafe MMIO or DMA ordering/ownership can corrupt memory or device state;
- malformed or untrusted input crosses a privilege/isolation boundary;
- an interrupt/ring/reset race can lose work, deadlock, hang, or reuse live memory;
- supported reset/power/update interruption can brick or boot unauthenticated code;
- host/firmware or silicon-version mismatch can execute an invalid contract without
  detection/fallback;
- a hard watchdog, memory, stack, timing, thermal, or power limit can be exceeded.
