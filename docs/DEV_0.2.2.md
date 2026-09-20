# Hermes-Jev 0.2.2 development line

## v0.2.2.dev1

Adds OpenCode Zen as a native System One provider without changing the current Hermes catalog entry.

- provider: `opencode`
- endpoint: `https://opencode.ai/zen/v1/systemone`
- credential: `OPENCODE_API_KEY`
- default model: `jev-1.13-free`
- optional paid model: `jev-1.13`
- provenance transport: `opencode-zen-system-one`

OpenRouter remains the default provider. OpenRouter and direct TypeSafe remain supported. Provider credentials are isolated. No credentialed OpenCode live result is claimed by this source change. `packaging/hermes-catalog/jev.yaml` intentionally remains at v0.2.1.2 until a later reviewed stable release.
