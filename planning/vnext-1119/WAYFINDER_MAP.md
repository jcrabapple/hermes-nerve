# Wayfinder Map — Hermes-Jev vNext

## Destination

A production-ready implementation graph that turns Hermes-Jev into an asynchronous, adaptive decision nervous system while preserving all 1,119 requirements and avoiding synchronous ~500 ms overhead on ordinary work.

## Notes

Planning methodology follows Matt Pocock’s wayfinder/to-spec/to-tickets/codebase-design/prototype/TDD/implement-spec/code-review skills. The implementation tickets are tracer bullets; this map records the major architecture decisions already resolved in this thread.

## Decisions so far

- **Asynchronous tandem supervision:** Hermes continues work while Jev evaluates; synchronous gating is exceptional.
- **Prompt-level admission:** one non-recursive turn arbiter returns OFF/WATCH/ON.
- **Decision-plane semantics:** accountability, not chat/tool surface, determines eligibility.
- **Actor/director split:** roleplay dialogue is not Jev work; accountable director decisions can be.
- **Structured runtime events:** do not mine natural-language assistant output for decisions.
- **Hermes proposal in original event:** comparison needs no second model round trip.
- **Adaptive local router:** state delta and expected usefulness replace fixed every-N-event polling.
- **Sparse challenge channel:** agreements and low-confidence results are normally silent.
- **State/version validation:** stale Jev output is telemetry/advice, never blind mutation.
- **Decision leases and hysteresis:** equivalent state reuses the previous judgment.
- **Critical-event bypass:** completion, consequential action, strategy change, repeated failure and irreversible action can bypass batching.
- **Authority modes:** SHADOW, CORRECT_NEXT, PRECOMMIT.
- **Learning loop:** outcome receipts calibrate future router behavior/local classifier.
- **False PASS priority:** completion correctness matters more than call volume.

## Not yet specified

- Exact first production threshold/weight values for expected-value routing; tune from shadow telemetry rather than treating prototype numbers as constants.
- Whether the optional local relevance classifier graduates in the same release or remains a disabled adapter until enough receipts exist.
- Exact direct-TypeSafe live performance until a direct credential is available.

## Out of scope

- Per-tool synchronous Jev approval.
- Raw-transcript continuous Jev monitoring.
- A remote LLM router in front of Jev.
- Blind retroactive reversal of committed actions.
