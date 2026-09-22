# Dev6 Event-Delivery A/B Benchmark

This fixture is frozen for the Hermes-Jev v0.2.2.dev6 token-savings experiment.

## Purpose

It is a deterministic medium-hard maintenance task with interacting retry, idempotency,
backoff, dead-letter, and batch-continuation defects. It is deliberately **not** tailored
to a particular Jev verdict. Plain Hermes can solve it. The treatment arm may benefit
from supervision if it repeats a failing hypothesis or burns budget without verified
progress.

The task also contains one semantic Definition-of-Done criterion. Mechanical facts
should be proved locally by Hermes-Jev; the semantic remainder should require a real
Jev completion decision when the treatment attempts `kanban_complete`.

## Freeze rules

1. Create one Git commit from `fixture/` before either arm starts.
2. Clone that exact commit into independent control and treatment workspaces.
3. Give both cards byte-identical copies of `task-body.md`.
4. Do not edit the fixture/task after seeing either arm's behavior.
5. Keep `hidden_acceptance.py` outside both worker workspaces until both runs terminate.
6. Both arms must pass the same visible DoD and hidden acceptance before token totals are compared.
7. If the treatment makes no mid-run trajectory call, report that fact; do not make the task harder post hoc.

## Expected baseline

Before fixes, the visible suite currently has 8 failures and 5 passes. Exact assertion
messages are not part of the benchmark contract; the committed fixture SHA is.

## Primary metric

`total tokens to independently verified completion`

For treatment:

`Hermes worker tokens + Jev supervisor tokens`

Cache-read tokens are reported separately rather than added to the primary token total.