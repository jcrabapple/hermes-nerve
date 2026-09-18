# Roadmap

## v0.1.5.5 — telemetry hardening + shadow-safe community release (current)

Delivered:

- seven public tools: six Jev decision/context tools plus local `jev_stats` telemetry
- explicit execution provenance on provider results
- decomposed semantic context assessment
- deterministic KEEP_EXACT/PIN/ANCHOR/DROP policy
- contradiction/supersession signals
- verification-linked lifecycle leases
- privacy-minimized evidence ledger
- shadow-mode telemetry/reporting
- opt-in Hermes ContextEngine registration
- protocol-safe automatic anchoring
- built-in compressor fallback on no safe Jev progress
- selective local pre-tool bypass for conservative read-only calls, with gate telemetry and `gate_scope=all` compatibility

## Next

- collect real shadow telemetry and tune thresholds from evidence
- add replay corpus/version comparison across Jev model pins
- continuation-fidelity A/B harness over real Hermes session checkpoints
- richer lifecycle leases tied to goals/branches/artifacts, not only verification
- per-tool recoverability adapters and rerun-cost classes
- automatic anchor rehydration when the active goal references older evidence
- optional context status/ledger CLI commands
- richer user-configurable gate policies by tool patterns/consequence class beyond the conservative built-in selective scope
