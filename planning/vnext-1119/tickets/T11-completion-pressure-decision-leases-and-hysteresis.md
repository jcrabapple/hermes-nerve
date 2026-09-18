# T11: Completion pressure, decision leases, and hysteresis

**Phase:** Phase 4 — adaptive routing

**Blocked by:** T07, T09, T10

**Status:** ready-for-agent

## What to build

Treat completion as high-value supervision, keep Jev decisions valid through a lease while state is equivalent, and prevent call storms with semantic hysteresis.

## Public seam(s)

CompletionPressure detector; DecisionLeaseManager; Hysteresis policy.

## TDD focus

Completion bypasses sparse suppression; lease invalidates on material change; repeated equivalent evidence does not retrigger Jev.

## Acceptance criteria

- [ ] All source requirements **478–512** are implemented through the declared public seam(s).
- [ ] Each mapped behavior has an externally observable test or an explicitly documented live/credential-gated verification.
- [ ] No mapped requirement is moved to another ticket without updating the traceability matrix and rerunning coverage verification.
- [ ] Relevant receipts/telemetry prove behavior where the requirement is observational rather than directly user-visible.
## Source requirements owned by this ticket

| Point | Requirement | Verification ID |
|---:|---|---|
| 478 | Detect transition from active work toward I think this is done. | `T11-R0478` |
| 479 | Detect COMPLETION_CANDIDATE. | `T11-R0479` |
| 480 | Completion events receive high Jev priority. | `T11-R0480` |
| 481 | Completion review can bypass sparse polling. | `T11-R0481` |
| 482 | Jev checks whether observed evidence satisfies done criteria. | `T11-R0482` |
| 483 | Jev can return DONE. | `T11-R0483` |
| 484 | Jev can return NOT_DONE. | `T11-R0484` |
| 485 | Jev can return NEEDS_VERIFICATION. | `T11-R0485` |
| 486 | Completion assessment can map to PASS/RETRY/REPLAN/ESCALATE. | `T11-R0486` |
| 487 | Premature completion detection. | `T11-R0487` |
| 488 | False PASS treated as a critical metric. | `T11-R0488` |
| 489 | Completion decisions tied to explicit objective done criteria. | `T11-R0489` |
| 490 | Jev decisions can remain valid across multiple Hermes actions. | `T11-R0490` |
| 491 | Decision lease concept. | `T11-R0491` |
| 492 | Lease allows Hermes to act autonomously under an already-selected strategy. | `T11-R0492` |
| 493 | Lease remains valid while decision state stays materially equivalent. | `T11-R0493` |
| 494 | Lease invalidated when active hypothesis is disproven. | `T11-R0494` |
| 495 | Lease invalidated by material failure. | `T11-R0495` |
| 496 | Lease invalidated by major strategy change. | `T11-R0496` |
| 497 | Lease invalidated when destructive/consequential action boundary appears. | `T11-R0497` |
| 498 | Lease invalidated when enough evidence exists to advance state. | `T11-R0498` |
| 499 | Lease invalidated when relevant state version changes materially. | `T11-R0499` |
| 500 | Lease reduces repeated Jev calls. | `T11-R0500` |
| 501 | Router checks Jev freshness before calling again. | `T11-R0501` |
| 502 | Hysteresis based on meaningful state change rather than time alone. | `T11-R0502` |
| 503 | Post-Jev-call hysteresis. | `T11-R0503` |
| 504 | Repeated equivalent observations do not immediately trigger another call. | `T11-R0504` |
| 505 | Confirming evidence alone normally does not trigger. | `T11-R0505` |
| 506 | Same-hypothesis file reads normally do not trigger. | `T11-R0506` |
| 507 | Unexpected failure can break hysteresis. | `T11-R0507` |
| 508 | Contradictory evidence can break hysteresis. | `T11-R0508` |
| 509 | Strategy transition can break hysteresis. | `T11-R0509` |
| 510 | Completion candidate can break hysteresis. | `T11-R0510` |
| 511 | High-risk boundary can break hysteresis. | `T11-R0511` |
| 512 | Hysteresis prevents Jev call storms. | `T11-R0512` |
