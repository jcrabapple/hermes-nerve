# T15: Resource routing and multi-question control assessment

**Phase:** Phase 5 — decision contracts

**Blocked by:** T14

**Status:** ready-for-agent

## What to build

Support bounded routing/ranking choices and combine previous-result, next-action, evidence, completion, confidence and supervision questions into a single Jev assessment.

## Public seam(s)

RoutingDecision contract; ControlAssessment batch interface.

## TDD focus

A single provider request can answer all related control questions and route bounded worker/tool/environment candidates.

## Acceptance criteria

- [ ] All source requirements **625–646** are implemented through the declared public seam(s).
- [ ] Each mapped behavior has an externally observable test or an explicitly documented live/credential-gated verification.
- [ ] No mapped requirement is moved to another ticket without updating the traceability matrix and rerunning coverage verification.
- [ ] Relevant receipts/telemetry prove behavior where the requirement is observational rather than directly user-visible.
## Source requirements owned by this ticket

| Point | Requirement | Verification ID |
|---:|---|---|
| 625 | Worker selection. | `T15-R0625` |
| 626 | Tool selection. | `T15-R0626` |
| 627 | Tool-family selection. | `T15-R0627` |
| 628 | Environment selection. | `T15-R0628` |
| 629 | Local versus remote compute. | `T15-R0629` |
| 630 | CPU versus GPU where material. | `T15-R0630` |
| 631 | j2 versus win4060 style routing. | `T15-R0631` |
| 632 | Cheap versus expensive path selection. | `T15-R0632` |
| 633 | Candidate prioritization. | `T15-R0633` |
| 634 | Hypothesis prioritization. | `T15-R0634` |
| 635 | File/remediation candidate ranking. | `T15-R0635` |
| 636 | Queue/work-item prioritization. | `T15-R0636` |
| 637 | Jev ranking used only where bounded candidate sets exist. | `T15-R0637` |
| 638 | Batch related control questions into one Jev call. | `T15-R0638` |
| 639 | Previous-step success assessment. | `T15-R0639` |
| 640 | Next-action selection. | `T15-R0640` |
| 641 | Evidence-sufficiency assessment. | `T15-R0641` |
| 642 | Completion assessment. | `T15-R0642` |
| 643 | Confidence assessment. | `T15-R0643` |
| 644 | Potential supervision-intensity recommendation. | `T15-R0644` |
| 645 | Potential watch-category recommendation. | `T15-R0645` |
| 646 | Avoid separate network round trips for each sub-question. | `T15-R0646` |
