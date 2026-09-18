# T07: Jev response envelope, confidence gating, and challenge pipeline

**Phase:** Phase 3 — tandem supervision

**Blocked by:** T06

**Status:** ready-for-agent

## What to build

Normalize Jev responses and implement silent agreement/low-confidence handling plus a challenge queue/inbox for useful high-confidence disagreement.

## Public seam(s)

DecisionAssessmentResponse; ChallengeQueue; HermesChallengeInbox.

## TDD focus

Agreement never blocks; low-confidence disagreement logs; high-confidence useful conflict reaches Hermes and outcome is recorded.

## Acceptance criteria

- [ ] All source requirements **264–330** are implemented through the declared public seam(s).
- [ ] Each mapped behavior has an externally observable test or an explicitly documented live/credential-gated verification.
- [ ] No mapped requirement is moved to another ticket without updating the traceability matrix and rerunning coverage verification.
- [ ] Relevant receipts/telemetry prove behavior where the requirement is observational rather than directly user-visible.
## Source requirements owned by this ticket

| Point | Requirement | Verification ID |
|---:|---|---|
| 264 | Original event_id. | `T07-R0264` |
| 265 | Original turn_id. | `T07-R0265` |
| 266 | Original state version. | `T07-R0266` |
| 267 | Original decision version. | `T07-R0267` |
| 268 | jev_decision. | `T07-R0268` |
| 269 | Jev probabilities. | `T07-R0269` |
| 270 | Jev confidence. | `T07-R0270` |
| 271 | Agreement/disagreement disposition. | `T07-R0271` |
| 272 | Jev model. | `T07-R0272` |
| 273 | Jev provider. | `T07-R0273` |
| 274 | Jev transport. | `T07-R0274` |
| 275 | Jev request ID. | `T07-R0275` |
| 276 | Jev latency. | `T07-R0276` |
| 277 | Jev token usage. | `T07-R0277` |
| 278 | Jev cost. | `T07-R0278` |
| 279 | Jev contract. | `T07-R0279` |
| 280 | Jev supervision recommendation where applicable. | `T07-R0280` |
| 281 | Jev freshness/validity metadata. | `T07-R0281` |
| 282 | Jev watch recommendations where applicable. | `T07-R0282` |
| 283 | Low-confidence Jev answers do not interrupt Hermes. | `T07-R0283` |
| 284 | Low-confidence Jev answers may still be logged. | `T07-R0284` |
| 285 | Medium-confidence agreement normally log-only. | `T07-R0285` |
| 286 | High-confidence agreement normally log-only. | `T07-R0286` |
| 287 | High-confidence disagreement can generate a challenge. | `T07-R0287` |
| 288 | Very-high-confidence/high-consequence disagreement can generate stronger intervention. | `T07-R0288` |
| 289 | Agreement never needs to block Hermes. | `T07-R0289` |
| 290 | Most Jev responses should produce no user-visible or worker-visible interruption. | `T07-R0290` |
| 291 | Jev becomes a sparse exception channel. | `T07-R0291` |
| 292 | Confidence thresholds empirically calibrated. | `T07-R0292` |
| 293 | No permanent reliance on arbitrary example thresholds like .70/.85/.95. | `T07-R0293` |
| 294 | Confidence interpreted together with consequence. | `T07-R0294` |
| 295 | Confidence interpreted together with uncertainty. | `T07-R0295` |
| 296 | Confidence interpreted together with staleness. | `T07-R0296` |
| 297 | Confidence interpreted together with reversibility. | `T07-R0297` |
| 298 | Challenge system records why a challenge was raised. | `T07-R0298` |
| 299 | Dedicated jev_challenge component. | `T07-R0299` |
| 300 | Dedicated challenge queue. | `T07-R0300` |
| 301 | Hermes challenge inbox. | `T07-R0301` |
| 302 | Challenge associated with original decision/event. | `T07-R0302` |
| 303 | Challenge delivered only when useful. | `T07-R0303` |
| 304 | Challenge can arrive after Hermes has continued working. | `T07-R0304` |
| 305 | Challenge validated against current state before application. | `T07-R0305` |
| 306 | Challenge may modify current action when still actionable. | `T07-R0306` |
| 307 | Challenge may modify next action when current action already occurred. | `T07-R0307` |
| 308 | Challenge may be logged as stale. | `T07-R0308` |
| 309 | Challenge may be advisory only. | `T07-R0309` |
| 310 | Challenge may become precommit checkpoint for selected consequential actions. | `T07-R0310` |
| 311 | Challenge acceptance logged. | `T07-R0311` |
| 312 | Challenge rejection/override logged. | `T07-R0312` |
| 313 | Override outcome logged. | `T07-R0313` |
| 314 | Challenge usefulness later correlated with final outcomes. | `T07-R0314` |
| 315 | Hermes/Jev agreement logging. | `T07-R0315` |
| 316 | Hermes/Jev disagreement logging. | `T07-R0316` |
| 317 | No interruption for ordinary agreement. | `T07-R0317` |
| 318 | High-confidence disagreement surfaced. | `T07-R0318` |
| 319 | Final executed action logged. | `T07-R0319` |
| 320 | Whether Hermes adopted Jev correction logged. | `T07-R0320` |
| 321 | Whether Hermes correctly overrode Jev logged. | `T07-R0321` |
| 322 | Whether Jev correctly overrode Hermes logged. | `T07-R0322` |
| 323 | Outcome after agreement logged. | `T07-R0323` |
| 324 | Outcome after disagreement logged. | `T07-R0324` |
| 325 | Outcome after accepted challenge logged. | `T07-R0325` |
| 326 | Outcome after rejected challenge logged. | `T07-R0326` |
| 327 | Agreement rate metric. | `T07-R0327` |
| 328 | Disagreement rate metric. | `T07-R0328` |
| 329 | Useful-disagreement rate metric. | `T07-R0329` |
| 330 | Jev disagreement precision metric. | `T07-R0330` |
