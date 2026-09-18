# BUG-002: Jev-internal tool failures may recursively trigger Jev nervous-system provider calls

**Severity:** P1
**Component:** nervous-system routing / hook filtering / provider-call suppression
**Observed version:** 0.2.1
**Target fix:** 0.2.2
**Status:** Strongly suspected; correlation reproduced, root cause needs instrumentation confirmation

## Summary

During the strict verification test, Hermes produced five immediate local `jev_assess` errors. At the same time, OpenRouter recorded five unusually large Jev generations at 11:56, each with 304 output tokens.

The malformed `jev_assess` payloads are validated locally before the direct assessment provider call, so those direct tool invocations should not themselves account for the five OpenRouter requests.

The leading hypothesis is that the `post_tool_call` / nervous-system path observes the failed `jev_assess` calls as generic failures and routes them back into Jev as fresh supervisory events.

That creates a recursive pattern:

```text
bad jev_assess request
  -> local validation failure
  -> tool failure event
  -> nervous system observes failure
  -> remote Jev assessment
```

## Evidence

Hermes trace at the failure point:

```text
jev_assess 0.0s [choice question 'is_active_process' requires ...]
jev_assess 0.0s [error]
jev_assess 0.0s [error]
jev_assess 0.0s [error]
jev_assess 0.0s [error]
```

OpenRouter at 11:56 showed five generations:

```text
11:56  7,030 input / 304 output
11:56  9,153 input / 304 output
11:56  5,173 input / 304 output
11:56  5,199 input / 304 output
11:56  5,418 input / 304 output
```

The one-to-one count is suspicious and consistent with recursive self-observation, but timing/correlation alone is not sufficient to call the exact hook path proven.

## Why this matters

Hermes-Jev is designed to reduce remote-call amplification by supervising meaningful decisions rather than every tool event.

Jev supervising failures produced by Jev itself creates the opposite behavior:

- wasted provider calls
- higher cost
- higher background load
- possible challenge/control churn
- harder-to-understand telemetry
- risk of recursive Jev-on-Jev behavior

It can also defeat repeated-failure dedup if each malformed call has slightly different arguments and therefore a distinct failure fingerprint.

## Expected behavior

All Hermes-Jev internal tools should be considered an internal supervision boundary.

Failures from these tools should be locally recorded for diagnostics but not remotely supervised by Jev:

```text
jev_decide
jev_rank
jev_verify
jev_assess
jev_context_curate
jev_context_rehydrate
jev_stats
jev_nervous_event
```

Expected path:

```text
jev_* tool failure
  -> local diagnostic receipt/counter
  -> optional debug log
  -> nervous remote routing suppressed
```

## Actual behavior

The live run is consistent with Jev-internal tool failures generating background Jev calls.

## Proposed fix

Add an explicit internal-origin guard before nervous-system routing, for example:

```text
if tool_name starts with "jev_":
    classify reason = "jev-internal"
    record local observation
    suppress remote nervous routing
```

Apply this consistently across:

- `pre_tool_call`
- `post_tool_call`
- any failure/recovery event constructor
- batching paths
- challenge attribution

Do not rely solely on repeated-failure fingerprints.

## Instrumentation needed to prove root cause

Add counters such as:

```text
nervous.events.jevinternal_seen
nervous.events.jevinternal_suppressed
nervous.provider_calls.by_origin
```

Each remote nervous assessment should carry an origin tuple:

```text
origin_tool
origin_event_type
origin_event_id
origin_failure_fingerprint
```

Then reproduce one invalid `jev_assess` call and verify no remote Jev call is attributed to it.

## Acceptance criteria

### Regression A: invalid Jev tool call

```text
baseline provider_calls = N
invalid jev_assess
-> local TOOL_ERROR
-> provider_calls remains N
-> jev-internal-suppressed += 1
```

### Regression B: ordinary external tool failure

```text
external tool fails materially
-> nervous router may assess according to normal policy
```

This ensures the suppression is narrow rather than disabling failure supervision globally.

### Regression C: direct explicit Jev call still works

```text
valid jev_assess
-> exactly one direct provider call
-> no second nervous-system Jev call caused by observing its success
```

