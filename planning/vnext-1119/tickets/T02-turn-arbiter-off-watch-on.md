# T02: Turn arbiter: OFF / WATCH / ON

**Phase:** Phase 1 — foundation

**Blocked by:** T01

**Status:** ready-for-agent

## What to build

Add one non-recursive Jev admission assessment per user turn, dispatched in parallel with Hermes, producing OFF/WATCH/ON plus complete admission telemetry.

## Public seam(s)

TurnAdmission interface at prompt ingress; Jev provider adapter behind it.

## TDD focus

Casual chat OFF, ambiguous operational WATCH, explicit autonomous work ON; admission never blocks initial Hermes work.

## Acceptance criteria

- [ ] All source requirements **26–62** are implemented through the declared public seam(s).
- [ ] Each mapped behavior has an externally observable test or an explicitly documented live/credential-gated verification.
- [ ] No mapped requirement is moved to another ticket without updating the traceability matrix and rerunning coverage verification.
- [ ] Relevant receipts/telemetry prove behavior where the requirement is observational rather than directly user-visible.
## Source requirements owned by this ticket

| Point | Requirement | Verification ID |
|---:|---|---|
| 26 | Every user prompt receives a unique turn_id. | `T02-R0026` |
| 27 | The same user prompt can be sent to Hermes and the Jev admission system in parallel. | `T02-R0027` |
| 28 | Hermes starts processing immediately. | `T02-R0028` |
| 29 | Hermes does not wait for Jev admission before beginning work. | `T02-R0029` |
| 30 | Dedicated Jev Turn Arbiter. | `T02-R0030` |
| 31 | Dedicated turn-admission contract. | `T02-R0031` |
| 32 | Suggested contract namespace: hermes/jev-turn-admission/v1. | `T02-R0032` |
| 33 | Admission contract explicitly non-recursive. | `T02-R0033` |
| 34 | Admission Jev call cannot cause another admission Jev call. | `T02-R0034` |
| 35 | Turn arbiter predicts whether a meaningful decision plane exists. | `T02-R0035` |
| 36 | Turn arbiter predicts whether a decision plane is likely to emerge before the turn completes. | `T02-R0036` |
| 37 | Turn arbiter does not merely classify chat versus work. | `T02-R0037` |
| 38 | Turn arbiter evaluates likelihood of materially different actions. | `T02-R0038` |
| 39 | Turn arbiter evaluates likelihood of materially different strategies. | `T02-R0039` |
| 40 | Turn arbiter evaluates likelihood of recovery decisions. | `T02-R0040` |
| 41 | Turn arbiter evaluates likelihood of completion judgments. | `T02-R0041` |
| 42 | Turn arbiter evaluates likelihood of resource-allocation decisions. | `T02-R0042` |
| 43 | Turn arbiter evaluates likelihood of consequential operations. | `T02-R0043` |
| 44 | Turn arbiter evaluates likelihood of genuine routing choices. | `T02-R0044` |
| 45 | Turn arbiter evaluates likelihood of meaningful human-escalation decisions. | `T02-R0045` |
| 46 | Admission output includes OFF. | `T02-R0046` |
| 47 | Admission output includes WATCH. | `T02-R0047` |
| 48 | Admission output includes ON. | `T02-R0048` |
| 49 | OFF means no active Jev nervous-system supervision. | `T02-R0049` |
| 50 | WATCH means locally observe the event stream without routinely calling Jev. | `T02-R0050` |
| 51 | WATCH can promote itself to active supervision when a material decision emerges. | `T02-R0051` |
| 52 | ON immediately enables active Jev nervous-system supervision. | `T02-R0052` |
| 53 | Admission decision logged even when result is OFF. | `T02-R0053` |
| 54 | Admission confidence logged. | `T02-R0054` |
| 55 | Admission probabilities logged. | `T02-R0055` |
| 56 | Admission contract/version logged. | `T02-R0056` |
| 57 | Admission latency logged. | `T02-R0057` |
| 58 | Admission provider/model provenance logged. | `T02-R0058` |
| 59 | Admission results become part of later calibration data. | `T02-R0059` |
| 60 | False-negative turn admission measured. | `T02-R0060` |
| 61 | False-positive turn admission measured. | `T02-R0061` |
| 62 | WATCH mode specifically designed to mitigate admission false negatives. | `T02-R0062` |
