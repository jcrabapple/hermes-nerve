# Hermes-Jev

**Give Hermes a bounded System One decision layer and a context-value governor.**

Hermes-Jev connects Hermes Agent to TypeSafe Jev either through **OpenRouter's Decisions API** (default) or the **TypeSafe System One API directly**. It is built for narrow, typed judgments that should not require the main generative model to improvise an answer: routing, ranking, verification, multi-question assessment, tool gating, and context-value decisions.

> Community project. Not affiliated with or endorsed by TypeSafe AI or Nous Research.

## v0.1.5.5

The release moves context management from "save tokens" to **preserve the smallest sufficient working set for correct continuation**.

Public tools:

- `jev_decide` — one bounded choice plus calibrated probabilities.
- `jev_rank` — rank a bounded candidate set from Jev probabilities.
- `jev_verify` — `PASS | RETRY | REPLAN | ESCALATE` verification.
- `jev_assess` — up to 16 native `noul`, `choice`, or `score` questions over one shared state.
- `jev_context_curate` — semantic context-value planning with deterministic retention policy.
- `jev_context_rehydrate` — restore sanitized evidence from a local evidence anchor; no provider call.
- `jev_stats` — local active-profile receipt + context telemetry; no provider call.

Hooks:

- `pre_tool_call` — optional `off | advisory | enforce` Jev gate.
- `post_tool_call` — privacy-minimized evidence observation for context telemetry/rehydration.

Optional context engine:

- `context.engine: jev` — Jev-first context management using Hermes' public `ContextEngine` interface.
- Never auto-activated. The built-in Hermes compressor remains the default until explicitly selected.
- If Jev cannot safely reclaim eligible tool evidence, the engine can fall back to Hermes' built-in `ContextCompressor` rather than stall on text-heavy sessions.

## Quick start

Install and validate:

```bash
hermes plugins install hermes-jev
hermes plugins doctor hermes-jev --ci
```

Choose a provider:

```bash
# OpenRouter (default; live-tested)
export OPENROUTER_API_KEY='...'
hermes config set plugins.entries.hermes-jev.settings.jev_provider openrouter --force

# OR TypeSafe direct
export TYPESAFE_API_KEY='...'
hermes config set plugins.entries.hermes-jev.settings.jev_provider typesafe --force
```

See the full [community guide](docs/GUIDE.md) and [provider setup](docs/PROVIDER_SETUP.md).

## The context governor

Jev does **not** decide deletion directly. For each eligible evidence unit it estimates four semantic quantities:

- `needed_again` — probability the evidence will matter later in the current goal.
- `exact_required` — probability exact original detail will be needed rather than provenance/identity.
- `superseded` — probability newer state has made the evidence stale or redundant.
- `conflict` — probability it participates in an unresolved contradiction.

Local deterministic code then chooses an action:

- `KEEP_EXACT` — retain original content.
- `PIN` — keep exact while a lifecycle lease is active or conflict is unresolved.
- `ANCHOR` — replace bulk content with deterministic provenance, hash, prefix, and recovery pointer.
- `DROP` — allowed only for deterministically recoverable, low-value, superseded evidence in explicit curation.
- `REHYDRATE` — restore sanitized anchored evidence from the local ledger.

Automatic ContextEngine mode never physically removes a tool-result message because doing so can orphan its corresponding assistant tool call. A proposed `DROP` becomes a minimal anchor instead.

### Lifecycle leases

User/assistant text is protected. Nonrecoverable failure evidence is automatically leased `until_verification_pass`; a real `jev_verify` `PASS` releases that lease for later curation. Callers can also provide an explicit `metadata.lease`.

### Shadow mode

Use `mode=shadow` to collect Jev's proposed actions without changing returned evidence. Shadow plans are written to the evidence ledger and can be summarized with:

```bash
python3 scripts/context_shadow_report.py
python3 scripts/jev_report.py
```

The report includes proposed action counts, proposed character savings, rehydration counts, and recovery-demand rate. The standalone reporter is profile-aware: when launched from `~/.hermes/profiles/<name>/plugins/hermes-jev`, it infers that profile instead of silently reading the global default ledger. Recovery demand is a tuning signal, not automatically a false-forget failure.

Inside Hermes, `jev_stats` is the preferred sanity check because it reads the exact active-profile paths used by the running process.

See [`docs/CONTEXT_CURATION.md`](docs/CONTEXT_CURATION.md).

## Provenance

Every live Jev result carries an explicit execution block so a main chat model cannot be mistaken for the decision provider:

```json
{
  "execution": {
    "engine": "hermes-jev",
    "version": "0.1.5.5",
    "transport": "openrouter-decisions",
    "live_provider_call": true
  },
  "provider": "TypeSafe",
  "model": "typesafe/jev-1.13-20260917",
  "request_id": "gen-dec-..."
}
```

`jev_context_rehydrate` instead reports `transport: local-evidence-ledger` and `live_provider_call: false`. `jev_stats` reports `transport: local-telemetry`.

## Setup and provider selection

See [`docs/SETUP.md`](docs/SETUP.md) for a complete install guide. v0.1.5.5 supports two transports:

