# T12: Adaptive batching and supervision intensity

**Phase:** Phase 4 — adaptive routing

**Blocked by:** T09, T10, T11

**Status:** ready-for-agent

## What to build

Batch high-volume event streams into state transitions, support sparse/intensive modes, and allow Jev to recommend future watch intensity without controlling every event.

## Public seam(s)

EventBatcher; SupervisionIntensity policy.

## TDD focus

High volume compresses rather than explodes provider calls; critical events bypass batching; provenance remains traceable.

## Acceptance criteria

- [ ] All source requirements **513–556** are implemented through the declared public seam(s).
- [ ] Each mapped behavior has an externally observable test or an explicitly documented live/credential-gated verification.
- [ ] No mapped requirement is moved to another ticket without updating the traceability matrix and rerunning coverage verification.
- [ ] Relevant receipts/telemetry prove behavior where the requirement is observational rather than directly user-visible.
## Source requirements owned by this ticket

| Point | Requirement | Verification ID |
|---:|---|---|
| 513 | Event batching under high-volume execution. | `T12-R0513` |
| 514 | Repeated observations grouped. | `T12-R0514` |
| 515 | Repeated tool results summarized. | `T12-R0515` |
| 516 | Repeated failures summarized. | `T12-R0516` |
| 517 | Intermediate hypothesis evolution summarized. | `T12-R0517` |
| 518 | State transition summary sent instead of dozens of raw events. | `T12-R0518` |
| 519 | Batch may contain event count. | `T12-R0519` |
| 520 | Batch may contain tool-call count. | `T12-R0520` |
| 521 | Batch may contain failure count. | `T12-R0521` |
| 522 | Batch may contain new-hypothesis count. | `T12-R0522` |
| 523 | Batch may contain strategy-change count. | `T12-R0523` |
| 524 | Batch may contain current decision. | `T12-R0524` |
| 525 | Batch may contain current evidence delta. | `T12-R0525` |
| 526 | Batch may contain router trigger reasons. | `T12-R0526` |
| 527 | Batch may contain accumulated relevant state. | `T12-R0527` |
| 528 | Batch maintains provenance back to underlying events. | `T12-R0528` |
| 529 | Polling/batching mode retained as a concept. | `T12-R0529` |
| 530 | Polling is not based primarily on fixed every N events. | `T12-R0530` |
| 531 | Polling triggered by workload/state characteristics. | `T12-R0531` |
| 532 | Adaptive sparse mode. | `T12-R0532` |
| 533 | Adaptive intensive mode. | `T12-R0533` |
| 534 | Event pressure can change Jev granularity. | `T12-R0534` |
| 535 | Decision materiality independently changes Jev priority. | `T12-R0535` |
| 536 | High event density can decrease ordinary Jev frequency. | `T12-R0536` |
| 537 | High decision consequence can increase Jev priority even under high density. | `T12-R0537` |
| 538 | Ordinary low-value events can be accumulated locally. | `T12-R0538` |
| 539 | Important decisions bypass polling. | `T12-R0539` |
| 540 | Completion candidates bypass polling. | `T12-R0540` |
| 541 | Consequential actions bypass polling. | `T12-R0541` |
| 542 | Strategy changes bypass polling when sufficiently material. | `T12-R0542` |
| 543 | Repeated failures bypass polling. | `T12-R0543` |
| 544 | Human escalation decisions bypass polling. | `T12-R0544` |
| 545 | Irreversible actions bypass polling. | `T12-R0545` |
| 546 | High-materiality decisions bypass polling. | `T12-R0546` |
| 547 | Jev may recommend its own future supervision intensity. | `T12-R0547` |
| 548 | Jev may return supervision mode. | `T12-R0548` |
| 549 | Example SPARSE supervision mode. | `T12-R0549` |
| 550 | Example INTENSIVE supervision mode. | `T12-R0550` |
| 551 | Jev may recommend which event classes to watch. | `T12-R0551` |
| 552 | Jev may recommend looser observation when trajectory is stable. | `T12-R0552` |
| 553 | Jev may recommend tighter observation when trajectory is unstable. | `T12-R0553` |
| 554 | Jev may recommend a future polling cadence as a hint. | `T12-R0554` |
| 555 | Poll cadence remains subordinate to local critical-event overrides. | `T12-R0555` |
| 556 | Jev does not get called solely to decide whether each individual event warrants Jev. | `T12-R0556` |
