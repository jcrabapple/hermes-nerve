# BUG-001: `jev_assess` deferred schema does not encode runtime `choice.criteria` requirements

**Severity:** P1
**Component:** Hermes-Jev tool schema / `jev_assess`
**Observed version:** 0.2.1
**Target fix:** 0.2.2
**Status:** Reproduced

## Summary

`jev_assess` exposes a model-facing schema that is insufficiently specific for deferred-tool use. During a real Muna test, the model attempted multiple `jev_assess` calls and the runtime validator rejected them immediately with:

```text
choice question 'is_disposable' requires at least two criteria labels
```

The same class of failure appeared for `is_active_process`.

The model had enough information to know the high-level question and choice values, but not enough schema guidance to construct the exact `criteria` object expected by the runtime validator.

## Why this matters

Hermes 0.21.2 defers non-core plugin tools behind `tool_describe` / `tool_call`. A deferred model must be able to construct a valid request from the JSON schema alone. Hidden validator requirements are effectively unusable API requirements.

This failure blocked the intended workflow:

```text
filesystem evidence
  -> jev_assess
  -> jev_verify
  -> receipt-backed SAFE / REVIEW / KEEP classification
```

Instead, all candidates had to remain `UNVERIFIED`.

## Reproduction

1. Start Hermes with Hermes-Jev 0.2.1 on the Muna profile.
2. Ask the agent to inspect candidate files using read-only commands.
3. Ask it to call `tool_describe` for `jev_assess`.
4. Ask it to assess structured choice questions such as:
   - `is_disposable`
   - `is_active_process`
5. Observe the real `jev_assess` tool invocation.

Observed trace:

```text
jev_assess 0.0s [choice question 'is_active_process' requires ...]
jev_assess 0.0s [error]
jev_assess 0.0s [error]
jev_assess 0.0s [error]
jev_assess 0.0s [error]
```

Final agent report correctly stated:

```text
Error: choice question 'is_disposable' requires at least two criteria labels
Status: Blocked by tool validation error.
```

## Expected behavior

`tool_describe(["jev_assess"])` should expose a schema that makes the runtime contract mechanically constructible.

For a `choice` question, the model-facing schema should explicitly define at least:

```json
{
  "type": "choice",
  "instructions": "Classify the candidate.",
  "criteria": {
    "SAFE": "Evidence supports deletion",
    "REVIEW": "More evidence is required",
    "KEEP": "Evidence supports retaining it"
  }
}
```

The schema should communicate:

- `type` enum
- required fields by type
- that `choice.criteria` is an object/map
- that `choice.criteria` must contain at least two labels
- the expected shape of score criteria
- which question types do not need choice labels

## Actual behavior

The runtime enforces constraints that are not sufficiently encoded in the model-facing schema. The model repeatedly constructs invalid requests and gets a local tool error.

## Root-cause hypothesis

The runtime validator is more specific than the JSON schema surfaced through Hermes deferred-tool discovery. The tool contract relies partly on prose or implementation knowledge instead of typed schema constraints.

## Proposed fix

Use a discriminated schema for question objects, ideally `oneOf` / tagged-union semantics around `type`.

Conceptually:

```json
{
  "oneOf": [
    {
      "properties": {
        "type": {"const": "choice"},
        "instructions": {"type": "string"},
        "criteria": {
          "type": "object",
          "minProperties": 2,
          "additionalProperties": {"type": "string"}
        }
      },
      "required": ["type", "instructions", "criteria"]
    },
    {
      "properties": {
        "type": {"const": "score"},
        "instructions": {"type": "string"},
        "criteria": {"type": "array", "minItems": 2}
      },
      "required": ["type", "instructions", "criteria"]
    },
    {
      "properties": {
        "type": {"const": "noul"},
        "instructions": {"type": "string"}
      },
      "required": ["type", "instructions"]
    }
  ]
}
```

Exact field names should match the existing implementation; this example is illustrative.

## Acceptance criteria

- `tool_describe` exposes enough structure for a model to construct valid choice questions without external documentation.
- A minimal valid `choice` question passes local validation.
- A malformed `choice` question is rejected locally with a precise error.
- A valid assessment reaches the provider and returns a real request ID/receipt.
- Add at least one integration test that uses the same deferred `tool_describe` -> `tool_call` path Hermes uses in production.

## Regression tests

### Test A: valid deferred choice assessment

Expected:

```text
tool_describe(jev_assess)
-> model constructs valid criteria map
-> jev_assess provider call count +1
-> ok=true
-> request_id present
```

### Test B: invalid choice assessment

Expected:

```text
missing/one-label criteria
-> local validation error
-> provider call count +0
```

