# Synthetic PR Context

The PR proves an executable transition table equal to `exact_result`, a `spec fn`
that repeats the same three accepted rows and six rejected rows. A second integer
relation is checked only at values produced by `phase_code` and `input_code`.
Nothing proves that the integer relation rejects values outside those images, and
two acknowledgement variants may map to the same integer if the table, spec, and
encoder are edited together.

An outer `install_and_project` helper has quantified frame postconditions but no
verified caller. Deleting one frame conjunct leaves the proof count and all tests
unchanged. The source checker pins the whole file but does not bind the outer
contract after its digest is deliberately reviewed and refreshed.

The normal gate contains a raw substring test for this command:

```text
cargo test -p protocol --no-default-features
```

The command can be commented out while `cargo test --workspace` remains green,
because feature unification selects the default proof-enabled implementation.

Archive qualification requires one hardcoded SHA-256. Base and candidate are
byte-identical on every builder, but `-Z build-std` embeds absolute sysroot paths,
so an independent builder with a different HOME rejects both artifacts against
the hardcoded digest.
