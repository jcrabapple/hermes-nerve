# Hermes-Jev vNext Implementation Plan

## Destination

Ship an asynchronous, adaptive Jev decision nervous system for Hermes that preserves all 1,119 requirements, uses remote Jev only when decision value justifies it, and keeps ordinary Hermes work out of the ~500 ms provider critical path.

## Execution strategy

Start with `P00` to falsify the state model cheaply. Then work the task graph frontier rather than treating the tickets as a serial checklist. Each T-ticket is a tracer-bullet slice with a public seam and TDD focus. Parallelize tickets only when their blocking edges are clear. Integrate onto one vNext branch, run T27 adversarial scenarios, T28 defaults, T29 release integrity, T30 consolidation, then T31 final invariant/spec review.

## Phase 1 — foundation

### T01 — Async decision-engine foundation

- **Blocked by:** None
- **Owns:** 1–25 (25 points)
- **Outcome:** Establish the production control-plane skeleton in which Hermes continues reasoning/executing while Jev supervises asynchronously, with decision epochs and batched control assessment as the primitive.
- **Seam:** Turn supervisor public interface; async provider boundary; decision-epoch contract.
- **Verification focus:** Prove Hermes does not block on normal Jev supervision; prove one assessment can carry multiple control judgments.

### T02 — Turn arbiter: OFF / WATCH / ON

- **Blocked by:** T01
- **Owns:** 26–62 (37 points)
- **Outcome:** Add one non-recursive Jev admission assessment per user turn, dispatched in parallel with Hermes, producing OFF/WATCH/ON plus complete admission telemetry.
- **Seam:** TurnAdmission interface at prompt ingress; Jev provider adapter behind it.
- **Verification focus:** Casual chat OFF, ambiguous operational WATCH, explicit autonomous work ON; admission never blocks initial Hermes work.

### T03 — Decision-plane and accountability semantics

- **Blocked by:** T02
- **Owns:** 63–105 (43 points)
- **Outcome:** Represent interaction type separately from decision context and determine Jev eligibility from accountable decision semantics rather than chat/tool surface.
- **Seam:** DecisionPlaneClassifier local interface; objective context interface.
- **Verification focus:** Conversation, research, creative, operational, and chat-looking-work fixtures classify correctly without tool-call heuristics.

### T04 — Roleplay director plane, decision scope, and objective envelope

- **Blocked by:** T03
- **Owns:** 106–160 (55 points)
- **Outcome:** Separate actor-plane roleplay from accountable director-plane decisions and persist the objective envelope/scopes Jev needs across a turn.
- **Seam:** ObjectiveEnvelope interface; DecisionScope type; roleplay director adapter.
- **Verification focus:** Pure roleplay produces no nervous-system decisions; training/director work can; all envelope fields persist through a turn.

## Phase 2 — event substrate

### T05 — Structured Hermes event bus and high-value event taxonomy

- **Blocked by:** T01, T04
- **Owns:** 161–227 (67 points)
- **Outcome:** Emit structured runtime events independent of assistant prose and define the event/decision categories that can feed the local nervous system.
- **Seam:** JevEventBus public seam; typed event schema; provenance/version fields.
- **Verification focus:** Runtime emits typed events with IDs/provenance; raw assistant text is not parsed to discover decisions.

### T06 — Decision request schema with Hermes proposal embedded

- **Blocked by:** T05
- **Owns:** 228–263 (36 points)
- **Outcome:** Create the canonical decision event/request shape containing Hermes’s proposed choice, alternatives, state, evidence, materiality, reversibility and versions in the original event.
- **Seam:** DecisionEvent schema; DecisionAssessmentRequest builder.
- **Verification focus:** One emitted decision event is sufficient for Jev to compare against Hermes without a follow-up query.

## Phase 3 — tandem supervision

### T07 — Jev response envelope, confidence gating, and challenge pipeline

- **Blocked by:** T06
- **Owns:** 264–330 (67 points)
- **Outcome:** Normalize Jev responses and implement silent agreement/low-confidence handling plus a challenge queue/inbox for useful high-confidence disagreement.
- **Seam:** DecisionAssessmentResponse; ChallengeQueue; HermesChallengeInbox.
- **Verification focus:** Agreement never blocks; low-confidence disagreement logs; high-confidence useful conflict reaches Hermes and outcome is recorded.

### T08 — Stale-response protection, reversibility, and supervision modes

