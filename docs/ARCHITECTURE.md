

## Provider transports

The `DecisionEngine` contract is transport-independent. `JevClient` selects one of two dependency-free HTTP transports:

- `openrouter` -> OpenRouter Decisions, `OPENROUTER_API_KEY`, model setting `jev_model`.
- `typesafe` -> direct TypeSafe System One, `TYPESAFE_API_KEY`, model setting `typesafe_model`.

Both normalize into the same `JevResponse` shape. Execution provenance records `openrouter-decisions` or `typesafe-system-one`, so receipts remain attributable after switching providers.

# Architecture — Hermes-Jev v0.1.5.5

```text
Hermes / main model
   |
   +-- explicit Jev tools ------------------------+
   |                                              |
   +-- pre_tool_call gate                         |
   |                                              v
   +-- post_tool_call evidence observer       DecisionEngine
   |                                              |
   +-- optional ContextEngine ----------------> JevClient
                                                  |
                                          OpenRouter Decisions
                                                  |
                                             TypeSafe Jev
```

## Decision layer

`DecisionEngine` validates typed contracts, redacts state, calls the provider, validates returned labels, records receipts, and attaches execution provenance.

`jev_assess` is the preferred primitive for shared-state policies because up to 16 independent typed questions can share one provider request.


## Pre-tool gate

The automatic gate is intentionally split into two stages:

1. a deterministic local prefilter handles only conservative, known read-only calls,
2. Jev evaluates everything else when `gate_mode` is enabled.

`gate_scope=selective` is the default because live telemetry showed the old evaluate-every-call path spending most provider requests on routine `ALLOW` decisions. `gate_scope=all` disables the prefilter for compatibility/testing. Jev's own `jev_*` tools always bypass the gate to prevent recursion. Local `gate-events.jsonl` telemetry records bypass/evaluation counts and observed Jev latency without storing raw tool arguments.

## Context-value layer

`context.py` separates uncertain semantics from deterministic policy:

- Jev: needed again / exact required / superseded / conflict.
- Local code: recoverability, leases, thresholds, KEEP/PIN/ANCHOR/DROP.

`ledger.py` provides redacted local evidence persistence, shadow telemetry, and rehydration.

`lifecycle.py` shares the most recent verification state with context policy.

## ContextEngine

`JevContextEngine` implements Hermes' public context engine interface. It governs eligible old tool-result evidence while protecting system/head/tail messages. It does not mutate persistent history through `select_context`; selection remains no-op for cache stability.

At an apply boundary:

1. collect eligible old tool results and pair them with their originating tool call,
2. classify recoverability deterministically,
3. run semantic curation,
4. replace ANCHOR/DROP candidates with anchors while preserving tool protocol,
5. if no safe progress is possible, optionally delegate to built-in `ContextCompressor`.

The engine is registered but never selected automatically; global `context.engine` must be set to `jev`.
