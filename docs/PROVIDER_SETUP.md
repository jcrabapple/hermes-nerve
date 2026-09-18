# Provider setup

Hermes-Jev 0.1.5.5 supports two Jev transports without changing any Hermes tool contract:

- **OpenRouter** — default and live-tested in Hermes-Jev.
- **TypeSafe direct** — first-class direct System One transport using TypeSafe's public API wire contract.

Only one credential is needed for the provider you select.

## Option A — OpenRouter (default)

Use this if you already use OpenRouter, want one shared billing/key surface, or want to reproduce the path exercised by the published Hermes-Jev live tests.

### 1. Create an OpenRouter key

Create a key in the OpenRouter dashboard and expose it to the Hermes process:

```bash
export OPENROUTER_API_KEY='...'
```

For a persistent Hermes profile, put the secret in the profile environment using the normal Hermes secrets/configuration flow instead of committing it to a repository.

### 2. Select OpenRouter

```bash
hermes config set plugins.entries.hermes-jev.settings.jev_provider openrouter --force
hermes config set plugins.entries.hermes-jev.settings.jev_model typesafe/jev-1.13 --force
```

`typesafe/jev-1.13` is the exact model family used by the recorded live tests. OpenRouter also publishes a Jev latest alias; pinning an exact version is preferable when reproducing tests.

### 3. Verify

```bash
hermes plugins doctor hermes-jev --ci
HERMES_JEV_PROVIDER=openrouter python3 scripts/live_api_smoke.py
```

A live result should show provenance similar to:

```text
transport: openrouter-decisions
provider: TypeSafe
model: typesafe/jev-1.13-...
request_id: gen-dec-...
```

Hermes-Jev uses OpenRouter's Decisions transport for Jev, not a normal chat-completions prompt.

---

## Option B — TypeSafe direct

Use this if you have direct TypeSafe access and want Hermes-Jev to call the System One API without routing through OpenRouter.

### 1. Obtain a TypeSafe API key

Expose it to the Hermes process:

```bash
export TYPESAFE_API_KEY='...'
```

TypeSafe's public SDK uses the same environment variable.

### 2. Select TypeSafe direct

```bash
hermes config set plugins.entries.hermes-jev.settings.jev_provider typesafe --force
hermes config set plugins.entries.hermes-jev.settings.typesafe_model jev-latest --force
```

The direct transport defaults to:

```text
base URL: https://api.typesafe.ai
endpoint: POST /v1/systemone
model: jev-latest
credential: TYPESAFE_API_KEY
```

If TypeSafe gives you a different base URL, the underlying client also honors `TYPESAFE_BASE_URL`.

### 3. Verify

```bash
HERMES_JEV_PROVIDER=typesafe python3 scripts/live_api_smoke.py
```

A direct result should show:

```text
transport: typesafe-system-one
provider: TypeSafe
model: jev-latest (or the resolved model)
request_id: <x-typesafe-request-id>
```

The direct wire contract is covered by the offline test suite against the current public TypeSafe SDK schema. The release's published real-account telemetry was collected through OpenRouter, so direct mode should be described as **wire-verified** until a direct-key live report is contributed.

---

## Switching providers

Switching provider does not change the Hermes-visible tools:

```text
jev_decide
jev_rank
jev_verify
jev_assess
jev_context_curate
jev_context_rehydrate
jev_stats
```

Only the transport, credential, default model, request-id source, and provider billing path change.

```bash
# OpenRouter
hermes config set plugins.entries.hermes-jev.settings.jev_provider openrouter --force

# TypeSafe direct
hermes config set plugins.entries.hermes-jev.settings.jev_provider typesafe --force
```

Restart the Hermes session after changing provider configuration.

## Troubleshooting

### `OPENROUTER_API_KEY is not configured`

The selected provider is `openrouter`, but the Hermes process cannot see that variable.

### `TYPESAFE_API_KEY is not configured`

The selected provider is `typesafe`, but the Hermes process cannot see that variable.

### Wrong model format

OpenRouter model IDs and direct TypeSafe model IDs are intentionally separate settings:

```text
OpenRouter: jev_model = typesafe/jev-1.13
TypeSafe direct: typesafe_model = jev-latest
```

Do not put the OpenRouter slug into `typesafe_model` unless TypeSafe explicitly documents that slug.
