from __future__ import annotations
import pytest
from delivery.backoff import retry_delay
from delivery.dispatcher import Dispatcher
from delivery.model import Event
from delivery.store import DeliveryStore


def make(*, handler=None, max_attempts=3):
    store = DeliveryStore()
    store.put(Event("e1", "one"))
    if handler is None:
        handler = lambda event: None
    return store, Dispatcher(store, handler, max_attempts=max_attempts)


def test_success_is_delivered_once():
    calls=[]
    store, d = make(handler=lambda event: calls.append(event.event_id))
    assert d.dispatch("e1") == "delivered"
    assert d.dispatch("e1") == "duplicate"
    assert calls == ["e1"]
    assert store.attempts("e1") == 1


def test_transient_failure_can_retry_then_deliver():
    calls=[]
    def handler(event):
        calls.append(event.event_id)
        if len(calls) == 1:
            raise RuntimeError("transient")
    store, d = make(handler=handler)
    assert d.dispatch("e1").startswith("retry:")
    assert d.dispatch("e1") == "delivered"
    assert calls == ["e1", "e1"]
    assert store.delivered("e1")
    assert store.attempts("e1") == 2


def test_failed_attempt_is_counted():
    store, d = make(handler=lambda event: (_ for _ in ()).throw(RuntimeError("nope")))
    assert d.dispatch("e1").startswith("retry:")
    assert store.attempts("e1") == 1


def test_dead_letters_on_max_attempts_not_one_late():
    store, d = make(handler=lambda event: (_ for _ in ()).throw(RuntimeError("nope")), max_attempts=2)
    assert d.dispatch("e1").startswith("retry:")
    assert d.dispatch("e1") == "dead"
    assert store.dead("e1")
    assert store.attempts("e1") == 2


def test_retry_queue_contains_event_once():
    store, d = make(handler=lambda event: (_ for _ in ()).throw(RuntimeError("nope")))
    d.dispatch("e1")
    # Re-observing failure/retry state must not create duplicate queue work.
    store.enqueue_retry("e1")
    assert store.retry_items() == ["e1"]


@pytest.mark.parametrize("attempt,expected", [(1,1),(2,2),(3,4),(6,32)])
def test_backoff_is_one_based(attempt, expected):
    assert retry_delay(attempt) == expected


def test_batch_continues_after_retryable_failure():
    store = DeliveryStore()
    for i in range(1,4): store.put(Event(f"e{i}", str(i)))
    calls=[]
    def handler(event):
        calls.append(event.event_id)
        if event.event_id == "e1": raise RuntimeError("transient")
    d=Dispatcher(store,handler)
    results=d.dispatch_batch(["e1","e2","e3"])
    assert [x[0] for x in results] == ["e1","e2","e3"]
    assert calls == ["e1","e2","e3"]
    assert store.delivered("e2") and store.delivered("e3")


def test_batch_preserves_input_result_order():
    store=DeliveryStore()
    for key in ["c","a","b"]: store.put(Event(key,key))
    d=Dispatcher(store,lambda event: None)
    assert [x[0] for x in d.dispatch_batch(["c","a","b"])] == ["c","a","b"]


def test_unknown_event_raises_key_error():
    store, d = make()
    with pytest.raises(KeyError): d.dispatch("missing")


def test_duplicate_put_rejected():
    store=DeliveryStore();store.put(Event("x","1"))
    with pytest.raises(ValueError): store.put(Event("x","2"))