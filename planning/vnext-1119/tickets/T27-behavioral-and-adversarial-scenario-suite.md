# T27: Behavioral and adversarial scenario suite

**Phase:** Phase 10 — verification

**Blocked by:** T26, T25, T21

**Status:** ready-for-agent

## What to build

Implement the complete real-task, disagreement, staleness, roleplay, WATCH, high-volume, batching, provider, context and rehydration scenario matrix.

## Public seam(s)

Test only through agreed public seams: TurnSupervision, AdaptiveRouter, ChallengeInbox, ProviderAdapter, GoalVerifier.

## TDD focus

Every scenario in points 1015–1048 has an executable test or explicitly credential-gated live test with a receipt.

## Acceptance criteria

- [ ] All source requirements **1015–1048** are implemented through the declared public seam(s).
- [ ] Each mapped behavior has an externally observable test or an explicitly documented live/credential-gated verification.
- [ ] No mapped requirement is moved to another ticket without updating the traceability matrix and rerunning coverage verification.
- [ ] Relevant receipts/telemetry prove behavior where the requirement is observational rather than directly user-visible.
## Source requirements owned by this ticket

| Point | Requirement | Verification ID |
|---:|---|---|
| 1015 | Real bug diagnosis task. | `T27-R1015` |
| 1016 | Failing-test repair task. | `T27-R1016` |
| 1017 | Service-failure diagnosis task. | `T27-R1017` |
| 1018 | Multiple-plausible-root-causes task. | `T27-R1018` |
| 1019 | Local versus remote-worker routing task. | `T27-R1019` |
| 1020 | Retry-versus-replan task. | `T27-R1020` |
| 1021 | Premature completion trap. | `T27-R1021` |
| 1022 | Repeated failure loop. | `T27-R1022` |
| 1023 | High-confidence Hermes/Jev disagreement. | `T27-R1023` |
| 1024 | Low-confidence Jev disagreement. | `T27-R1024` |
| 1025 | Jev agreement. | `T27-R1025` |
| 1026 | Stale Jev response. | `T27-R1026` |
| 1027 | State changed before challenge arrives. | `T27-R1027` |
| 1028 | Reversible action corrected after challenge. | `T27-R1028` |
| 1029 | Irreversible action already completed before challenge. | `T27-R1029` |
| 1030 | Precommit consequential action. | `T27-R1030` |
| 1031 | Casual chat admission. | `T27-R1031` |
| 1032 | Ordinary explanation admission. | `T27-R1032` |
| 1033 | Pure fictional roleplay admission. | `T27-R1033` |
| 1034 | Roleplay with real training objective. | `T27-R1034` |
| 1035 | Research-only turn. | `T27-R1035` |
| 1036 | Research that becomes real execution mid-turn. | `T27-R1036` |
| 1037 | WATCH→ON promotion. | `T27-R1037` |
| 1038 | Two-hour/high-event-count autonomous turn. | `T27-R1038` |
| 1039 | Hundreds of low-value tool calls with few real decisions. | `T27-R1039` |
| 1040 | Event batching. | `T27-R1040` |
| 1041 | Event compression. | `T27-R1041` |
| 1042 | Adaptive router suppression. | `T27-R1042` |
| 1043 | Router hysteresis. | `T27-R1043` |
| 1044 | Router trigger after hypothesis contradiction. | `T27-R1044` |
| 1045 | Direct TypeSafe live smoke. | `T27-R1045` |
| 1046 | OpenRouter live regression. | `T27-R1046` |
| 1047 | Context pressure/shadow planning. | `T27-R1047` |
| 1048 | Anchor→rehydrate continuation. | `T27-R1048` |
