# Setup: OpenRouter or direct TypeSafe

Hermes-Jev supports two Jev transports in v0.1.5.5:

- **OpenRouter** (default): OpenRouter Decisions API -> TypeSafe Jev.
- **TypeSafe direct**: TypeSafe System One API directly.

You only need **one** credential path. The plugin deliberately does not require both keys at load time.

## Install

Before catalog admission:

```bash
hermes plugins install keeltrace/hermes-jev --no-enable
hermes plugins enable hermes-jev
```

After catalog admission:

```bash
hermes plugins install hermes-jev
```

Verify registration:

```bash
hermes plugins doctor hermes-jev --ci
```

v0.1.5.5 should register 7 tools, 2 hooks, and the optional `jev` ContextEngine.

## Option A: OpenRouter (default)

Get an OpenRouter key from <https://openrouter.ai/keys> and make it available to the Hermes profile:

```bash
export OPENROUTER_API_KEY='...'
```

For a named Hermes profile, storing it in that profile's `.env` is usually more convenient.

Select OpenRouter explicitly:

```bash
hermes config set plugins.entries.hermes-jev.settings.jev_provider openrouter --force
hermes config set plugins.entries.hermes-jev.settings.jev_model typesafe/jev-1.13 --force
```

Transport details:

```text
API:   https://openrouter.ai/api/alpha/decisions
Key:   OPENROUTER_API_KEY
Model: typesafe/jev-1.13
```

This is the path used for the project's recorded live Hermes tests. Real calls returned TypeSafe provider metadata, versioned Jev model IDs, request IDs, token usage, cost, and latency.

## Option B: direct TypeSafe

Get a TypeSafe API key and expose it to the Hermes profile:

```bash
export TYPESAFE_API_KEY='...'
```

Select the direct provider:

```bash
hermes config set plugins.entries.hermes-jev.settings.jev_provider typesafe --force
hermes config set plugins.entries.hermes-jev.settings.typesafe_model jev-latest --force
```

Transport details:

```text
API:   https://api.typesafe.ai/v1/systemone
Key:   TYPESAFE_API_KEY
Model: jev-latest
```

The direct transport is dependency-free and follows TypeSafe's current official Python SDK wire contract: Bearer authentication, `/v1/systemone`, typed `noul` / `choice` / `score` questions, and `answers` in the response. The client also records `x-typesafe-request-id` when present.

The direct path is covered by offline wire-contract tests. At the time of the v0.1.5.5 PR update, the project's recorded live test evidence is from the OpenRouter path, not a live direct-TypeSafe account. That distinction is intentional.

## Synthetic live smoke

The same smoke script works for either transport.

OpenRouter:

```bash
HERMES_JEV_PROVIDER=openrouter python3 scripts/live_api_smoke.py
```

Direct TypeSafe:

```bash
HERMES_JEV_PROVIDER=typesafe python3 scripts/live_api_smoke.py
```

The scripts send synthetic state only.

## Recommended first configuration

Keep automatic gating off while learning the tools:

```bash
hermes config set plugins.entries.hermes-jev.settings.gate_mode off --force
```

Try `jev_decide`, `jev_assess`, and `jev_verify` manually first.

If you want to evaluate automatic tool gating later:

```bash
hermes config set plugins.entries.hermes-jev.settings.gate_mode advisory --force
hermes config set plugins.entries.hermes-jev.settings.gate_scope selective --force
```

`selective` locally bypasses conservative read-only calls and sends material/unknown calls to Jev. Use `gate_scope=all` only if you explicitly want every non-Jev tool call evaluated.

For context governance, start shadow-first:

```bash
hermes config set plugins.entries.hermes-jev.settings.context_curation_mode shadow --force
hermes config set plugins.entries.hermes-jev.settings.context_engine_mode shadow --force
hermes config set context.engine jev --force
```

In shadow mode, Hermes' built-in compressor continues to perform real compaction while Jev records non-mutating proposals.

## Confirm which provider actually ran

Live Jev results include execution provenance. OpenRouter results use:

```json
{"transport":"openrouter-decisions","live_provider_call":true}
```

Direct TypeSafe results use:

```json
{"transport":"typesafe-system-one","live_provider_call":true}
```

Use `jev_stats` for local receipt, gate, and context telemetry without making another provider call.
