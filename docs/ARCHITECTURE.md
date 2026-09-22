# Architecture — Nerve v0.2.2.dev4

## Public seam

The v0.2 decision architecture is deliberately deep: `NervousSystem` is the main orchestration seam. It owns turn admission, structured event intake, local relevance routing, remote assessment dispatch, challenge lifecycle, batching, staleness checks, and telemetry. `router.py` is local-only significance logic; `outcomes.py` owns decision/outcome learning data; `client.py` owns provider transport.

```text
user prompt
   |\
   | +--> async Jev turn admission --> OFF / WATCH / ON
   |
   +----> Hermes work loop -------------------------------+
                         |                                |
                         +--> structured events           |
                                  |                       |
                                  v                       |
                         local adaptive router             |
                           | no        | yes               |
                           v           v                   |
                       accumulate   async Jev              |
                                      |                    |
                         agree/low confidence              |
                              |       high-conflict        |
                              v            |               |
                             log           v               |
                                      challenge queue      |
                                           |               |
                              transform_tool_result <------+
```

Hermes remains the reasoning and execution engine. Jev is not placed in front of ordinary tool calls. The old pre-tool gate remains an opt-in compatibility/safety surface and defaults off.

## Hook mapping

- `pre_llm_call`: start/reuse turn; enqueue admission; returns immediately.
- `post_tool_call`: observe tool outcome and update the local event stream.
- `transform_tool_result`: attach a still-current high-confidence challenge to the next model-bound result.
- `pre_verify`: completion boundary; may consume an already-arrived challenge in precommit mode, never waits for one.
- `post_llm_call` / `on_session_end`: close turn-scoped supervision.
- `pre_tool_call`: legacy selective gate only.

## Provider seam

All three transports implement the same System One contract:

- OpenRouter Decisions -> `openrouter-decisions`
- TypeSafe System One direct -> `typesafe-system-one`
- OpenCode Zen System One -> `opencode-zen-system-one`

Provider selection does not change Hermes-visible tools or nervous-system schemas.

## State and challenge safety

Every event can carry state and decision versions. The challenge queue validates freshness before delivery. Late Jev answers are telemetry, not retroactive commands. Already-committed irreversible actions are never blindly rewound.

## Context governor

The v0.1.x context-value governor remains a separate, optional deep seam. The nervous system can coexist with shadow/apply context curation; neither requires the other.