# Hermes-Jev v0.2.2 Bug Report Handoff

Date: 2026-09-18
Test environment:
- Hermes Agent v0.21.2
- Hermes-Jev v0.2.1
- Profile: `muna`
- Jev provider path: OpenRouter Decisions / TypeSafe Jev
- Model observed in successful direct call: `typesafe/jev-1.13-20260917`

## Scope

This package captures the Jev-specific issues found during live smoke testing on the Muna profile.

Included reports:

1. `BUG-001-jev-assess-schema-validator-mismatch.md`
   - `jev_assess`'s model-facing schema does not expose the runtime requirements for `choice.criteria` clearly enough.
   - Result: deferred-tool models can construct calls that are syntactically accepted by Hermes but rejected immediately by Jev validation.

2. `BUG-002-jev-self-observation-amplification.md`
   - Failed `jev_*` calls appear to be observable by the Jev nervous system and may generate additional background Jev provider traffic.
   - This is a high-confidence correlation from the live trace and OpenRouter log pattern, but should be verified with explicit instrumentation before calling the root cause proven.

3. `BUG-003-receipt-backed-provenance.md`
   - Muna previously presented `Jev decision`, `Jev confidence`, and `Jev verification result` values while reporting `Jev request ID: N/A` and without visible matching Jev tool calls.
   - Jev-facing claims should require a real receipt/request ID so the model cannot blur its own inference with provider-backed verification.

## Explicitly out of scope

Hermes' automatic self-improvement system created a skill after one test. That behavior is controlled by Hermes rather than by the acting agent or Hermes-Jev and is **not** treated as a Jev failure in this handoff.

## Release gate proposed for v0.2.2

The release should not be considered fixed until all of these pass:

- A deferred model can inspect `jev_assess` and construct a valid `choice` assessment without hidden schema knowledge.
- Invalid `jev_assess` input fails locally and causes **zero** Jev provider calls through the nervous system.
- Valid `jev_assess` input causes exactly the expected provider request(s) and returns a real request ID/receipt.
- A result with no Jev receipt cannot be surfaced as `Jev verified`, `Jev PASS`, or a Jev confidence score.
- Existing v0.2.1 loop-breaker, control-lease, bounded-stats, and 1,119-requirement traceability tests continue to pass.

## Evidence files

- `evidence/muna-trace-excerpts.md`
- `evidence/openrouter-1155-1156.txt`

