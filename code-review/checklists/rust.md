# Rust Review Checklist

Use this checklist to direct attention, not to generate one comment per checkbox.
Report only PR-introduced, actionable findings with evidence. Repository and target
rules override generic advice.

## Change model

- [ ] Identify the exact safe/public behavior being added, removed, or changed.
- [ ] Trace changed inputs through state changes, outputs, errors, cleanup, and
      externally observable side effects.
- [ ] List supported targets, pointer widths, endianness, MSRV/toolchain, panic
      strategy, allocators, features, and `std`/`no_std` modes affected.
- [ ] Identify all newly reachable `unsafe`, FFI, inline-assembly, hardware, and
      concurrency boundaries, including safe wrappers called indirectly.
- [ ] Check callers and consumers outside the diff; a locally valid edit can break
      an unstated crate-wide invariant.
- [ ] Separate pre-existing problems from regressions introduced or materially
      worsened by the PR.

## Functional correctness

### Inputs, ranges, and arithmetic

- [ ] Check empty, singleton, minimum, maximum, odd, non-power-of-two, and
      non-divisible lengths; malformed and truncated inputs; duplicate and
      out-of-order events.
- [ ] Check overflow/underflow before comparisons, bounds checks, address/size
      calculations, allocation layouts, timeouts, sequence numbers, and ring math.
- [ ] Check debug versus release overflow behavior and intentional wrapping,
      saturating, checked, or overflowing operations.
- [ ] Check signed/unsigned and narrowing conversions, especially `usize` to fixed
      widths, negative foreign values, and 32-bit targets.
- [ ] Check multiplication/addition order in `count * stride + offset`; a final
      bounds check cannot repair arithmetic that already wrapped.
- [ ] Check shifts by type width, bit masks, sign extension, rotations, and
      assumptions about integer representation.
- [ ] Check division/modulo by zero and signed minimum divided by `-1`.
- [ ] Check float-to-int conversion semantics, NaN/Inf handling, loss of precision,
      signed zero, denormals, and comparison tolerances when relevant.

### Collections, parsing, and state

- [ ] Check indexing, slicing, chunk remainders, UTF-8 boundaries, cursor progress,
      and parser acceptance of trailing or ambiguous data.
- [ ] Check iterator invalidation assumptions and whether laziness changes the
      lifetime or timing of side effects.
- [ ] Check map/set collision, duplicate-key, replacement, and ordering behavior.
- [ ] Check state transitions for illegal, repeated, skipped, concurrent, and
      partial transitions; make terminal and recovery states explicit.
- [ ] Check idempotency of retry, initialization, teardown, reset, and replay.
- [ ] Check cached/derived values are invalidated on every mutation path.
- [ ] Check equality, ordering, hashing, and serialization implementations remain
      mutually consistent.

### Errors, panics, and resources

- [ ] Check every `unwrap`, `expect`, assertion, index, and panic is unreachable or
      acceptable for all supported inputs and runtime modes.
- [ ] Check errors are neither swallowed nor converted into success/default values
      that violate the caller's contract.
- [ ] Check partial initialization and early returns release or roll back every
      acquired resource in the required order.
- [ ] Check `Drop` behavior, double-close/free/unmap, forgotten guards, reference
      cycles, and intentionally leaked resources.
- [ ] Check destructors cannot observe invalid partial state and do not panic during
      unwinding unless abort is the explicit policy.
- [ ] Check retry/backoff has bounds, preserves the original cause, and does not
      duplicate non-idempotent work.
- [ ] Check cancellation or timeout does not report failure while work still owns
      caller buffers or can later publish a result unexpectedly.

### API and type semantics

- [ ] Check new safe APIs cannot express invalid states or silently weaken existing
      preconditions/postconditions.
- [ ] Check generic bounds, variance, auto-traits, lifetimes, and marker types
      encode the intended ownership and thread-safety constraints.
- [ ] Check `Clone`/`Copy` does not duplicate unique ownership, handles, mappings,
      guards, or registration state.
- [ ] Check `Default` produces a valid and safe operational state.
- [ ] Check `From`/`Into` versus `TryFrom` does not hide fallibility or truncation.
- [ ] Check public enum/struct changes, `#[non_exhaustive]`, trait methods, feature
      exposure, and error variants for semver/consumer impact.

## Unsafe Rust soundness

