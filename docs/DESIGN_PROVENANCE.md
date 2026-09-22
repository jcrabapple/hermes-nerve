# Design provenance — v0.1.5.5

The original context work was inspired by the general product idea demonstrated by `tamaratran/fast-jev-compaction`: use a fast typed decision model to judge context value instead of asking a generative model to rewrite all old context.

For Nerve development, only that repository's README and repository layout were inspected through GitHub. Its implementation files were not fetched into the working tree or copied.

v0.1.5.5 is independently designed for Hermes' Python plugin architecture and current public ContextEngine API. Distinctive choices include:

- four independent `noul` semantic judgments rather than direct KEEP/DROP classification,
- deterministic recoverability and action thresholds,
- `KEEP_EXACT / PIN / ANCHOR / DROP / REHYDRATE`,
- lifecycle leases tied to `nerve_verify`,
- contradiction/supersession assessment,
- privacy-minimized local evidence ledger,
- explicit shadow telemetry,
- automatic tool-result anchoring that preserves protocol structure,
- opt-in `ctx.register_context_engine()` integration,
- no-op per-request `select_context()` for cache stability,
- fallback to Hermes' built-in compressor when Jev makes no safe progress.

The implementation uses Hermes' documented public plugin/context-engine surfaces; it does not patch private compaction internals.
