# Synthetic Corrected Counterexample

The checker scans comment-masked tokens and has paired tests: semantic mutations
fail while comment, string, and whitespace controls pass. Tests invoke the real
CLI and assert success/failure exit codes, stderr diagnostics, missing files, and
invalid UTF-8 behavior. A trusted-base workflow or digest-bound manifest detects
removal of the checker, its invocation, or its tests.

The admission macro owns the rejection order and returns a closed result code;
callers supply only state predicates. Payload paths use `$crate::QueueState` and
`$crate::Phase`, with a call-site shadowing regression test.

Qualification states base/head byte equality as the load-bearing result. Any
absolute archive size/digest is labeled with the producing toolchain and archive
tool environment.
