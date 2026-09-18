# T13: Expected-value routing, materiality, and safety budgets

**Phase:** Phase 4 — adaptive routing

**Blocked by:** T10, T12

**Status:** ready-for-agent

## What to build

Replace hard-coded N-event polling with an expected-value call policy combining usefulness probability, consequence, uncertainty, novelty, materiality, risk, freshness, cost and staleness, with budgets only as safety rails.

## Public seam(s)

JevCallPolicy interface; Materiality model; ProviderBudget safety valve.

## TDD focus

No primary fixed-event trigger exists; same event count can yield different call behavior based on state significance.

## Acceptance criteria

- [ ] All source requirements **557–589** are implemented through the declared public seam(s).
- [ ] Each mapped behavior has an externally observable test or an explicitly documented live/credential-gated verification.
- [ ] No mapped requirement is moved to another ticket without updating the traceability matrix and rerunning coverage verification.
- [ ] Relevant receipts/telemetry prove behavior where the requirement is observational rather than directly user-visible.
## Source requirements owned by this ticket

| Point | Requirement | Verification ID |
|---:|---|---|
| 557 | Explicit concept of expected value of a Jev call. | `T13-R0557` |
| 558 | Estimate probability Jev will produce a useful disagreement. | `T13-R0558` |
| 559 | Weight by consequence of current decision. | `T13-R0559` |
| 560 | Weight by uncertainty. | `T13-R0560` |
| 561 | Weight by novelty. | `T13-R0561` |
| 562 | Weight by materiality. | `T13-R0562` |
| 563 | Weight by risk. | `T13-R0563` |
| 564 | Weight by Jev freshness. | `T13-R0564` |
| 565 | Subtract provider cost. | `T13-R0565` |
| 566 | Subtract latency cost. | `T13-R0566` |
| 567 | Subtract stale-answer risk. | `T13-R0567` |
| 568 | Subtract redundant-call penalty. | `T13-R0568` |
| 569 | Invoke Jev when expected benefit is sufficiently positive. | `T13-R0569` |
| 570 | No requirement that expected-value logic literally use a single hand-coded equation. | `T13-R0570` |
| 571 | Design philosophy centered on could another Jev opinion materially matter now? | `T13-R0571` |
| 572 | No primary call Jev every 10 events behavior. | `T13-R0572` |
| 573 | No primary call Jev after 25 events behavior. | `T13-R0573` |
| 574 | No primary call Jev after 100 tool calls behavior. | `T13-R0574` |
| 575 | Event counts may remain as contextual signals. | `T13-R0575` |
| 576 | Event counts may remain as diagnostics. | `T13-R0576` |
| 577 | Event counts may remain as emergency ceilings. | `T13-R0577` |
| 578 | Hard maximum/provider budget only as a safety valve. | `T13-R0578` |
| 579 | Adaptive state relevance remains primary call trigger. | `T13-R0579` |
| 580 | Continuous materiality signal. | `T13-R0580` |
| 581 | Earlier 0–5 materiality idea retained as a conceptual feature if useful. | `T13-R0581` |
| 582 | Materiality not used as a single permanent hard-coded threshold. | `T13-R0582` |
| 583 | Trivial operational details very low materiality. | `T13-R0583` |
| 584 | Meaningful but reversible details low/moderate materiality. | `T13-R0584` |
| 585 | Strategy-changing choices high materiality. | `T13-R0585` |
| 586 | External/irreversible choices high materiality. | `T13-R0586` |
| 587 | Completion high materiality. | `T13-R0587` |
| 588 | Materiality combined with uncertainty and consequence. | `T13-R0588` |
| 589 | Materiality included in telemetry. | `T13-R0589` |
