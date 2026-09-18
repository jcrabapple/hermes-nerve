# Confounders and findings that should NOT be filed as Jev bugs

## ARB `httpx2` collection failure

The workload repeatedly failed because Starlette/FastAPI test collection reported that the `httpx2` package was unavailable. That is an ARB/test-environment issue used to expose Jev behavior. It is not itself a Jev defect.

## Hermes native loop detector

Hermes independently emitted `same_tool_failure_warning` and `repeated_exact_failure_warning`. Therefore, an observed Muna tactic change cannot automatically be credited to Jev unless correlated to a Jev decision ID/control record.

## 90-second main-model stall

`jev_stats` itself took ~0.06 seconds. The 90-second stall occurred in the subsequent Gemma call after the large stats payload entered context. File JEV-004 as a stats/context-bloat issue, not as "Jev inference took 90 seconds."

## Jev normal inference latency

Observed Jev nervous-system latency was roughly:

- p50 ~295 ms
- p95 ~622 ms
- average ~343 ms

This is measurable overhead but not enough to explain the 78-90 second stalls seen elsewhere.

## Duplicate plugin backup collision

An older Jev backup under the active Hermes plugin tree had previously caused a collision and was moved outside the active plugin directory. Treat that as a resolved environment/configuration problem unless it reproduces with a clean plugin tree.

## Installed version

The stats snapshot identifies the running plugin as `0.2.0`. Do not label these reports as 0.2.1 unless a later run proves that version is installed.
