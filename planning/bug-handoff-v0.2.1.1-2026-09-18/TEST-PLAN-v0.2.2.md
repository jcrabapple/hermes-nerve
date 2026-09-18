# Hermes-Jev v0.2.2 Focused Regression Plan

## Test 1 — Deferred `jev_assess` schema

1. Start fresh Muna session.
2. `tool_describe(["jev_assess"])`.
3. Construct one `choice` question using only returned schema information.
4. Invoke exactly one local call via `tool_call`.

Pass:
- no schema/validation error
- exactly one expected provider call
- non-empty request/receipt ID

## Test 2 — Jev-internal failure suppression

1. Record provider-call counter.
2. Intentionally submit one malformed `jev_assess` payload.
3. Wait for nervous async work to settle.
4. Re-read provider-call counter and Jev stats.

Pass:
- local TOOL_ERROR
- zero provider-call delta
- internal-suppression counter increments

## Test 3 — Valid Jev call does not self-amplify

1. Record provider-call counter.
2. Submit one valid `jev_assess`.
3. Wait for async hooks to settle.

Pass:
- provider-call delta exactly 1
- no second Jev nervous call caused by observing the successful Jev tool itself

## Test 4 — Receipt-backed reporting

Run three explicit assessments.

Pass:
- every user-visible Jev-attributed result includes its real request/receipt ID
- no request ID -> final status must be UNVERIFIED/LOCAL_ONLY, never Jev PASS
- number of Jev-attributed outcomes <= number of corresponding receipts

## Test 5 — Preserve v0.2.1 regressions

Re-run complete plugin suite.

Minimum expected baseline from v0.2.1:
- 66/66 tests previously passing
- compileall PASS
- release verifier PASS
- 8 tools
- 7 hook names / 8 callbacks
- 1,119 traced requirements retained

Update expected counts if new v0.2.2 regression tests are added.
