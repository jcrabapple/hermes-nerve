# Final Code Review Gate

Run the Matt Pocock two-axis review after all implementation tickets land.

## Standards axis

Review the final diff against repository standards plus a smell baseline. Pay particular attention to shallow pass-through modules, duplicated policy, shotgun surgery, primitive obsession around IDs/states, repeated switches on event/control types, and speculative generality in the classifier/context layers.

## Spec axis

Use `SPEC.md`, `source/REQUIREMENTS_1119.md`, and `TRACEABILITY_MATRIX.csv` as the primary sources. For every finding, identify missing/partial behavior, scope creep, or apparently implemented behavior whose semantics do not match the mapped source point.

## Mandatory conformance checks

- `verification/COVERAGE_REPORT.md` reports 1119/1119 and zero duplicates/gaps.
- Every T01–T31 ticket is complete.
- Every verification ID has a test/receipt/live-gated result.
- False-PASS tests are green.
- Synthetic >=500 ms provider latency does not serialize ordinary worker events.
- No raw chat/tool transcript is continuously forwarded by default.
- PRECOMMIT is limited to explicitly consequential boundaries.
- Release artifact matches the pinned source tree and documentation/test claims.
