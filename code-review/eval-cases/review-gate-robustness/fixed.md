# Synthetic Corrected Counterexample

The checker scans comment-masked tokens and has paired tests: semantic mutations
fail while comment, string, and whitespace controls pass. Tests invoke the real
CLI and assert success/failure exit codes, stderr diagnostics, missing files, and
invalid UTF-8 behavior. A trusted-base workflow or digest-bound manifest detects
removal of the checker, its invocation, or its tests.

Direct-attribute delimiter matching uses a length-preserving view with Rust
strings, raw strings, byte strings, and character literals masked, while exact
attribute comparison slices a comments-only view. A rebound-digest regression
test applies `cfg(any())` plus `cfg_attr(any(), doc = "]")` to an otherwise
unreferenced required proof and requires the gate to reject it.

The admission macro owns the rejection order and returns a closed result code;
callers supply only state predicates. Payload paths use `$crate::QueueState` and
`$crate::Phase`, with a call-site shadowing regression test.

Qualification states base/head byte equality as the load-bearing result. Any
absolute archive size/digest is labeled with the producing toolchain and archive
tool environment. The comparison rejects path/inode aliases and binds each input
to its separate build provenance.
