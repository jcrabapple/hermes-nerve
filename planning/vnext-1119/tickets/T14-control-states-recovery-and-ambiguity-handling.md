# T14: Control states, recovery, and ambiguity handling

**Phase:** Phase 5 — decision contracts

**Blocked by:** T06, T13

**Status:** ready-for-agent

## What to build

Standardize bounded control states and recovery/evidence/human-escalation decisions for supervised work.

## Public seam(s)

ControlDecision contract; RecoveryDecision contract.

## TDD focus

RETRY/REPLAN/ESCALATE/GATHER_EVIDENCE/ASK_HUMAN semantics are behaviorally distinct and loop detection is covered.

## Acceptance criteria

- [ ] All source requirements **590–624** are implemented through the declared public seam(s).
- [ ] Each mapped behavior has an externally observable test or an explicitly documented live/credential-gated verification.
- [ ] No mapped requirement is moved to another ticket without updating the traceability matrix and rerunning coverage verification.
- [ ] Relevant receipts/telemetry prove behavior where the requirement is observational rather than directly user-visible.
## Source requirements owned by this ticket

| Point | Requirement | Verification ID |
|---:|---|---|
| 590 | CONTINUE. | `T14-R0590` |
| 591 | RETRY. | `T14-R0591` |
| 592 | REPLAN. | `T14-R0592` |
| 593 | ESCALATE. | `T14-R0593` |
| 594 | DONE. | `T14-R0594` |
| 595 | GATHER_EVIDENCE. | `T14-R0595` |
| 596 | ASK_HUMAN. | `T14-R0596` |
| 597 | Potential ROLLBACK. | `T14-R0597` |
| 598 | Potential INSPECT. | `T14-R0598` |
| 599 | Potential strategy-specific bounded labels. | `T14-R0599` |
| 600 | PASS. | `T14-R0600` |
| 601 | FAIL. | `T14-R0601` |
| 602 | PARTIAL. | `T14-R0602` |
| 603 | UNKNOWN. | `T14-R0603` |
| 604 | NOT_DONE. | `T14-R0604` |
| 605 | NEEDS_VERIFICATION. | `T14-R0605` |
| 606 | Recovery decision events. | `T14-R0606` |
| 607 | Retry vs replan. | `T14-R0607` |
| 608 | Retry vs gather evidence. | `T14-R0608` |
| 609 | Retry vs rollback. | `T14-R0609` |
| 610 | Retry vs human escalation. | `T14-R0610` |
| 611 | Replan vs escalation. | `T14-R0611` |
| 612 | Repeated retry detection. | `T14-R0612` |
| 613 | Repeated failure detection. | `T14-R0613` |
| 614 | Jev intervention on looping behavior. | `T14-R0614` |
| 615 | Failure events high-value compared with ordinary successful tool calls. | `T14-R0615` |
| 616 | Recovery outcomes logged. | `T14-R0616` |
| 617 | Explicit enough information? judgment. | `T14-R0617` |
| 618 | Evidence sufficiency assessment. | `T14-R0618` |
| 619 | Human escalation when genuinely required. | `T14-R0619` |
| 620 | Avoid automatic human escalation for ordinary uncertainty. | `T14-R0620` |
| 621 | Bounded ASK_HUMAN option. | `T14-R0621` |
| 622 | Bounded GATHER_EVIDENCE option. | `T14-R0622` |
| 623 | Jev can detect when Hermes is choosing prematurely. | `T14-R0623` |
| 624 | Jev can detect when a decision should wait for more evidence. | `T14-R0624` |
