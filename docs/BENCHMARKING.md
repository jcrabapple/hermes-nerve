# Benchmarking policy

Hermes-Jev should not publish speed/cost/reliability claims without a reproducible corpus and raw evidence.

A benchmark release should record:

- exact Hermes version/commit
- exact Hermes-Jev commit
- exact Jev model string
- corpus derivation method and privacy treatment
- decision contracts and thresholds
- latency distribution, not only average
- provider/API failures
- label agreement against a documented reference process
- human-interruption rate for approval-style gates
- false-allow and false-block analysis for consequential decisions
- raw JSONL result artifacts when redistribution is safe

Offline unit tests are not Jev quality benchmarks.
