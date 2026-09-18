# Hermes-Jev roadmap

## Now — v0.1

- Generic decision runtime, not a one-off approvals wrapper.
- `jev_decide`, `jev_rank`, `jev_verify`.
- Opt-in `pre_tool_call` gate.
- Redaction, confidence-aware fail-to-human policy, hash receipts.
- Offline deterministic tests.
- Catalog-ready manifest and security docs.

## 0–6 months

- Contract loader + schema versioning.
- Replay/evaluation harness over real Hermes session-derived corpora with explicit privacy controls.
- Decision recipes: tool risk, worker/model routing, skill routing, result verification, retry/replan.
- Compare Jev vs System One adapters under the same contracts.
- Dashboard tab for decision volume, latency, confidence, escalations, and avoided LLM calls.
- Stable recipe/contract contribution process.

## 6–12 months

- Decision graph runtime: multiple parallel typed questions feeding deterministic policy code.
- Per-tool and per-project policies.
- Context/memory relevance gates.
- Agent/subagent delegation and completion gates.
- Provider interface supporting new Jev versions and compatible System One backends without changing contracts.
- Public benchmark corpus + calibration reports.

## 12–24 months

- Hermes-wide decision fabric: routing, verification, policy, orchestration, and confidence-aware control flow.
- Local/hosted Jev backends if TypeSafe makes them available.
- Contract marketplace/recipe registry with reproducible eval evidence.
- High-frequency System One decisions surrounding lower-frequency frontier-model deliberation.
