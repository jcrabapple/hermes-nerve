# Changelog

## v0.1.3 — first public release candidate

- Three typed Hermes tools: `jev_decide`, `jev_rank`, and `jev_verify`.
- Optional `pre_tool_call` decision gate with `off`, `advisory`, and `enforce` modes.
- Hermes plugin settings now drive gate mode, confidence threshold, and receipt detail through `PluginContext.get_config()`.
- Privacy redaction and hash-only decision receipts by default.
- Dependency-free TypeSafe System One HTTP client with bounded output-contract validation.
- Scanner-safe offline test fixtures.
- Explicit live API smoke test and tester report template.

### Validation status

Offline tests and mocked wire-contract validation pass. A successful live authenticated TypeSafe Jev call has **not yet been recorded for this release** because the maintainer is waiting for API access. See `docs/LIVE_API_TESTING.md`.
