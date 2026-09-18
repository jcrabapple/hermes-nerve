# Hermes-Jev v0.2.1.1 verification receipt

## Build result

- Baseline: user-provided `hermes-jev-v0.2.1(1).zip`.
- Bug specification: user-provided `hermes-jev-v0.2.2-bug-reports(1).zip`.
- Version produced: `0.2.1.1`.
- Patch scope: BUG-001 deferred `jev_assess` schema, BUG-002 Jev self-observation amplification, BUG-003 receipt-backed provenance.

## Verified offline

- Full unit suite: **74/74 PASS**.
- Python bytecode compile: **PASS**.
- Release verifier: **PASS**.
- Registered public surface remains **8 tools**, **7 hook names**, **8 hook callbacks**.
- Preserved vNext implementation trace remains exactly **1,119** sequential requirement IDs with unique verification IDs.

### BUG-001

The model-facing `jev_assess` schema now publishes a typed union matching runtime validation. Choice questions expose a criteria object with `minProperties: 2`; score questions expose an ordered criteria array with `minItems: 2`; noul questions do not require choice labels. A regression proves a valid choice reaches the provider once and a one-label choice fails before any additional provider call.

### BUG-002

The post-tool nervous observer now suppresses all `jev_*` tools before failure-episode creation or remote routing. Regressions prove both a failed and successful `jev_assess` observation are local-only and generate no nervous provider call. Existing non-Jev external failure supervision remains covered by the preserved suite. Runtime telemetry records internal observations/suppressions and provider calls by origin.

### BUG-003

Every successful explicit remote `jev_decide`, `jev_rank`, `jev_assess`, and `jev_verify` result is written to the receipt ledger and returned with the same `receipt_id`. Each receipt binds the contract, sanitized subject hash, result hash, model, request id, and creation time. Returned provenance contains provider/model/transport, request/receipt IDs, subject/result hashes, and `provenance_status=VERIFIED`. Local-only and error tool results are explicitly non-verified.

## Not claimed by this build

This isolated environment does not have the user's live Muna/Hermes session or provider credentials. Therefore the package does **not** claim a live Hermes 0.21.2 `tool_describe -> tool_call` replay, a live OpenRouter generation-count comparison, or a direct TypeSafe account smoke. Those are external post-install validations; the offline regression harness covers the corresponding plugin seams and invariants.
