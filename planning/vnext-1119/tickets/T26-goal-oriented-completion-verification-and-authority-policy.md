# T26: Goal-oriented completion verification and authority policy

**Phase:** Phase 9 — vertical integration

**Blocked by:** T11, T14, T23

**Status:** ready-for-agent

## What to build

Tie completion to explicit goal/done evidence and formalize how confidence, staleness, reversibility, consequence and mode govern Jev authority versus Hermes overrides.

## Public seam(s)

GoalVerifier; AuthorityPolicy.

## TDD focus

PASS requires evidence; override/correction paths are explicit; stale or irreversible-state constraints dominate inappropriate corrections.

## Acceptance criteria

- [ ] All source requirements **993–1014** are implemented through the declared public seam(s).
- [ ] Each mapped behavior has an externally observable test or an explicitly documented live/credential-gated verification.
- [ ] No mapped requirement is moved to another ticket without updating the traceability matrix and rerunning coverage verification.
- [ ] Relevant receipts/telemetry prove behavior where the requirement is observational rather than directly user-visible.
## Source requirements owned by this ticket

| Point | Requirement | Verification ID |
|---:|---|---|
| 993 | Verification tied to explicit goal. | `T26-R0993` |
| 994 | Verification tied to observed evidence. | `T26-R0994` |
| 995 | Verification tied to done criteria. | `T26-R0995` |
| 996 | Verification not based solely on Hermes saying work is complete. | `T26-R0996` |
| 997 | Completion evidence bundled into Jev assessment. | `T26-R0997` |
| 998 | PASS only when required state is actually supported. | `T26-R0998` |
| 999 | RETRY for execution failure with still-valid strategy. | `T26-R0999` |
| 1000 | REPLAN when current approach is inadequate. | `T26-R1000` |
| 1001 | ESCALATE when genuine external/human dependency exists. | `T26-R1001` |
| 1002 | GATHER_EVIDENCE when state is insufficient. | `T26-R1002` |
| 1003 | Avoid completion without relevant evidence. | `T26-R1003` |
| 1004 | Jev authoritative enough that high-confidence disagreements can alter trajectory. | `T26-R1004` |
| 1005 | Hermes not required to blindly follow every Jev output. | `T26-R1005` |
| 1006 | Hermes overrides explicitly recorded. | `T26-R1006` |
| 1007 | Jev corrections explicitly recorded. | `T26-R1007` |
| 1008 | Staleness can override Jev authority. | `T26-R1008` |
| 1009 | Reversibility can affect Jev authority. | `T26-R1009` |
| 1010 | Consequence can affect Jev authority. | `T26-R1010` |
| 1011 | Confidence can affect Jev authority. | `T26-R1011` |
| 1012 | Precommit mode can temporarily increase Jev authority. | `T26-R1012` |
| 1013 | Shadow mode deliberately reduces Jev authority. | `T26-R1013` |
| 1014 | Correct-next mode gives Jev future-state authority without unsafe retroactive undo. | `T26-R1014` |
