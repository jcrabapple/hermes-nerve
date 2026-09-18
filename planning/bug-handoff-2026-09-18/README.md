# Hermes Jev 0.2.0 - Bug Handoff

Date: 2026-09-18
Environment: Hermes Agent / Muna profile
Jev plugin version observed in telemetry: 0.2.0
Main model: `@google/gemma-4-26b-a4b-it` via `https://inference.muna.ai/v1`
Observed returned provider model: `nvidia/Gemma-4-26B-A4B-NVFP4`
Jev provider model in receipts: `typesafe/jev-1.13-20260917`

## Purpose

This package captures the distinct Jev defects and anomalies observed during a long real ARB debugging run. The goal is to let a new agent reproduce and repair the Jev integration without re-litigating what happened.

## Executive summary

Jev is not inactive. The nervous system clearly observed the run, routed failures, called the Jev provider, and generated control actions. The strongest failure is downstream effectiveness: the agent reached **33 identical terminal failures** even though Jev reported many `REPLAN` and `GATHER_EVIDENCE` control decisions.

The current evidence supports these separate work items:

| ID | Title | Status | Priority |
|---|---|---|---|
| JEV-001 | Nervous control fails to break repeated identical failure loop | Confirmed behavior defect | P0 |
| JEV-002 | Stats mix control/outcome scopes and cannot attribute whether Jev was followed | Confirmed observability defect | P0 |
| JEV-003 | Pre-tool gate telemetry appears stale/disconnected during active nervous supervision | High-confidence anomaly | P0 |
| JEV-004 | `jev_stats` unbounded payload can poison the surrounding model turn | Confirmed usability/perf defect | P1 |
| JEV-005 | Context rehydration remains zero after repeated compression | Needs targeted confirmation | P1 |
| JEV-006 | Repeated identical failures trigger excessive Jev calls without effective deduplication | High-confidence perf/control defect | P1 |
| JEV-007 | Decision lease churn is extreme with zero recorded reuse | High-confidence anomaly | P1 |
| JEV-008 | Startup reports Jev as unknown/not found while runtime later uses it | Confirmed diagnostic inconsistency | P2 |

## Key observed numbers

From the captured `jev_stats` snapshot:

- nervous raw events: 176
- nervous events forwarded: 96
- nervous provider calls: 99
- `control_continue`: 44
- `control_gather_evidence`: 35
- `control_replan`: 15
- `control_retry`: 1
- `control_escalate`: 1
- decision lease invalidations: 172
- decision lease reuse: 0
- failure decisions: 48
- Jev decisions/outcomes rows: 195
- historical disagreements: 5
- historical challenges issued: 3
- current quality `decision_correction_success`: 0
- current quality `jev_decisions_followed`: 0
- current quality `jev_decisions_overridden`: 0
- current `recent_challenges`: empty
- p50 Jev latency: ~295 ms
- p95 Jev latency: ~622 ms
- Jev tokens: 219,092
- Jev provider cost: ~$0.00852
- `jev_calls_per_turn`: 33
- `jev_calls_per_100_events`: 56.25
- context evidence events: 445
- rehydrations: 0
- gate event count: 24
- gate terminal observations: 16
- gate evaluated: 15
- gate bypassed: 8
- receipts: 346
- receipt provider calls: 336
- `hermes/jev-nervous-control/v1` receipts: 190
- `hermes/pre-tool-gate/v1` receipts: 121

## Important interpretation constraints

Do not claim that every Muna tactic change was caused by Jev. Hermes' native loop detector was also issuing explicit warnings. The evidence proves Jev generated control activity; it does not yet prove which individual agent actions were caused by those controls.

Do not call the ARB `httpx2` failure a Jev bug. It is the workload failure that exposed Jev behavior.

Do not call the 90-second model stall Jev inference latency. `jev_stats` itself returned in ~0.06 seconds. The stall occurred in the main Gemma call after a ~29.6 KB stats result had been injected into context.

## Package layout

- `bugs/` - one unique report per defect/anomaly
- `evidence/` - focused, line-numbered source excerpts
- `TEST_LEDGER.md` - what is proven vs still untested
- `NOT_JEV_BUGS.md` - confounders and resolved environment issues
- `NEXT_INVESTIGATIONS.md` - highest-value next work
- `SOURCE_MANIFEST.txt` - hashes of source logs used

## Recommended repair order

1. JEV-001: make `correct_next` controls actually terminate repeated-failure loops.
2. JEV-002: make outcome attribution trustworthy so fixes can be measured.
3. JEV-003: determine why the gate event stream stopped advancing during the run.
4. JEV-006/JEV-007: add dedup/hysteresis and repair lease semantics to reduce supervision churn.
5. JEV-004: make stats queryable/bounded by default.
6. JEV-005: explicitly test rehydration after compression.
7. JEV-008: clean up registration/diagnostic messaging.
