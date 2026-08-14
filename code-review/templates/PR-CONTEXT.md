# PR Review Context

Complete this before agent review. Write `UNKNOWN` rather than guessing. Remove
secrets and use stable links or checked-in specifications where possible.

## Identity and immutable target

- Repository:
- PR/issue/design link:
- Author/owner:
- Human domain reviewers:
- Base branch:
- Base SHA:
- Head SHA:
- Merge-base SHA:
- Review lane: Quick | Standard | High-risk
- Review date:

## Intent

- Problem being solved:
- User/system-visible outcome:
- Explicit non-goals:
- Success criteria:
- Alternatives considered and why rejected:
- Incident/CVE/customer context, if any:

## Change map

- Components/crates/files changed:
- Changed executable/configuration/documentation languages and embedded languages:
- Generated/vendor files and reviewed source/generator instead:
- Data/state flow before:
- Data/state flow after:
- New or changed invariants:
- New `unsafe`, FFI, inline assembly, concurrency, MMIO, DMA, GPU, or firmware
  boundaries:
- Public API/ABI, wire, on-disk, firmware, kernel-launch, register, log/metric, or
  configuration contracts changed:
- Generated code/artifacts and source generator:
- Dependencies/features/toolchains changed:

## Required reviewer manifest

Inventory every semantic file class using `language-routing.md`. `Covered by`
must name one persona; do not write only “general review.”

| Changed file class/language | Risk-bearing behavior | Required persona | Covered by provider/model | Status/coverage limit |
| --- | --- | --- | --- | --- |
| | | | | planned/running/complete/missing |

## Supported matrix

| Dimension | Supported/relevant values | Tested values | Owner for gaps |
| --- | --- | --- | --- |
| Rust toolchain/MSRV/edition | | | |
| Targets and pointer widths | | | |
| Endianness | | | |
| Cargo features / `std` / `no_std` | | | |
| Panic/allocator/build mode | | | |
| OS/driver/runtime | | | |
| GPU vendor/family/generation/stepping | | | |
| Firmware/host protocol versions | | | |
| Board/platform/power modes | | | |

## Hardware and numerical contract

- Authoritative ISA/register/protocol/ABI/errata documents and revisions:
- Required capabilities and detection/fallback:
- Shapes, strides, layouts, dtypes, alignment, aliasing allowed:
- Numerical oracle, tolerance/error model, exceptional values, determinism:
- Timing/watchdog/latency/throughput targets:
- Stack/heap/static/code/register/local-memory/occupancy/power budgets:
- Cache coherency, memory ordering/scope, and synchronization assumptions:

## Trust and safety

- Assets to protect:
- Trusted actors/inputs:
- Untrusted actors/inputs:
- Privilege/isolation/DMA/IOMMU boundaries:
- Authentication/signing/key/anti-rollback behavior:
- Debug/manufacturing/recovery paths:
- Confidentiality/integrity/availability priorities and fail-open/closed policy:

## Failure, compatibility, and rollout

- Expected error and partial-failure behavior:
- Cancellation/timeout/retry/idempotency:
- Boot/reset/power-loss/surprise-removal behavior:
- Recovery and rollback:
- Old/new host, firmware, API, and stored-data compatibility:
- Deployment/update order and compatibility window:
- Feature flag/kill switch and owner/expiry:
- Observability, alert, dump, and runbook changes:

## Evidence already collected

Record exact commands, environment/hardware, result, and artifact link. Do not write
only “CI passed.”

| Check | Command/configuration | Environment/hardware | Result/artifact |
| --- | --- | --- | --- |
| Format/lint | | | |
| Build/check | | | |
| Unit/integration/doc | | | |
| Feature/target matrix | | | |
| Miri/sanitizer/model/fuzz | | | |
| GPU differential/memory/race | | | |
| Simulator/emulator/HIL/fault injection | | | |
| Performance/resource/binary size | | | |
| Dependency/license/security policy | | | |
| ABI/layout/generated artifact | | | |

## Known limitations and requested focus

- Known pre-existing failures or debt:
- Untested targets/hardware/features and why:
- Specifications or proprietary context unavailable to agents:
- Accepted risks with owner, issue, and expiry:
- Questions the reviewers must answer:
- Areas explicitly out of scope and why:
