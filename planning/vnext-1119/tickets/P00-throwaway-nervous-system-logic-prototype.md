# P00: Throwaway nervous-system logic prototype

**Blocked by:** None

**Status:** ready-for-agent

## Question

Does the proposed asynchronous tandem state model behave correctly before production integration?

## What to build

A disposable logic prototype that simulates prompt admission, event emission, adaptive local routing, asynchronous Jev responses, staleness, challenge delivery and turn completion with a synthetic 500–800 ms provider.

## Acceptance criteria

- [ ] Hermes timeline continues while synthetic Jev is delayed.
- [ ] OFF/WATCH/ON can be driven manually.
- [ ] A stale challenge is visibly rejected.
- [ ] High-volume low-value events compress locally.
- [ ] A high-value contradiction triggers Jev immediately.
- [ ] Prototype records the design decisions it validates; production code does not depend on the prototype.

**Matt prototype rule:** throw this away after the state-model decisions are captured; do not evolve it into production.