- **Blocked by:** T07
- **Owns:** 331–364 (34 points)
- **Outcome:** Validate late Jev responses against current state, respect reversibility/commit status, and support SHADOW, CORRECT_NEXT and PRECOMMIT authority modes.
- **Seam:** StateVersion interface; ChallengeValidator; SupervisionMode policy.
- **Verification focus:** Stale challenges cannot mutate new state; irreversible completed actions are never blindly undone; PRECOMMIT is narrow and explicit.

## Phase 4 — adaptive routing

### T09 — Adaptive local router and compact turn-state accumulator

- **Blocked by:** T05, T06
- **Owns:** 365–414 (50 points)
- **Outcome:** Build the local stateful router that consumes all Hermes events, accumulates compact turn state, compresses events and decides whether remote Jev could matter.
- **Seam:** AdaptiveRouter public interface; TurnStateAccumulator; EventCompressor.
- **Verification focus:** Hundreds of low-value events can update local state without remote calls; router state exposes every required signal.

### T10 — Novelty, decision, evidence, risk, and uncertainty delta detectors

- **Blocked by:** T09
- **Owns:** 415–477 (63 points)
- **Outcome:** Implement the state-delta detectors that raise or lower Jev value based on strategy, evidence, risk, uncertainty, novelty, contradictions and stability.
- **Seam:** DecisionDelta, EvidenceDelta, RiskDelta, UncertaintyDelta detector interfaces.
- **Verification focus:** Single significant contradiction outranks many routine events; stable/confirming sequences suppress calls.

### T11 — Completion pressure, decision leases, and hysteresis

- **Blocked by:** T07, T09, T10
- **Owns:** 478–512 (35 points)
- **Outcome:** Treat completion as high-value supervision, keep Jev decisions valid through a lease while state is equivalent, and prevent call storms with semantic hysteresis.
- **Seam:** CompletionPressure detector; DecisionLeaseManager; Hysteresis policy.
- **Verification focus:** Completion bypasses sparse suppression; lease invalidates on material change; repeated equivalent evidence does not retrigger Jev.

### T12 — Adaptive batching and supervision intensity

- **Blocked by:** T09, T10, T11
- **Owns:** 513–556 (44 points)
- **Outcome:** Batch high-volume event streams into state transitions, support sparse/intensive modes, and allow Jev to recommend future watch intensity without controlling every event.
- **Seam:** EventBatcher; SupervisionIntensity policy.
- **Verification focus:** High volume compresses rather than explodes provider calls; critical events bypass batching; provenance remains traceable.

### T13 — Expected-value routing, materiality, and safety budgets

- **Blocked by:** T10, T12
- **Owns:** 557–589 (33 points)
- **Outcome:** Replace hard-coded N-event polling with an expected-value call policy combining usefulness probability, consequence, uncertainty, novelty, materiality, risk, freshness, cost and staleness, with budgets only as safety rails.
- **Seam:** JevCallPolicy interface; Materiality model; ProviderBudget safety valve.
- **Verification focus:** No primary fixed-event trigger exists; same event count can yield different call behavior based on state significance.

## Phase 5 — decision contracts

### T14 — Control states, recovery, and ambiguity handling

- **Blocked by:** T06, T13
- **Owns:** 590–624 (35 points)
- **Outcome:** Standardize bounded control states and recovery/evidence/human-escalation decisions for supervised work.
- **Seam:** ControlDecision contract; RecoveryDecision contract.
- **Verification focus:** RETRY/REPLAN/ESCALATE/GATHER_EVIDENCE/ASK_HUMAN semantics are behaviorally distinct and loop detection is covered.

### T15 — Resource routing and multi-question control assessment

- **Blocked by:** T14
- **Owns:** 625–646 (22 points)
- **Outcome:** Support bounded routing/ranking choices and combine previous-result, next-action, evidence, completion, confidence and supervision questions into a single Jev assessment.
- **Seam:** RoutingDecision contract; ControlAssessment batch interface.
- **Verification focus:** A single provider request can answer all related control questions and route bounded worker/tool/environment candidates.

### T16 — Useful-work filter and legacy gate demotion

- **Blocked by:** T09, T13
- **Owns:** 647–667 (21 points)
- **Outcome:** Keep routine introspection local, treat tools as signals rather than work definitions, and retain selective pre-tool gating only as compatibility/precommit behavior.
- **Seam:** LocalAdmissionPolicy; legacy GateAdapter.
- **Verification focus:** Reads/status/tests without a decision fork do not trigger remote Jev; high-consequence precommit remains possible.

