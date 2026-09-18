# Live API testing

Hermes-Jev's supported live provider path is OpenRouter's Decisions API using `OPENROUTER_API_KEY`.

## Proven path

A real Muna/Hermes session has invoked the live registered `jev_decide`, `jev_assess`, and `jev_context_curate` tools and received TypeSafe provider metadata, `typesafe/jev-1.13-20260917`, `gen-dec-*` request ids, usage/cost, and network latency. That proves the Hermes -> plugin -> OpenRouter -> TypeSafe path rather than main-model simulation.

## Synthetic smoke

```bash
set -a
source ~/.hermes/profiles/muna/.env
set +a
python3 scripts/live_api_smoke.py
```

## Full live regression suite

```bash
python3 scripts/live_api_suite.py
```

The suite uses synthetic state only and covers decide, rank, verify, multi-question assess, semantic context curation, and advisory pre-tool classification. It reports per-case provider provenance plus aggregate latency/cost.

Context-engine automatic apply should be tested first in `context_engine_mode=shadow` on real sessions; the live suite is a transport/contract regression, not proof that any threshold is optimal.
