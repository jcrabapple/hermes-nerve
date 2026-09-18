# JEV-001 - Nervous control fails to break repeated identical failure loop

**Status:** Confirmed behavior defect  
**Priority:** P0  
**Subsystem:** nervous system / `correct_next` control application

## Summary

During a real ARB debugging run, Muna reached **33 identical terminal failures with identical arguments**. Jev simultaneously reported substantial supervisory activity: 48 failure decisions, 35 `GATHER_EVIDENCE`, 15 `REPLAN`, one `RETRY`, and one `ESCALATE`.

Jev therefore detected the failure regime and generated corrective control signals, but the overall control loop did not terminate the repeated-failure behavior.

## Expected

Once the same action/failure pair repeats beyond a small threshold, `correct_next` should force a materially different next step or stop/escalate. A `REPLAN` must have an observable effect on the next action lease.

## Actual

The same failing pytest command was executed 33 times with identical arguments. Hermes' native loop warning explicitly said to inspect the error and change strategy, yet execution continued.

## Evidence

See:

- `evidence/loop_count_33.txt`
- `evidence/stats_snapshot_and_compression.txt`

Key Jev telemetry:

- `FAILURE` decisions: 48
- `control_replan`: 15
- `control_gather_evidence`: 35
- `control_escalate`: 1
- `control_retry`: 1
- `decision_correction_success`: 0

## Reproduction shape

1. Run a task that repeatedly invokes the same terminal command.
2. Ensure the command deterministically fails with the same output.
3. Let nervous supervision remain `ON` in `correct_next` mode.
4. Observe whether repeated `REPLAN` or `GATHER_EVIDENCE` controls change the next action.
5. Fail if the identical action executes more than N times after a replan/escalation signal.

## Suspected failure modes

- Control recommendation is generated but never injected into the agent's next-step context.
- Control is injected but does not invalidate/replace the already planned tool call.
- Lease invalidation occurs but a semantically identical action is re-leased immediately.
- `REPLAN` is advisory text rather than an execution constraint.
- Failure identity is not deduplicated across calls, so the system treats every repetition as new evidence.

## Acceptance criteria

- A deterministic repeated failure is interrupted within a bounded number of repetitions.
- At least one metric explicitly records whether the Jev control changed the next agent action.
- A `REPLAN` cannot be followed by an identical action unless Jev explicitly approves retry and records why.
- Regression test covers identical command + identical failure loop.
