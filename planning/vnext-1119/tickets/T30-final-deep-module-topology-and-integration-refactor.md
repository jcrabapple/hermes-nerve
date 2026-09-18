# T30: Final deep-module topology and integration refactor

**Phase:** Phase 11 — architecture consolidation

**Blocked by:** T23, T25, T26

**Status:** ready-for-agent

## What to build

Consolidate the implementation into the explicit deep modules that emerged from the design, keeping small public interfaces and internal complexity behind stable seams.

## Public seam(s)

TurnArbiter, EventBus, Supervisor/Router, accumulators/detectors, lease manager, async provider worker, challenge components, receipt/outcome stores, classifier adapter.

## TDD focus

Deletion/interface tests demonstrate module depth/locality; callers do not depend on detector internals.

## Acceptance criteria

- [ ] All source requirements **1080–1101** are implemented through the declared public seam(s).
- [ ] Each mapped behavior has an externally observable test or an explicitly documented live/credential-gated verification.
- [ ] No mapped requirement is moved to another ticket without updating the traceability matrix and rerunning coverage verification.
- [ ] Relevant receipts/telemetry prove behavior where the requirement is observational rather than directly user-visible.
## Source requirements owned by this ticket

| Point | Requirement | Verification ID |
|---:|---|---|
| 1080 | jev_turn_arbiter. | `T30-R1080` |
| 1081 | jev_event_bus. | `T30-R1081` |
| 1082 | jev_supervisor. | `T30-R1082` |
| 1083 | Adaptive local relevance router. | `T30-R1083` |
| 1084 | Local turn-state accumulator. | `T30-R1084` |
| 1085 | Event compressor. | `T30-R1085` |
| 1086 | Novelty detector. | `T30-R1086` |
| 1087 | Decision-delta detector. | `T30-R1087` |
| 1088 | Evidence-delta detector. | `T30-R1088` |
| 1089 | Risk-delta detector. | `T30-R1089` |
| 1090 | Uncertainty-delta detector. | `T30-R1090` |
| 1091 | Completion-pressure detector. | `T30-R1091` |
| 1092 | Jev freshness/decision-lease manager. | `T30-R1092` |
| 1093 | Jev asynchronous provider worker. | `T30-R1093` |
| 1094 | Jev challenge queue. | `T30-R1094` |
| 1095 | Hermes challenge inbox. | `T30-R1095` |
| 1096 | Challenge-state validator. | `T30-R1096` |
| 1097 | Agreement/disagreement logger. | `T30-R1097` |
| 1098 | Nervous-system receipt store. | `T30-R1098` |
| 1099 | Outcome correlation layer. | `T30-R1099` |
| 1100 | Router calibration dataset. | `T30-R1100` |
| 1101 | Optional future local classifier. | `T30-R1101` |
