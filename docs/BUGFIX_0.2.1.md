# Hermes-Jev 0.2.1 bug-handoff actualization

This release implements the 2026-09-18 Muna bug handoff preserved under
`planning/bug-handoff-2026-09-18/`.

## Status by handoff item

| ID | Status | 0.2.1 implementation |
|---|---|---|
| JEV-001 | Fixed | Repeated-failure episodes get stable fingerprints. Confident remote recovery controls create an execution lease, and a provider-independent third identical failure activates a local `REPLAN`. The composed pre-tool hook blocks the exact failed action under `REPLAN`, `GATHER_EVIDENCE`, or `ESCALATE`; `RETRY` explicitly permits one retry. |
| JEV-002 | Fixed | Stable `decision_id` values link decision rows to control lifecycle rows (`created`, `delivered`, `next_action`, `expired`) and outcomes. `jev_stats` exposes attribution counts and an explicit decision-correction denominator definition. |
| JEV-003 | Fixed in plugin telemetry | The gate hook records `disabled` observations when `gate_mode=off` and includes `turn_id`, `session_id`, and `tool_call_id`. Gate metrics are explicitly labeled as a profile-lifetime gate-event ledger, separate from receipts. |
| JEV-004 | Fixed | `jev_stats` defaults to a bounded `summary`, supports section filters, makes recent arrays opt-in, caps recent limits, and defensively truncates oversized targeted output. |
| JEV-005 | Clarified + regression covered | Rehydration remains explicit/demand-driven rather than automatic after every compression. A regression verifies anchored evidence can be rehydrated and increments `rehydrated_compacted_evidence` / recovery-demand telemetry. Zero rehydrations without an actual recovery request is not treated as failure. |
| JEV-006 | Fixed | First failure may reach Jev; exact repeated failures are locally deduplicated. From the second equivalent failure onward, no provider call is required unless material state/evidence changes. Third identical failure activates the local loop breaker by default. |
| JEV-007 | Fixed | Decision-state fingerprints exclude monotonic `state_version` and `decision_version`. Lease reuse is based on semantic state; invalidations are reason-labeled (contradiction, strategy change, completion boundary, failure state change, consequence boundary, or other material state change). |
| JEV-008 | Plugin-side improvement | Plugin registration logs exact Hermes-Jev version and source path. The package does not claim to eliminate Hermes host warnings emitted before general-plugin discovery; those remain an upstream integration concern if reproduced. |

## Control semantics

A control lease is local and does not make a provider request at the pre-tool seam.

- `REPLAN`, `GATHER_EVIDENCE`, `ESCALATE`: the exact controlled action fingerprint is blocked; a materially different next tool action counts as followed and consumes the lease.
- `RETRY`: one next action is permitted and the lease is consumed.
- `shadow` mode: controls are recorded but never enforced.
- `correct_next` / `precommit`: eligible controls can constrain the next action.

The local loop breaker activates after `nervous_repeated_failure_local_replan_at`
identical failures (default `3`). This bounds failure-loop continuation even if a
remote Jev response is late, silent, or unavailable.

## Telemetry scopes

`jev_stats` labels metric provenance instead of merging unlike lifetimes:

- receipts: profile-lifetime receipt ledger
- gate: profile-lifetime gate-event ledger
- context: profile-lifetime context ledger
- nervous runtime: current process
- nervous outcomes: profile-lifetime outcome ledger

Default stats output is intentionally compact. Use `section=...`,
`include_recent=true`, and a small `recent_limit` for targeted debugging.

## Validation posture

The 0.2.1 package is offline regression-verified. Live provider/account behavior is
not re-claimed unless a real credential-backed run is performed after installation.
