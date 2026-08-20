# Synthetic PR Context

The PR adds `check-routing.py`, a branch-owned Python source checker. It compares
normalized Rust fragments and is called from `check.sh`. Unit tests import the
module and call `validate()` with semantic mutations.

The checker searches both raw source and a comment-masked copy for `include`,
`macro_rules!`, and item macros. Therefore a doc comment saying "include the
identifier" fails. No test invokes `check-routing.py` as a process. Deleting the
checker, its shell invocation, and its unit test reduces the test count but does
not fail another policy gate.

The checked Rust helper exports this macro:

```rust
macro_rules! admission {
    ($busy:expr, $reject:block, $accept:block) => {{
        if $busy $reject
        $accept
    }};
}

macro_rules! payload {
    () => { QueueState { phase: Phase::Ready } };
}
```

Callers can supply a non-diverging rejection block, and `QueueState`/`Phase`
resolve at the expansion site. The PR records one archive size and SHA-256 as a
qualification fact, but does not record the archive tool or producer environment.
Another host reproduces base/head byte equality while producing a different
absolute archive digest. Its comparison CLI also accepts the same archive path in
both the base and candidate roles.
