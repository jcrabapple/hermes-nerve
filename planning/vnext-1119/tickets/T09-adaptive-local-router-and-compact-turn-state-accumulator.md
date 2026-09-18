# T09: Adaptive local router and compact turn-state accumulator

**Phase:** Phase 4 — adaptive routing

**Blocked by:** T05, T06

**Status:** ready-for-agent

## What to build

Build the local stateful router that consumes all Hermes events, accumulates compact turn state, compresses events and decides whether remote Jev could matter.

## Public seam(s)

AdaptiveRouter public interface; TurnStateAccumulator; EventCompressor.

## TDD focus

Hundreds of low-value events can update local state without remote calls; router state exposes every required signal.

## Acceptance criteria

- [ ] All source requirements **365–414** are implemented through the declared public seam(s).
- [ ] Each mapped behavior has an externally observable test or an explicitly documented live/credential-gated verification.
- [ ] No mapped requirement is moved to another ticket without updating the traceability matrix and rerunning coverage verification.
- [ ] Relevant receipts/telemetry prove behavior where the requirement is observational rather than directly user-visible.
## Source requirements owned by this ticket

| Point | Requirement | Verification ID |
|---:|---|---|
| 365 | Dedicated local adaptive relevance engine. | `T09-R0365` |
| 366 | Dedicated jev_supervisor. | `T09-R0366` |
| 367 | Router consumes all structured Hermes events. | `T09-R0367` |
| 368 | Router does not send all events remotely. | `T09-R0368` |
| 369 | Router maintains compact local turn state. | `T09-R0369` |
| 370 | Router accumulates state over time. | `T09-R0370` |
| 371 | Router performs event compression. | `T09-R0371` |
| 372 | Router performs novelty detection. | `T09-R0372` |
| 373 | Router performs decision-change detection. | `T09-R0373` |
| 374 | Router performs risk-change detection. | `T09-R0374` |
| 375 | Router performs uncertainty-change detection. | `T09-R0375` |
| 376 | Router performs evidence-change detection. | `T09-R0376` |
| 377 | Router performs completion-pressure detection. | `T09-R0377` |
| 378 | Router estimates whether another Jev call can plausibly change Hermes’s behavior. | `T09-R0378` |
| 379 | Router treats Jev calls as a resource with expected value. | `T09-R0379` |
| 380 | Router suppresses redundant Jev calls. | `T09-R0380` |
| 381 | Router batches related events. | `T09-R0381` |
| 382 | Router consolidates repetitive observations. | `T09-R0382` |
| 383 | Router can remain local for hundreds of events. | `T09-R0383` |
| 384 | Router forwards one state transition instead of raw event history when appropriate. | `T09-R0384` |
| 385 | Current goal. | `T09-R0385` |
| 386 | Current objective. | `T09-R0386` |
| 387 | Current strategy. | `T09-R0387` |
| 388 | Active hypothesis. | `T09-R0388` |
| 389 | Recent decisions. | `T09-R0389` |
| 390 | Recent failures. | `T09-R0390` |
| 391 | Recent retries. | `T09-R0391` |
| 392 | Recent strategy changes. | `T09-R0392` |
| 393 | Recent evidence. | `T09-R0393` |
| 394 | Evidence novelty. | `T09-R0394` |
| 395 | Confidence trend. | `T09-R0395` |
| 396 | Tool/result novelty. | `T09-R0396` |
| 397 | Contradictions. | `T09-R0397` |
| 398 | Pending irreversible actions. | `T09-R0398` |
| 399 | Pending consequential actions. | `T09-R0399` |
| 400 | Completion evidence. | `T09-R0400` |
| 401 | Current completion confidence/state. | `T09-R0401` |
| 402 | Last Jev opinion. | `T09-R0402` |
| 403 | Last Jev decision state. | `T09-R0403` |
| 404 | Last Jev state version. | `T09-R0404` |
| 405 | Last Jev trigger reason. | `T09-R0405` |
| 406 | Last Jev challenge outcome. | `T09-R0406` |
| 407 | Jev freshness. | `T09-R0407` |
| 408 | Relevant event summary. | `T09-R0408` |
| 409 | Event density. | `T09-R0409` |
| 410 | Recent failure density. | `T09-R0410` |
| 411 | Decision uncertainty. | `T09-R0411` |
| 412 | Current reversibility. | `T09-R0412` |
| 413 | Current materiality. | `T09-R0413` |
| 414 | Current consequence level. | `T09-R0414` |
