"""Small dependency-free client for TypeSafe's public System One wire protocol."""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Callable

DEFAULT_BASE_URL = "https://api.typesafe.ai"
DEFAULT_MODEL = "jev-latest"
DEFAULT_TIMEOUT = 10.0
SYSTEM_ONE_PATH = "/v1/systemone"


class JevError(RuntimeError):
    pass


@dataclass(frozen=True)
class JevResponse:
    model: str
    answers: dict[str, dict[str, Any]]
    usage: dict[str, Any]
    latency_ms: float


class JevClient:
    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str | None = None,
        timeout: float | None = None,
        transport: Callable[[str, dict[str, str], bytes, float], tuple[int, bytes]] | None = None,
    ) -> None:
        self.api_key = api_key or os.getenv("TYPESAFE_API_KEY", "").strip()
        self.base_url = (base_url or os.getenv("TYPESAFE_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
        self.model = model or os.getenv("TYPESAFE_DEFAULT_MODEL") or DEFAULT_MODEL
        self.timeout = timeout or float(os.getenv("HERMES_JEV_TIMEOUT", str(DEFAULT_TIMEOUT)))
        self._transport = transport or self._urllib_transport
        if not self.api_key:
            raise JevError("TYPESAFE_API_KEY is not configured")

    @staticmethod
    def _urllib_transport(url: str, headers: dict[str, str], body: bytes, timeout: float) -> tuple[int, bytes]:
        request = urllib.request.Request(url, data=body, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310 - fixed https URL by default
                return int(response.status), response.read()
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", "replace")[:500]
            raise JevError(f"TypeSafe API returned HTTP {exc.code}: {detail}") from exc
        except (urllib.error.URLError, TimeoutError) as exc:
            raise JevError(f"TypeSafe API connection failed: {exc}") from exc

    def system_one(self, *, state: Any, questions: dict[str, dict[str, Any]], model: str | None = None) -> JevResponse:
        if not questions:
            raise JevError("At least one question is required")
        payload = {"state": state, "model": model or self.model, "questions": questions}
        body = json.dumps(payload, separators=(",", ":"), ensure_ascii=False, default=str).encode("utf-8")
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "hermes-jev/0.1.3",
        }
        started = time.monotonic()
        status, raw = self._transport(self.base_url + SYSTEM_ONE_PATH, headers, body, self.timeout)
        latency_ms = (time.monotonic() - started) * 1000
        if status < 200 or status >= 300:
            raise JevError(f"TypeSafe API returned HTTP {status}: {raw.decode('utf-8', 'replace')[:500]}")
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise JevError("TypeSafe API returned invalid JSON") from exc
        answers = data.get("answers")
        if not isinstance(answers, dict):
            raise JevError("TypeSafe API response is missing answers")
        return JevResponse(
            model=str(data.get("model") or model or self.model),
            answers=answers,
            usage=data.get("usage") if isinstance(data.get("usage"), dict) else {},
            latency_ms=latency_ms,
        )