| Provider | Setting | Credential | Default model | Endpoint |
| --- | --- | --- | --- | --- |
| OpenRouter (default) | `jev_provider=openrouter` | `OPENROUTER_API_KEY` | `typesafe/jev-1.13` | `/api/alpha/decisions` |
| TypeSafe direct | `jev_provider=typesafe` | `TYPESAFE_API_KEY` | `jev-latest` | `/v1/systemone` |

OpenRouter:

```bash
hermes config set plugins.entries.hermes-jev.settings.jev_provider openrouter --force
hermes config set plugins.entries.hermes-jev.settings.jev_model typesafe/jev-1.13 --force
```

Direct TypeSafe:

```bash
hermes config set plugins.entries.hermes-jev.settings.jev_provider typesafe --force
hermes config set plugins.entries.hermes-jev.settings.typesafe_model jev-latest --force
```

Only the key for the selected provider is required. `model_id` remains accepted as a migration alias for the hand-fixed 0.1.5.1 OpenRouter tree.

```bash
hermes config set plugins.entries.hermes-jev.settings.timeout_seconds 15 --force
```

### Gate

```bash
hermes config set plugins.entries.hermes-jev.settings.gate_mode advisory --force
```

Modes:

- `off` — no automatic Jev gate calls.
- `advisory` — evaluate material/unknown calls and receipt them, never alter execution.
- `enforce` — high-confidence `BLOCK` can block; `APPROVAL`, low confidence, or provider failure route toward human approval.

`0.1.5.5` defaults the gate to `gate_scope=selective`. A conservative local prefilter bypasses Jev for exact known read-only Hermes tools and narrowly parsed read-only terminal commands (`pwd`, `ls`, `rg`, `git status`, `git diff`, etc.). Unknown, mutating, shell-composed, or ambiguous calls still go to Jev. This removes a network round trip from routine introspection without weakening the gate for consequential actions.

To restore the old evaluate-every-call behavior:

```bash
hermes config set plugins.entries.hermes-jev.settings.gate_scope all --force
```

`jev_stats` reports gate events separately (`bypassed`, `evaluated`, provider errors, provider latency, and estimated provider calls avoided) so the latency impact is directly measurable.

### Explicit curation

Recommended evaluation phase:

```bash
hermes config set plugins.entries.hermes-jev.settings.context_curation_mode shadow --force
```

Switch to `apply` only after reviewing your own shadow telemetry.

### Evidence ledger

Defaults:

```text
$HERMES_HOME/jev/context-ledger.jsonl
```

`context_ledger_detail=sanitized` stores force-redacted content and supports rehydration. `hash` stores no rehydratable content and is the stricter privacy mode.

### Opt-in ContextEngine

Hermes still uses its built-in compressor unless you explicitly select Jev:

```bash
hermes config set context.engine jev --force
```

Useful settings:

```bash
hermes config set plugins.entries.hermes-jev.settings.context_engine_mode shadow --force
hermes config set plugins.entries.hermes-jev.settings.context_engine_threshold_percent 0.72 --force
hermes config set plugins.entries.hermes-jev.settings.context_engine_fallback_builtin true --force
```

Both `context_curation_mode` and `context_engine_mode` default to `shadow` in 0.1.5.5. After evaluating shadow mode, use `context_engine_mode=apply` to let the engine anchor eligible old tool evidence at compaction boundaries.

Do **not** add `jev` to a saved static platform-toolset list merely to expose these tools. Hermes dynamically registers plugin tools; on current Hermes builds a saved `jev` entry may produce an early `Unknown toolsets: jev` warning before plugin discovery even though the plugin subsequently loads correctly.

## Privacy

All Jev-bound state goes through Hermes-Jev's recursive secret redaction. Decision receipts default to hash-only state. The evidence ledger is separate because rehydration requires retaining content; its `sanitized` mode force-redacts stored content and metadata.

Decision receipts:

```text
$HERMES_HOME/jev/receipts.jsonl
```

Evidence ledger:

```text
$HERMES_HOME/jev/context-ledger.jsonl
```

See [`SECURITY.md`](SECURITY.md).

## Testing

Offline:

```bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q .
```

Live synthetic regression suite:

```bash
set -a
source ~/.hermes/profiles/muna/.env
set +a
python3 scripts/live_api_suite.py
```

The **OpenRouter** path has been validated live through Hermes -> hermes-jev -> OpenRouter Decisions -> TypeSafe Jev using free primary Hermes models. The harvested session later reached 121 receipts / 111 provider calls, and the selective-gate fix was verified to bypass read-only calls with zero new provider calls. The **direct TypeSafe** transport is covered by offline wire-contract tests against the current official SDK contract; it is not presented as live-validated by this project yet. See [`docs/LIVE_TEST_NOTES_2026-09-17.md`](docs/LIVE_TEST_NOTES_2026-09-17.md) and [`docs/SETUP.md`](docs/SETUP.md).

## Benchmarking objective

Raw compression ratio is not the primary metric. The target is **continuation fidelity per context token**: preserve constraints and exact failure evidence, reduce stale/recoverable clutter, avoid repeated work, and successfully rehydrate when older evidence becomes relevant again.

See [`docs/BENCHMARKING.md`](docs/BENCHMARKING.md).

## License

MIT