The burden is universal quantification: a safe abstraction must be sound for every
safe caller, not only for current call sites.

### Safety contracts

- [ ] Every `unsafe` block states the invariant it relies on and how the local code
      establishes it; every `unsafe fn` documents caller obligations.
- [ ] The unsafe operation is as small and local as practical; unrelated safe work
      is outside the block.
- [ ] Safe constructors and mutators preserve the invariant through all success,
      error, panic, cancellation, and drop paths.
- [ ] Debug assertions are not the only enforcement for safety preconditions.
- [ ] The contract accounts for malicious-but-safe trait implementations and safe
      reentrancy where traits/callbacks are involved.

### Pointer validity, provenance, and aliasing

- [ ] Raw pointers have appropriate provenance, are non-null when required, aligned,
      dereferenceable for the full range, and point to live storage.
- [ ] Pointer offset calculations remain within the language/API's allowed object
      bounds and cannot wrap `isize`/address space constraints.
- [ ] No reference is formed before its pointee is valid for that reference type,
      even if the reference is never subsequently dereferenced.
- [ ] `&T` data is not mutated except through a valid `UnsafeCell` pattern; `&mut T`
      has exclusive access for its entire live/use period.
- [ ] Foreign code, another thread, hardware, or DMA cannot mutate memory while a
      conflicting Rust reference exists.
- [ ] Reference lifetime is not artificially extended by transmute, raw-pointer
      round trips, leaked guards, or unconstrained output lifetimes.
- [ ] Integer-pointer conversions and tagged pointers preserve required alignment,
      address bits, and provenance under the supported Rust model.

### Validity, initialization, and layout

- [ ] Values obey type validity: initialized bytes, valid `bool`/`char`/enum,
      non-null references/boxes, and valid function pointers.
- [ ] `MaybeUninit` transitions initialize every byte/element before assume-init,
      reference creation, length publication, or drop.
- [ ] Partial array/vector initialization tracks exactly which elements must drop;
      `Vec::set_len` follows full initialization.
- [ ] Padding is not assumed initialized, compared, hashed, serialized, or exposed
      unless the representation and initialization make that valid.
- [ ] `repr(Rust)` layout is never treated as a stable ABI. `repr(C)`, `transparent`,
      `packed`, and explicit alignments are used and validated for the real boundary.
- [ ] Packed fields are not referenced through an unaligned reference; use explicit
      unaligned operations or copies where permitted.
- [ ] Transmutes have equal size and compatible validity/alignment/lifetime, and a
      narrower, auditable conversion was considered.
- [ ] Zero-sized and over-aligned types work with allocation, pointer arithmetic,
      collections, and FFI assumptions.

### Allocation, ownership, and destruction

- [ ] `Layout` size/alignment is valid and arithmetic cannot overflow.
- [ ] Allocation and deallocation use the same allocator, layout, ownership domain,
      and ABI; Rust/C/firmware sides do not free one another's objects incorrectly.
- [ ] `Box::from_raw`, `Vec::from_raw_parts`, `CString::from_raw`, and similar
      reconstruction APIs receive exactly the pointer/capacity/ownership expected.
- [ ] Moves do not invalidate self-references; pinning invariants are preserved and
      pinned fields are not moved through projection/drop/replacement.
- [ ] Manually dropped or forgotten values cannot be dropped twice or leave a safe
      handle pointing to released/reused storage.

### Auto-traits and concurrency safety

- [ ] Every `unsafe impl Send` and `Sync` proves all contained raw pointers, foreign
      handles, thread-affine resources, and mutation protocols satisfy the trait.
- [ ] Interior mutability uses synchronization appropriate to every accessor and
      target; `UnsafeCell` permits mutation but provides no synchronization.
- [ ] Shared ownership/refcounts cannot overflow, resurrect freed storage, or race
      with weak/strong conversion and destruction.

### Inline assembly

- [ ] Instructions, registers, operand widths/classes, clobbers, flags, stack use,
      memory effects, and `options(...)` match actual behavior.
- [ ] The compiler is informed of memory reads/writes and ordering; `nomem`,
      `readonly`, `pure`, and `nostack` are justified rather than optimistic.
- [ ] Calling convention, callee-saved registers, stack alignment, unwind, target
      features, privilege level, and unsupported targets are handled.
