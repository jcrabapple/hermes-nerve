# Security

Hermes-Jev sends decision state to the selected external Jev provider — OpenRouter or TypeSafe direct — only when a Jev tool, gate, or active Jev ContextEngine semantic pass is invoked.

## Provider egress

Before provider calls, state is recursively redacted for common secret-bearing keys and token/bearer patterns. The selected transport uses a fixed provider path (`/api/alpha/decisions` for OpenRouter or `/v1/systemone` for TypeSafe direct) rather than exposing an arbitrary bearer-token destination.

## Receipts

Decision receipts default to hash-only state at:

```text
$HERMES_HOME/jev/receipts.jsonl
```

`receipt_detail=sanitized` persists redacted state and should be enabled only when needed for evaluation/replay.

## Evidence ledger

Context rehydration requires a separate evidence ledger:

```text
$HERMES_HOME/jev/context-ledger.jsonl
```

Modes:

- `sanitized` (default): force-redacted content/metadata are stored and can be rehydrated.
- `hash`: only hashes/provenance are retained; `jev_context_rehydrate` will refuse to invent missing content.

The ledger is not intended as a second verbatim transcript. Operators handling highly sensitive tool outputs should choose hash mode or disable the ledger.

## Automatic context engine

The Jev context engine is opt-in. It preserves valid tool-call/result structure and fails open. When Jev cannot safely make progress it may use Hermes' built-in compressor if `context_engine_fallback_builtin=true`.

## Gate

`gate_scope=selective` uses a deliberately narrow deterministic bypass only for known read-only tools/commands. It is not a general shell safety classifier. Shell composition (`|`, `>`, `&&`, command substitution), unknown commands, and commands with names that can mutate state (`date`, `nvidia-smi`, `env`, etc.) are not bypassed and still reach Jev when the gate is enabled. `gate_scope=all` disables the read-only bypass.

`enforce` mode routes low-confidence or provider-failure cases toward human approval rather than silently treating them as safe execution.

Do not treat a Jev probability as proof of correctness.
