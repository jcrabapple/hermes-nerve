# Provider setup

Hermes-Jev v0.2.1.2 supports two System One transports behind one decision contract.

## OpenRouter

- Credential: `OPENROUTER_API_KEY`
- Endpoint: `https://openrouter.ai/api/alpha/decisions`
- Default model: `typesafe/jev-1.13`
- Provenance transport: `openrouter-decisions`

```bash
export OPENROUTER_API_KEY='...'
hermes config set plugins.entries.hermes-jev.settings.jev_provider openrouter --force
```

## TypeSafe direct

- Credential: `TYPESAFE_API_KEY`
- Endpoint: `https://api.typesafe.ai/v1/systemone`
- Default model: `jev-latest`
- Request id: `x-typesafe-request-id` when supplied
- Provenance transport: `typesafe-system-one`

```bash
export TYPESAFE_API_KEY='...'
hermes config set plugins.entries.hermes-jev.settings.jev_provider typesafe --force
```

The v0.2.1.2 release suite verifies the direct wire contract offline. Separately, issue #1 contains an independent successful live direct-TypeSafe smoke against v0.2.1.1 (typesafe-system-one, model jev-1.13.0, verified request/receipt provenance, about 299 ms). That is interoperability evidence for the v0.2.1.1 transport path, not a benchmark and not a credentialed live validation of the v0.2.1.2 candidate.