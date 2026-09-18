# T01: Async decision-engine foundation

**Phase:** Phase 1 — foundation

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

## What to build

Establish the production control-plane skeleton in which Hermes continues reasoning/executing while Jev supervises asynchronously, with decision epochs and batched control assessment as the primitive.

## Public seam(s)

Turn supervisor public interface; async provider boundary; decision-epoch contract.

## TDD focus

Prove Hermes does not block on normal Jev supervision; prove one assessment can carry multiple control judgments.

## Acceptance criteria

- [ ] All source requirements **1–25** are implemented through the declared public seam(s).
- [ ] Each mapped behavior has an externally observable test or an explicitly documented live/credential-gated verification.
- [ ] No mapped requirement is moved to another ticket without updating the traceability matrix and rerunning coverage verification.
- [ ] Relevant receipts/telemetry prove behavior where the requirement is observational rather than directly user-visible.
## Source requirements owned by this ticket

| Point | Requirement | Verification ID |
|---:|---|---|
| 1 | Jev as Hermes’s decision engine, not merely an optional decision tool. | `T01-R0001` |
| 2 | Hermes remains the reasoning engine. | `T01-R0002` |
| 3 | Hermes remains the execution engine. | `T01-R0003` |
| 4 | Jev becomes the decision/control plane. | `T01-R0004` |
| 5 | Jev operates as an asynchronous tandem process. | `T01-R0005` |
| 6 | Jev removed from the normal synchronous critical path. | `T01-R0006` |
| 7 | Jev operates as a parallel supervisory process. | `T01-R0007` |
| 8 | Jev operates as a decision auditor. | `T01-R0008` |
| 9 | Jev operates as a decision corrector. | `T01-R0009` |
| 10 | Jev operates as a high-confidence exception generator. | `T01-R0010` |
| 11 | Jev supervision attached to selected Hermes turns. | `T01-R0011` |
| 12 | Jev supervision can persist for the entire lifetime of a long-running autonomous turn. | `T01-R0012` |
| 13 | A supervised turn may last seconds, minutes, or hours without changing the supervision model. | `T01-R0013` |
| 14 | A turn may contain hundreds or thousands of Hermes events without creating equivalent Jev calls. | `T01-R0014` |
| 15 | Hermes continues executing while Jev evaluates. | `T01-R0015` |
| 16 | Jev’s ~500+ ms network latency treated as oversight latency, not worker latency. | `T01-R0016` |
| 17 | No synchronous Jev micro-controller loop around ordinary Hermes actions. | `T01-R0017` |
| 18 | No Jev → action → Jev → action requirement for every action. | `T01-R0018` |
| 19 | Jev controls important forks while touching only a small fraction of individual Hermes operations. | `T01-R0019` |
| 20 | Jev calls concentrated around decision epochs rather than tool-call epochs. | `T01-R0020` |
| 21 | When appropriate, one Jev call can combine verification, next-state selection, uncertainty assessment, and completion assessment. | `T01-R0021` |
| 22 | Existing jev_assess primitive reused/expanded for multi-question control assessments. | `T01-R0022` |
| 23 | New higher-level control assessment contract. | `T01-R0023` |
| 24 | New higher-level decision epoch contract. | `T01-R0024` |
| 25 | Decision supervision separate from ordinary assistant dialogue generation. | `T01-R0025` |
