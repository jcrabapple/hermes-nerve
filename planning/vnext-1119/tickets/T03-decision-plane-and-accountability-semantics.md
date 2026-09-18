# T03: Decision-plane and accountability semantics

**Phase:** Phase 1 — foundation

**Blocked by:** T02

**Status:** ready-for-agent

## What to build

Represent interaction type separately from decision context and determine Jev eligibility from accountable decision semantics rather than chat/tool surface.

## Public seam(s)

DecisionPlaneClassifier local interface; objective context interface.

## TDD focus

Conversation, research, creative, operational, and chat-looking-work fixtures classify correctly without tool-call heuristics.

## Acceptance criteria

- [ ] All source requirements **63–105** are implemented through the declared public seam(s).
- [ ] Each mapped behavior has an externally observable test or an explicitly documented live/credential-gated verification.
- [ ] No mapped requirement is moved to another ticket without updating the traceability matrix and rerunning coverage verification.
- [ ] Relevant receipts/telemetry prove behavior where the requirement is observational rather than directly user-visible.
## Source requirements owned by this ticket

| Point | Requirement | Verification ID |
|---:|---|---|
| 63 | Explicit internal concept of a decision plane. | `T03-R0063` |
| 64 | Decision plane independent from whether the UI interaction looks conversational. | `T03-R0064` |
| 65 | Decision plane independent from whether tools are being used. | `T03-R0065` |
| 66 | Decision plane independent from whether the assistant is roleplaying. | `T03-R0066` |
| 67 | Decision plane independent from whether the user calls something work. | `T03-R0067` |
| 68 | Decision plane based primarily on accountability. | `T03-R0068` |
| 69 | Accountable decision defined around whether the result matters beyond producing the next conversational turn. | `T03-R0069` |
| 70 | Decision must belong to an active objective before becoming normally Jev-eligible. | `T03-R0070` |
| 71 | Decision should have materially different alternatives. | `T03-R0071` |
| 72 | Decision should be capable of changing trajectory, outcome, risk, cost, or completion state. | `T03-R0072` |
| 73 | Immediate conversational wording choices excluded by default. | `T03-R0073` |
| 74 | Fictional character choices excluded by default. | `T03-R0074` |
| 75 | Pure stylistic decisions excluded by default. | `T03-R0075` |
| 76 | Ordinary conversational responses excluded by default. | `T03-R0076` |
| 77 | Material real-world/workflow decisions eligible. | `T03-R0077` |
| 78 | Material training/director decisions eligible. | `T03-R0078` |
| 79 | Material engineering decisions eligible. | `T03-R0079` |
| 80 | Material operational decisions eligible. | `T03-R0080` |
| 81 | Material resource decisions eligible. | `T03-R0081` |
| 82 | Material recovery decisions eligible. | `T03-R0082` |
| 83 | Material completion decisions eligible. | `T03-R0083` |
| 84 | Separate interaction_type from Jev supervision state. | `T03-R0084` |
| 85 | CONVERSATION interaction type. | `T03-R0085` |
| 86 | ROLEPLAY interaction type. | `T03-R0086` |
| 87 | RESEARCH interaction type. | `T03-R0087` |
| 88 | CREATIVE interaction type. | `T03-R0088` |
| 89 | OPERATIONAL interaction type. | `T03-R0089` |
| 90 | Separate decision_context. | `T03-R0090` |
| 91 | NONE decision context. | `T03-R0091` |
| 92 | SIMULATION decision context. | `T03-R0092` |
| 93 | ADVISORY decision context. | `T03-R0093` |
| 94 | WORK decision context. | `T03-R0094` |
| 95 | Potential EXTERNAL/consequential decision context. | `T03-R0095` |
| 96 | Conversational-looking work can still receive decision supervision. | `T03-R0096` |
| 97 | Operational-looking activity can still remain Jev-free if no meaningful decision exists. | `T03-R0097` |
| 98 | Research generally stays outside Jev unless research results control subsequent work. | `T03-R0098` |
| 99 | Brainstorming generally remains Jev-free. | `T03-R0099` |
| 100 | Moving from brainstorming to implementation may create a decision plane. | `T03-R0100` |
| 101 | Read-only activity does not automatically imply Jev supervision. | `T03-R0101` |
| 102 | Tool usage does not automatically imply Jev supervision. | `T03-R0102` |
| 103 | Mutation intent is a strong signal but not sufficient alone. | `T03-R0103` |
| 104 | External-state changes are stronger Jev candidates. | `T03-R0104` |
| 105 | Consequential external-state decisions receive elevated priority. | `T03-R0105` |
