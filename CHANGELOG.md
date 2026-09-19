# Changelog

## 0.2.1.2 — bounded context-engine and fail-open stabilization

- Fix issue #2: automatic apply-mode curation no longer passes more than 48 evidence items into the bounded `jev_context_curate` contract.
- Select recoverable raw tool-result evidence oldest-first, defer excess candidates unchanged, and exclude existing Jev anchors from future semantic curation.
- Make the full compression boundary fail-open: Jev curation failures try the configured Hermes built-in compressor, and fallback-compressor failures return the original message list instead of escaping into the turn loop.
- Make shadow curation failures and selection pressure observable through ContextEngine status.
- Fix shadow telemetry so proposed ANCHOR/DROP actions do not count as applied compaction or inflate recovery-demand metrics.
- Avoid automatic remote semantic assessments for deterministically unrecoverable evidence.
- Add 0.2.1.2 regressions for 48/49/60/851-item boundaries, double-failure fail-open behavior, anchor idempotence, shadow telemetry, unrecoverable evidence, and the 12-request maximum semantic fan-out for 48 items.
- Record the independent successful v0.2.1.1 direct-TypeSafe smoke from issue #1 without overstating it as a v0.2.1.2 credentialed validation.

## 0.2.1.1 — deferred schema, self-observation, and provenance patch

- Fix **BUG-001**: make the deferred `jev_assess` schema mechanically constructible from `tool_describe`, including explicit `choice.criteria` map/`minProperties: 2`, `score.criteria` array/`minItems: 2`, and noul semantics.
- Fix **BUG-002**: make every `jev_*` post-tool result/failure an internal nervous-system boundary. Internal Jev observations are logged/counted locally and cannot recursively trigger a remote Jev nervous assessment.
- Add origin telemetry for nervous provider calls and decisions so provider traffic can be attributed to the originating tool/event.
- Fix **BUG-003**: remote `jev_decide`, `jev_rank`, `jev_assess`, and `jev_verify` results now carry a persisted content-bound `receipt_id`, normalized provenance block, and reporting-safe `provenance_status`.
- Mark local-only results as `LOCAL_ONLY` and handler failures as `ERROR`; results without remote/receipt evidence cannot be represented structurally as `VERIFIED`.
- Expand the offline suite from 66 to 74 tests with focused regressions for the three supplied P1 reports.
- Preserve the 0.2.1 loop breaker, control leases, bounded stats, 8 tools / 7 hook names / 8 callbacks, and 1,119-requirement trace.

## 0.2.1 — recovery/control hardening

- Fix **JEV-001**: repeated identical failures now have an enforceable pre-tool control path. A confident remote `REPLAN`/`GATHER_EVIDENCE`/`ESCALATE` can prevent the exact failed action from running again, while `RETRY` explicitly permits one retry.
- Add a provider-independent third-strike local `REPLAN` loop breaker so late/quiet Jev responses cannot allow an unbounded identical failure loop.
- Fix **JEV-002**: add stable decision IDs and control lifecycle receipts covering decision creation, delivery, next-action attribution, enforcement/following, expiry, and outcomes. Define the decision-correction denominator explicitly.
- Fix **JEV-003** telemetry ambiguity: the legacy pre-tool gate records correlated hook observations even when `gate_mode=off`, including turn/session/tool-call IDs.
- Fix **JEV-004**: `jev_stats` is compact and sectioned by default, recent arrays are opt-in, and bounded tool-result protection prevents accidental ~30 KB telemetry injections.
- Clarify **JEV-005**: rehydration is explicit/demand-driven; add a regression proving anchored evidence can be rehydrated and counted as recovery demand.
- Fix **JEV-006**: stable repeated-failure fingerprints deduplicate equivalent failure assessments after the first provider evaluation; later exact repeats stay local until state/evidence changes.
- Fix **JEV-007**: semantic decision-lease fingerprints no longer include monotonic state/decision counters, enabling real lease reuse and reasoned invalidation.
- Improve **JEV-008** plugin-side startup diagnostics by logging the loaded version and source path. Hermes pre-discovery `unknown toolset`/context-engine warnings, if present, remain host-level behavior.
- Compose local nervous control and the optional legacy gate into one `pre_tool_call` callback so a locally blocked retry does not unnecessarily fall through to a synchronous Jev gate call.
- Add `nervous_repeated_failure_local_replan_at` (default `3`, range 2–20).
- Expand the offline suite with repeated-failure dedup, local loop-breaking, remote REPLAN enforcement, RETRY allowance, control attribution, gate-off observation, bounded stats, fingerprint normalization, and rehydration-demand regressions.

## 0.2.0

- Added asynchronous OFF/WATCH/ON turn admission so Hermes begins work without waiting for Jev.
- Added structured Jev nervous-system events and `jev_nervous_event`.
- Added adaptive local semantic routing, hysteresis, decision leases, and in-flight event batching.
- Added confidence-gated decision challenges delivered through `transform_tool_result`.
- Added state-version staleness protection and SHADOW/CORRECT_NEXT/PRECOMMIT authority modes.
- Added local outcome store and optional historical relevance calibration.
- Expanded `jev_stats` with nervous-system decision-quality and provider-avoidance telemetry.
- Added direct TypeSafe System One transport alongside OpenRouter.
- Preserved the existing seven tools, selective legacy gate, evidence ledger, rehydration, and ContextEngine.
- Added adversarial offline tests for async non-blocking admission, batching, WATCH promotion, stale challenges, confidence gating, provider budget, and direct TypeSafe wire behavior.

