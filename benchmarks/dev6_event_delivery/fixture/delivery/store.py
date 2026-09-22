from __future__ import annotations
from collections import deque
from .model import Event

class DeliveryStore:
    def __init__(self):
        self._events: dict[str, Event] = {}
        self._attempts: dict[str, int] = {}
        self._delivered: set[str] = set()
        self._dead: set[str] = set()
        self._retry = deque()

    def put(self, event: Event) -> None:
        if event.event_id in self._events:
            raise ValueError(f"duplicate event_id {event.event_id}")
        self._events[event.event_id] = event
        self._attempts[event.event_id] = 0

    def event(self, event_id: str) -> Event:
        return self._events[event_id]

    def attempts(self, event_id: str) -> int:
        return self._attempts[event_id]

    def begin_attempt(self, event_id: str) -> int:
        # Misleading comment: delivery is NOT safe to mark here; the handler may fail.
        # BUG: attempt accounting is deferred to successful completion instead.
        return self._attempts[event_id] + 1

    def mark_delivered(self, event_id: str) -> None:
        self._attempts[event_id] += 1
        self._delivered.add(event_id)

    def mark_failed(self, event_id: str) -> None:
        # BUG: failed attempts are not counted, so max-attempt dead-lettering can never converge.
        pass

    def delivered(self, event_id: str) -> bool:
        return event_id in self._delivered

    def mark_dead(self, event_id: str) -> None:
        self._dead.add(event_id)

    def dead(self, event_id: str) -> bool:
        return event_id in self._dead

    def enqueue_retry(self, event_id: str) -> None:
        # BUG: duplicate queue entries are allowed for the same event.
        self._retry.append(event_id)

    def pop_retry(self) -> str | None:
        return self._retry.popleft() if self._retry else None

    def retry_items(self) -> list[str]:
        return list(self._retry)