# T08: Stale-response protection, reversibility, and supervision modes

**Phase:** Phase 3 — tandem supervision

**Blocked by:** T07

**Status:** ready-for-agent

## What to build

Validate late Jev responses against current state, respect reversibility/commit status, and support SHADOW, CORRECT_NEXT and PRECOMMIT authority modes.

## Public seam(s)

StateVersion interface; ChallengeValidator; SupervisionMode policy.

## TDD focus

Stale challenges cannot mutate new state; irreversible completed actions are never blindly undone; PRECOMMIT is narrow and explicit.

## Acceptance criteria

- [ ] All source requirements **331–364** are implemented through the declared public seam(s).
- [ ] Each mapped behavior has an externally observable test or an explicitly documented live/credential-gated verification.
- [ ] No mapped requirement is moved to another ticket without updating the traceability matrix and rerunning coverage verification.
- [ ] Relevant receipts/telemetry prove behavior where the requirement is observational rather than directly user-visible.
## Source requirements owned by this ticket

| Point | Requirement | Verification ID |
|---:|---|---|
| 331 | State-versioned Jev requests. | `T08-R0331` |
| 332 | Decision-versioned Jev requests. | `T08-R0332` |
| 333 | State-versioned Jev responses. | `T08-R0333` |
| 334 | Jev response validity check before action. | `T08-R0334` |
| 335 | Current-state equality/compatibility check. | `T08-R0335` |
| 336 | Stale Jev result detection. | `T08-R0336` |
| 337 | Stale Jev results never blindly applied. | `T08-R0337` |
| 338 | Stale results can remain telemetry. | `T08-R0338` |
| 339 | Stale results can inform a subsequent decision. | `T08-R0339` |
| 340 | State version can use semantic version IDs. | `T08-R0340` |
| 341 | State version can use commit SHA. | `T08-R0341` |
| 342 | State version can use tree hash. | `T08-R0342` |
| 343 | State version can use test-run ID. | `T08-R0343` |
| 344 | State version can use tool receipt ID. | `T08-R0344` |
| 345 | State version can use other workflow-specific immutable identifiers. | `T08-R0345` |
| 346 | Explicit reversibility metadata. | `T08-R0346` |
| 347 | Explicit committed/uncommitted state. | `T08-R0347` |
| 348 | Jev disagreement before reversible uncommitted action may change the decision. | `T08-R0348` |
| 349 | Jev disagreement after committed action does not blindly undo it. | `T08-R0349` |
| 350 | Post-commit disagreement influences the next decision. | `T08-R0350` |
| 351 | Consequential but not-yet-committed actions may use precommit supervision. | `T08-R0351` |
| 352 | Irreversible actions receive elevated router priority. | `T08-R0352` |
| 353 | External sends/deploys/deletes/pushes can receive elevated priority. | `T08-R0353` |
| 354 | No automatic reverse-whatever-Hermes-just-did behavior. | `T08-R0354` |
| 355 | Recovery after already-executed action treated as a new decision. | `T08-R0355` |
| 356 | SHADOW mode. | `T08-R0356` |
| 357 | CORRECT_NEXT mode. | `T08-R0357` |
| 358 | PRECOMMIT mode. | `T08-R0358` |
| 359 | SHADOW logs Jev opinions without changing execution. | `T08-R0359` |
| 360 | CORRECT_NEXT allows Jev to influence future action. | `T08-R0360` |
| 361 | PRECOMMIT can briefly gate selected high-consequence boundaries. | `T08-R0361` |
| 362 | Most operation remains asynchronous. | `T08-R0362` |
| 363 | Synchronous behavior restricted to deliberately chosen consequential checkpoints. | `T08-R0363` |
| 364 | Existing synchronous gating no longer primary architecture. | `T08-R0364` |