## Phase 6 — compatibility

### T17 — Compatibility layer for existing tools, hooks, and context engine

- **Blocked by:** T16
- **Owns:** 668–700 (33 points)
- **Outcome:** Preserve existing Jev tools/hooks/context surfaces while placing the new nervous system above them and keeping context shadow-first with rehydration capabilities intact.
- **Seam:** Compatibility adapter for existing tool registry/hooks/context engine.
- **Verification focus:** All seven existing tools and both hooks still register; existing context fallback works; anchor/rehydrate remains available.

## Phase 7 — observability and learning

### T18 — Outcome learning dataset and future local classifier seam

- **Blocked by:** T07, T09
- **Owns:** 701–750 (50 points)
- **Outcome:** Persist normalized decision outcomes and create the local-classifier seam so the router can later learn where Jev disagreement is valuable without adding another remote LLM.
- **Seam:** OutcomeStore; RouterFeatureVector; optional LocalRelevanceModel adapter.
- **Verification focus:** Dataset captures Hermes/Jev/final outcome and router features; deterministic router works when classifier is absent.

### T19 — Telemetry and decision-quality metrics

- **Blocked by:** T18
- **Owns:** 751–816 (66 points)
- **Outcome:** Instrument turn/event/call/challenge/lease/completion/cost/latency/calibration metrics, prioritizing false PASS, useful intervention, and final task success over raw call volume.
- **Seam:** MetricsSink interface; calibration aggregators.
- **Verification focus:** Metrics cover every listed counter/distribution and explicitly surface false PASS and useful-disagreement quality.

### T20 — Receipts and jev_stats nervous-system expansion

- **Blocked by:** T19
- **Owns:** 817–862 (46 points)
- **Outcome:** Create structured receipts for every supervisory transition and extend local-only jev_stats with admission/router/challenge/staleness/lease/metric summaries.
- **Seam:** ReceiptStore public seam; JevStats projection.
- **Verification focus:** Every listed receipt exists; jev_stats makes no provider call and reports the required nervous-system sections.

## Phase 8 — provider hardening

### T21 — Provider compatibility and direct-TypeSafe validation

- **Blocked by:** T01
- **Owns:** 863–885 (23 points)
- **Outcome:** Retain OpenRouter/direct-TypeSafe interchangeable transports, preserve provenance/usage/error behavior, and add honest direct-account live validation when credentials exist.
- **Seam:** Provider adapter interface; OpenRouter adapter; TypeSafe adapter.
- **Verification focus:** Both transports satisfy the same assessment contract; wire/live claims remain distinct; provider failure never silently authorizes consequential work.

### T22 — Latency, long-running supervision, and compact provider payloads

- **Blocked by:** T12, T13, T21
- **Owns:** 886–913 (28 points)
- **Outcome:** Prove the system remains asynchronous under ~500 ms provider latency, survives multi-hour/high-event turns, and sends structured compact state rather than raw conversation/tool transcripts.
- **Seam:** LongTurnSupervisor behavior at the existing interfaces; payload sanitizer/compactor.
- **Verification focus:** Synthetic 500+ ms latency does not serialize ordinary work; long-run critical checks survive; payload fixtures exclude raw transcripts by default.

## Phase 9 — vertical integration

### T23 — End-to-end turn lifecycle and WATCH wake-up

- **Blocked by:** T02, T05, T07, T09, T22
- **Owns:** 914–942 (29 points)
- **Outcome:** Wire prompt ingress through admission, local event flow, WATCH promotion, ON supervision, challenges, completion and TURN_COMPLETE final summary.
- **Seam:** Single end-to-end TurnSupervision seam.
- **Verification focus:** OFF/WATCH/ON scenarios execute through the full public seam; WATCH promotes only on real decision-plane signals.

### T24 — Useful-call policy, anti-bureaucracy, and asynchronous invariants

- **Blocked by:** T16, T22, T23
- **Owns:** 943–974 (32 points)
- **Outcome:** Enforce that remote Jev calls must be actionable/useful, prevent per-tool bureaucracy, and codify the supersession of synchronous loops while allowing one prompt-level arbiter read.
- **Seam:** Policy invariants at TurnSupervision/AdaptiveRouter seams.
- **Verification focus:** Explicit negative tests show ls/read/grep/status/successful-test/chat do not create nervous-system call storms.

