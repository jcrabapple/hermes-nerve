# TDD / Verification Plan

## Agreed seams

Test external behavior through `TurnSupervision`, `JevEventBus`, `AdaptiveRouter`, `DecisionAssessor`, `ChallengeInbox`, `GoalVerifier`, `ReceiptStore/JevStats`, and provider adapters. Do not test private delta detectors directly unless they later gain multiple adapters and become real seams.

## Red → green order

1. Turn admission starts in parallel and does not block Hermes.
2. OFF/WATCH/ON lifecycle through `TurnSupervision`.
3. Structured decision event embeds Hermes choice.
4. Agreement is silent; confident disagreement becomes challenge.
5. Stale challenge is rejected.
6. Router suppresses routine reads/status/tests.
7. Contradictory evidence triggers assessment.
8. Decision lease suppresses equivalent repeat assessments.
9. Completion candidate bypasses sparse suppression.
10. High-volume event stream batches while critical events bypass.
11. Expected-value policy differs for equal event counts with different consequence/novelty.
12. Recovery and goal verification semantics.
13. Long-running delayed-provider test.
14. Provider parity OpenRouter/direct TypeSafe wire tests.
15. Stats/receipts/outcome calibration projections.
16. Full scenario matrix in T27.

## Test quality constraints

- Expected values derive from this spec/requirement inventory, not the implementation.
- No implementation-coupled private-method assertions.
- One vertical behavior per red/green cycle.
- Performance tests distinguish provider latency from worker wall-clock blocking.
- Credential-gated live tests must state `unverified` when credentials are unavailable; never fake success.
