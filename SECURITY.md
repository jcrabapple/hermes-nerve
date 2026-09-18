# Security

Hermes-Jev executes in the Hermes process and is **not a sandbox**.

## Threat model

The highest-risk boundary is automatic evaluation of tool arguments by a third-party API. Tool arguments can contain credentials, private paths, customer data, or commands with embedded secrets.

Mitigations in v0.1:

1. Automatic gating is off by default.
2. Common secret-bearing keys and token patterns are redacted before sending state.
3. Receipts store only a state hash by default.
4. Low-confidence enforce-mode decisions route to human approval.
5. Provider/network failure in enforce mode routes to human approval.
6. Jev tool calls are not automatically gated by the Jev gate.
7. Model output is checked against the caller-declared choice set before use.

Redaction is defense in depth, not a guarantee. Do not enable automatic external evaluation in environments where sending sanitized tool context to TypeSafe is prohibited.

Report security issues privately to the repository maintainer once the standalone repository is published.