- [ ] Outputs are initialized on every control path, including branches and errors.

## FFI and ABI

- [ ] Both sides agree on calling convention, symbol name, integer widths,
      signedness, struct/union layout, alignment, packing, endianness, and ownership.
- [ ] Only FFI-safe representations cross the boundary; Rust references, slices,
      trait objects, `String`, `Vec`, ordinary Rust enums, and `repr(Rust)` values do
      not cross as if they had a stable C ABI.
- [ ] Nullable pointers are represented and checked correctly; non-null Rust
      references are not used to encode optional foreign pointers.
- [ ] Buffer pointer/length pairs have validated units, bounds, mutability, lifetime,
      aliasing, and behavior for zero length/null combinations.
- [ ] Strings define encoding, termination, embedded-NUL behavior, length units,
      ownership, and maximum scan length.
- [ ] Callbacks define lifetime, thread, reentrancy, cancellation/unregistration,
      context ownership, and behavior after teardown.
- [ ] Foreign handles are not duplicated/dropped incorrectly and thread-affinity or
      process/device ownership is encoded.
- [ ] Panic/unwind cannot cross an ABI that forbids it; `C` versus `C-unwind`,
      foreign exceptions, and abort/catch policy match both toolchains.
- [ ] Foreign functions cannot retain Rust references or stack pointers longer than
      promised; asynchronous foreign/device work owns or pins data until completion.
- [ ] Headers/bindings are regenerated from the intended source and diffed; ABI
      tests cover size, align, offsets, discriminants/constants, and symbols.
- [ ] Version negotiation and mixed old/new library behavior are explicit.

## Concurrency, atomics, and async

- [ ] Identify shared state, all actors (threads, tasks, signals, interrupts,
      devices), synchronization primitives, and required happens-before edges.
- [ ] Atomic/non-atomic accesses never conflict; atomic width and alignment are
      supported by the target and external participants.
- [ ] Ordering is sufficient for the data protected, not merely for the flag; each
      acquire has a corresponding release sequence and correct object/scope.
- [ ] Relaxed atomics are used only when ordering truly is irrelevant or supplied
      by another proven edge.
- [ ] Fences are paired with the correct operations and cannot be replaced by a
      compiler fence when hardware ordering is required.
- [ ] `volatile` is used for externally observable I/O access, not as a substitute
      for atomicity, mutual exclusion, or CPU/device memory barriers.
- [ ] Lock order is acyclic across error, callback, drop, logging, and interrupt
      paths; blocking operations do not occur in atomic/interrupt contexts.
- [ ] Condition variables/wakes use a predicate loop and cannot lose notifications.
- [ ] Sequence/refcount/ring counters handle wraparound and ABA/reuse explicitly.
- [ ] Progress does not depend on fairness or task/block scheduling not guaranteed
      by the runtime or GPU.
- [ ] Async futures remain correct when polled repeatedly, moved if `Unpin`, dropped
      at any await, timed out, or cancelled after starting external work.
- [ ] No lock/borrow/thread-local guard is held across `await` unless explicitly
      safe and intended; cancellation preserves invariants.
- [ ] Blocking or CPU/GPU-intensive work is not accidentally placed on a latency-
      sensitive async executor.

## `no_std`, firmware, and constrained targets

- [ ] The crate builds under every supported `no_std`/`alloc` feature combination;
      `std` does not leak through dependencies, tests, macros, or error types.
- [ ] Panic handler/strategy, allocation failure, OOM, and unwinding assumptions
      match the target.
- [ ] Stack, heap, static memory, code size, recursion, monomorphization, and large
      temporaries fit stated budgets in debug and release artifacts as applicable.
- [ ] Global initialization order and mutable statics are safe across cores,
      interrupts, boot stages, and reset.
- [ ] Critical sections actually mask or synchronize every possible actor and have
      bounded duration.
- [ ] Target atomics/features/instructions exist or have a correct fallback.
- [ ] Time/tick conversions, counter width, wraparound, clock changes, and busy-wait
      progress are handled.
- [ ] MMIO/DMA/hardware-specific points are reviewed with the
      [firmware checklist](gpu-firmware.md).

## Conditional compilation, build, and dependencies

- [ ] Review the effective code under each meaningful feature/cfg combination, not
      only the default; additive Cargo feature unification cannot create an invalid
      combination.
