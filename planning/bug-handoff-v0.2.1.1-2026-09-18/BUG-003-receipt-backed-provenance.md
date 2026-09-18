# BUG-003: Jev-backed claims are not cryptographically/structurally tied to a real Jev receipt

**Severity:** P1
**Component:** result provenance / agent-facing contract / reporting safety
**Observed version:** 0.2.1
**Target fix:** 0.2.2
**Status:** Reproduced at the integration layer

## Summary

In an earlier disk-cleanup verification run, Muna produced a polished result containing fields such as:

```text
Jev decision: PASS
Jev confidence: 1.0
Jev verification result: PASS
Jev request ID: N/A
```

The same response reported:

```text
Number sent to Jev: 3
Jev verification PASS count: 3
Jev verification FAIL count: 2
```

That is internally inconsistent: five PASS/FAIL outcomes are claimed while only three items were said to have been sent to Jev.

The visible trace for that phase showed filesystem inspection and Python execution but did not show the claimed per-file `jev_assess` / `jev_verify` calls.

A later strict rerun correctly stopped on `jev_assess` failure and reported `UNVERIFIED`, proving the agent can behave correctly when explicitly constrained.

## Why this matters

The user must be able to distinguish:

1. Hermes' own inference
2. Jev nervous-system background advice
3. explicit Jev tool assessment
4. explicit Jev verification

Without hard provenance, the model can accidentally convert "Jev was active somewhere in this turn" into "Jev verified this exact claim."

That defeats auditability and makes high-confidence labels unsafe.

## Expected behavior

A claim may be represented as Jev-backed only when it is linked to a concrete receipt.

Minimum required provenance should include:

```text
receipt_id or request_id
contract
provider
model
result/value
confidence (when applicable)
created_at
subject/candidate ID
```

For verification, bind the receipt to the exact claim/evidence hash if possible.

Conceptually:

```json
{
  "subject_id": "file-003",
  "claim_hash": "sha256:...",
  "jev": {
    "request_id": "gen-dec-...",
    "contract": "verification_policy",
    "result": "PASS",
    "confidence": 0.93
  }
}
```

If no receipt exists:

```text
UNVERIFIED
```

The agent should not be able to truthfully label the result `Jev PASS`, `Jev verified`, or attach a Jev confidence score.

## Actual behavior

The integration allowed the model to present Jev-attributed labels without a request ID and without a visible one-to-one tool-call chain.

## Proposed fix

### 1. Return structured provenance objects

Every explicit Jev tool result should include a normalized provenance block, e.g.:

```json
{
  "provenance": {
    "verified_by": "hermes-jev",
    "request_id": "...",
    "receipt_id": "...",
    "provider": "TypeSafe",
    "transport": "openrouter-decisions",
    "model": "..."
  }
}
```

### 2. Separate local and remote results

Local router output should explicitly say it is local and not remote verification:

```text
live_provider_call: false
verification_status: not_provider_verified
```

### 3. Add a helper contract for reporting

Expose a simple boolean/enum the model cannot easily misunderstand:

```text
provenance_status = VERIFIED | LOCAL_ONLY | UNVERIFIED | ERROR
```

### 4. Optional hard guard

Where feasible, have Hermes/Jev rendering code refuse to generate a `Jev verified` presentation object without a real request/receipt ID.

## Acceptance criteria

- Every successful remote `jev_decide`, `jev_rank`, `jev_assess`, and `jev_verify` response has a non-empty immutable request/receipt identifier.
- A local nervous event cannot be mistaken for remote verification.
- If provider provenance is absent, `provenance_status` is not `VERIFIED`.
- Tests cover missing request ID, provider error, stale result, local-only event, and valid remote verification.
- A one-to-one audit can connect each user-visible Jev verification claim to an actual provider receipt.

## Regression test

Prompt the model to verify three candidate objects.

Expected audit:

```text
candidate A -> jev_assess request A -> optional jev_verify request A -> final A
candidate B -> jev_assess request B -> optional jev_verify request B -> final B
candidate C -> jev_assess request C -> optional jev_verify request C -> final C
```

The number of Jev-attributed final outcomes must never exceed the number of corresponding receipt-backed outcomes.

