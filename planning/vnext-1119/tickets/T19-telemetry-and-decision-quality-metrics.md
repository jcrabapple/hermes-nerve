# T19: Telemetry and decision-quality metrics

**Phase:** Phase 7 — observability and learning

**Blocked by:** T18

**Status:** ready-for-agent

## What to build

Instrument turn/event/call/challenge/lease/completion/cost/latency/calibration metrics, prioritizing false PASS, useful intervention, and final task success over raw call volume.

## Public seam(s)

MetricsSink interface; calibration aggregators.

## TDD focus

Metrics cover every listed counter/distribution and explicitly surface false PASS and useful-disagreement quality.

## Acceptance criteria

- [ ] All source requirements **751–816** are implemented through the declared public seam(s).
- [ ] Each mapped behavior has an externally observable test or an explicitly documented live/credential-gated verification.
- [ ] No mapped requirement is moved to another ticket without updating the traceability matrix and rerunning coverage verification.
- [ ] Relevant receipts/telemetry prove behavior where the requirement is observational rather than directly user-visible.
## Source requirements owned by this ticket

| Point | Requirement | Verification ID |
|---:|---|---|
| 751 | Total turns. | `T19-R0751` |
| 752 | OFF turns. | `T19-R0752` |
| 753 | WATCH turns. | `T19-R0753` |
| 754 | ON turns. | `T19-R0754` |
| 755 | WATCH→ON promotions. | `T19-R0755` |
| 756 | Total raw events. | `T19-R0756` |
| 757 | Events consumed locally. | `T19-R0757` |
| 758 | Events suppressed. | `T19-R0758` |
| 759 | Events batched. | `T19-R0759` |
| 760 | Events forwarded to Jev. | `T19-R0760` |
| 761 | Provider-call avoidance count. | `T19-R0761` |
| 762 | Jev calls per turn. | `T19-R0762` |
| 763 | Jev calls per 100 Hermes events. | `T19-R0763` |
| 764 | Jev calls per meaningful decision. | `T19-R0764` |
| 765 | Meaningful decision count. | `T19-R0765` |
| 766 | Jev decisions followed. | `T19-R0766` |
| 767 | Jev decisions overridden. | `T19-R0767` |
| 768 | Agreements. | `T19-R0768` |
| 769 | Disagreements. | `T19-R0769` |
| 770 | High-confidence disagreements. | `T19-R0770` |
| 771 | Challenges issued. | `T19-R0771` |
| 772 | Challenges accepted. | `T19-R0772` |
| 773 | Challenges rejected. | `T19-R0773` |
| 774 | Stale challenges. | `T19-R0774` |
| 775 | Useful disagreements. | `T19-R0775` |
| 776 | Useless disagreements. | `T19-R0776` |
| 777 | False-positive challenges. | `T19-R0777` |
| 778 | False-negative supervision events where measurable. | `T19-R0778` |
| 779 | Retry count. | `T19-R0779` |
| 780 | Replan count. | `T19-R0780` |
| 781 | Escalate count. | `T19-R0781` |
| 782 | Gather-evidence count. | `T19-R0782` |
| 783 | Completion assessments. | `T19-R0783` |
| 784 | False PASS. | `T19-R0784` |
| 785 | False REPLAN. | `T19-R0785` |
| 786 | Premature-DONE catches. | `T19-R0786` |
| 787 | Rehydrations. | `T19-R0787` |
| 788 | Decision-lease reuse. | `T19-R0788` |
| 789 | Decision-lease invalidations. | `T19-R0789` |
| 790 | Average Jev latency. | `T19-R0790` |
| 791 | P50 Jev latency. | `T19-R0791` |
| 792 | P95 Jev latency. | `T19-R0792` |
| 793 | Jev token usage. | `T19-R0793` |
| 794 | Jev provider cost. | `T19-R0794` |
| 795 | Estimated avoided Jev calls. | `T19-R0795` |
| 796 | Estimated avoided provider cost. | `T19-R0796` |
| 797 | Avoided synchronous wait time. | `T19-R0797` |
| 798 | Final task success. | `T19-R0798` |
| 799 | Decision correction success. | `T19-R0799` |
| 800 | Router precision. | `T19-R0800` |
| 801 | Router recall where ground truth can be approximated. | `T19-R0801` |
| 802 | Challenge precision. | `T19-R0802` |
| 803 | Confidence calibration. | `T19-R0803` |
| 804 | False PASS as a critical metric. | `T19-R0804` |
| 805 | Final task success as ultimate metric. | `T19-R0805` |
| 806 | Useful decision disagreement over raw Jev call count. | `T19-R0806` |
| 807 | Avoid number of Jev calls as the primary success measure. | `T19-R0807` |
| 808 | Measure whether Jev actually changed the trajectory usefully. | `T19-R0808` |
| 809 | Measure whether Jev catches premature completion. | `T19-R0809` |
| 810 | Measure whether Jev catches pointless retry loops. | `T19-R0810` |
| 811 | Measure whether Jev improves routing. | `T19-R0811` |
| 812 | Measure how often Hermes correctly overrides Jev. | `T19-R0812` |
| 813 | Measure how often Jev correctly overrides Hermes. | `T19-R0813` |
| 814 | Measure decision-added latency. | `T19-R0814` |
| 815 | Measure avoided tool/model calls. | `T19-R0815` |
| 816 | Measure avoided Jev calls. | `T19-R0816` |
