# T29: Release and handoff integrity

**Phase:** Phase 10 — verification

**Blocked by:** T27

**Status:** ready-for-agent

## What to build

Fix release-tree/handoff/test-runner/docs/checksum/pin/validation-claim inconsistencies so the shipped artifact and published commit are reproducible.

## Public seam(s)

Release packaging seam; CI/release verification.

## TDD focus

Canonical package byte/content checks, docs presence, suite-count labeling, pin/checksum validation and honest provider claims all pass.

## Acceptance criteria

- [ ] All source requirements **1065–1079** are implemented through the declared public seam(s).
- [ ] Each mapped behavior has an externally observable test or an explicitly documented live/credential-gated verification.
- [ ] No mapped requirement is moved to another ticket without updating the traceability matrix and rerunning coverage verification.
- [ ] Relevant receipts/telemetry prove behavior where the requirement is observational rather than directly user-visible.
## Source requirements owned by this ticket

| Point | Requirement | Verification ID |
|---:|---|---|
| 1065 | Canonical release tree should match the pinned published repository. | `T29-R1065` |
| 1066 | Handoff ZIP should not silently differ from the pinned source tree. | `T29-R1066` |
| 1067 | Clearly distinguish full development test suite from compact admission/release suite. | `T29-R1067` |
| 1068 | Clearly document intended test runner. | `T29-R1068` |
| 1069 | unittest remains the known intended runner for the examined v0.1.5.5 tree. | `T29-R1069` |
| 1070 | Avoid confusing pytest collection failures being mistaken for functional failures. | `T29-R1070` |
| 1071 | Include GUIDE.md in canonical handoff/package where expected. | `T29-R1071` |
| 1072 | Include SETUP.md in canonical handoff/package where expected. | `T29-R1072` |
| 1073 | Include PROVIDER_SETUP.md in canonical handoff/package where expected. | `T29-R1073` |
| 1074 | Preserve exact release checksums. | `T29-R1074` |
| 1075 | Preserve exact pinned commit reference. | `T29-R1075` |
| 1076 | Keep PR/release documentation aligned with actual packaged contents. | `T29-R1076` |
| 1077 | Report test counts accurately by suite. | `T29-R1077` |
| 1078 | Keep provider-validation claims precise. | `T29-R1078` |
| 1079 | Keep direct-TypeSafe wire-tested distinct from live-tested. | `T29-R1079` |
