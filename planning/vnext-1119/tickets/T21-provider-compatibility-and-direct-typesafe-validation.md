# T21: Provider compatibility and direct-TypeSafe validation

**Phase:** Phase 8 — provider hardening

**Blocked by:** T01

**Status:** ready-for-agent

## What to build

Retain OpenRouter/direct-TypeSafe interchangeable transports, preserve provenance/usage/error behavior, and add honest direct-account live validation when credentials exist.

## Public seam(s)

Provider adapter interface; OpenRouter adapter; TypeSafe adapter.

## TDD focus

Both transports satisfy the same assessment contract; wire/live claims remain distinct; provider failure never silently authorizes consequential work.

## Acceptance criteria

- [ ] All source requirements **863–885** are implemented through the declared public seam(s).
- [ ] Each mapped behavior has an externally observable test or an explicitly documented live/credential-gated verification.
- [ ] No mapped requirement is moved to another ticket without updating the traceability matrix and rerunning coverage verification.
- [ ] Relevant receipts/telemetry prove behavior where the requirement is observational rather than directly user-visible.
## Source requirements owned by this ticket

| Point | Requirement | Verification ID |
|---:|---|---|
| 863 | OpenRouter Jev transport retained. | `T21-R0863` |
| 864 | Direct TypeSafe transport retained. | `T21-R0864` |
| 865 | Provider selection without changing Hermes-visible decision contracts. | `T21-R0865` |
| 866 | Only credential for selected provider required. | `T21-R0866` |
| 867 | OpenRouter credential path. | `T21-R0867` |
| 868 | TypeSafe credential path. | `T21-R0868` |
| 869 | OpenRouter model configuration retained. | `T21-R0869` |
| 870 | Direct TypeSafe model configuration retained. | `T21-R0870` |
| 871 | Transport provenance included in responses. | `T21-R0871` |
| 872 | Request IDs preserved. | `T21-R0872` |
| 873 | Provider token usage preserved when available. | `T21-R0873` |
| 874 | Provider cost preserved when available. | `T21-R0874` |
| 875 | Provider latency preserved. | `T21-R0875` |
| 876 | Provider errors incorporated into supervision telemetry. | `T21-R0876` |
| 877 | Provider failures do not silently authorize consequential execution. | `T21-R0877` |
| 878 | Direct TypeSafe transport remains wire-verified. | `T21-R0878` |
| 879 | Add first genuine direct-account live smoke when credentials are available. | `T21-R0879` |
| 880 | Distinguish wire-contract verification from live-account verification. | `T21-R0880` |
| 881 | Do not claim direct live validation before it exists. | `T21-R0881` |
| 882 | Keep OpenRouter path as known live-tested reference. | `T21-R0882` |
| 883 | Compare direct TypeSafe and OpenRouter latency if live access becomes available. | `T21-R0883` |
| 884 | Compare cost where applicable. | `T21-R0884` |
| 885 | Compare response/probability behavior where appropriate. | `T21-R0885` |
