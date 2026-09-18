# JEV-004 - `jev_stats` produces an unbounded payload that can poison the surrounding model turn

**Status:** Confirmed usability/performance defect  
**Priority:** P1  
**Subsystem:** `jev_stats` API / Hermes tool-result integration

## Summary

`jev_stats` itself completed in approximately **0.06 seconds**, but returned **29,652 characters**. The immediately following main-model call then sat stale for 90 seconds, was killed by Hermes, and retried.

This does not prove Jev inference caused the 90-second delay. It demonstrates that the default stats payload is large enough to materially inflate downstream context and make introspection expensive/unreliable.

## Expected

Routine stats introspection should be bounded and cheap. The caller should be able to request only the needed sections and recent records.

## Actual

- `jev_stats`: ~0.06 s
- tool result: 29,652 characters
- next main-model request had a much larger context
- main-model call stale for 90 s and was aborted/retried

## Evidence

See `evidence/receipts_and_90s_timeout.txt` and `evidence/stats_snapshot_and_compression.txt`.

## Recommended API additions

Support parameters such as:

- `summary=true`
- `section="nervous"`
- `since=<timestamp>`
- `limit=<N>`
- `recent_receipts=<N>`
- `delta_since_last=true`
- `include_recent_router=false`

Default output should be a compact summary rather than full recent arrays.

## Acceptance criteria

- Default `jev_stats` payload is bounded to a documented maximum.
- Section filtering is supported.
- Recent arrays are limited by default.
- A compact summary can be consumed without adding tens of thousands of characters to the agent context.
