# GPU Kernel Review Checklist

Apply this to Rust GPU code and to CUDA, HIP, SPIR-V, shader, or DSL kernels called
from Rust. Use the actual language, runtime, compiler, ISA, and device-generation
specifications. CUDA/HIP terms below are illustrative; similar words do not imply
identical semantics across vendors.

## Establish the execution contract

- [ ] Record supported GPU vendors, architectures/generations, driver/runtime and
      compiler versions, subgroup/wave/warp sizes, and required capabilities.
- [ ] Record tensor/buffer shapes, strides, layouts, dtypes, alignment, aliasing,
      residency, and ownership permitted by the host API.
- [ ] Record launch grid/workgroup/block dimensions, dynamic local/shared memory,
      stream/queue, synchronization, and completion/lifetime contract.
- [ ] Identify the simple mathematical/reference result, allowed numerical error,
      determinism requirement, and exceptional-value behavior.
- [ ] Distinguish correctness requirements from performance targets and define the
      benchmark hardware and distributions.

## Indexing, bounds, and geometry

- [ ] Prove global, group/block, local/thread, lane, tile, vector, batch, and
      multidimensional index formulas for every supported dimension.
- [ ] Check arithmetic cannot overflow before the bounds check, including products
      of dimensions, strides, element sizes, and byte offsets.
- [ ] Check zero-sized launches/inputs and sizes `1`, odd prime, just below/above a
      tile, and not divisible by block, wave, vector, or unroll width.
- [ ] Check the final partial tile/wave/vector and masked lanes neither access nor
      contribute invalid elements.
- [ ] Check signed/unsigned width and host/device type agreement for dimensions,
      strides, offsets, and loop counters.
- [ ] Check flatten/unflatten order, transposition, broadcasting, negative/zero
      strides if allowed, and non-contiguous views.
- [ ] Check grid-stride loops for progress, overflow, duplicate work, and complete
      coverage at maximum launch dimensions.
- [ ] Check launch limits and device capability queries; do not assume requested
      workgroup, shared memory, registers, or grid dimensions are supported.

## Control flow and synchronization

- [ ] Every required workgroup/block barrier is reached by all participating
      threads in compatible control flow; early returns and bounds guards do not
      make the barrier divergent.
- [ ] Subgroup barriers/votes/shuffles use a correct active mask and only read
      values from participating, initialized lanes.
- [ ] No correctness dependency assumes lockstep execution, a fixed wave/warp size,
      implicit reconvergence, or scheduling order unless guaranteed for every
      target and encoded as a requirement.
- [ ] Cross-workgroup/block communication uses a supported mechanism. Ordinary
      barriers do not synchronize independent blocks, which may run in any order
      or serially.
- [ ] Cooperative/cluster/grid synchronization checks launch eligibility,
      residency constraints, and fallback/error behavior.
- [ ] Spin waits and device locks cannot deadlock because a producer block is not
      resident; progress and fairness assumptions are documented.
- [ ] Producer/consumer protocols pair memory visibility with execution
      synchronization; a barrier alone may not establish the required scope/order.
- [ ] Async copies/pipelines wait before consumption and before source/destination
      reuse; stage indices and in-flight limits are correct for partial tiles.

## Memory model and races

- [ ] Classify every buffer/access by memory space and actors: lane/thread,
      subgroup, workgroup/block, device, peer device, and host.
- [ ] Check read/write and write/write overlap for all indices and allowed aliases;
      an apparently unique per-thread output may collide through stride/broadcast.
- [ ] Check atomic width, alignment, operation support, memory order, and scope
      include every producer and consumer.
- [ ] Check mixed atomic/non-atomic access, atomics through differently scoped
      objects, and mismatched host/device atomic domains.
- [ ] Check fences order the intended memory space and are paired with the correct
      publication/observation operations.
- [ ] Check local/shared memory allocation, initialization, lifetime, reuse, and
      double buffering across every iteration and participating lane.
- [ ] Check host/device and peer visibility for mapped, managed/unified, pinned,
      coherent, and non-coherent memory; record required flush/invalidate/sync.
- [ ] Check stream/queue/event dependencies across launches and copies. Same-stream
      ordering must not be assumed for different streams without an event/edge.
- [ ] Check buffer lifetime extends through asynchronous completion and error paths;
      host mutation/free/unmap/reuse cannot race with device work.
- [ ] Check texture/image/surface access coordinates, formats, normalized values,
      address modes, and read/write ordering.

## Layout, ABI, and compilation

- [ ] Host and device agree on parameter order, widths, signedness, alignment,
      padding, `repr`, pointer address space, endianness, and boolean/enum encoding.
- [ ] Struct/vector loads are actually aligned for all offsets or use an explicitly
      supported unaligned path.
- [ ] Kernel symbol, specialization constants, target features, device libraries,
      and link-time code match the intended architecture.
