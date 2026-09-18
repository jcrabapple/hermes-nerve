# Live API testing wanted

Hermes-Jev's offline unit tests, contract checks, and mocked wire-protocol tests do **not** prove that the current public TypeSafe Jev service accepts and answers this build correctly in a real account.

The maintainer is currently waiting for TypeSafe API access for live validation.

If you already have a `TYPESAFE_API_KEY`, please test the release and report the result. The smoke test sends **synthetic state only**.

```bash
export TYPESAFE_API_KEY='...'
python3 scripts/live_api_smoke.py
```

Do **not** paste your API key into an issue, PR, terminal transcript, screenshot, or chat.

Please report:

- Hermes version
- Python version
- OS
- Hermes-Jev release/commit
- whether the smoke test returned `ok: true`
- returned model name
- selected choice and confidence
- HTTP/status error text if it failed (with credentials removed)
- approximate latency

A successful smoke is useful interoperability evidence, not a benchmark and not proof that Jev decisions are always correct.
