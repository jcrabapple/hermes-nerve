# Architecture and Test Seams

## Design rule

Each module below is intended to be deep: a small public interface with policy/state complexity hidden behind it. Tests and callers use the same public seam. Internal detectors are implementation details unless a second adapter creates a real seam.

## Public seams

### 1. `TurnSupervision`
Accepts a user turn and emits supervision lifecycle outcomes. Hides admission dispatch, WATCH promotion, turn closure and final summary. Primary end-to-end seam.

### 2. `JevEventBus`
Accepts typed Hermes runtime events and assigns sequence/provenance. It does not decide whether remote Jev should be called.

### 3. `AdaptiveRouter`
Consumes typed events/current turn state and returns local decisions such as accumulate, batch, assess-now, critical-bypass. Hides novelty/delta/materiality/expected-value implementation.

### 4. `DecisionAssessor`
Accepts compact bounded decision assessments and returns normalized Jev responses, independent of OpenRouter vs direct TypeSafe.

### 5. `ChallengeInbox`
Accepts normalized Jev disagreements, checks state validity/authority, and exposes actionable correction/challenge outcomes to Hermes.

### 6. `GoalVerifier`
Evaluates completion candidates against explicit goal/done evidence and exposes PASS/RETRY/REPLAN/ESCALATE/GATHER_EVIDENCE semantics.

### 7. `ReceiptStore` / `JevStats` projection
Persists immutable-ish supervision receipts and produces local telemetry/stat views without provider calls.

### 8. `LocalRelevanceModel` (optional adapter)
A disabled-by-default local predictor of useful Jev disagreement. Deterministic routing works without it.

## Internal components hidden behind those seams

Turn arbiter, objective envelope, state accumulator, event compressor, novelty detector, decision/evidence/risk/uncertainty/completion detectors, lease manager, batching/intensity policy, expected-value policy, provider workers, challenge validator, outcome correlator, calibration dataset.

## Deletion tests

- Delete `AdaptiveRouter`: policy complexity should reappear across many event producers; if not, the module is too shallow.
- Delete `DecisionAssessor`: provider-specific transport concerns should reappear in all callers; if not, the seam is not earning its keep.
- Delete `ChallengeInbox`: stale/reversibility/authority logic should otherwise leak into Hermes execution; keep it localized.
- `JevEventBus` must remain policy-free; if deleting it removes decision policy, responsibilities are mixed.
