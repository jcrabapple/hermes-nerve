# Nerve 0.2.1.1 patch actualization

Date: 2026-09-18
Baseline: `hermes-nerve-v0.2.1(1).zip`
Bug handoff: `hermes-nerve-v0.2.2-bug-reports(1).zip`

This is a narrow patch release derived from the supplied 0.2.1 source and the three P1 reports originally proposed for 0.2.2. It intentionally preserves the 0.2.1 nervous-system behavior and fixes only the reported integration/audit defects.

## Bug matrix

| Bug | Status | 0.2.1.1 implementation |
| --- | --- | --- |
| BUG-001 `nerve_assess` deferred schema/validator mismatch | FIXED | `JEV_ASSESS` now exposes a typed `oneOf` question contract. `choice.criteria` is explicitly an object with `minProperties: 2`; `score.criteria` is an array with `minItems: 2`; `noul` does not require choice labels. Runtime validation remains authoritative. |
| BUG-002 Jev self-observation amplification | FIXED | `post_tool_call` observation now treats all `jev_*` tools as an internal supervision boundary. Internal success/failure observations are logged and counted locally, never converted into a nervous remote assessment. Origin metadata and provider-call-by-origin telemetry were added. |
| BUG-003 receipt-backed provenance | FIXED | Remote `nerve_decide`, `nerve_rank`, `nerve_assess`, and `nerve_verify` results now return a content-bound local `receipt_id`, normalized provenance, `provenance_status`, provider/model/transport metadata, subject hash, and result hash. Local/error outputs are explicitly `LOCAL_ONLY`/`ERROR`, not `VERIFIED`. |

## Provenance contract

Remote successful decision results now include:

```json
{
  "request_id": "provider request id when available",
  "receipt_id": "jevrec-...",
  "provenance_status": "VERIFIED",
  "provenance": {
    "verified_by": "hermes-nerve",
    "request_id": "...",
    "receipt_id": "jevrec-...",
    "provider": "...",
    "transport": "...",
    "model": "...",
    "contract": "...",
    "created_at": "...",
    "subject_sha256": "...",
    "result_sha256": "..."
  }
}
```

A provider that does not expose a request id is still auditable through the locally persisted content-bound `receipt_id`. Results with neither a provider call nor a receipt are never marked `VERIFIED`.

## Nervous-system self-observation boundary

The existing 0.2.1 pre-tool path already exempted `jev_*` tools. 0.2.1.1 closes the missing post-tool seam:

```text
jev_* tool completion/failure
  -> local diagnostic log/counters
  -> forwarded=false, reason=jev-internal
  -> zero nervous provider calls
```

New runtime telemetry includes:

- `metrics.jev_internal_seen`
- `metrics.jev_internal_suppressed`
- `quality_metrics.jev_internal_events_seen`
- `quality_metrics.jev_internal_events_suppressed`
- `quality_metrics.provider_calls_by_origin`
- origin metadata on remotely assessed nervous decisions

## Focused regression coverage

Added `tests/test_patch_0211.py` covering:

1. Deferred `nerve_assess` schema exposes the runtime choice/score constraints.
2. Valid choice assessment reaches the provider exactly once.
3. Invalid one-label choice fails locally with no provider-call increment.
4. Failed `nerve_assess` post-tool observation is locally suppressed and cannot reach the nervous provider.
5. Successful explicit `nerve_assess` does not self-amplify through post-tool observation.
6. `nerve_decide`, `nerve_rank`, `nerve_assess`, and `nerve_verify` all produce persisted receipt-backed provenance.
7. Missing provider request id still leaves a real local receipt id.
8. Error and local-only results cannot be represented as `VERIFIED`.

## Verification boundary

Offline verification is complete for this package. A real Hermes 0.21.2 deferred `tool_describe -> tool_call` replay and live OpenRouter/TypeSafe provider-count comparison require the user's Muna runtime/credentials and are therefore external follow-up, not claimed by this build.
