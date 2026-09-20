# Live API testing

Hermes-Jev supports OpenRouter Decisions, direct TypeSafe System One, and OpenCode Zen System One. Only the selected provider credential is required.

## Proven live paths

### OpenRouter -> TypeSafe

A real Muna/Hermes session invoked the registered `jev_decide`, `jev_assess`, and `jev_context_curate` tools through OpenRouter and received TypeSafe provider metadata, model/request IDs, usage/cost, and network latency. This proves the Hermes -> plugin -> OpenRouter -> TypeSafe path rather than main-model simulation.

### Direct TypeSafe System One

Issue #1 contains two independent direct-account reports against Hermes-Jev v0.2.1.1. One reported a successful smoke with `live_provider_call: true`, `transport: typesafe-system-one`, `provenance_status: VERIFIED`, provider `TypeSafe`, model `jev-1.13.0`, a TypeSafe request ID, a receipt ID, `ok: true`, and approximately 299 ms latency. A second tester ran the smoke, full live suite, and the plugin through Hermes itself: all eight tools registered, the direct transport remained verified, and the suite completed successfully.

The second report also confirmed that direct TypeSafe responses include token usage but may omit a provider cost field. Current development telemetry therefore reports missing cost as unknown rather than inventing a zero, while retaining any provider-reported cost subtotal separately.

These reports are interoperability evidence for the v0.2.1.1 direct transport. They are not benchmarks, do not establish decision accuracy/calibration, and are not represented as credentialed live runs of a later release unless that later candidate is explicitly retested.

### OpenCode Zen System One

v0.2.2.dev4 retains offline wire-contract coverage for OpenCode Zen. No credentialed OpenCode live run is claimed until one is actually performed.

## Synthetic smoke

Select the provider and set only its credential:

```bash
export HERMES_JEV_PROVIDER=openrouter
export OPENROUTER_API_KEY='...'
python3 scripts/live_api_smoke.py
```

or:

```bash
export HERMES_JEV_PROVIDER=typesafe
export TYPESAFE_API_KEY='...'
python3 scripts/live_api_smoke.py
```

or:

```bash
export HERMES_JEV_PROVIDER=opencode
export OPENCODE_API_KEY='...'
export HERMES_JEV_OPENCODE_MODEL=jev-1.13
python3 scripts/live_api_smoke.py
```

The smoke sends synthetic state only.

## Full live regression suite

```bash
python3 scripts/live_api_suite.py
```

The suite uses synthetic state only and covers decide, rank, verify, multi-question assess, semantic context curation, and advisory pre-tool classification. It reports per-case provider provenance plus aggregate latency and provider-reported cost coverage. If any provider-backed case omits cost metadata, `total_cost` is `null`; `provider_reported_cost` and the reported/missing case counts remain available without inventing a zero.

Context-engine automatic apply should be tested first in `context_engine_mode=shadow` on real sessions. The live suite is a transport/contract regression, not proof that any context threshold or retention policy is optimal.
