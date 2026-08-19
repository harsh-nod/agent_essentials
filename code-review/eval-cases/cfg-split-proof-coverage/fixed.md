# Synthetic Corrected Counterexample

The target and host call the same executable `decide` function. Its result has an
independent specification and a verified postcondition; changing a guard or error
priority without changing the specification fails verification. Structural
datatype lemmas are listed separately in the proof report.

The documented `check.sh` runs host tests and proof-free target compilation. CI
runs that same command and the proof job. A mutation test changes one decision
guard while holding the specification fixed and confirms verification fails.
