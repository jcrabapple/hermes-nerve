# JEV-005 - Context rehydration remains zero after repeated session compression

**Status:** Needs targeted confirmation  
**Priority:** P1  
**Subsystem:** context engine / recovery / rehydration

## Summary

The session was compressed repeatedly; Hermes reported **4 compressions** and warned that accuracy may degrade. Jev's context ledger simultaneously grew to 445 evidence events, but rehydration remained zero.

This is not sufficient to prove a bug because rehydration may be demand-driven and no recovery request may have fired. It is, however, an important missing behavior under exactly the sort of degraded long session where Jev context recovery is expected to provide value.

## Observed

- `evidence_events = 445`
- `unique_evidence = 445`
- `compacted_unique_evidence = 1`
- `rehydrated_compacted_evidence = 0`
- `rehydrations = 0`
- `shadow_plans = 1`
- `shadow_proposed_saved_chars = 54654`
- Hermes: session compressed 4 times

## Expected test

1. Establish durable facts/constraints.
2. Force compression until the original text is absent from active context.
3. Ask for an action that requires one of those facts.
4. Verify Jev requests/executes rehydration and records it.

## Evidence

See `evidence/stats_snapshot_and_compression.txt`.

## Acceptance criteria

- A deterministic regression test proves at least one successful rehydration after compaction.
- `rehydrations` and `rehydrated_compacted_evidence` increment.
- The recovered evidence is traceable to the action that needed it.
- If zero rehydration is intentional, stats/documentation explain the exact trigger conditions.
