# C and C++ Low-level Review Checklist

Use for C/C++, headers, native firmware, host interfaces, and generated native
code. Apply GPU/firmware, concurrency, security, and architecture checklists for
the relevant domain. The exact language standard, compiler, flags, ABI, and target
are part of the contract.

## Build modes and effective program

- [ ] Record C/C++ standard, compiler/version, target/ABI, optimization, exceptions,
      RTTI, sanitizers, warnings, LTO, packing, defines, and freestanding/hosted mode.
- [ ] Inspect every meaningful preprocessor/feature/target path; default compilation
      does not establish correctness of mutually exclusive backends.
- [ ] Headers are self-contained, declarations match definitions, inline/ODR rules
      hold, and C/C++ linkage and visibility are deliberate.
- [ ] Generated code, compiler extensions, pragmas, attributes, linker scripts, and
      weak/section symbols are supported and preserved in final artifacts.

## Memory, lifetime, and undefined behavior

- [ ] Bounds and allocation arithmetic are checked before pointer/index operations;
      zero, maximum, overflow, negative-to-unsigned, and flexible-array cases work.
- [ ] Every object is initialized before read and remains alive, correctly aligned,
      and of a permitted effective/dynamic type for each access.
- [ ] Ownership and allocator/deallocator pairs are explicit across success, error,
      early return, exception, callback, thread, FFI, and hardware completion.
- [ ] Pointer provenance, one-past rules, aliasing, restrict assumptions, unions,
      casts, placement construction, and manual destruction meet the language rule.
- [ ] `memcpy`/`memmove`/`memset`, string functions, format strings, and variadic
      calls use correct sizes/types and preserve object validity and termination.
- [ ] Iterators, references, views/spans, callbacks, and captures cannot outlive or
      be invalidated by mutation, reallocation, teardown, reset, or async work.

## Integers, enums, and representation

- [ ] Signed overflow, promotions, comparison conversions, narrowing, shifts,
      negation, division edge cases, bit masks, and pointer-size truncation are safe.
- [ ] Units and widths use checked conversions at boundaries; counters, time, ring
      indices, offsets, addresses, and lengths handle wrap deliberately.
- [ ] Struct/union layout, padding, packing, alignment, endianness, bit fields,
      enums, `bool`, and calling convention match every ABI/wire/hardware consumer.
- [ ] Serialized/hashed/signed bytes are canonical and never include uninitialized
      padding or compiler-dependent representation.

## Errors, cleanup, and runtime behavior

- [ ] Return values, `errno`, status enums, out-parameters, exceptions, `noexcept`,
      panic/abort, and logging distinguish failure from valid empty/zero results.
- [ ] Partial initialization unwinds in reverse order and is safe under retries,
      cancellation, signals/interrupts, `longjmp`, exceptions, and process teardown.
- [ ] Assertions are not the sole validation for supported or untrusted inputs and
      release builds do not remove required side effects.
- [ ] Recursion, stack frames, heap, static initialization/destruction, logging, and
      allocation fit constrained firmware and failure-path budgets.

## Concurrency, volatile, and hardware

- [ ] Shared accesses use the correct language atomics/locks and happens-before;
      data races are not justified by timing or ordinary `volatile`.
- [ ] Atomic type width, alignment, lock freedom, order, and scope exist on every
      target and interoperate correctly across C/C++/Rust/device boundaries.
- [ ] MMIO/DMA uses platform primitives, barriers, cache maintenance, ownership,
      and lifetimes; compiler volatile alone is not a hardware synchronization rule.
- [ ] Callback, interrupt, signal, thread, and teardown interactions avoid reentry,
      use-after-free, deadlock, lost wakeup, and destruction while active.

## APIs, FFI, and compatibility

- [ ] Ownership, nullability, lengths, aliasing, mutability, thread affinity,
      lifetime, callbacks, allocator, errors, and unwind rules are documented and
      enforced on both sides of each boundary.
- [ ] ABI symbols, names, visibility, layout, alignment, enum widths, calling
      convention, exception/unwind policy, and compiler runtime are compatible.
- [ ] Public changes define source, binary, wire, firmware, and mixed-version
      compatibility plus rollout/rollback.
- [ ] Macros evaluate arguments safely, preserve types/control flow, and do not
      create name, precedence, or side-effect surprises.

## Verification

- [ ] Compile all supported targets/configurations with strict warnings and project
      static analysis; inspect generated warnings rather than duplicating them.
- [ ] Run unit/property/fuzz/differential tests with debug/release, zero/max/boundary
      inputs, allocation/error injection, and alternate feature paths.
- [ ] Use ASan/UBSan/MSan/TSan or target-appropriate equivalents where meaningful;
      record unsupported firmware/hardware gaps rather than claiming coverage.
- [ ] Verify ABI/layout/symbols/disassembly and final linked artifact, not only
      individual objects; test real cross-language callers and allocators.
