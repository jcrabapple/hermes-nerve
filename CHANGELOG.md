# Changelog

## 0.1.5.5 — profile-aware telemetry + shadow-safe community defaults

- Add dual Jev transport selection: OpenRouter Decisions (`OPENROUTER_API_KEY`, `typesafe/jev-1.13`) or direct TypeSafe System One (`TYPESAFE_API_KEY`, `jev-latest`).
- Add direct TypeSafe `/v1/systemone` wire support and `x-typesafe-request-id` capture while preserving the dependency-free client.
- Add `docs/SETUP.md` with community install, OpenRouter setup, direct TypeSafe setup, smoke tests, and recommended shadow-first configuration.
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

### 0.1.5.5 release-candidate hardening (same version)

- Added `jev_provider=openrouter|typesafe` transport selection without changing public tool contracts.
- OpenRouter remains the default and recorded live-test path (`OPENROUTER_API_KEY`, `typesafe/jev-1.13`).
- Added dependency-free direct TypeSafe System One transport (`TYPESAFE_API_KEY`, `POST /v1/systemone`, `jev-latest`, `x-typesafe-request-id`).
- Provider credentials are alternative optional manifest secrets rather than incorrectly requiring both.
- Added `docs/GUIDE.md` and `docs/PROVIDER_SETUP.md` with community usage, OpenRouter setup, direct TypeSafe setup, shadow-mode adoption, and telemetry guidance.
- Direct TypeSafe support is wire-tested against the current public SDK contract; published real-account telemetry remains OpenRouter-backed until a direct-key live report is recorded.
