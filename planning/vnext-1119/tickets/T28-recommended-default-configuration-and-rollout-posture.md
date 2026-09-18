# T28: Recommended default configuration and rollout posture

**Phase:** Phase 10 — verification

**Blocked by:** T27

**Status:** ready-for-agent

## What to build

Ship defaults that enable admission and adaptive async supervision while keeping legacy gate/context mutation conservative and provider budgets bounded.

## Public seam(s)

Configuration schema and default policy surface.

## TDD focus

Fresh install exactly matches every recommended default; migration does not silently enable synchronous all-tool gating.

## Acceptance criteria

- [ ] All source requirements **1049–1064** are implemented through the declared public seam(s).
- [ ] Each mapped behavior has an externally observable test or an explicitly documented live/credential-gated verification.
- [ ] No mapped requirement is moved to another ticket without updating the traceability matrix and rerunning coverage verification.
- [ ] Relevant receipts/telemetry prove behavior where the requirement is observational rather than directly user-visible.
## Source requirements owned by this ticket

| Point | Requirement | Verification ID |
|---:|---|---|
| 1049 | Turn arbiter enabled. | `T28-R1049` |
| 1050 | Nervous system asynchronous. | `T28-R1050` |
| 1051 | Most casual turns OFF. | `T28-R1051` |
| 1052 | Ambiguous potentially operational turns WATCH. | `T28-R1052` |
| 1053 | Clearly autonomous/material work turns ON. | `T28-R1053` |
| 1054 | Local adaptive router enabled. | `T28-R1054` |
| 1055 | Confidence-gated challenges enabled. | `T28-R1055` |
| 1056 | Agreement log-only by default. | `T28-R1056` |
| 1057 | Low-confidence disagreement log-only by default. | `T28-R1057` |
| 1058 | High-confidence disagreement eligible for challenge. | `T28-R1058` |
| 1059 | PRECOMMIT restricted to consequential boundaries. | `T28-R1059` |
| 1060 | Legacy automatic gate remains off by default. | `T28-R1060` |
| 1061 | Context mutation remains shadow-first initially. | `T28-R1061` |
| 1062 | Built-in Hermes context fallback retained. | `T28-R1062` |
| 1063 | Provider call budget safety valve enabled. | `T28-R1063` |
| 1064 | Adaptive relevance remains primary call-limiting mechanism. | `T28-R1064` |
