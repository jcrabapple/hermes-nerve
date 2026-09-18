# Implementation Task Graph

Tickets are a dependency graph, not a linear checklist. Work the ready frontier; parallelize independent tickets in separate worktrees/branches, merge into one integration branch, then run the two-axis review.

`P00` is the recommended first learning ticket and owns no normative source point.

## T01 — Async decision-engine foundation

- **Phase:** Phase 1 — foundation
- **Blocked by:** None
- **Owns:** points 1–25 (25 requirements)
- **Delivers:** Establish the production control-plane skeleton in which Hermes continues reasoning/executing while Jev supervises asynchronously, with decision epochs and batched control assessment as the primitive.

## T02 — Turn arbiter: OFF / WATCH / ON

- **Phase:** Phase 1 — foundation
- **Blocked by:** T01
- **Owns:** points 26–62 (37 requirements)
- **Delivers:** Add one non-recursive Jev admission assessment per user turn, dispatched in parallel with Hermes, producing OFF/WATCH/ON plus complete admission telemetry.

## T03 — Decision-plane and accountability semantics

- **Phase:** Phase 1 — foundation
- **Blocked by:** T02
- **Owns:** points 63–105 (43 requirements)
- **Delivers:** Represent interaction type separately from decision context and determine Jev eligibility from accountable decision semantics rather than chat/tool surface.

## T04 — Roleplay director plane, decision scope, and objective envelope

- **Phase:** Phase 1 — foundation
- **Blocked by:** T03
- **Owns:** points 106–160 (55 requirements)
- **Delivers:** Separate actor-plane roleplay from accountable director-plane decisions and persist the objective envelope/scopes Jev needs across a turn.

## T05 — Structured Hermes event bus and high-value event taxonomy

- **Phase:** Phase 2 — event substrate
- **Blocked by:** T01, T04
- **Owns:** points 161–227 (67 requirements)
- **Delivers:** Emit structured runtime events independent of assistant prose and define the event/decision categories that can feed the local nervous system.

## T06 — Decision request schema with Hermes proposal embedded

- **Phase:** Phase 2 — event substrate
- **Blocked by:** T05
- **Owns:** points 228–263 (36 requirements)
- **Delivers:** Create the canonical decision event/request shape containing Hermes’s proposed choice, alternatives, state, evidence, materiality, reversibility and versions in the original event.

## T07 — Jev response envelope, confidence gating, and challenge pipeline

- **Phase:** Phase 3 — tandem supervision
- **Blocked by:** T06
- **Owns:** points 264–330 (67 requirements)
- **Delivers:** Normalize Jev responses and implement silent agreement/low-confidence handling plus a challenge queue/inbox for useful high-confidence disagreement.

## T08 — Stale-response protection, reversibility, and supervision modes

- **Phase:** Phase 3 — tandem supervision
- **Blocked by:** T07
- **Owns:** points 331–364 (34 requirements)
- **Delivers:** Validate late Jev responses against current state, respect reversibility/commit status, and support SHADOW, CORRECT_NEXT and PRECOMMIT authority modes.

## T09 — Adaptive local router and compact turn-state accumulator

- **Phase:** Phase 4 — adaptive routing
- **Blocked by:** T05, T06
- **Owns:** points 365–414 (50 requirements)
- **Delivers:** Build the local stateful router that consumes all Hermes events, accumulates compact turn state, compresses events and decides whether remote Jev could matter.

## T10 — Novelty, decision, evidence, risk, and uncertainty delta detectors

- **Phase:** Phase 4 — adaptive routing
- **Blocked by:** T09
- **Owns:** points 415–477 (63 requirements)
- **Delivers:** Implement the state-delta detectors that raise or lower Jev value based on strategy, evidence, risk, uncertainty, novelty, contradictions and stability.

## T11 — Completion pressure, decision leases, and hysteresis

- **Phase:** Phase 4 — adaptive routing
- **Blocked by:** T07, T09, T10
- **Owns:** points 478–512 (35 requirements)
- **Delivers:** Treat completion as high-value supervision, keep Jev decisions valid through a lease while state is equivalent, and prevent call storms with semantic hysteresis.

## T12 — Adaptive batching and supervision intensity

- **Phase:** Phase 4 — adaptive routing
- **Blocked by:** T09, T10, T11
- **Owns:** points 513–556 (44 requirements)
- **Delivers:** Batch high-volume event streams into state transitions, support sparse/intensive modes, and allow Jev to recommend future watch intensity without controlling every event.

## T13 — Expected-value routing, materiality, and safety budgets

- **Phase:** Phase 4 — adaptive routing
- **Blocked by:** T10, T12
- **Owns:** points 557–589 (33 requirements)
- **Delivers:** Replace hard-coded N-event polling with an expected-value call policy combining usefulness probability, consequence, uncertainty, novelty, materiality, risk, freshness, cost and staleness, with budgets only as safety rails.

## T14 — Control states, recovery, and ambiguity handling

- **Phase:** Phase 5 — decision contracts
- **Blocked by:** T06, T13
- **Owns:** points 590–624 (35 requirements)
- **Delivers:** Standardize bounded control states and recovery/evidence/human-escalation decisions for supervised work.

## T15 — Resource routing and multi-question control assessment

- **Phase:** Phase 5 — decision contracts
- **Blocked by:** T14
- **Owns:** points 625–646 (22 requirements)
- **Delivers:** Support bounded routing/ranking choices and combine previous-result, next-action, evidence, completion, confidence and supervision questions into a single Jev assessment.

## T16 — Useful-work filter and legacy gate demotion

