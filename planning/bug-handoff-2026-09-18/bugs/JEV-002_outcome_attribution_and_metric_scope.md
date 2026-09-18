# JEV-002 - Stats cannot reliably attribute whether Jev controls were followed

**Status:** Confirmed observability defect  
**Priority:** P0  
**Subsystem:** nervous telemetry / quality metrics / stats semantics

## Summary

The stats output reports extensive control activity but zero observable follow/override/correction outcomes. It also exposes apparently contradictory challenge counts in different sections.

This makes it impossible to answer the most important question: did Jev alter the agent's behavior?

## Conflicting telemetry

Control activity:

- `control_replan = 15`
- `control_gather_evidence = 35`
- `control_escalate = 1`
- `decision_lease_invalidations = 172`

Outcome/quality telemetry:

- `decision_correction_success = 0`
- `jev_decisions_followed = 0`
- `jev_decisions_overridden = 0`
- `meaningful_decisions = 0`
- `useful_disagreements = 0`
- `recent_challenges = []`

Challenge telemetry also differs by section:

- cumulative/outcomes `challenges_issued = 3`
- quality metrics `challenges_issued = 0`

These values may have different scopes, but the stats schema does not make those scopes obvious enough to safely interpret.

## Expected

Every Jev control that can alter behavior should have an attributable lifecycle:

`event -> decision -> delivered -> next action -> followed/overridden/expired -> outcome`

Stats should clearly label whether a metric is lifetime, profile, session, turn, or rolling-window scoped.

## Actual

The operator sees large counts of replans and lease invalidations but zero followed/overridden decisions. The current schema cannot distinguish "controls were ignored" from "controls were obeyed but not measured."

## Evidence

See `evidence/stats_snapshot_and_compression.txt`.

## Acceptance criteria

- Every control decision gets a stable decision ID.
- The next material agent action records the decision ID it followed or overrode.
- Stats expose separate labeled scopes: lifetime/profile/session/turn/recent.
- `challenges_issued` cannot differ between sections without a visible scope label.
- `decision_correction_success` has a documented denominator.
