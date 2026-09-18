# T10: Novelty, decision, evidence, risk, and uncertainty delta detectors

**Phase:** Phase 4 — adaptive routing

**Blocked by:** T09

**Status:** ready-for-agent

## What to build

Implement the state-delta detectors that raise or lower Jev value based on strategy, evidence, risk, uncertainty, novelty, contradictions and stability.

## Public seam(s)

DecisionDelta, EvidenceDelta, RiskDelta, UncertaintyDelta detector interfaces.

## TDD focus

Single significant contradiction outranks many routine events; stable/confirming sequences suppress calls.

## Acceptance criteria

- [ ] All source requirements **415–477** are implemented through the declared public seam(s).
- [ ] Each mapped behavior has an externally observable test or an explicitly documented live/credential-gated verification.
- [ ] No mapped requirement is moved to another ticket without updating the traceability matrix and rerunning coverage verification.
- [ ] Relevant receipts/telemetry prove behavior where the requirement is observational rather than directly user-visible.
## Source requirements owned by this ticket

| Point | Requirement | Verification ID |
|---:|---|---|
| 415 | decision_delta. | `T10-R0415` |
| 416 | evidence_delta. | `T10-R0416` |
| 417 | risk_delta. | `T10-R0417` |
| 418 | uncertainty_delta. | `T10-R0418` |
| 419 | completion_pressure. | `T10-R0419` |
| 420 | Strategy changes increase Jev pressure. | `T10-R0420` |
| 421 | Unexpected results increase Jev pressure. | `T10-R0421` |
| 422 | Hypothesis contradictions increase Jev pressure. | `T10-R0422` |
| 423 | Repeated failures increase Jev pressure. | `T10-R0423` |
| 424 | Falling Hermes confidence increases Jev pressure. | `T10-R0424` |
| 425 | Multiple viable paths increase Jev pressure. | `T10-R0425` |
| 426 | Approaching external mutation increases Jev pressure. | `T10-R0426` |
| 427 | Increasing cost increases Jev pressure. | `T10-R0427` |
| 428 | Increasing risk increases Jev pressure. | `T10-R0428` |
| 429 | Approaching task completion increases Jev pressure. | `T10-R0429` |
| 430 | Aging/stale Jev guidance increases Jev pressure. | `T10-R0430` |
| 431 | Repetitive work decreases Jev pressure. | `T10-R0431` |
| 432 | Stable state decreases Jev pressure. | `T10-R0432` |
| 433 | Evidence confirming the current strategy decreases Jev pressure. | `T10-R0433` |
| 434 | Redundant observations decrease Jev pressure. | `T10-R0434` |
| 435 | Easily reversible actions decrease Jev pressure. | `T10-R0435` |
| 436 | Recent Jev assessment of equivalent state decreases Jev pressure. | `T10-R0436` |
| 437 | Materially new information can immediately increase pressure. | `T10-R0437` |
| 438 | A single highly significant event can outweigh hundreds of mundane events. | `T10-R0438` |
| 439 | Detect same strategy/same trajectory. | `T10-R0439` |
| 440 | Detect meaningful strategy transition. | `T10-R0440` |
| 441 | Detect implementation-path changes. | `T10-R0441` |
| 442 | Detect hypothesis switching. | `T10-R0442` |
| 443 | Detect abandonment of current approach. | `T10-R0443` |
| 444 | Detect newly introduced alternatives. | `T10-R0444` |
| 445 | Detect closing/eliminating alternatives. | `T10-R0445` |
| 446 | Detect when Hermes is merely continuing an already-selected strategy. | `T10-R0446` |
| 447 | Continuing a stable strategy does not automatically re-call Jev. | `T10-R0447` |
| 448 | Major trajectory shift strongly triggers Jev consideration. | `T10-R0448` |
| 449 | Detect genuinely new information. | `T10-R0449` |
| 450 | Detect redundant evidence. | `T10-R0450` |
| 451 | Detect confirming evidence. | `T10-R0451` |
| 452 | Detect contradictory evidence. | `T10-R0452` |
| 453 | Detect evidence disproving active hypothesis. | `T10-R0453` |
| 454 | Detect evidence substantially changing likelihoods. | `T10-R0454` |
| 455 | Detect evidence sufficient to move from investigation to remediation. | `T10-R0455` |
| 456 | Detect evidence sufficient to move from remediation to verification. | `T10-R0456` |
| 457 | Detect evidence sufficient to consider completion. | `T10-R0457` |
| 458 | Condense multiple evidence events before Jev. | `T10-R0458` |
| 459 | Prefer state transition summaries over raw logs. | `T10-R0459` |
| 460 | Read-only introspection low risk. | `T10-R0460` |
| 461 | Local reversible edits moderate risk. | `T10-R0461` |
| 462 | Service restarts elevated risk. | `T10-R0462` |
| 463 | Git push elevated risk. | `T10-R0463` |
| 464 | Deployment elevated risk. | `T10-R0464` |
| 465 | Message/send actions elevated risk. | `T10-R0465` |
| 466 | Deletes elevated risk. | `T10-R0466` |
| 467 | Purchases or irreversible external state elevated risk. | `T10-R0467` |
| 468 | Risk trajectory used in Jev call-worthiness calculation. | `T10-R0468` |
| 469 | Risk escalation can bypass ordinary batching. | `T10-R0469` |
| 470 | Detect one obvious continuation path. | `T10-R0470` |
| 471 | Detect multiple plausible paths. | `T10-R0471` |
| 472 | Detect unresolved competing hypotheses. | `T10-R0472` |
| 473 | Detect low-confidence Hermes decision. | `T10-R0473` |
| 474 | Detect ambiguity requiring evidence. | `T10-R0474` |
| 475 | Detect ambiguity requiring human input. | `T10-R0475` |
| 476 | Increased uncertainty increases Jev call value. | `T10-R0476` |
| 477 | Reduced uncertainty suppresses unnecessary Jev calls. | `T10-R0477` |
