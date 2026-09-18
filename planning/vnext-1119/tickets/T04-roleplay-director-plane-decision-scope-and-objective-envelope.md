# T04: Roleplay director plane, decision scope, and objective envelope

**Phase:** Phase 1 — foundation

**Blocked by:** T03

**Status:** ready-for-agent

## What to build

Separate actor-plane roleplay from accountable director-plane decisions and persist the objective envelope/scopes Jev needs across a turn.

## Public seam(s)

ObjectiveEnvelope interface; DecisionScope type; roleplay director adapter.

## TDD focus

Pure roleplay produces no nervous-system decisions; training/director work can; all envelope fields persist through a turn.

## Acceptance criteria

- [ ] All source requirements **106–160** are implemented through the declared public seam(s).
- [ ] Each mapped behavior has an externally observable test or an explicitly documented live/credential-gated verification.
- [ ] No mapped requirement is moved to another ticket without updating the traceability matrix and rerunning coverage verification.
- [ ] Relevant receipts/telemetry prove behavior where the requirement is observational rather than directly user-visible.
## Source requirements owned by this ticket

| Point | Requirement | Verification ID |
|---:|---|---|
| 106 | Explicit Actor Plane. | `T04-R0106` |
| 107 | Explicit Director Plane. | `T04-R0107` |
| 108 | Roleplay dialogue stays in Actor Plane. | `T04-R0108` |
| 109 | Actor Plane dialogue does not become Jev decision events. | `T04-R0109` |
| 110 | Imaginary in-character decisions do not automatically invoke Jev. | `T04-R0110` |
| 111 | Roleplay transcript not continuously forwarded to Jev. | `T04-R0111` |
| 112 | Roleplay objectives can maintain a separate Director Plane. | `T04-R0112` |
| 113 | Director Plane may contain accountable real-world training objectives. | `T04-R0113` |
| 114 | Director Plane decisions may be Jev-eligible. | `T04-R0114` |
| 115 | Example director decisions include changing exercise difficulty. | `T04-R0115` |
| 116 | Example director decisions include switching objection categories. | `T04-R0116` |
| 117 | Example director decisions include repetition versus advancement. | `T04-R0117` |
| 118 | Example director decisions include stopping for critique. | `T04-R0118` |
| 119 | Simulation default Jev policy is off or observation-only. | `T04-R0119` |
| 120 | Optional simulation policy director_only. | `T04-R0120` |
| 121 | Roleplay decision scope distinguishable from fictional content. | `T04-R0121` |
| 122 | Jev never decides what Hermes should literally say next merely because Hermes is speaking. | `T04-R0122` |
| 123 | Jev supervises real decisions that occur around the roleplay when appropriate. | `T04-R0123` |
| 124 | Structured decision_scope. | `T04-R0124` |
| 125 | conversation scope. | `T04-R0125` |
| 126 | fiction scope. | `T04-R0126` |
| 127 | simulation scope. | `T04-R0127` |
| 128 | advisory scope. | `T04-R0128` |
| 129 | work scope. | `T04-R0129` |
| 130 | external scope. | `T04-R0130` |
| 131 | Default drop policy for conversation scope. | `T04-R0131` |
| 132 | Default drop policy for fiction scope. | `T04-R0132` |
| 133 | Default drop or director-only policy for simulation scope. | `T04-R0133` |
| 134 | Advisory scope generally quiet unless materially accountable. | `T04-R0134` |
| 135 | Work scope normally Jev-eligible. | `T04-R0135` |
| 136 | External/consequential scope high priority. | `T04-R0136` |
| 137 | Decision scope included in event receipts. | `T04-R0137` |
| 138 | Decision scope included in router state. | `T04-R0138` |
| 139 | Decision scope usable as a router relevance feature. | `T04-R0139` |
| 140 | Persistent structured objective envelope. | `T04-R0140` |
| 141 | Earlier Work Envelope generalized beyond literal work. | `T04-R0141` |
| 142 | Objective ID. | `T04-R0142` |
| 143 | Goal ID. | `T04-R0143` |
| 144 | Goal description. | `T04-R0144` |
| 145 | Turn ID. | `T04-R0145` |
| 146 | Work/session ID where applicable. | `T04-R0146` |
| 147 | Done criteria. | `T04-R0147` |
| 148 | Current status. | `T04-R0148` |
| 149 | Current strategy. | `T04-R0149` |
| 150 | Active hypothesis. | `T04-R0150` |
| 151 | Decision context. | `T04-R0151` |
| 152 | Interaction type. | `T04-R0152` |
| 153 | Jev supervision policy. | `T04-R0153` |
| 154 | Jev admission result. | `T04-R0154` |
| 155 | Jev admission confidence. | `T04-R0155` |
| 156 | Allowed/priority event types. | `T04-R0156` |
| 157 | Current risk/consequence state. | `T04-R0157` |
| 158 | Current reversibility state. | `T04-R0158` |
| 159 | Current completion evidence. | `T04-R0159` |
| 160 | Active Jev decision/freshness state. | `T04-R0160` |
