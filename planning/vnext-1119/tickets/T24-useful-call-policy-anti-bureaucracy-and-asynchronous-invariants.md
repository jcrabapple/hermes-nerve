# T24: Useful-call policy, anti-bureaucracy, and asynchronous invariants

**Phase:** Phase 9 — vertical integration

**Blocked by:** T16, T22, T23

**Status:** ready-for-agent

## What to build

Enforce that remote Jev calls must be actionable/useful, prevent per-tool bureaucracy, and codify the supersession of synchronous loops while allowing one prompt-level arbiter read.

## Public seam(s)

Policy invariants at TurnSupervision/AdaptiveRouter seams.

## TDD focus

Explicit negative tests show ls/read/grep/status/successful-test/chat do not create nervous-system call storms.

## Acceptance criteria

- [ ] All source requirements **943–974** are implemented through the declared public seam(s).
- [ ] Each mapped behavior has an externally observable test or an explicitly documented live/credential-gated verification.
- [ ] No mapped requirement is moved to another ticket without updating the traceability matrix and rerunning coverage verification.
- [ ] Relevant receipts/telemetry prove behavior where the requirement is observational rather than directly user-visible.
## Source requirements owned by this ticket

| Point | Requirement | Verification ID |
|---:|---|---|
| 943 | Jev call should have a reasonable chance of changing Hermes’s next meaningful action. | `T24-R0943` |
| 944 | Jev call should have a reasonable chance of preventing an error. | `T24-R0944` |
| 945 | Jev call should have a reasonable chance of catching false completion. | `T24-R0945` |
| 946 | Jev call should have a reasonable chance of improving recovery. | `T24-R0946` |
| 947 | Jev call should have a reasonable chance of improving routing. | `T24-R0947` |
| 948 | Jev call should have a reasonable chance of identifying need for more evidence. | `T24-R0948` |
| 949 | Calls that merely reconfirm obvious harmless behavior should be suppressed. | `T24-R0949` |
| 950 | Calls whose answer cannot influence any still-actionable state should normally be suppressed. | `T24-R0950` |
| 951 | Do not Jev-check every ls. | `T24-R0951` |
| 952 | Do not Jev-check every file read. | `T24-R0952` |
| 953 | Do not Jev-check every grep. | `T24-R0953` |
| 954 | Do not Jev-check every status command. | `T24-R0954` |
| 955 | Do not Jev-check every successful test. | `T24-R0955` |
| 956 | Do not Jev-check every harmless tool call. | `T24-R0956` |
| 957 | Do not turn Jev into an ALLOW-everything latency tax. | `T24-R0957` |
| 958 | Do not optimize for maximizing percentage of actions reviewed. | `T24-R0958` |
| 959 | Do not equate more Jev calls with better control. | `T24-R0959` |
| 960 | Do not use Jev as a conversational shadow for ordinary dialogue. | `T24-R0960` |
| 961 | Do not make route → act → verify → route a mandatory synchronous network loop. | `T24-R0961` |
| 962 | Do not require Jev verification after every meaningful Hermes unit if it would block execution. | `T24-R0962` |
| 963 | Do not independently call Jev for verification and then again for next-action selection when one assessment can batch them. | `T24-R0963` |
| 964 | Do not make Hermes wait 500+ ms at every fork unless that fork is deliberately precommit/consequential. | `T24-R0964` |
| 965 | Preserve the conceptual control states from that design while moving them into the asynchronous nervous system. | `T24-R0965` |
| 966 | Do not completely forbid Jev from seeing the user prompt. | `T24-R0966` |
| 967 | The turn arbiter may see the original prompt once. | `T24-R0967` |
| 968 | The nervous system should not continuously consume raw chat. | `T24-R0968` |
| 969 | After admission, structured decision state becomes the primary Jev input. | `T24-R0969` |
| 970 | Casual prompts should normally terminate after the admission decision. | `T24-R0970` |
| 971 | Chat can still contain work. | `T24-R0971` |
| 972 | Work can still look like chat. | `T24-R0972` |
| 973 | Roleplay can still contain accountable director-level work. | `T24-R0973` |
| 974 | Therefore Jev activation must follow decision-plane/accountability semantics, not UI surface. | `T24-R0974` |
