# Benchmarking policy — context governor

Hermes-Jev should not publish context-quality claims from compression ratio alone.

## Primary objective

Measure **continuation fidelity per context token**.

For a checkpointed real session, compare at least:

- A: full uncompressed context
- B: Hermes built-in context compressor
- C: Hermes-Jev context governor

Give each branch the same next task and main model. Over the following turns measure:

- task completion / verification result
- exact user-constraint retention
- exact unresolved-failure retention
- next-action agreement where a documented reference exists
- prompt tokens sent over the next N turns
- repeated tool calls caused by missing context
- anchors created and later rehydrated
- unnecessary rehydrations
- recovery-demand rate
- stale evidence retained after it was superseded
- contradictory evidence incorrectly discarded
- Jev requests, latency and cost
- main-model latency/cost
- wall-clock completion time

## False-forget definition

A rehydration alone is not a false forget. Treat a curation action as harmful when removal/anchoring causes a materially incorrect decision, unrecoverable loss, avoidable repeated work, or task failure that the full-context control does not exhibit.

## Shadow calibration

Before apply mode, collect shadow plans from real sessions and record:

- proposed action
- semantic probabilities
- later reference/re-execution
- later rehydration
- task outcome
- turns-until-next-use

Use these observations to tune action thresholds rather than selecting a global confidence floor by intuition.

## Reproducibility

Record:

- exact Hermes version/commit
- exact Hermes-Jev version/commit
- exact Jev model string
- corpus derivation/privacy treatment
- curation thresholds and engine settings
- context window and primary model
- raw JSONL measurements where redistribution is safe

Offline unit tests are contract tests, not Jev-quality benchmarks.
