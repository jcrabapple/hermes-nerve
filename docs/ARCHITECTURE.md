# Architecture

`DecisionEngine` is the stable center of Hermes-Jev. It depends on a tiny `DecisionProvider` protocol. `JevClient` is the first backend.

```text
Hermes tool/agent state
        |
      redact
        |
 DecisionEngine
        |
 DecisionProvider
        |
      Jev API
        |
 typed answer + probabilities
        |
 deterministic local policy
        |
 execute / approval / block / retry / replan
        |
 privacy-minimized receipt
```

This keeps policy and semantics local while using Jev for the bounded semantic judgment.