## 0.1.5.5 — profile-aware telemetry + shadow-safe community defaults

- Fix pre-tool gate latency discovered in live telemetry: 106/106 sampled `hermes/pre-tool-gate/v1` calls returned `ALLOW`, so `gate_scope=selective` now bypasses conservative read-only calls locally instead of paying a Jev network round trip for every introspection.
- Add `gate_scope=all` compatibility mode to restore evaluate-every-call behavior.
- Add local gate event telemetry (`bypassed`, `evaluated`, provider failures, provider latency, and avoided provider-call count) to `jev_stats`.
- Keep the selective bypass intentionally narrow: shell composition, unknown tools, and potentially mutating command families still go to Jev.
- Fix named-profile telemetry resolution: receipts and evidence ledgers now prefer Hermes' own active `HERMES_HOME` resolver, including context-local profile overrides.
- Fix `scripts/context_shadow_report.py` so launching it from a named-profile plugin directory reads that profile instead of silently falling back to `~/.hermes`.
- Add `scripts/jev_report.py` for combined decision receipt + context telemetry.
- Add local-only `jev_stats` tool (7th tool) for exact active-profile cost/token/latency and context-ledger statistics.
- Add receipt aggregation by contract/model with totals for provider calls, tokens, cost, and average latency.
- Change fresh-install `context_curation_mode` and `context_engine_mode` defaults to `shadow`; applying context changes is now explicitly opt-in.
- Add harvested live test notes from the 2026-09-17 Muna/TypeSafe run.

## 0.1.5.4 — context-value governor

- Replace direct KEEP/STUB/DROP confidence gating with four Jev semantic estimates: future need, exactness need, supersession, and unresolved conflict.
- Add deterministic `KEEP_EXACT`, `PIN`, `ANCHOR`, and `DROP` policy plus local `REHYDRATE`.
- Add `jev_context_rehydrate`; public surface is now six tools.
- Add explicit execution provenance to distinguish real OpenRouter/TypeSafe calls from main-model simulation.
- Add lifecycle leases; nonrecoverable failure evidence stays pinned until a real `jev_verify` PASS.
- Add a privacy-minimized evidence ledger, shadow plans, and `scripts/context_shadow_report.py`.
- Add `post_tool_call` observation hook; plugin now exposes two hooks.
- Add opt-in `JevContextEngine` using Hermes' public ContextEngine API. Automatic DROP proposals become anchors to preserve tool-call/result protocol.
- Add optional fallback to Hermes' built-in ContextCompressor when Jev has no eligible evidence or makes no safe progress.
- Preserve `model_id` as a migration alias while using `jev_model` as the canonical non-reserved setting.
- 36 offline tests pass.

## 0.1.5.2

- Fix Hermes registration on current builds by renaming the plugin setting `model` to `jev_model`. Hermes reserves `model` as a core config root and rejects `ctx.get_config("model", ...)` before tool registration.
- Add a regression test context that enforces Hermes plugin-relative config-key restrictions so reserved-root mistakes fail offline.
- No Jev decision semantics changed from 0.1.5.1.

## v0.1.5.1 — explicit Jev context curation

- Add `jev_context_curate`, an original Hermes-native evidence-retention utility inspired by the general Jev-as-retention-judge pattern in `tamaratran/fast-jev-compaction` without copying its code or internal design.
- Preserve user/assistant text, pinned evidence, and a configurable recent tail exactly.
- Classify eligible evidence into `KEEP`, deterministic-prefix `STUB`, or `DROP`.
- Fail conservative: low-confidence/malformed answers become `KEEP`; unrecoverable evidence is never dropped.
- Send bounded evidence previews to Jev, aggregate request usage/cost/latency, and preserve retained item order.
- Keep Hermes' native compaction untouched; this release exposes an explicit tool rather than depending on private compaction internals.
- Add `context-curation/v1`, context policy settings, documentation, and live-suite coverage.
- 22 offline tests pass.

## v0.1.5 — usefulness + observability pass

- Add `jev_assess` for up to 16 native `noul`, `choice`, and `score` questions in one request.
- Return OpenRouter/TypeSafe request id, provider, usage, and cost metadata from decision results and receipts.
- Expose `model` and `timeout_seconds` through Hermes plugin settings.
- Keep the normal Hermes plugin transport pinned to OpenRouter instead of allowing settings to redirect the API credential.
- Add a synthetic live regression suite covering decide, rank, verify, multi-question assessment, and advisory gating.
- Record successful live validation through OpenRouter with TypeSafe Jev 1.13.
- 16 offline tests pass.

## v0.1.4

- Route Jev calls through OpenRouter Decisions API (`/api/alpha/decisions`).
- Use `OPENROUTER_API_KEY` and model `typesafe/jev-1.13`.
- Preserve the existing Hermes tool/hook contracts.

## v0.1.3 — first public release candidate

- Three typed Hermes tools: `jev_decide`, `jev_rank`, and `jev_verify`.
- Optional `pre_tool_call` decision gate with `off`, `advisory`, and `enforce` modes.
- Hermes plugin settings drive gate mode, confidence threshold, and receipt detail through `PluginContext.get_config()`.
- Privacy redaction and hash-only decision receipts by default.
- Dependency-free decision HTTP client with bounded output-contract validation.
- Scanner-safe offline test fixtures.