- **Phase:** Phase 5 — decision contracts
- **Blocked by:** T09, T13
- **Owns:** points 647–667 (21 requirements)
- **Delivers:** Keep routine introspection local, treat tools as signals rather than work definitions, and retain selective pre-tool gating only as compatibility/precommit behavior.

## T17 — Compatibility layer for existing tools, hooks, and context engine

- **Phase:** Phase 6 — compatibility
- **Blocked by:** T16
- **Owns:** points 668–700 (33 requirements)
- **Delivers:** Preserve existing Jev tools/hooks/context surfaces while placing the new nervous system above them and keeping context shadow-first with rehydration capabilities intact.

## T18 — Outcome learning dataset and future local classifier seam

- **Phase:** Phase 7 — observability and learning
- **Blocked by:** T07, T09
- **Owns:** points 701–750 (50 requirements)
- **Delivers:** Persist normalized decision outcomes and create the local-classifier seam so the router can later learn where Jev disagreement is valuable without adding another remote LLM.

## T19 — Telemetry and decision-quality metrics

- **Phase:** Phase 7 — observability and learning
- **Blocked by:** T18
- **Owns:** points 751–816 (66 requirements)
- **Delivers:** Instrument turn/event/call/challenge/lease/completion/cost/latency/calibration metrics, prioritizing false PASS, useful intervention, and final task success over raw call volume.

## T20 — Receipts and jev_stats nervous-system expansion

- **Phase:** Phase 7 — observability and learning
- **Blocked by:** T19
- **Owns:** points 817–862 (46 requirements)
- **Delivers:** Create structured receipts for every supervisory transition and extend local-only jev_stats with admission/router/challenge/staleness/lease/metric summaries.

## T21 — Provider compatibility and direct-TypeSafe validation

- **Phase:** Phase 8 — provider hardening
- **Blocked by:** T01
- **Owns:** points 863–885 (23 requirements)
- **Delivers:** Retain OpenRouter/direct-TypeSafe interchangeable transports, preserve provenance/usage/error behavior, and add honest direct-account live validation when credentials exist.

## T22 — Latency, long-running supervision, and compact provider payloads

- **Phase:** Phase 8 — provider hardening
- **Blocked by:** T12, T13, T21
- **Owns:** points 886–913 (28 requirements)
- **Delivers:** Prove the system remains asynchronous under ~500 ms provider latency, survives multi-hour/high-event turns, and sends structured compact state rather than raw conversation/tool transcripts.

## T23 — End-to-end turn lifecycle and WATCH wake-up

- **Phase:** Phase 9 — vertical integration
- **Blocked by:** T02, T05, T07, T09, T22
- **Owns:** points 914–942 (29 requirements)
- **Delivers:** Wire prompt ingress through admission, local event flow, WATCH promotion, ON supervision, challenges, completion and TURN_COMPLETE final summary.

## T24 — Useful-call policy, anti-bureaucracy, and asynchronous invariants

- **Phase:** Phase 9 — vertical integration
- **Blocked by:** T16, T22, T23
- **Owns:** points 943–974 (32 requirements)
- **Delivers:** Enforce that remote Jev calls must be actionable/useful, prevent per-tool bureaucracy, and codify the supersession of synchronous loops while allowing one prompt-level arbiter read.

## T25 — Second-level local admission and future relevance intelligence

- **Phase:** Phase 9 — vertical integration
- **Blocked by:** T18, T23, T24
- **Owns:** points 975–992 (18 requirements)
- **Delivers:** Make the local router the second admission layer inside an admitted turn and expose a future lightweight statistical/classifier adapter driven by router features.

## T26 — Goal-oriented completion verification and authority policy

- **Phase:** Phase 9 — vertical integration
- **Blocked by:** T11, T14, T23
- **Owns:** points 993–1014 (22 requirements)
- **Delivers:** Tie completion to explicit goal/done evidence and formalize how confidence, staleness, reversibility, consequence and mode govern Jev authority versus Hermes overrides.

## T27 — Behavioral and adversarial scenario suite

- **Phase:** Phase 10 — verification
- **Blocked by:** T26, T25, T21
- **Owns:** points 1015–1048 (34 requirements)
- **Delivers:** Implement the complete real-task, disagreement, staleness, roleplay, WATCH, high-volume, batching, provider, context and rehydration scenario matrix.

## T28 — Recommended default configuration and rollout posture

- **Phase:** Phase 10 — verification
- **Blocked by:** T27
- **Owns:** points 1049–1064 (16 requirements)
- **Delivers:** Ship defaults that enable admission and adaptive async supervision while keeping legacy gate/context mutation conservative and provider budgets bounded.

## T29 — Release and handoff integrity

- **Phase:** Phase 10 — verification
- **Blocked by:** T27
- **Owns:** points 1065–1079 (15 requirements)
- **Delivers:** Fix release-tree/handoff/test-runner/docs/checksum/pin/validation-claim inconsistencies so the shipped artifact and published commit are reproducible.

## T30 — Final deep-module topology and integration refactor

- **Phase:** Phase 11 — architecture consolidation
- **Blocked by:** T23, T25, T26
- **Owns:** points 1080–1101 (22 requirements)
- **Delivers:** Consolidate the implementation into the explicit deep modules that emerged from the design, keeping small public interfaces and internal complexity behind stable seams.

## T31 — System invariants, performance gates, and final spec conformance

- **Phase:** Phase 11 — architecture consolidation
- **Blocked by:** T28, T29, T30
- **Owns:** points 1102–1119 (18 requirements)
- **Delivers:** Make the final design principles executable as invariant/performance/spec gates: decisions-not-tokens, async-by-default, sparse challenges, semantic state change, stale safety and useful-intervention optimization.

