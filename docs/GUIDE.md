# Hermes-Jev v0.2.1.1 guide

## What changed

Jev is no longer primarily a synchronous gate. The recommended architecture is an asynchronous decision nervous system:

- one parallel OFF/WATCH/ON admission assessment per user turn;
- a local structured-event router that accumulates state without provider calls;
- remote Jev only when semantic decision value justifies it;
- Hermes' proposed choice embedded in the original decision event;
- silent agreement / low-confidence disagreement;
- high-confidence, still-current disagreement delivered as a challenge;
- completion, recovery and major strategy changes treated as high-value decision boundaries;
- event batching and semantic hysteresis for long autonomous runs.

## When to emit an explicit decision event

Use `jev_nervous_event` for accountable choices that can alter trajectory, completion, risk, cost, or external state. Do not emit it for ordinary reads, status checks, conversational turns, or fictional actor-plane choices.

Useful types include `DECISION`, `STRATEGY_CHANGE`, `RECOVERY`, `COMPLETION_CANDIDATE`, `CONSEQUENTIAL_ACTION`, `HUMAN_ESCALATION`, and `IRREVERSIBLE_ACTION`.

## Existing tools remain

`jev_decide`, `jev_rank`, `jev_verify`, `jev_assess`, `jev_context_curate`, `jev_context_rehydrate`, and `jev_stats` remain supported. `jev_nervous_event` is the eighth tool.

## Context governor

The existing KEEP_EXACT/PIN/ANCHOR/DROP/REHYDRATE context-governance system remains available and shadow-first. It is complementary to the decision nervous system, not a replacement for it.

See `NERVOUS_SYSTEM.md`, `SETUP.md`, and `PROVIDER_SETUP.md` for the v0.2 architecture and setup.
