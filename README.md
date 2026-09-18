# Hermes-Jev

**Give Hermes a System One.**

Hermes is excellent at open-ended reasoning, planning, coding, browsing, and tool use. A large fraction of autonomous-agent control flow is not open-ended generation, though. It is bounded decisions: which tool, which worker, whether a result passed, whether to retry, whether an action needs approval, and whether confidence is high enough to continue.

Hermes-Jev turns [TypeSafe Jev](https://typesafe.ai/) into that decision layer for [Hermes Agent](https://github.com/NousResearch/hermes-agent).

> Community project. Not affiliated with or endorsed by TypeSafe AI or Nous Research.

> [!IMPORTANT]
> **LIVE API TESTING WANTED.** Offline tests and the mocked wire-contract suite pass, but this release has **not yet been validated against a real TypeSafe Jev account** because the maintainer is waiting for API access. If you already have a `TYPESAFE_API_KEY`, please run [`scripts/live_api_smoke.py`](scripts/live_api_smoke.py) using synthetic state and report the result. **Never post your key.** See [Live API testing](docs/LIVE_API_TESTING.md).

## Why this repo exists

Existing early Jev/Hermes experiments focus on one task such as skill routing or smart approvals. Hermes-Jev is intentionally broader: a reusable **DecisionContract runtime** with typed decisions, ranking, verification, privacy-aware receipts, and an opt-in Hermes lifecycle gate.

```text
             Hermes / System 2
       reason · plan · code · create
                   |
                   v
          Hermes-Jev / System One
       decide · rank · verify · gate
                   |
                   v
     execute · retry · replan · human
```

## v0.1.3 surface

### `jev_decide`
Choose exactly one label from an explicit allowed set and return the full probability distribution.

### `jev_rank`
Use the same Choice probabilities to rank a bounded candidate set for routing and prioritization.

### `jev_verify`
Return exactly one of `PASS | RETRY | REPLAN | ESCALATE` after an execution attempt.

### Optional `pre_tool_call` gate
Hermes-Jev can evaluate proposed tool calls before execution.

- `off` (default): no automatic Jev call.
- `advisory`: evaluate + receipt, never alter execution.
- `enforce`: high-confidence `BLOCK` blocks; `APPROVAL` or low confidence routes to Hermes human approval.
- provider failure in `enforce` mode **fails to human approval**, not silent execution.

The gate is intentionally opt-in because tool arguments may contain sensitive data.

## Install

Install from the standalone repository before catalog admission:

```bash
hermes plugins install keeltrace/hermes-jev --no-enable
hermes plugins enable hermes-jev
```

Set your TypeSafe key through Hermes' normal plugin environment flow or your environment:

```bash
export TYPESAFE_API_KEY='...'
```

Then verify the plugin with Hermes' real loader:

```bash
hermes plugins doctor /path/to/hermes-jev --ci
```

Once cataloged, the intended install path is:

```bash
hermes plugins install hermes-jev
```

## Automatic gate

Default is **off**.

Configure the plugin through Hermes settings:

```bash
hermes config set plugins.entries.hermes-jev.settings.gate_mode advisory --force
# or, only after evaluating it on your own traffic:
hermes config set plugins.entries.hermes-jev.settings.gate_mode enforce --force

hermes config set plugins.entries.hermes-jev.settings.min_confidence 0.85 --force
```

Hermes-Jev never treats typed output as proof of correctness. A valid label can still be the wrong label. Low confidence is routed toward human review.

## Privacy

Before any tool-call state is sent to Jev, Hermes-Jev recursively redacts common secret-bearing keys and common bearer/API-token patterns.

Receipts default to **hash-only state**:

```json
{
  "schema": "hermes-jev-receipt/v1",
  "contract": "hermes/pre-tool-gate/v1",
  "state_sha256": "...",
  "model": "jev-latest",
  "latency_ms": 123.4,
  "result": {"value": "APPROVAL", "confidence": 0.88}
}
```

Set `plugins.entries.hermes-jev.settings.receipt_detail` to `sanitized` only when you explicitly want sanitized state persisted for replay/evaluation.

Default receipt path:

```text
$HERMES_HOME/jev/receipts.jsonl
```

## Wire compatibility

The built-in client follows TypeSafe's current public System One wire shape:

- `POST /v1/systemone`
- `Authorization: Bearer <key>`
- default model `jev-latest`
- questions use the public `choice`, `noul`, and `score` schema shape

The DecisionEngine is provider-independent by design. Jev is the flagship backend, while contracts and receipts are ours.

## Decision contracts

A contract names a stable semantic boundary rather than an API call. v0.1 ships:

- `hermes/pre-tool-gate/v1`
- `rank/v1`
- `verify/v1`

The next release will add versioned external contract loading, policy compilation, and replay comparisons across model/provider versions.

## Testing

No TypeSafe key is required for the unit suite:

```bash
python -m unittest discover -s tests -v
python -m compileall -q .
```

A live Jev smoke/eval requires `TYPESAFE_API_KEY` and is deliberately separate from offline tests:

```bash
python3 scripts/live_api_smoke.py
```

See [docs/LIVE_API_TESTING.md](docs/LIVE_API_TESTING.md) for the report template.

## What is deliberately NOT claimed yet

- No successful live TypeSafe Jev API call has yet been recorded for this release.
- No live Jev benchmark has been run from this build environment.
- No claim that Jev decisions are always correct.
- No claim that the automatic gate is production-safe for every tool set.
- No claim of official TypeSafe or Nous support.

The first public benchmark should ship raw corpus/evidence, not marketing numbers.

## Roadmap

See [ROADMAP.md](ROADMAP.md). The short version: own the generic decision runtime, then add replay/evals, decision recipes, model/skill/worker routing, dashboard observability, and provider adapters while keeping the Hermes integration external to core.

## License

MIT.


## Compatibility

**v0.1.3** uses the Hermes v1 manifest envelope so it installs cleanly on Hermes Agent v0.21.2 / upstream `4716ec0b`, while retaining the same v2-era optional metadata fields that the loader understands.

