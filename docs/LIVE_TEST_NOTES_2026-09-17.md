# Live test notes — 2026-09-17

These observations came from an interactive Hermes/Muna session using a free primary model (`solar-pro4:free`) while Hermes-Jev made real TypeSafe Jev calls through OpenRouter Decisions.

## Verified provider chain

The live registry exposed the Jev plugin tools, and Hermes actually dispatched them. Real results returned `provider=TypeSafe`, a pinned `typesafe/jev-1.13-20260917` model id, `gen-dec-*` request ids, token usage, latency, and nonzero cost. This distinguishes provider execution from the primary LLM merely imitating a Jev response.

## Samples

| Test | Result | Input tokens | Output tokens | Latency | Cost |
|---|---|---:|---:|---:|---:|
| Obvious CUDA route | `gpu_worker`, confidence 1.0 | 334 | 43 | 473.072 ms | $0.000014028 |
| Indistinguishable workers | `ask_human`, confidence 0.84; P(ask_human)=0.90 | 348 | 44 | 215.180 ms | $0.000014616 |
| Batched incident assessment | payments owner=1.0, critical=1.0, urgent=0.97 | 472 | 77 | 389.252 ms | $0.000019824 |
| Context curation prototype | preserved all four items; no destructive reduction | 1110 | 117 | 599.600 ms | $0.000046620 |

Totals for these four provider calls:

- cost: **$0.000095088**
- input tokens: **2,264**
- output tokens: **281**
- average provider latency: **419.276 ms**

## What the tests changed

The original context curation prototype used one confidence threshold for `KEEP/STUB/DROP`. In the live synthetic curation case, stale/recoverable `pwd` and `ls` evidence remained because Jev's returned confidences were below the global destructive threshold. This was safe but yielded zero reduction.

The resulting design change is the context-value governor now shipped in 0.1.5.4+: Jev estimates separate semantic dimensions (`needed_again`, `exact_required`, `superseded`, `conflict`) and local deterministic policy selects `KEEP_EXACT`, `PIN`, `ANCHOR`, or `DROP`. Recoverability, size, lifecycle, and protocol safety are determined locally rather than delegated to the model.

## Telemetry issue found during 0.1.5.4 testing

Running `python3 scripts/context_shadow_report.py` directly from a named profile plugin directory reported the global default ledger at `~/.hermes/jev/context-ledger.jsonl`, even though the `muna` wrapper runs Hermes with `HERMES_HOME=~/.hermes/profiles/muna`. A zero report therefore could mean "wrong ledger selected" rather than "no telemetry produced."

0.1.5.5 fixes this by:

- resolving paths through Hermes' own `get_hermes_home()` when available,
- inferring the named profile from the plugin path for standalone reporting,
- adding `scripts/jev_report.py` for combined decision/context telemetry,
- adding the local `jev_stats` tool so a running Hermes session can report the exact active-profile telemetry without shell-path ambiguity.

## Release posture

Context curation and the Jev context engine default to **shadow** in 0.1.5.5. The bounded decision/assessment/verification tools remain usable normally. Automatic application should be enabled only after a user reviews their own telemetry and continuation behavior.
## Extended live telemetry — selective gate finding

After the longer Muna run, `jev_stats` reported:

- 119 total receipts
- 109 live provider calls
- 106 `hermes/pre-tool-gate/v1` receipts, all `ALLOW`
- 90,403 input tokens and 4,880 output tokens
- $0.003796926 total provider cost
- 593.36 ms average provider latency
- 106 unique context evidence events in the active Muna profile ledger

The financial cost was negligible, but the synchronous gate dominated call volume and added avoidable latency. This directly changed the same `0.1.5.5` release candidate: `gate_scope=selective` is now the default and known read-only introspection is bypassed locally. Unknown/mutating actions still receive Jev classification. `gate_scope=all` preserves the previous behavior for users who explicitly want every non-Jev tool call evaluated.

The context ledger itself was healthy (106/106 unique evidence events). Automatic shadow plans remained zero because the tested sessions did not reach the configured context-pressure trigger, so pressure-driven anchoring/rehydration remains not yet exercised by this dataset.
