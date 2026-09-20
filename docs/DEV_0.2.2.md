# Hermes-Jev 0.2.2 development line

## v0.2.2.dev3

Runtime/reliability hardening on top of the paid-only OpenCode provider work:

- completed nervous-system turns are evicted instead of accumulating for the process lifetime;
- missing provider cost is represented as unknown, with reported-cost subtotals kept separate from missing-cost counts;
- JSONL receipts, outcomes, nervous events, and evidence records use serialized append helpers with advisory cross-process locking where available;
- secret redaction covers additional common credential formats and secret-bearing assignments/query parameters;
- development CI verifies the Hermes catalog file remains unchanged from the PR base;
- stable v0.2.1.2 verification artifacts are explicitly documented as historical release evidence.

OpenRouter remains the default provider. OpenCode remains paid-only `jev-1.13`, and the catalog entry remains v0.2.1.2.

## v0.2.2.dev2

Adds OpenCode Zen as a native System One provider without changing the current Hermes catalog entry.

- provider: `opencode`
- endpoint: `https://opencode.ai/zen/v1/systemone`
- credential: `OPENCODE_API_KEY`
- supported model: `jev-1.13` (paid only)
- provenance transport: `opencode-zen-system-one`

OpenRouter remains the default provider. OpenRouter and direct TypeSafe remain supported. Provider credentials are isolated. `jev-1.13-free` is explicitly rejected because it does not work with Hermes. No credentialed OpenCode live result is claimed by this source change. `packaging/hermes-catalog/jev.yaml` intentionally remains at v0.2.1.2 until a later reviewed stable release.
