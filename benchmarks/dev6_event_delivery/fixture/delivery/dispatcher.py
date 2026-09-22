from __future__ import annotations
from collections.abc import Callable
from .backoff import retry_delay
from .model import Event
from .store import DeliveryStore

class Dispatcher:
    def __init__(self, store: DeliveryStore, handler: Callable[[Event], None], *, max_attempts: int = 3):
        if max_attempts <= 0:
            raise ValueError("max_attempts must be positive")
        self.store = store
        self.handler = handler
        self.max_attempts = max_attempts
        self._seen: set[str] = set()

    def dispatch(self, event_id: str) -> str:
        event = self.store.event(event_id)
        if self.store.delivered(event_id) or event_id in self._seen:
            return "duplicate"
        # BUG: adding to _seen before the handler succeeds suppresses a legitimate retry.
        self._seen.add(event_id)
        attempt = self.store.begin_attempt(event_id)
        try:
            self.handler(event)
        except Exception:
            self.store.mark_failed(event_id)
            # BUG interaction: attempts() did not increment, and > should be >= at the threshold.
            if self.store.attempts(event_id) > self.max_attempts:
                self.store.mark_dead(event_id)
                return "dead"
            self.store.enqueue_retry(event_id)
            return f"retry:{retry_delay(attempt)}"
        self.store.mark_delivered(event_id)
        return "delivered"

    def dispatch_batch(self, event_ids: list[str]) -> list[tuple[str, str]]:
        results: list[tuple[str, str]] = []
        for event_id in event_ids:
            result = self.dispatch(event_id)
            results.append((event_id, result))
            # BUG: one retryable event must not prevent independent later events from being attempted.
            if result.startswith("retry"):
                break
        return results