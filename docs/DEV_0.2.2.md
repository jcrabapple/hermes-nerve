# Hermes-Jev 0.2.2 development line

## v0.2.2.dev2

Adds OpenCode Zen as a native System One provider without changing the current Hermes catalog entry.

- provider: `opencode`
- endpoint: `https://opencode.ai/zen/v1/systemone`
- credential: `OPENCODE_API_KEY`
- supported model: `jev-1.13` (paid only)
- provenance transport: `opencode-zen-system-one`

OpenRouter remains the default provider. OpenRouter and direct TypeSafe remain supported. Provider credentials are isolated. `jev-1.13-free` is explicitly rejected because it does not work with Hermes. No credentialed OpenCode live result is claimed by this source change. `packaging/hermes-catalog/jev.yaml` intentionally remains at v0.2.1.2 until a later reviewed stable release.