- [ ] If one semantic operation has separate target/feature implementations, map
      every source body to a test, proof, differential check, or shared executable
      definition that detects independent drift. A compile-only target job and a
      one-time identical binary comparison do not test future behavior.
- [ ] Mutation-test duplicated cfg branches when practical: remove or reorder one
      guard in only one branch and confirm a deterministic gate fails without
      refreshing source-digest allowlists as the sole response.
- [ ] Mutually exclusive backends/features fail clearly or compose correctly.
- [ ] `build.rs`, proc macros, generated bindings, link scripts, and environment-
      derived configuration are deterministic, scoped, and reviewed as executable
      supply-chain code.
- [ ] Target and feature cfg names are spelled/checked; fallback branches do not
      silently select a wrong architecture.
- [ ] MSRV and edition changes are intentional; public docs/tests compile at MSRV
      where required.
- [ ] New dependencies justify functionality, maintenance, license, provenance,
      transitive features, build scripts, native code, target support, and size.
- [ ] Dependency/default-feature changes do not enable networking, allocation,
      `std`, logging, unsafe backends, or incompatible versions unexpectedly.
- [ ] Lockfile/checksum/source changes match the manifest and policy; git/path
      dependencies are pinned and reproducible where required.

## Formal verification

- [ ] Inventory every new theorem, postcondition, refinement function, trusted
      declaration, and proof-excluded executable function; identify which runtime
      decision each obligation constrains.
- [ ] Distinguish structural or definitional lemmas from falsifiable executable
      refinement. A theorem that unfolds a datatype projection is useful type
      documentation but is not behavioral coverage of a protocol adapter.
- [ ] Keep the specification independent enough to detect implementation drift;
      do not count two functions generated from the same body as independent
      evidence unless a separate contract constrains their result.
- [ ] Search for verified consumers of new postconditions. An executable helper
      with a correct postcondition does not verify an unconnected caller that maps
      its result into errors, updates, effects, or hardware actions.
- [ ] Apply a plausible semantic mutation while holding the specification fixed,
      and a specification mutation while holding the implementation fixed. Record
      which proof or gate fails; if neither fails, narrow the claim.
- [ ] Treat `external_body`, assumptions, opaque/external type models, admitted
      axioms, and proof-disabled cfg branches as explicit trust boundaries rather
      than verified implementation.

## Tests and tools

Choose applicable commands; record exact toolchain, target, features, and results.
Do not claim coverage from a tool that cannot execute the hardware/FFI path.

- [ ] Format and compile: `cargo fmt --all -- --check`, then `cargo check`/`build`
      for workspace, targets, and features required by the repository.
- [ ] Lint: `cargo clippy --workspace --all-targets --all-features -- -D warnings`
      when that matches project policy; do not enable noisy restriction groups
      blindly.
- [ ] Test default, all-feature, no-default-feature, doctest, release, and target
      variants that represent supported configurations.
- [ ] Use feature-combination tooling when interactions matter; do not assume
      `--all-features` represents mutually exclusive production configurations.
- [ ] Run Miri on focused unsafe tests where supported, including alternative
      aliasing modes/seeds when useful; document unsupported syscalls/FFI/hardware.
- [ ] Run address/memory/thread/leak sanitizers on supported host targets and
      instrument relevant foreign code when required; note nightly/tool limits.
- [ ] Use Loom or an equivalent scheduler model for small synchronization
      protocols; use a model checker such as Kani where proof bounds are meaningful.
- [ ] Fuzz parsers, unsafe boundaries, descriptors, and state machines; keep the
      crashing/minimized input as a regression test.
- [ ] Use property and differential tests against a simpler oracle for arithmetic,
      serialization, protocols, and kernels.
- [ ] Inspect generated assembly/IR/layout/symbols when correctness depends on ABI,
      atomics, volatile access, target features, register use, or code generation.
- [ ] Run tests on real supported targets/hardware for behavior Miri, sanitizers,
      emulators, and host execution cannot model.

## Review completion evidence

The final report states:

- which checklist sections applied and who reviewed them;
- which targets/features/build modes were compiled or tested;
- which unsafe/FFI/concurrency boundaries were traced;
- tool findings and their limitations;
- specifications and repository invariants used;
- untested hardware/configurations and the risk they leave;
- required human owners for soundness, ABI, memory-model, or hardware claims.
