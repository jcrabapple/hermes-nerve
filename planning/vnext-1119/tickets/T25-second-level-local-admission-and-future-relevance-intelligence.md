# T25: Second-level local admission and future relevance intelligence

**Phase:** Phase 9 — vertical integration

**Blocked by:** T18, T23, T24

**Status:** ready-for-agent

## What to build

Make the local router the second admission layer inside an admitted turn and expose a future lightweight statistical/classifier adapter driven by router features.

## Public seam(s)

LocalAdmissionPolicy plus LocalRelevanceModel seam.

## TDD focus

Turn admission and per-state admission remain distinct; no remote Jev is used to decide every local routing event.

## Acceptance criteria

- [ ] All source requirements **975–992** are implemented through the declared public seam(s).
- [ ] Each mapped behavior has an externally observable test or an explicitly documented live/credential-gated verification.
- [ ] No mapped requirement is moved to another ticket without updating the traceability matrix and rerunning coverage verification.
- [ ] Relevant receipts/telemetry prove behavior where the requirement is observational rather than directly user-visible.
## Source requirements owned by this ticket

| Point | Requirement | Verification ID |
|---:|---|---|
| 975 | Local router acts as second-level admission after turn-level Jev admission. | `T25-R0975` |
| 976 | Turn admission answers could this turn need Jev? | `T25-R0976` |
| 977 | Local router answers does Jev matter right now? | `T25-R0977` |
| 978 | Jev itself not invoked for every local router decision. | `T25-R0978` |
| 979 | Local router designed to be far cheaper than remote Jev. | `T25-R0979` |
| 980 | Local router stateful across the turn. | `T25-R0980` |
| 981 | Local router decision based on state deltas rather than raw event count. | `T25-R0981` |
| 982 | Critical-event bypass always available. | `T25-R0982` |
| 983 | Lightweight local statistical model. | `T25-R0983` |
| 984 | Lightweight classifier. | `T25-R0984` |
| 985 | No need for full conversational intelligence. | `T25-R0985` |
| 986 | Input primarily router-state features. | `T25-R0986` |
| 987 | Output useful-disagreement probability. | `T25-R0987` |
| 988 | Potential confidence calibration. | `T25-R0988` |
| 989 | Potential event-type calibration. | `T25-R0989` |
| 990 | Potential per-objective calibration. | `T25-R0990` |
| 991 | Potential model-specific calibration. | `T25-R0991` |
| 992 | Potential online/offline tuning from collected receipts. | `T25-R0992` |
