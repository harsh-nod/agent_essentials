# Primary Sources and Maintenance Notes

Last checked: **2026-08-13**.

The playbook is a team policy, not a restatement of any one vendor's guidance.
These sources support the time-sensitive product instructions and the language,
GPU, and firmware review concerns. Always use the specification for the actual
Rust toolchain, ABI, GPU generation, firmware protocol, and silicon stepping.

## Agent products and models

### OpenAI Codex

- [Codex code review](https://learn.chatgpt.com/docs/code-review) documents the
  dedicated `/review` scopes, prioritized read-only findings, custom instructions,
  and the `review_model` setting.
- [Custom Code Review rules for Codex](https://learn.chatgpt.com/blog/custom-code-review-rules-for-codex)
  explains scoped `AGENTS.md` review rules, recommends consequential and non-obvious
  invariants with a safe path, and recommends keeping deterministic checks in CI.
- [Current OpenAI model guidance](https://developers.openai.com/api/docs/guides/latest-model)
  describes the GPT-5.6 Sol/Terra/Luna capability/cost tiers, reasoning effort,
  pro mode, and multi-agent support.

### Anthropic Claude

- [Claude Code Review](https://code.claude.com/docs/en/code-review) documents the
  managed multi-agent review and verification pipeline, `CLAUDE.md` versus
  `REVIEW.md`, severity/noise tuning, and the local/background review flow. Product
  availability, pricing, effort behavior, and which instruction files apply can
  change; verify them before rollout.
- [Run agents in parallel](https://code.claude.com/docs/en/agents) distinguishes
  isolated subagents, agent view, agent teams, and scripted cross-check workflows.
- [Choosing a Claude model](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model)
  describes current capability, speed, cost, effort, and coding/agentic model tiers.

## Rust language and toolchain

- [Behavior considered undefined — Rust Reference](https://doc.rust-lang.org/stable/reference/behavior-considered-undefined.html)
  is the primary starting point for unsafe-code obligations. It explicitly notes
  that `unsafe` does not relax the prohibition on undefined behavior.
- [Rustonomicon](https://doc.rust-lang.org/stable/nomicon/) covers unsafe Rust,
  ownership, layout, concurrency, FFI, and other advanced topics. It is explanatory;
  use the Reference and relevant ABI specifications for authoritative decisions.
- [`read_volatile` documentation](https://doc.rust-lang.org/core/ptr/fn.read_volatile.html)
  distinguishes I/O volatility from concurrency. Volatile access does not make
  concurrent ordinary memory access atomic or synchronized.
- [Miri](https://github.com/rust-lang/miri) detects many classes of undefined
  behavior in executable Rust tests but does not cover all language behavior,
  external hardware, or every FFI interaction.
- [Rust sanitizer support](https://doc.rust-lang.org/beta/unstable-book/compiler-flags/sanitizer.html)
  documents target/toolchain limitations and incomplete-instrumentation caveats.
- [Clippy lint documentation](https://rust-lang.github.io/rust-clippy/master/)
  distinguishes correctness, suspicious, style, complexity, performance, and other
  lint groups; teams should enable lints intentionally rather than treating every
  optional restriction as review policy.
- [Cargo features](https://doc.rust-lang.org/cargo/reference/features.html) and
  [SemVer compatibility](https://doc.rust-lang.org/cargo/reference/semver.html)
  support the feature-composition and public-API portions of the checklist.
- [The Embedded Rust Book](https://docs.rust-embedded.org/book/) is a useful primary
  project reference for `no_std`, startup, interrupts, and embedded constraints.

## Optional Rust verification tools

These tools complement rather than replace reasoning, specifications, target tests,
and human review. Confirm that they support the relevant toolchain and target.

- [Loom](https://github.com/tokio-rs/loom) explores permutations of small concurrent
  Rust programs under a model.
- [Kani Rust Verifier](https://model-checking.github.io/kani/) performs bounded
  model checking for supported Rust code and proof harnesses.
- [The Rust Fuzz Book / `cargo-fuzz`](https://rust-fuzz.github.io/book/) covers
  libFuzzer-based Rust fuzzing.
- [`cargo-hack`](https://github.com/taiki-e/cargo-hack) helps exercise Cargo feature
  combinations.
- [`cargo-deny`](https://embarkstudios.github.io/cargo-deny/) checks dependency
  advisories, licenses, bans, and sources according to repository policy.

## GPU programming and performance

Use the actual programming model; host and device semantics are not automatically
portable between CUDA, HIP, Vulkan/SPIR-V, OpenCL, Metal, or a Rust GPU toolchain.

- [CUDA Programming Guide](https://docs.nvidia.com/cuda/cuda-programming-guide/)
  is NVIDIA's comprehensive programming-model reference, including asynchronous
  execution, memory spaces, synchronization, execution, and floating point.
- [CUDA C++ memory model](https://docs.nvidia.com/cuda/cuda-programming-guide/05-appendices/cuda-cpp-memory-model.html)
  details thread scopes, atomicity, data races, and scope-sensitive synchronization.
- [HIP performance guidelines](https://rocm.docs.amd.com/projects/HIP/en/latest/how-to/performance_guidelines.html)
  covers AMD HIP execution, synchronization, memory throughput, occupancy, and
  profiling considerations.
- [HIP C++ language extensions](https://rocm.docs.amd.com/projects/HIP/en/latest/how-to/hip_cpp_language_extensions.html)
  documents HIP kernel language and built-ins; pair it with target ISA and runtime
  documentation for architecture-specific behavior.
- [Vulkan memory model](https://registry.khronos.org/vulkan/specs/latest/html/vkspec.html#memory-model)
  is the Khronos specification entry point when Rust generates or launches SPIR-V
  under Vulkan.

## Firmware, MMIO, DMA, and resilience

- [Rust `read_volatile`](https://doc.rust-lang.org/core/ptr/fn.read_volatile.html)
  defines compiler-level volatile behavior and safety, but the platform/device
  specification still defines address validity and I/O ordering.
- [Linux bus-independent device access](https://www.kernel.org/doc/html/latest/driver-api/device-io.html)
  documents MMIO mappings/accessors and ordering behavior for Linux drivers.
- [Linux kernel memory barriers](https://www.kernel.org/doc/html/latest/core-api/wrappers/memory-barriers.html)
  describes CPU, I/O, DMA, interrupt, and cache-coherency ordering concerns. It
  explicitly identifies itself as a guide rather than a hardware specification.
- [Linux DMA API](https://www.kernel.org/doc/html/latest/core-api/dma-api.html) covers
  mapping, cache-line, direction, synchronization, and lifetime obligations.
- [NIST SP 800-193: Platform Firmware Resiliency Guidelines](https://csrc.nist.gov/pubs/sp/800/193/final)
  frames firmware resilience around protecting against unauthorized changes,
  detecting changes, and recovering rapidly and securely.

## How to maintain this playbook

Review this file and the model assignments at least quarterly and whenever a model,
agent product, compiler, GPU target, firmware protocol, or security policy changes.

For product/model updates:

1. read the current official source, not an old comparison blog;
2. rerun the team eval in `personas-and-models.md` on held-out PRs;
3. compare weighted Major recall, Major precision, unique confirmed findings,
   unsupported claims, latency, and cost;
4. update the dated assignment table and note the evidence in the commit/ADR.

For checklist updates, convert escaped defects and repeated false positives into
small, scoped invariants. Prefer deterministic CI for mechanically enforceable
rules and keep agent instructions for judgment that requires context.
