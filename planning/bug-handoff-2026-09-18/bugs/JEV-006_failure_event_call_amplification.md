# JEV-006 - Repeated identical failures cause excessive Jev calls without effective deduplication

**Status:** High-confidence performance/control defect  
**Priority:** P1  
**Subsystem:** nervous router / local learning / failure deduplication

## Summary

During the pathological run Jev made 99 nervous-system provider calls for 176 raw events. The router repeatedly marked failure events as score `1.0`, `worth_calling=true`, with the same generic reason set. The agent still repeated the same failing action many times.

The supervision system appears to spend provider calls re-evaluating highly similar failures instead of collapsing them into a repeated-failure episode with stronger local handling.

## Observed

- raw events: 176
- forwarded events: 96
- provider calls: 99
- `jev_calls_per_100_events = 56.25`
- `jev_calls_per_turn = 33.0`
- Jev tokens: 219,092
- `budget_suppressed = 78`
- repeated identical terminal failure count reached 33
- many recent router entries show `FAILURE`, score `1.0`, `worth_calling=true`, `historical_samples=0`

## Expected

Identical or near-identical failures within one turn should be fingerprinted and deduplicated. After one or two provider evaluations, subsequent repeats should be handled locally unless state materially changes.

## Proposed behavior

Maintain a failure fingerprint using tool name + normalized args + exit status + normalized error signature. Apply hysteresis:

- first occurrence: evaluate
- second identical occurrence: evaluate only if new evidence exists
- third+ occurrence: local forced replan/escalate; do not call provider again until state changes

## Evidence

See:

- `evidence/loop_count_33.txt`
- `evidence/stats_snapshot_and_compression.txt`

## Acceptance criteria

- Repeated identical failures do not generate a provider call per occurrence.
- A repeated-failure episode has one stable fingerprint and counter.
- Provider calls decrease substantially in the regression scenario.
- Loop-breaking effectiveness improves, not just cost.
