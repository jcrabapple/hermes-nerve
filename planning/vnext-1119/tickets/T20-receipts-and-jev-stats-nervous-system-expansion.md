# T20: Receipts and jev_stats nervous-system expansion

**Phase:** Phase 7 — observability and learning

**Blocked by:** T19

**Status:** ready-for-agent

## What to build

Create structured receipts for every supervisory transition and extend local-only jev_stats with admission/router/challenge/staleness/lease/metric summaries.

## Public seam(s)

ReceiptStore public seam; JevStats projection.

## TDD focus

Every listed receipt exists; jev_stats makes no provider call and reports the required nervous-system sections.

## Acceptance criteria

- [ ] All source requirements **817–862** are implemented through the declared public seam(s).
- [ ] Each mapped behavior has an externally observable test or an explicitly documented live/credential-gated verification.
- [ ] No mapped requirement is moved to another ticket without updating the traceability matrix and rerunning coverage verification.
- [ ] Relevant receipts/telemetry prove behavior where the requirement is observational rather than directly user-visible.
## Source requirements owned by this ticket

| Point | Requirement | Verification ID |
|---:|---|---|
| 817 | Immutable-ish structured decision receipts. | `T20-R0817` |
| 818 | Turn-admission receipt. | `T20-R0818` |
| 819 | Router-trigger receipt. | `T20-R0819` |
| 820 | Jev-request receipt. | `T20-R0820` |
| 821 | Agreement receipt. | `T20-R0821` |
| 822 | Challenge receipt. | `T20-R0822` |
| 823 | Challenge-resolution receipt. | `T20-R0823` |
| 824 | Stale-response receipt. | `T20-R0824` |
| 825 | Decision-lease receipt. | `T20-R0825` |
| 826 | Completion receipt. | `T20-R0826` |
| 827 | Recovery receipt. | `T20-R0827` |
| 828 | Final-turn supervision summary. | `T20-R0828` |
| 829 | Choices preserved. | `T20-R0829` |
| 830 | Hermes selected value preserved. | `T20-R0830` |
| 831 | Jev selected value preserved. | `T20-R0831` |
| 832 | Probabilities preserved. | `T20-R0832` |
| 833 | Confidence preserved. | `T20-R0833` |
| 834 | Decision contract preserved. | `T20-R0834` |
| 835 | Resulting Hermes action preserved. | `T20-R0835` |
| 836 | Observed outcome preserved. | `T20-R0836` |
| 837 | Provider provenance preserved. | `T20-R0837` |
| 838 | State/version provenance preserved. | `T20-R0838` |
| 839 | Turn admission section. | `T20-R0839` |
| 840 | Nervous-system section. | `T20-R0840` |
| 841 | Event-router section. | `T20-R0841` |
| 842 | Router trigger reasons. | `T20-R0842` |
| 843 | Router suppression reasons. | `T20-R0843` |
| 844 | Batch statistics. | `T20-R0844` |
| 845 | Challenge statistics. | `T20-R0845` |
| 846 | Agreement statistics. | `T20-R0846` |
| 847 | Disagreement statistics. | `T20-R0847` |
| 848 | Staleness statistics. | `T20-R0848` |
| 849 | Decision-lease statistics. | `T20-R0849` |
| 850 | Completion statistics. | `T20-R0850` |
| 851 | Recovery statistics. | `T20-R0851` |
| 852 | Supervision-mode statistics. | `T20-R0852` |
| 853 | WATCH→ON transition statistics. | `T20-R0853` |
| 854 | Provider usage statistics. | `T20-R0854` |
| 855 | Cost statistics. | `T20-R0855` |
| 856 | Latency statistics. | `T20-R0856` |
| 857 | Avoided-call estimates. | `T20-R0857` |
| 858 | Confidence calibration buckets. | `T20-R0858` |
| 859 | Recent high-confidence disagreements. | `T20-R0859` |
| 860 | Recent stale responses. | `T20-R0860` |
| 861 | Recent challenge outcomes. | `T20-R0861` |
| 862 | Local-only jev_stats behavior retained. | `T20-R0862` |
