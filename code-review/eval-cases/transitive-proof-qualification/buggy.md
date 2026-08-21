# Synthetic PR Context

The PR claims a selected-state update is refined and qualified. A source checker
pins the top-level planner function, but that function calls an unpinned installer.
The installer always writes queue zero. Tests select only queue zero, so rebinding
the reviewed planner digest still leaves every gate green.

The installer has a complete frame postcondition, but no verified caller consumes
any clause. Deleting the whole postcondition changes neither proof success nor the
reported aggregate obligation count.

The build gate searches raw shell text for the no-default test command. Commenting
out that line satisfies the test while feature-unified workspace tests execute only
the proof-enabled body.

Qualification admits one hardcoded archive digest. Absolute build paths make that
digest producer-layout-dependent even though base and candidate archives built
together are byte-identical. The normative refinement Markdown defines when this
shortcut may waive hardware testing, but the document is outside every checker and
reviewed-source input.
