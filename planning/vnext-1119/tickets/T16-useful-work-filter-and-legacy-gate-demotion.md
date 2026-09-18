# T16: Useful-work filter and legacy gate demotion

**Phase:** Phase 5 — decision contracts

**Blocked by:** T09, T13

**Status:** ready-for-agent

## What to build

Keep routine introspection local, treat tools as signals rather than work definitions, and retain selective pre-tool gating only as compatibility/precommit behavior.

## Public seam(s)

LocalAdmissionPolicy; legacy GateAdapter.

## TDD focus

Reads/status/tests without a decision fork do not trigger remote Jev; high-consequence precommit remains possible.

## Acceptance criteria

- [ ] All source requirements **647–667** are implemented through the declared public seam(s).
- [ ] Each mapped behavior has an externally observable test or an explicitly documented live/credential-gated verification.
- [ ] No mapped requirement is moved to another ticket without updating the traceability matrix and rerunning coverage verification.
- [ ] Relevant receipts/telemetry prove behavior where the requirement is observational rather than directly user-visible.
## Source requirements owned by this ticket

| Point | Requirement | Verification ID |
|---:|---|---|
| 647 | Known read-only introspection not automatically Jev-assessed. | `T16-R0647` |
| 648 | File reading generally local. | `T16-R0648` |
| 649 | Grep/search generally local. | `T16-R0649` |
| 650 | Git status generally local. | `T16-R0650` |
| 651 | Status inspection generally local. | `T16-R0651` |
| 652 | Test execution generally local unless the test result creates a decision fork. | `T16-R0652` |
| 653 | Routine evidence gathering generally local. | `T16-R0653` |
| 654 | Repetitive same-hypothesis diagnostics generally local. | `T16-R0654` |
| 655 | Jev invoked on the decision produced by evidence, not the mere act of collecting evidence. | `T16-R0655` |
| 656 | Tool calls treated as signals, not definitions of work. | `T16-R0656` |
| 657 | Mutating tool calls treated as stronger signals. | `T16-R0657` |
| 658 | External mutations treated as stronger signals. | `T16-R0658` |
| 659 | Decision plane determines ultimate eligibility. | `T16-R0659` |
| 660 | Existing selective pre_tool_call gating can remain. | `T16-R0660` |
| 661 | Existing gate_scope=selective behavior retained. | `T16-R0661` |
| 662 | Known read-only bypass retained. | `T16-R0662` |
| 663 | Existing gate no longer treated as primary Jev architecture. | `T16-R0663` |
| 664 | Automatic gating remains off by default. | `T16-R0664` |
| 665 | Synchronous gating reserved for narrow precommit/high-consequence use. | `T16-R0665` |
| 666 | gate_scope=all remains compatibility/explicit mode rather than recommended operation. | `T16-R0666` |
| 667 | Legacy gate telemetry retained. | `T16-R0667` |
