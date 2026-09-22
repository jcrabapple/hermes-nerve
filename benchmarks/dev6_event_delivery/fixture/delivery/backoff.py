from __future__ import annotations

def retry_delay(attempt: int, *, base_seconds: int = 1, max_seconds: int = 32) -> int:
    """Return deterministic exponential backoff for a 1-based attempt number."""
    if attempt <= 0:
        raise ValueError("attempt must be >= 1")
    # BUG: exponent is one step too high. Attempt 1 should wait 1s, not 2s.
    return min(max_seconds, base_seconds * (2 ** attempt))