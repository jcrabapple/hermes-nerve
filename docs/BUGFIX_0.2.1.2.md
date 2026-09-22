# Nerve v0.2.1.2 stabilization

## Scope

This patch fixes the long-session ContextEngine failure reported in issue #2 and adjacent regressions found while reproducing the exact v0.2.1.1 release. It deliberately does not redesign the nervous system, retune semantic thresholds, or add provider transports.

## Root causes and fixes

| Defect | Root cause | Fix |
| --- | --- | --- |
| Apply mode crashes above 48 evidence items | The automatic engine built an unbounded evidence list and passed it into the public curation seam, which intentionally caps input at 48 | Select at most 48 recoverable raw candidates per boundary, oldest first; defer the rest unchanged |
| Fallback can still kill a turn | `_fallback_compress()` only handled signature `TypeError`; arbitrary compressor failures escaped | Contain all fallback exceptions and return the original messages |
| Existing anchors are re-curated | Tool-result scanning treated `[JEV_CONTEXT_ANCHOR ...]` as raw evidence | Treat Jev anchors as terminal compacted artifacts and skip them |
| Shadow mode inflates compaction metrics | Proposed shadow ANCHOR/DROP actions were written as evidence actions later counted as applied | Record proposals only in the shadow-plan ledger; applied compaction is recorded only in apply mode |
| Unrecoverable evidence consumes provider capacity | Semantic assessment ran before deterministic `KEEP_EXACT` policy | Automatic engine selection excludes unrecoverable evidence from remote curation and does not delegate safety-rejected tool evidence to the generic fallback |
| Shadow failure is invisible | `on_turn_complete()` swallowed every exception | Preserve fail-open behavior while exposing failure counts/type/stage in engine status |

## Bounded-work invariant

The public context curation contract remains capped at 48 evidence units. `_BATCH_SIZE = 4`, with four typed semantic questions per item, therefore automatic curation issues at most 12 semantic assessment requests for one boundary.

The engine does not raise this limit and does not chunk an entire 851-item history into hundreds of calls.

## Regression coverage

The 0.2.1.2 patch suite covers:

- exactly 48 candidates;
- 49, 60, and 851 candidates;
- curation failure -> built-in fallback;
- curation failure + fallback failure -> original messages;
- existing-anchor idempotence across repeated compression boundaries;
- unrecoverable evidence excluded from automatic provider work;
- shadow proposals not counted as applied compaction;
- observable shadow failure;
- 48-item public curation fan-out capped at 12 requests.

All pre-existing 0.2.1 and 0.2.1.1 regression suites remain release blockers.

## Direct TypeSafe evidence

Issue #1 received an independent successful live direct-TypeSafe smoke against v0.2.1.1 with verified TypeSafe request/receipt provenance. v0.2.1.2 documentation records that evidence precisely; the 0.2.1.2 package must not claim a new credentialed live run unless one is actually performed against its candidate SHA.
