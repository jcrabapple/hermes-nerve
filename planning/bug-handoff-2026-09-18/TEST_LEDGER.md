# Jev Test Ledger

## Proven working

- Plugin runtime is active despite confusing startup diagnostics.
- `jev_stats` explicit tool call works.
- Jev nervous system receives real task events.
- Turn admission produces both ON and OFF states.
- Nervous router identifies failures as high-value events.
- Jev provider is called for nervous control decisions.
- Control action generation includes CONTINUE, GATHER_EVIDENCE, REPLAN, RETRY, ESCALATE.
- Historical pre-tool gate activity exists.
- Read-only gate bypass behavior has been observed historically.
- Context evidence ledger is populated.
- Context shadow planning has occurred.
- Historical disagreements and challenges exist in cumulative outcomes.

## Proven problematic

- A real agent loop reached 33 identical failures despite Jev supervisory activity.
- Current stats cannot attribute control decisions to followed/overridden next actions.
- `jev_stats` can return ~30 KB and inflate the main-model context.
- Gate event telemetry does not obviously track the later high-volume terminal run.
- Decision lease invalidation rate is nearly one per raw event with zero reuse.

## Still unproven / needs controlled test

- Successful live `correct_next` correction attributable to Jev.
- Successful live challenge that changes the next action.
- Premature-done catch.
- Stale-state challenge.
- Context rehydration after compression.
- Challenge acceptance/rejection accounting in the current session.
- Whether gate inactivity is real hook failure vs metric-scope mismatch.
