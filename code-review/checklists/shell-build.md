# Shell and Build/Release Interface Checklist

Use for shell, Make/CMake glue, linker wrappers, packaging, signing, firmware
artifact selection, and scripts embedded in CI. Review against the declared shell
and actual downstream tools; generic lint does not prove integration behavior.

## Interpreter and execution context

- [ ] Shebang, executable mode, shell dialect, minimum version, OS, and required
      utilities match every invocation site.
- [ ] Sourced and executed behavior are not confused; `$0`, `BASH_SOURCE`, return,
      exit, traps, options, and positional parameters behave in both contexts.
- [ ] Working directory is explicit or paths are anchored to a validated script or
      repository root; callers may invoke the script from another directory.
- [ ] Environment variables have one owner, documented units/format, safe defaults,
      validation, and no collision with common/system variables.
- [ ] Locale, timezone, umask, PATH, HOME-like state, temporary directories, and
      host tool versions cannot silently change a reproducible artifact.

## Expansion and control flow

- [ ] Parameter, command, and arithmetic expansions are quoted unless splitting or
      globbing is deliberate and bounded; arrays preserve argument boundaries.
- [ ] Empty, unset, whitespace, newline, leading-dash, glob, Unicode, and long path
      values cannot redirect options or combine/split arguments.
- [ ] `set -e`, `set -u`, `pipefail`, `&&`/`||`, conditions, negation, functions,
      command substitutions, and subshells propagate failures as intended.
- [ ] Pipeline status identifies the failing stage; logging helpers such as `tee`
      do not manufacture success.
- [ ] Loops do not consume a pipeline subshell when later state is required, and
      reads preserve backslashes/last lines as intended.
- [ ] Signals and early exits run safe, idempotent cleanup without hiding the
      original exit status or deleting another invocation's files.

## Tool interface contracts

- [ ] Every producer/consumer interface defines arguments, stdin, stdout, stderr,
      exit status, files, permissions, and whether diagnostic output is stable.
- [ ] Command substitution is used only when all captured stdout is the value. If
      a tool logs validation messages before a result, use a deterministic path,
      dedicated descriptor, structured output, or last-line parser with a contract.
- [ ] Parsers handle trailing newlines, multiple lines, warnings, progress output,
      localization, and empty success output without treating prose as a filename.
- [ ] A zero exit with missing/malformed output fails; a nonzero exit cannot be
      ignored because an expected file or stale stdout also exists.
- [ ] Tests use the real tool or a contract-faithful fake that emits realistic
      diagnostics, status, files, timing, and partial failures—not a path-only stub.
- [ ] Version/capability detection validates semantics instead of fragile help-text
      parsing when a machine-readable interface exists.

## Artifacts, linking, packaging, and signing

- [ ] Every artifact has a deterministic identity tied to source SHA, target,
      configuration, toolchain, and current invocation.
- [ ] Output directories are unique or cleaned safely; success checks cannot accept
      an older artifact after the current compiler/linker/package step failed.
- [ ] Temporary output is created safely and promoted atomically only after full
      validation; parallel jobs cannot overwrite or consume partial files.
- [ ] Linker scripts, archive/member order, symbols, sections, entry point, layout,
      permissions, and target architecture are checked on the final artifact.
- [ ] Packaging consumes the just-validated artifact rather than rediscovering a
      similarly named file; hashes/manifests cover what is actually shipped.
- [ ] Signing failures, wrong keys/roles, unsigned fallbacks, re-signing, and mixed
      metadata fail closed while preserving the supported recovery path.
- [ ] Backend/feature selectors validate exact allowed values, choose one path,
      expose the selected implementation, and test default, every supported value,
      invalid value, missing prerequisite, and rollback.

## Make, CMake, and build graph semantics

- [ ] Cache variables, normal variables, environment, options, presets, and command
      line values have deliberate precedence and validated string/boolean semantics.
- [ ] CMake lists/semicolons, generator expressions, quoting, platform paths, and
      single- versus multi-config generators preserve the intended arguments.
- [ ] Targets declare complete dependencies, inputs, outputs, byproducts, working
      directory, environment, depfiles, and terminal/resource requirements so clean,
      incremental, and parallel builds produce the same current artifact.
- [ ] Configure-time discovery is not mistaken for build-time availability; a tool,
      generated file, or selected backend cannot change without invalidating the
      owning configure/build step.
- [ ] Make recipes propagate shell failures, avoid timestamp/stamp false success,
      and remain correct under parallel execution and interrupted rebuilds.
- [ ] Install/package/export behavior consumes the selected target/configuration and
      does not omit, mix, or rename artifacts relative to build-tree tests.

## Filesystem, security, and cleanup

- [ ] Paths crossing a trust boundary reject traversal, option injection, unsafe
      symlinks, device files, FIFOs, and TOCTOU where relevant.
- [ ] Temporary files/directories use secure creation and least permissions; names
      are not predictable in shared locations.
- [ ] Recursive/destructive operations resolve and validate an exact narrow target;
      they do not depend on empty variables, broad roots, unsafe globs, or `eval`.
- [ ] Secrets do not appear in command lines, tracing, stdout/stderr, logs, caches,
      artifacts, or inherited environments; debug modes do not expose them.
- [ ] Downloaded tools/artifacts are authenticated and pinned according to policy;
      archive extraction cannot escape the destination.

## Verification

- [ ] Run syntax and configured lint (`bash -n`, ShellCheck, project equivalents)
      for the declared dialect, while separately testing behavioral contracts.
- [ ] Exercise success and each prerequisite/failure boundary in a fresh directory,
      a path containing spaces, and a non-default caller working directory.
- [ ] Exercise real multi-line stdout/stderr, warnings, partial files, stale files,
      concurrent invocations, signal interruption, and downstream rejection.
- [ ] Compare artifact hashes/layout/manifests and package inputs across all selected
      backends/configurations; record exact tools and versions.