### T25 — Second-level local admission and future relevance intelligence

- **Blocked by:** T18, T23, T24
- **Owns:** 975–992 (18 points)
- **Outcome:** Make the local router the second admission layer inside an admitted turn and expose a future lightweight statistical/classifier adapter driven by router features.
- **Seam:** LocalAdmissionPolicy plus LocalRelevanceModel seam.
- **Verification focus:** Turn admission and per-state admission remain distinct; no remote Jev is used to decide every local routing event.

### T26 — Goal-oriented completion verification and authority policy

- **Blocked by:** T11, T14, T23
- **Owns:** 993–1014 (22 points)
- **Outcome:** Tie completion to explicit goal/done evidence and formalize how confidence, staleness, reversibility, consequence and mode govern Jev authority versus Hermes overrides.
- **Seam:** GoalVerifier; AuthorityPolicy.
- **Verification focus:** PASS requires evidence; override/correction paths are explicit; stale or irreversible-state constraints dominate inappropriate corrections.

## Phase 10 — verification

### T27 — Behavioral and adversarial scenario suite

- **Blocked by:** T26, T25, T21
- **Owns:** 1015–1048 (34 points)
- **Outcome:** Implement the complete real-task, disagreement, staleness, roleplay, WATCH, high-volume, batching, provider, context and rehydration scenario matrix.
- **Seam:** Test only through agreed public seams: TurnSupervision, AdaptiveRouter, ChallengeInbox, ProviderAdapter, GoalVerifier.
- **Verification focus:** Every scenario in points 1015–1048 has an executable test or explicitly credential-gated live test with a receipt.

### T28 — Recommended default configuration and rollout posture

- **Blocked by:** T27
- **Owns:** 1049–1064 (16 points)
- **Outcome:** Ship defaults that enable admission and adaptive async supervision while keeping legacy gate/context mutation conservative and provider budgets bounded.
- **Seam:** Configuration schema and default policy surface.
- **Verification focus:** Fresh install exactly matches every recommended default; migration does not silently enable synchronous all-tool gating.

### T29 — Release and handoff integrity

- **Blocked by:** T27
- **Owns:** 1065–1079 (15 points)
- **Outcome:** Fix release-tree/handoff/test-runner/docs/checksum/pin/validation-claim inconsistencies so the shipped artifact and published commit are reproducible.
- **Seam:** Release packaging seam; CI/release verification.
- **Verification focus:** Canonical package byte/content checks, docs presence, suite-count labeling, pin/checksum validation and honest provider claims all pass.

## Phase 11 — architecture consolidation

### T30 — Final deep-module topology and integration refactor

- **Blocked by:** T23, T25, T26
- **Owns:** 1080–1101 (22 points)
- **Outcome:** Consolidate the implementation into the explicit deep modules that emerged from the design, keeping small public interfaces and internal complexity behind stable seams.
- **Seam:** TurnArbiter, EventBus, Supervisor/Router, accumulators/detectors, lease manager, async provider worker, challenge components, receipt/outcome stores, classifier adapter.
- **Verification focus:** Deletion/interface tests demonstrate module depth/locality; callers do not depend on detector internals.

### T31 — System invariants, performance gates, and final spec conformance

- **Blocked by:** T28, T29, T30
- **Owns:** 1102–1119 (18 points)
- **Outcome:** Make the final design principles executable as invariant/performance/spec gates: decisions-not-tokens, async-by-default, sparse challenges, semantic state change, stale safety and useful-intervention optimization.
- **Seam:** End-to-end acceptance seam plus CI invariant checks.
- **Verification focus:** All final principles are represented by explicit acceptance tests/metrics, and full 1,119-point traceability is green.

## Initial ready frontier

- `P00` — throwaway nervous-system logic prototype.
- `T01` — async decision-engine foundation (production work can begin after/alongside the prototype only if the prototype has not exposed a state-model contradiction).

## Definition of done

- All T01–T31 tickets complete with their mapped verification IDs resolved.
- `verification/COVERAGE_REPORT.md` remains 1,119/1,119 with zero duplicates/gaps.
- T27 scenario suite green, with credential-gated live checks truthfully marked when unavailable.
- Synthetic >=500 ms provider latency proves ordinary work is not serialized.
- False-PASS adversarial tests green.
- Final two-axis Standards + Spec review has no unresolved blocking findings.
- Release ZIP/tree/docs/test claims/pin/checksums reconcile exactly.
