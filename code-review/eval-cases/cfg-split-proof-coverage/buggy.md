# Synthetic PR Context

The PR extracts a verified transition helper without changing target behavior.
The author reports an identical target binary at the reviewed head. The supported
target is `riscv64`; normal developer checks run on the host.

```diff
-fn step(state: State, event: Event) -> Result<State, Error> {
-    if state.busy { return Err(Error::Busy); }
-    Ok(state.connected())
-}
+#[cfg(target_arch = "riscv64")]
+fn step(state: State, event: Event) -> Result<State, Error> {
+    if state.busy { return Err(Error::Busy); }
+    Ok(state.connected())
+}
+
+#[cfg(not(target_arch = "riscv64"))]
+fn step(state: State, event: Event) -> Result<State, Error> {
+    decide(state, event)
+}
```

The new host tests exhaustively exercise `decide`; CI cross-compiles the target
body but does not execute it. The documented `check.sh` runs host tests only.

The proof crate also adds `update_after(Rejected(_)) = None` and an empty lemma
whose postcondition repeats that definition. The protocol `decide` adapter is
outside the verified block, while the design document counts the lemma as one of
three new protocol proof obligations.
