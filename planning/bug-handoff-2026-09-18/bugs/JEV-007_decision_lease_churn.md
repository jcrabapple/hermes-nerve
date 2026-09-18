# JEV-007 - Decision lease churn is extreme with zero recorded reuse

**Status:** High-confidence anomaly  
**Priority:** P1  
**Subsystem:** decision lease lifecycle

## Summary

Jev recorded **172 decision lease invalidations** over only 176 raw events and **0 lease reuse**. This suggests nearly every event invalidates the current decision context, defeating the purpose of a reusable decision lease and potentially amplifying provider calls.

## Observed

- total raw events: 176
- decision lease invalidations: 172
- decision lease reuse: 0
- provider calls: 99

## Why this matters

If leases are invalidated on essentially every event, they cannot stabilize decisions across related tool results. That can cause repeated re-evaluation, loss of hysteresis, and noisy control changes.

## Caveat

The intended lease semantics are not yet documented in the captured logs. If invalidation-per-event is intentional, the metric name or documentation is misleading.

## Evidence

See `evidence/stats_snapshot_and_compression.txt`.

## Acceptance criteria

- Define the exact lease validity/invalidation contract.
- Add counters for invalidation reason.
- Demonstrate lease reuse in a stable multi-tool sequence.
- Repeated identical failures should not invalidate/recreate an equivalent lease indefinitely.
