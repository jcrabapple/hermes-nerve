# T22: Latency, long-running supervision, and compact provider payloads

**Phase:** Phase 8 — provider hardening

**Blocked by:** T12, T13, T21

**Status:** ready-for-agent

## What to build

Prove the system remains asynchronous under ~500 ms provider latency, survives multi-hour/high-event turns, and sends structured compact state rather than raw conversation/tool transcripts.

## Public seam(s)

LongTurnSupervisor behavior at the existing interfaces; payload sanitizer/compactor.

## TDD focus

Synthetic 500+ ms latency does not serialize ordinary work; long-run critical checks survive; payload fixtures exclude raw transcripts by default.

## Acceptance criteria

- [ ] All source requirements **886–913** are implemented through the declared public seam(s).
- [ ] Each mapped behavior has an externally observable test or an explicitly documented live/credential-gated verification.
- [ ] No mapped requirement is moved to another ticket without updating the traceability matrix and rerunning coverage verification.
- [ ] Relevant receipts/telemetry prove behavior where the requirement is observational rather than directly user-visible.
## Source requirements owned by this ticket

| Point | Requirement | Verification ID |
|---:|---|---|
| 886 | Explicit architectural assumption: Jev ping cannot reliably get below roughly 500 ms in current setup. | `T22-R0886` |
| 887 | Avoid adding that latency to ordinary tool work. | `T22-R0887` |
| 888 | Avoid synchronous per-tool Jev calls. | `T22-R0888` |
| 889 | Avoid synchronous per-observation Jev calls. | `T22-R0889` |
| 890 | Avoid synchronous per-decision microchecks where asynchronous supervision suffices. | `T22-R0890` |
| 891 | Reserve synchronous waiting for deliberately selected precommit boundaries. | `T22-R0891` |
| 892 | Measure network latency separately from worker wall-clock penalty. | `T22-R0892` |
| 893 | Design every new Jev feature around asynchronous operation where possible. | `T22-R0893` |
| 894 | Supervision persists across very long turns. | `T22-R0894` |
| 895 | Supervision persists across hundreds of tool calls. | `T22-R0895` |
| 896 | Supervision persists across worker spawns. | `T22-R0896` |
| 897 | Supervision persists across strategy changes. | `T22-R0897` |
| 898 | Supervision persists until explicit turn completion. | `T22-R0898` |
| 899 | Long-running sessions shift toward more compressed event representation. | `T22-R0899` |
| 900 | High event volume does not disable critical-event Jev checks. | `T22-R0900` |
| 901 | High event volume can reduce low-value Jev call frequency. | `T22-R0901` |
| 902 | Long-run state summaries replace full raw history. | `T22-R0902` |
| 903 | Jev receives decision state, not 30,000-token conversation history. | `T22-R0903` |
| 904 | Jev input optimized toward hundreds of relevant tokens where possible. | `T22-R0904` |
| 905 | Jev receives structured relevant state instead of the complete transcript. | `T22-R0905` |
| 906 | Raw conversation transcript not automatically forwarded to nervous-system Jev. | `T22-R0906` |
| 907 | Raw roleplay transcript not automatically forwarded. | `T22-R0907` |
| 908 | Raw tool transcript not automatically forwarded. | `T22-R0908` |
| 909 | Relevant evidence condensed. | `T22-R0909` |
| 910 | Relevant state condensed. | `T22-R0910` |
| 911 | Decision alternatives explicitly represented. | `T22-R0911` |
| 912 | Hermes proposal explicitly represented. | `T22-R0912` |
| 913 | Event provenance retained despite compression. | `T22-R0913` |
