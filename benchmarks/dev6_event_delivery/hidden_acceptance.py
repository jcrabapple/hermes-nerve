"""External acceptance checks. Keep outside both worker workspaces."""
from __future__ import annotations
import sys
from pathlib import Path


def run(repo: str) -> None:
    root = Path(repo).resolve()
    sys.path.insert(0, str(root))
    from delivery import DeliveryStore, Dispatcher, Event
    from delivery.backoff import retry_delay

    # transient twice, then success: exactly one successful delivery, three attempts
    store = DeliveryStore()
    store.put(Event("z", "payload"))
    calls = []

    def handler(event):
        calls.append(event.event_id)
        if len(calls) < 3:
            raise RuntimeError("transient")

    d = Dispatcher(store, handler, max_attempts=4)
    assert d.dispatch("z").startswith("retry:")
    assert d.dispatch("z").startswith("retry:")
    assert d.dispatch("z") == "delivered"
    delivered_attempts = store.attempts("z")
    assert d.dispatch("z") == "duplicate"
    assert calls == ["z", "z", "z"]
    assert store.attempts("z") == delivered_attempts == 3
    assert store.delivered("z") and not store.dead("z")

    # hard failure reaches dead letter exactly at threshold, then becomes a
    # stable terminal read: no extra attempt and no handler re-invocation.
    s2 = DeliveryStore()
    s2.put(Event("d", "x"))
    dead_calls = []

    def hard_fail(event):
        dead_calls.append(event.event_id)
        raise RuntimeError("x")

    d2 = Dispatcher(s2, hard_fail, max_attempts=3)
    assert d2.dispatch("d").startswith("retry:")
    assert d2.dispatch("d").startswith("retry:")
    assert d2.dispatch("d") == "dead"
    assert s2.attempts("d") == 3 and s2.dead("d")
    before_attempts = s2.attempts("d")
    before_calls = len(dead_calls)
    assert d2.dispatch("d") == "dead"
    assert s2.attempts("d") == before_attempts, (
        f"dead redispatch changed attempts {before_attempts}->{s2.attempts('d')}"
    )
    assert len(dead_calls) == before_calls, (
        f"dead redispatch invoked handler again {before_calls}->{len(dead_calls)}"
    )

    # retry queue remains unique under repeated enqueue.
    q = DeliveryStore()
    q.put(Event("q", "x"))
    q.enqueue_retry("q")
    q.enqueue_retry("q")
    q.enqueue_retry("q")
    assert q.retry_items() == ["q"]

    assert [retry_delay(i) for i in (1, 2, 3, 4, 6)] == [1, 2, 4, 8, 32]
    print("HIDDEN_ACCEPTANCE_PASS")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: hidden_acceptance.py <repo>")
    run(sys.argv[1])