# Hermes-Jev community guide

Hermes-Jev gives Hermes Agent a bounded System One decision layer and an experimental context-value governor powered by TypeSafe Jev.

The main Hermes model still plans, writes, codes, browses, and reasons. Jev is used for small typed judgments where a probability distribution and a constrained answer are more useful than another paragraph of generated reasoning.

## What it is useful for

### Bounded decisions

Use `jev_decide` when the allowed outputs are known in advance:

- choose a worker or tool
- retry vs replan vs escalate
- select one implementation path
- decide whether more evidence is required

The caller defines the labels. Jev cannot invent an extra outcome.

### Ranking

Use `jev_rank` for a bounded candidate set such as workers, hypotheses, files, remediation paths, or queue items.

### Verification

Use `jev_verify` after meaningful work. It returns one of:

```text
PASS
RETRY
REPLAN
ESCALATE
```

This is useful when the main agent may otherwise declare success after seeing only part of the evidence.

### Batched assessment

Use `jev_assess` to ask up to 16 independent `noul`, `choice`, or `score` questions about one shared state in one provider request. This is usually better than repeating the same state across many Jev calls.

### Selective pre-tool gating

The optional `pre_tool_call` hook can run in `off`, `advisory`, or `enforce` mode.

`gate_scope=selective` is the 0.1.5.5 default. Known read-only introspection is bypassed locally, while unknown or potentially mutating actions still go to Jev. This was added after live telemetry showed that evaluating every harmless tool call was financially cheap but added unnecessary synchronous latency.

### Context governance

Long agent sessions contain several kinds of information:

- exact constraints that must survive
- unresolved failures
- large but recoverable tool output
- stale state
- contradictory observations
- repetitive low-value introspection

`jev_context_curate` asks narrow semantic questions about eligible evidence:

```text
needed_again
exact_required
superseded
conflict
```

Deterministic local policy then chooses:

```text
KEEP_EXACT
PIN
ANCHOR
DROP
```

The goal is not maximum compression. The goal is the smallest sufficient working context that still lets the main model continue correctly.

### Rehydration

`ANCHOR` preserves provenance and a recovery pointer. `jev_context_rehydrate` restores sanitized evidence from the local ledger if it becomes useful later. Rehydration itself is local and makes no Jev provider call.

### Telemetry

`jev_stats` is local-only and reports:

- provider receipt counts
- cost and token usage when available
- latency
- contracts and models
- selective-gate bypass/evaluation counts
- estimated provider calls avoided
- evidence events
- shadow plans
- rehydrations

## Recommended adoption path

### 1. Install and verify

```bash
hermes plugins install hermes-jev
hermes plugins doctor hermes-jev --ci
```

For pre-catalog testing, install from `keeltrace/hermes-jev` instead.

### 2. Configure a provider

See [PROVIDER_SETUP.md](PROVIDER_SETUP.md).

OpenRouter is the default/live-tested transport. Direct TypeSafe is also supported.

### 3. Start with the tools

Try `jev_decide`, `jev_assess`, and `jev_verify` before enabling automatic hooks.

Example prompt:

```text
You MUST call jev_verify.

Goal: deploy SHA abc123 to production.
Observed:
- SHA abc124
- environment production
- service healthy

PASS only if the SHA exactly matches abc123, the environment is production,
and service health is healthy. Return the exact Jev probabilities and provenance.
```

### 4. Enable advisory gating

```bash
hermes config set plugins.entries.hermes-jev.settings.gate_mode advisory --force
hermes config set plugins.entries.hermes-jev.settings.gate_scope selective --force
```

Advisory mode records the decision but does not change execution.

### 5. Evaluate context curation in shadow mode

```bash
hermes config set plugins.entries.hermes-jev.settings.context_curation_mode shadow --force
hermes config set plugins.entries.hermes-jev.settings.context_engine_mode shadow --force
hermes config set context.engine jev --force
```

In ContextEngine shadow mode, Jev may produce non-mutating plans while Hermes' built-in compressor remains responsible for real pressure-driven compression.

### 6. Inspect telemetry

Inside Hermes:

```text
Call jev_stats and return the complete result.
```

Or from the plugin directory:

```bash
python3 scripts/jev_report.py
```

### 7. Only then consider apply/enforce modes

After examining real workload behavior:

```bash
hermes config set plugins.entries.hermes-jev.settings.context_engine_mode apply --force
```

and, independently if desired:

```bash
hermes config set plugins.entries.hermes-jev.settings.gate_mode enforce --force
```

Do not enable either merely to maximize token savings or automation percentage.

## How to tell whether Jev really ran

A real provider-backed result contains an execution block plus provider metadata. OpenRouter-backed calls look like:

```json
{
  "execution": {
    "engine": "hermes-jev",
    "version": "0.1.5.5",
    "transport": "openrouter-decisions",
    "live_provider_call": true
  },
  "provider": "TypeSafe",
  "request_id": "gen-dec-..."
}
```

Direct TypeSafe calls use:

```text
transport: typesafe-system-one
```

Local operations such as `jev_stats` and rehydration explicitly report `live_provider_call: false`.

## What Hermes-Jev is not

Hermes-Jev is not a replacement for the main model, a general chat model, a security sandbox, a guarantee of correctness, or a memory database. It is a bounded decision/control layer plus an experimental context governor.

Typed output prevents free-form answer drift; it does not make an incorrect decision impossible. Keep deterministic safety rules around consequential actions.

## Privacy model

All state sent to Jev is passed through recursive secret redaction. Decision receipts default to hash-only state. The context ledger is separate: `sanitized` mode supports rehydration, while `hash` mode stores no rehydratable content.

External provider use still crosses a network boundary. Choose OpenRouter or direct TypeSafe according to your data-handling requirements.

## What to measure

Do not optimize only for tokens removed. Better measures include:

- task completion rate
- false-forget rate
- exact constraint retention
- stale evidence retained
- rehydrations
- repeated tool calls caused by missing evidence
- total prompt tokens over long tasks
- Jev latency overhead
- Jev provider cost
- continuation fidelity after context curation

The desired outcome is better agent continuation per context token, not the highest possible compression ratio.
