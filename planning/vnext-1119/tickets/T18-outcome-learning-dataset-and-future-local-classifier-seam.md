# T18: Outcome learning dataset and future local classifier seam

**Phase:** Phase 7 — observability and learning

**Blocked by:** T07, T09

**Status:** ready-for-agent

## What to build

Persist normalized decision outcomes and create the local-classifier seam so the router can later learn where Jev disagreement is valuable without adding another remote LLM.

## Public seam(s)

OutcomeStore; RouterFeatureVector; optional LocalRelevanceModel adapter.

## TDD focus

Dataset captures Hermes/Jev/final outcome and router features; deterministic router works when classifier is absent.

## Acceptance criteria

- [ ] All source requirements **701–750** are implemented through the declared public seam(s).
- [ ] Each mapped behavior has an externally observable test or an explicitly documented live/credential-gated verification.
- [ ] No mapped requirement is moved to another ticket without updating the traceability matrix and rerunning coverage verification.
- [ ] Relevant receipts/telemetry prove behavior where the requirement is observational rather than directly user-visible.
## Source requirements owned by this ticket

| Point | Requirement | Verification ID |
|---:|---|---|
| 701 | Begin with local deterministic/state-delta logic. | `T18-R0701` |
| 702 | Do not put another full remote LLM in front of Jev. | `T18-R0702` |
| 703 | Optional future tiny local classifier. | `T18-R0703` |
| 704 | Classifier estimates P(useful Jev disagreement \| state delta). | `T18-R0704` |
| 705 | Classifier should execute locally. | `T18-R0705` |
| 706 | Classifier should be low latency. | `T18-R0706` |
| 707 | Classifier should be cheap. | `T18-R0707` |
| 708 | Classifier should use accumulated historical telemetry. | `T18-R0708` |
| 709 | Classifier should learn which event patterns merit Jev. | `T18-R0709` |
| 710 | Rules + state delta + tiny classifier hybrid architecture. | `T18-R0710` |
| 711 | Classifier does not replace turn-level Jev admission unless proven useful. | `T18-R0711` |
| 712 | Router learns from Jev agreement/disagreement history. | `T18-R0712` |
| 713 | Router learns from challenge usefulness. | `T18-R0713` |
| 714 | Router learns from accepted Jev corrections. | `T18-R0714` |
| 715 | Router learns from rejected Jev corrections. | `T18-R0715` |
| 716 | Router learns from final task outcome. | `T18-R0716` |
| 717 | Router learns event classes with low Jev value. | `T18-R0717` |
| 718 | Router learns event classes with high Jev value. | `T18-R0718` |
| 719 | Router reduces calls for consistently low-value patterns. | `T18-R0719` |
| 720 | Router increases sensitivity for high-value patterns. | `T18-R0720` |
| 721 | Completion supervision can become aggressive if it frequently catches errors. | `T18-R0721` |
| 722 | Recovery supervision can become aggressive if it frequently catches bad retries. | `T18-R0722` |
| 723 | Calibration by event type. | `T18-R0723` |
| 724 | Calibration by objective type. | `T18-R0724` |
| 725 | Calibration by consequence class. | `T18-R0725` |
| 726 | Calibration by Hermes model. | `T18-R0726` |
| 727 | Calibration by Jev model/provider if relevant. | `T18-R0727` |
| 728 | Calibration by confidence bucket. | `T18-R0728` |
| 729 | Store Hermes decision. | `T18-R0729` |
| 730 | Store Jev decision. | `T18-R0730` |
| 731 | Store agreement boolean. | `T18-R0731` |
| 732 | Store Jev confidence. | `T18-R0732` |
| 733 | Store Jev probability distribution. | `T18-R0733` |
| 734 | Store final action. | `T18-R0734` |
| 735 | Store whether Jev changed the action. | `T18-R0735` |
| 736 | Store observed outcome. | `T18-R0736` |
| 737 | Store whether outcome was successful. | `T18-R0737` |
| 738 | Store whether Hermes override was correct. | `T18-R0738` |
| 739 | Store whether Jev correction was correct. | `T18-R0739` |
| 740 | Store state delta. | `T18-R0740` |
| 741 | Store router trigger reason. | `T18-R0741` |
| 742 | Store objective type. | `T18-R0742` |
| 743 | Store decision type. | `T18-R0743` |
| 744 | Store materiality. | `T18-R0744` |
| 745 | Store reversibility. | `T18-R0745` |
| 746 | Store consequence. | `T18-R0746` |
| 747 | Store latency. | `T18-R0747` |
| 748 | Store provider cost. | `T18-R0748` |
| 749 | Store stale/not-stale classification. | `T18-R0749` |
| 750 | Store challenge disposition. | `T18-R0750` |
