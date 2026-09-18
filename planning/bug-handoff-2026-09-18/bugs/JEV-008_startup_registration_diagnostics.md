# JEV-008 - Startup diagnostics say Jev is unknown/not found while runtime later uses Jev

**Status:** Confirmed diagnostic inconsistency  
**Priority:** P2  
**Subsystem:** plugin discovery / toolset registration / context-engine selection

## Summary

Hermes startup emits contradictory Jev diagnostics:

- `Warning: Unknown toolsets: hermes_remote_worker, jev`
- `Context engine 'jev' not found in .../plugins/context_engine`
- immediately followed by `Using context engine: jev`

Later runtime telemetry proves Jev is active. The startup messages therefore mislead operators about whether installation succeeded.

## Expected

Plugin registration should produce one unambiguous state:

- registered and active
- registered but disabled
- unavailable with a specific error

## Actual

The logs simultaneously imply Jev is unknown/not found and selected/active.

## Evidence

See:

- `evidence/startup_unknown_toolsets.txt`
- `evidence/startup_context_engine_resolution.txt`

## Acceptance criteria

- No `Unknown toolsets: ... jev` warning when Jev tools are actually registered.
- No `context engine not found` message immediately before selecting that engine unless a documented fallback path is being used.
- Startup logs identify the actual plugin source/path/version that was loaded.
