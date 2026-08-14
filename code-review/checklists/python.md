# Python Tooling Review Checklist

Use for executable Python, validators, generators, parsers, automation, and test
harnesses. Apply the domain checklist as well when the script interprets firmware,
hardware, security, ABI, or release artifacts.

## Runtime and dependencies

- [ ] Supported Python implementations/versions, entry point, invocation directory,
      packaging, dependency bounds, and optional extras match CI and users.
- [ ] Import-time side effects, mutable module state, environment discovery, and
      plugin loading cannot make results order-dependent or execute untrusted code.
- [ ] New dependencies justify transitive code, licenses, build hooks, native ABI,
      network access, target availability, and reproducible resolution.
- [ ] Type annotations and static analysis cover important boundaries, but runtime
      validation still protects inputs crossing trust or serialization boundaries.

## Inputs, parsing, and values

- [ ] Empty, missing, malformed, truncated, duplicated, oversized, deeply nested,
      differently encoded, and extra-field inputs have explicit behavior.
- [ ] Integers define signedness, range, units, base, width, endianness, overflow,
      offsets, and length relationships before allocation or slicing.
- [ ] Binary parsing validates total size and each offset/length before unpacking;
      alignment/padding/version/reserved fields match the external contract.
- [ ] Text handling states encoding and newline policy and does not confuse bytes,
      Unicode code points, display width, or locale-dependent conversions.
- [ ] Collection mutation, aliasing, default arguments, dataclass defaults, iterator
      exhaustion, truthiness, and equality/identity have intended semantics.
- [ ] Floating-point, decimal, time, path, and enum values preserve required
      precision, timezone, normalization, and unknown-value behavior.

## Errors, resources, and subprocesses

- [ ] Expected failures use stable exception/exit contracts; broad catches do not
      convert programming errors, cancellation, or security failures into success.
- [ ] Tracebacks and diagnostics preserve actionable causes without secrets; CLI
      errors go to the correct stream and use documented exit codes.
- [ ] Files, mappings, sockets, processes, pools, and temporary resources close on
      success, exception, signal, timeout, and cancellation.
- [ ] Subprocess arguments are arrays unless a reviewed shell program is intended;
      environment, working directory, stdin/stdout/stderr, timeout, encoding, and
      return-code handling match the real command contract.
- [ ] Captured output is parsed as structured data only when the producer guarantees
      it; diagnostic prose cannot be mistaken for a path, hash, count, or status.
- [ ] Parallel/asynchronous code defines shared-state ownership, cancellation,
      ordering, exception aggregation, process start method, and cleanup.

## Files and generated output

- [ ] Paths are resolved relative to an explicit root and validate traversal,
      symlinks, special files, permissions, and race assumptions where relevant.
- [ ] Writes use a same-filesystem temporary plus flush/fsync/atomic replace when
      readers must never observe partial state.
- [ ] Failed generation removes or quarantines incomplete output and cannot leave a
      stale file that a later step attributes to the current invocation.
- [ ] Generated output is deterministic across hash seeds, locale, time, directory
      order, dependency versions, and supported platforms, or variation is explicit.
- [ ] Serialization has versioning, canonicalization if signed/hashed, unknown-field
      behavior, and compatibility tests with real consumers.

## Security and resilience

- [ ] Avoid unsafe deserialization, dynamic `eval`/`exec`, shell interpolation,
      format injection, regex denial of service, and archive/path traversal.
- [ ] Input sizes, recursion, decompression, retries, logging, and concurrency have
      bounds before expensive work or allocation.
- [ ] Temporary files, credentials, tokens, customer data, firmware metadata, and
      addresses have least access and safe logging/lifetime behavior.
- [ ] Network/download behavior is explicit, authenticated, timeout-bounded, and
      unavailable in deterministic/offline modes where required.

## Verification

- [ ] Run project formatter/linter/type checks and tests on every supported runtime;
      investigate causes rather than posting raw tool output.
- [ ] Add table/property/fuzz tests for valid boundaries and malformed families,
      including negative exit status and absence of stale/partial artifacts.
- [ ] Test subprocesses with a real tool or contract-faithful fake containing
      warnings, multiline streams, nonzero status, timeouts, and partial files.
- [ ] Test from a clean directory, a path with spaces, alternate locale/timezone,
      randomized hash seed, and relevant platform/architecture.
