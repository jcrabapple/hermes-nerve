# T06: Decision request schema with Hermes proposal embedded

**Phase:** Phase 2 — event substrate

**Blocked by:** T05

**Status:** ready-for-agent

## What to build

Create the canonical decision event/request shape containing Hermes’s proposed choice, alternatives, state, evidence, materiality, reversibility and versions in the original event.

## Public seam(s)

DecisionEvent schema; DecisionAssessmentRequest builder.

## TDD focus

One emitted decision event is sufficient for Jev to compare against Hermes without a follow-up query.

## Acceptance criteria

- [ ] All source requirements **228–263** are implemented through the declared public seam(s).
- [ ] Each mapped behavior has an externally observable test or an explicitly documented live/credential-gated verification.
- [ ] No mapped requirement is moved to another ticket without updating the traceability matrix and rerunning coverage verification.
- [ ] Relevant receipts/telemetry prove behavior where the requirement is observational rather than directly user-visible.
## Source requirements owned by this ticket

| Point | Requirement | Verification ID |
|---:|---|---|
| 228 | Hermes’s proposed decision embedded in the original structured event. | `T06-R0228` |
| 229 | No second request asking Hermes what decision did you make. | `T06-R0229` |
| 230 | hermes_decision field. | `T06-R0230` |
| 231 | Candidate choices included with the event. | `T06-R0231` |
| 232 | Hermes reason summary optionally included. | `T06-R0232` |
| 233 | Relevant evidence included. | `T06-R0233` |
| 234 | Relevant state included. | `T06-R0234` |
| 235 | Materiality included. | `T06-R0235` |
| 236 | Reversibility included. | `T06-R0236` |
| 237 | Objective included. | `T06-R0237` |
| 238 | State version included. | `T06-R0238` |
| 239 | Decision version included. | `T06-R0239` |
| 240 | Jev evaluates the decision Hermes has already proposed. | `T06-R0240` |
| 241 | Agreement can be detected without another Hermes round trip. | `T06-R0241` |
| 242 | Disagreement can be detected without another Hermes round trip. | `T06-R0242` |
| 243 | event_id. | `T06-R0243` |
| 244 | turn_id. | `T06-R0244` |
| 245 | work_session_id/objective ID. | `T06-R0245` |
| 246 | decision_id. | `T06-R0246` |
| 247 | type. | `T06-R0247` |
| 248 | scope. | `T06-R0248` |
| 249 | goal. | `T06-R0249` |
| 250 | state. | `T06-R0250` |
| 251 | choices. | `T06-R0251` |
| 252 | hermes_decision. | `T06-R0252` |
| 253 | reason_summary. | `T06-R0253` |
| 254 | materiality. | `T06-R0254` |
| 255 | reversible. | `T06-R0255` |
| 256 | state_version. | `T06-R0256` |
| 257 | decision_version. | `T06-R0257` |
| 258 | contract. | `T06-R0258` |
| 259 | evidence. | `T06-R0259` |
| 260 | current_strategy. | `T06-R0260` |
| 261 | active_hypothesis. | `T06-R0261` |
| 262 | consequence. | `T06-R0262` |
| 263 | decision_context. | `T06-R0263` |
