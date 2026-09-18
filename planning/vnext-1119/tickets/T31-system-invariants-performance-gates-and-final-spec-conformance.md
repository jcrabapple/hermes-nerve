# T31: System invariants, performance gates, and final spec conformance

**Phase:** Phase 11 — architecture consolidation

**Blocked by:** T28, T29, T30

**Status:** ready-for-agent

## What to build

Make the final design principles executable as invariant/performance/spec gates: decisions-not-tokens, async-by-default, sparse challenges, semantic state change, stale safety and useful-intervention optimization.

## Public seam(s)

End-to-end acceptance seam plus CI invariant checks.

## TDD focus

All final principles are represented by explicit acceptance tests/metrics, and full 1,119-point traceability is green.

## Acceptance criteria

- [ ] All source requirements **1102–1119** are implemented through the declared public seam(s).
- [ ] Each mapped behavior has an externally observable test or an explicitly documented live/credential-gated verification.
- [ ] No mapped requirement is moved to another ticket without updating the traceability matrix and rerunning coverage verification.
- [ ] Relevant receipts/telemetry prove behavior where the requirement is observational rather than directly user-visible.
## Source requirements owned by this ticket

| Point | Requirement | Verification ID |
|---:|---|---|
| 1102 | Jev supervises decisions, not tokens. | `T31-R1102` |
| 1103 | Jev supervises decisions, not every tool call. | `T31-R1103` |
| 1104 | Jev supervises accountable objectives, not whatever happens to look like work. | `T31-R1104` |
| 1105 | Jev can inspect the prompt once to decide whether supervision is useful. | `T31-R1105` |
| 1106 | The nervous system sees structured state rather than raw conversation wherever possible. | `T31-R1106` |
| 1107 | Hermes never waits for Jev unless a deliberately chosen precommit boundary requires it. | `T31-R1107` |
| 1108 | Most Jev agreements stay silent. | `T31-R1108` |
| 1109 | Most low-confidence Jev results stay silent. | `T31-R1109` |
| 1110 | High-confidence meaningful disagreement is the scarce signal. | `T31-R1110` |
| 1111 | State change, not event count, determines when Jev should look again. | `T31-R1111` |
| 1112 | Novelty, uncertainty, consequence, risk, and completion pressure determine Jev value. | `T31-R1112` |
| 1113 | High-volume work should make the system smarter and more compressed, not simply more expensive. | `T31-R1113` |
| 1114 | One significant contradiction can matter more than hundreds of mundane tool events. | `T31-R1114` |
| 1115 | Jev’s previous opinion remains usable until the decision state materially changes. | `T31-R1115` |
| 1116 | Stale Jev answers never blindly mutate newer state. | `T31-R1116` |
| 1117 | Completed irreversible actions are not blindly reversed because of a late Jev disagreement. | `T31-R1117` |
| 1118 | The final optimization target is useful intervention per Jev call, not Jev-call volume. | `T31-R1118` |
| 1119 | The ultimate metric is whether Jev makes Hermes complete real work more reliably. | `T31-R1119` |
