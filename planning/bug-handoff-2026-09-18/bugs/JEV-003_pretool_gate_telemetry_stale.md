# JEV-003 - Pre-tool gate telemetry appears stale/disconnected during active nervous supervision

**Status:** High-confidence anomaly; requires code-level confirmation  
**Priority:** P0  
**Subsystem:** pre-tool gate integration / event persistence

## Summary

During the long ARB run, the nervous system clearly processed later activity, including receipts timestamped around 17:34-17:35 UTC. However, `gate.recent` remained populated with events from around 17:04-17:07 UTC and the gate counters remained at only 24 total events / 16 terminal observations.

The workload contained dozens of terminal calls after those timestamps.

## Expected

If the pre-tool gate is active for material terminal actions, its event counters and recent event timestamps should advance along with later terminal executions.

## Actual

Observed gate snapshot:

- `event_count = 24`
- `by_tool.terminal = 16`
- `evaluated = 15`
- `bypassed = 8`
- latest displayed terminal gate timestamps ~17:07 UTC

At the same time the nervous path continued generating provider receipts into ~17:35 UTC and the agent executed many more terminal calls.

Historical receipt totals also show `hermes/pre-tool-gate/v1 = 121`, which does not align obviously with `gate.event_count = 24`.

## Possible causes

- Pre-tool hook became inactive after a lifecycle transition/compression/session state change.
- Gate event log stopped appending while receipts continued elsewhere.
- `jev_stats.gate` reads a different scope/file than receipt totals.
- Only a subset of terminal actions are eligible, but eligibility is not observable.
- Gate is bypassed before event logging in this path.

## Evidence

See:

- `evidence/stats_snapshot_and_compression.txt`
- `evidence/receipts_and_90s_timeout.txt`

## Acceptance criteria

- For a controlled sequence of terminal/read/write actions, gate counters advance deterministically.
- Every material terminal call has a correlatable pre-tool gate event or an explicit reason it was not gated.
- Stats make receipt/event scope differences explicit.
- Regression test covers gate behavior across compression and long-running turns.
