# T23: End-to-end turn lifecycle and WATCH wake-up

**Phase:** Phase 9 — vertical integration

**Blocked by:** T02, T05, T07, T09, T22

**Status:** ready-for-agent

## What to build

Wire prompt ingress through admission, local event flow, WATCH promotion, ON supervision, challenges, completion and TURN_COMPLETE final summary.

## Public seam(s)

Single end-to-end TurnSupervision seam.

## TDD focus

OFF/WATCH/ON scenarios execute through the full public seam; WATCH promotes only on real decision-plane signals.

## Acceptance criteria

- [ ] All source requirements **914–942** are implemented through the declared public seam(s).
- [ ] Each mapped behavior has an externally observable test or an explicitly documented live/credential-gated verification.
- [ ] No mapped requirement is moved to another ticket without updating the traceability matrix and rerunning coverage verification.
- [ ] Relevant receipts/telemetry prove behavior where the requirement is observational rather than directly user-visible.
## Source requirements owned by this ticket

| Point | Requirement | Verification ID |
|---:|---|---|
| 914 | Prompt received. | `T23-R0914` |
| 915 | turn_id created. | `T23-R0915` |
| 916 | Hermes starts work immediately. | `T23-R0916` |
| 917 | Prompt simultaneously evaluated by turn arbiter. | `T23-R0917` |
| 918 | Arbiter returns OFF/WATCH/ON. | `T23-R0918` |
| 919 | Local event bus runs. | `T23-R0919` |
| 920 | Local router accumulates state. | `T23-R0920` |
| 921 | ON mode permits active Jev calls. | `T23-R0921` |
| 922 | WATCH mode waits for a decision-plane wake condition. | `T23-R0922` |
| 923 | OFF mode logs admission result and remains quiet. | `T23-R0923` |
| 924 | Material decision can create Jev assessment. | `T23-R0924` |
| 925 | Jev result can log agreement. | `T23-R0925` |
| 926 | Jev result can generate challenge. | `T23-R0926` |
| 927 | Router continues accumulating state. | `T23-R0927` |
| 928 | Supervision persists through autonomous execution. | `T23-R0928` |
| 929 | Completion candidate receives high-priority review where supervised. | `T23-R0929` |
| 930 | TURN_COMPLETE ends turn-scoped nervous system. | `T23-R0930` |
| 931 | Final supervision summary emitted. | `T23-R0931` |
| 932 | Structured DECISION. | `T23-R0932` |
| 933 | MUTATION_INTENT. | `T23-R0933` |
| 934 | RECOVERY. | `T23-R0934` |
| 935 | COMPLETION_CANDIDATE. | `T23-R0935` |
| 936 | Consequential operation intent. | `T23-R0936` |
| 937 | Strategy change. | `T23-R0937` |
| 938 | Repeated failure. | `T23-R0938` |
| 939 | High uncertainty. | `T23-R0939` |
| 940 | Human escalation candidate. | `T23-R0940` |
| 941 | Irreversible-action candidate. | `T23-R0941` |
| 942 | Other adaptive-router indication that a real decision plane has emerged. | `T23-R0942` |
