# Live API testing

Hermes-Jev supports two live provider paths: OpenRouter Decisions using `OPENROUTER_API_KEY` and direct TypeSafe System One using `TYPESAFE_API_KEY`. The recorded project live-validation evidence below is currently from OpenRouter; direct TypeSafe is wire-contract tested offline against the official SDK contract.

## Proven path

A real Muna/Hermes session has invoked the live registered `jev_decide`, `jev_assess`, and `jev_context_curate` tools and received TypeSafe provider metadata, `typesafe/jev-1.13-20260917`, `gen-dec-*` request ids, usage/cost, and network latency. That proves the Hermes -> plugin -> OpenRouter -> TypeSafe path rather than main-model simulation.

## Synthetic smoke

OpenRouter (default):

```bash
HERMES_JEV_PROVIDER=openrouter python3 scripts/live_api_smoke.py
```

Direct TypeSafe:

```bash
HERMES_JEV_PROVIDER=typesafe python3 scripts/live_api_smoke.py
```

See [`SETUP.md`](SETUP.md) for credential and Hermes config examples.

## Full live regression suite

```bash
python3 scripts/live_api_suite.py
```

The suite uses synthetic state only and covers decide, rank, verify, multi-question assess, semantic context curation, and advisory pre-tool classification. Set `HERMES_JEV_PROVIDER=openrouter` or `HERMES_JEV_PROVIDER=typesafe` before running it; the matching credential must be present. It reports per-case provider provenance plus aggregate latency/cost.

Context-engine automatic apply should be tested first in `context_engine_mode=shadow` on real sessions; the live suite is a transport/contract regression, not proof that any threshold is optimal.
