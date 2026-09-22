from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Event:
    event_id: str
    payload: str

    def __post_init__(self):
        if not self.event_id:
            raise ValueError("event_id required")