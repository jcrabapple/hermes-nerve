# Dev16 session findings folded into the release

This file is the engineering record from the dev14/dev15 Solar Pro 4 stress session that motivated dev16.

## Correctness findings

- Plain/control workers could report success with the visible suite green while hidden acceptance still failed the dead-event redispatch invariant.
- A representative control had `13 passed` yet re-dispatching an already-dead event mutated attempts from `3 -> 4`; the tree was also dirty.
- Jev's controller-owned DOD-07 behavioral probe correctly rejected the false completion and surfaced the concrete counterexample.
- Deterministic failures must remain authoritative and must never be overwritten by semantic PASS.

## Lifecycle findings

- The implementation could be fully correct (`21 passed`, clean commit) while the worker remained alive trying to discover a completion path.
- Child/delegated execution context could reject model-owned completion attempts even though controller-owned native completion was available.
- Solar then explored CLI, direct-adapter, generated helper script, DB, and tool-wrapper completion paths.
- Dev15 closes this with controller-owned completion; dev16 additionally treats any post-verification provider request as a lifecycle regression and retries native completion before escalating.

## Economics findings

Healthy Jev examples from the clean cohort:

- 18 calls / 376k combined tokens / 137s
- 23 calls / 484k combined tokens / 315s
- 32 calls / 968k combined tokens / 435s

Pathological Jev example:

- 109 calls / 4.760M combined tokens / 1197s

One runaway consumed more tokens than several healthy runs combined. Supervisor overhead was ~1.5k tokens/run and therefore not the meaningful optimization target. Tail control is.

The frozen benchmark's dev16 local estimator yields a 960k target, 1.056M completion tolerance ceiling, and ~1.68M default hard nerve ceiling. That preserves the measured 968k healthy run while bounding a repeat of the 4.76M spiral.

## Model-behavior finding

Solar Pro 4 is intentionally useful here as a loop-prone stress model. Prompting alone is not a sufficient control mechanism. The architecture must remain correct even when the worker repeatedly ignores lifecycle advice and invents alternate completion mechanisms.

## Nerve design principles

- Estimate before execution, without a provider call.
- Put the estimate in the locked DoD.
- Do not kill merely for crossing an estimate.
- Require a large deterministic overrun or multiple independent loop signals.
- Keep WATCH/REPLAN advisory and state-transition-only.
- Make the kill switch controller-owned, not worker-owned.
- Preserve the workspace when killed.
- Never overwrite an already successful terminal state.
- Zero provider calls after verified PASS remains a release invariant.

## Benchmark/harness QoL findings

- Harnesses must not assume a run row exists immediately after dispatch (`max()` on an empty run list was observed).
- Global `kanban.max_in_progress` can silently prevent a separate-board benchmark from spawning; per-board `--max` is not the same thing.
- Read-only capacity preflight must skip noncanonical SQLite DBs that do not contain a `tasks` table.
- Abandoned ready cards and rate-limited legacy workers can steal newly opened global slots.
- Ctrl+C can stop the harness without stopping a separately spawned worker; benchmark cleanup must explicitly terminate/archive the active arm.
- Mid-experiment concurrency changes contaminate wall-clock comparisons more than token/call comparisons.
- Valid-vs-invalid arms must not be used as strict token-savings pairs; report correctness separately.
- Prefer success rate + median + tail/max over mean alone because one pathological run can dominate the average.

Use `scripts/benchmark_preflight.py` before future live A/B runs to expose global capacity and ready/running contamination before dispatch.