- [ ] Compile-time constants and generated variants cover every runtime-dispatched
      case, with a safe fallback for unknown/new devices.
- [ ] Runtime capability detection cannot select a kernel compiled for unsupported
      instructions, subgroup width, shared memory, or numerical mode.
- [ ] Compiler flags for fast math, contraction, reassociation, denormals, rounding,
      debug, and optimization match the numerical contract.
- [ ] Inline device assembly has correct operands, clobbers, predicates, barriers,
      address spaces, architecture guards, and fallback.

## Numerical correctness

- [ ] Define reference precision and compare using an error model appropriate to
      scale and operation, not a single unexplained epsilon.
- [ ] Check intermediate overflow/underflow, integer accumulation width, conversion
      and rounding, saturation/wrap, and fused versus unfused operations.
- [ ] Check NaN, Inf, signed zero, subnormal/flush-to-zero, min/max, comparison, and
      transcendental behavior required by callers.
- [ ] Check reductions/scans for non-associativity, nondeterminism, compensation,
      identity values, inactive lanes, and empty inputs.
- [ ] Check mixed precision and quantization scale/zero-point/range, especially
      accumulation and dequantization order.
- [ ] Check atomic floating-point accumulation and race-free nondeterminism meet the
      reproducibility/tolerance contract.
- [ ] Compare across optimization modes and supported GPU generations where
      compiler lowering or native instruction precision varies.

## Host integration and errors

- [ ] Validate all launch arguments before dispatch: device, pointers, residency,
      sizes, strides, alignment, format, aliasing, and grid/shared-memory limits.
- [ ] Check asynchronous launch errors and later execution errors are observed at a
      defined synchronization point and attributed to the right operation.
- [ ] Check graph/capture, callbacks, events, and stream semantics under the modes
      the product uses; forbidden allocation/synchronization during capture is not
      introduced.
- [ ] Check multi-device context ownership, peer access, address/device association,
      topology, and cleanup on partial initialization.
- [ ] Check cancellation/timeout semantics: returning to the caller must not imply
      device work stopped if it can still access buffers or publish output.
- [ ] Check fallback path matches kernel semantics, error behavior, and layout.

## Performance and resource use

Do not trade correctness for performance, and do not assert regressions without a
measurement or sufficiently precise resource/cost model.

- [ ] Measure end-to-end and kernel-only time with synchronization, warm-up,
      repetitions, variance, clocks, and power state controlled/documented.
- [ ] Benchmark representative and adversarial shapes, not only aligned large
      tensors; report tail latency where relevant.
- [ ] Inspect global-memory access coalescing, transaction width, alignment,
      locality, cache behavior, and unnecessary transfers/materialization.
- [ ] Inspect local/shared-memory bank conflicts, padding, footprint, and reuse.
- [ ] Inspect register pressure, spills/local memory, occupancy, active waves/warps,
      workgroup size, and launch-bound assumptions on each target generation.
- [ ] Inspect divergence, predication, instruction mix, dependency chains, atomics,
      fences, and synchronization contention.
- [ ] Account for launch count, host overhead, compilation/specialization cache,
      allocation, copies, PCIe/interconnect traffic, and synchronization.
- [ ] Check tiling, unrolling, vectorization, fusion, and prefetching improve the
      actual bottleneck and do not harm small/edge inputs or other architectures.
- [ ] Confirm performance guardrails have stable baselines and account for noise;
      avoid brittle pass/fail thresholds without repetition/statistics.

## Verification matrix

- [ ] Differential test against a simple CPU/high-precision/reference
      implementation over random and structured cases.
- [ ] Cover zero/one, odd primes, boundary tiles, maximum dimensions, unusual
      strides/layouts, valid aliases, misalignment if supported, and all dtypes.
- [ ] Cover NaN/Inf/subnormal/signed-zero/extreme magnitudes and cancellation-prone
      values where numerical behavior matters.
- [ ] Stress repeated/concurrent launches, multiple streams/queues, multiple
      devices, buffer reuse, and host/device overlap.
- [ ] Run the vendor's memory/race/synchronization checker where available and
      understand its blind spots.
- [ ] Run on each materially different supported architecture or document gaps;
      simulator and one GPU model cannot establish portable correctness.
- [ ] Inspect profiler counters and disassembly when performance or instruction
      selection is part of the PR claim.
- [ ] Preserve minimized failing shapes/seeds and exact device/compiler/runtime
      details in regression tests.

## Automatic Major triggers when confirmed

- supported input can cause out-of-bounds or illegal device access;
- data race, insufficient atomic scope/order, or divergent barrier can corrupt or
  hang execution;
- wrong result exceeds the declared numerical contract;
- host/device ABI mismatch or asynchronous lifetime error can corrupt memory;
- unsupported hardware is selected without safe detection/fallback;
- a hard watchdog, memory, latency, or safety budget is violated in production.
