# Security

## Reporting security issues

Do not post API keys, bearer tokens, private prompts, credential-bearing logs, or other secrets in a public issue.

For a potentially sensitive vulnerability, use GitHub's private security-reporting surface for this repository when available. If private reporting is unavailable, open only a minimal public issue asking the maintainer for a private reporting path; do not include exploit details or secrets there.

For non-sensitive security hardening or ordinary bugs, a normal issue is appropriate.

Nerve sends decision state to the selected OpenRouter, TypeSafe, or OpenCode provider only when a Jev tool, gate, or active Jev ContextEngine semantic pass is invoked.

## Provider egress

Before provider calls, state is recursively redacted for common secret-bearing keys plus common bearer, GitHub/OpenAI-style, Slack, AWS access-key, JWT, private-key, secret-assignment, and secret query-parameter shapes. Redaction is defense in depth, not a guarantee that every vendor credential format can be recognized. Provider defaults are pinned to documented HTTPS endpoints; operator-controlled base-URL overrides should only target trusted HTTPS services.

Local JSONL ledgers serialize writes within the process and use advisory file locking where the platform provides `fcntl`, reducing the risk of interleaved records under concurrent Hermes/Jev activity.

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
- `hash`: only hashes/provenance are retained; `nerve_context_rehydrate` will refuse to invent missing content.

The ledger is not intended as a second verbatim transcript. Operators handling highly sensitive tool outputs should choose hash mode or disable the ledger.

## Automatic context engine

The Jev context engine is opt-in. It preserves valid tool-call/result structure and fails open. When Jev cannot safely make progress it may use Hermes' built-in compressor if `context_engine_fallback_builtin=true`.

## Gate

`gate_scope=selective` uses a deliberately narrow deterministic bypass only for known read-only tools/commands. It is not a general shell safety classifier. Shell composition (`|`, `>`, `&&`, command substitution), unknown commands, and commands with names that can mutate state (`date`, `nvidia-smi`, `env`, etc.) are not bypassed and still reach Jev when the gate is enabled. `gate_scope=all` disables the read-only bypass.

`enforce` mode routes low-confidence or provider-failure cases toward human approval rather than silently treating them as safe execution.

Do not treat a Jev probability as proof of correctness.
