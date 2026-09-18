# Agent Kickoff - Jev 0.2.0 Bug Repair

You are taking over a real Jev integration/debugging investigation. Do not assume the plugin is inactive; telemetry proves the nervous system is active.

Start by reading `README.md`, then every file under `bugs/`, then `TEST_LEDGER.md`, `NOT_JEV_BUGS.md`, and `NEXT_INVESTIGATIONS.md`.

Your first engineering target is JEV-001 + JEV-002 together:

1. Trace each `REPLAN`/`GATHER_EVIDENCE` control to the exact next agent action.
2. Determine whether controls are delivered but ignored, delivered and followed but unmeasured, or never injected into the execution loop.
3. Repair the smallest responsible integration layer.
4. Add deterministic regression coverage where an identical failing terminal action cannot execute repeatedly after a Jev replan/escalation.
5. Make the stats lifecycle attributable: decision ID -> delivered -> followed/overridden -> outcome.
6. Do not tune thresholds until control propagation and attribution are trustworthy.

Then investigate JEV-003 (gate lifecycle/telemetry) before performance tuning.

Do not misclassify the ARB `httpx2` failure or the 90-second Gemma provider stall as Jev inference failures. See `NOT_JEV_BUGS.md`.
