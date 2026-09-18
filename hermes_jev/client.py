"""Small dependency-free Jev client with OpenRouter and direct TypeSafe transports."""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from typing import Any, Callable, Mapping

OPENROUTER_BASE_URL = "https://openrouter.ai"
OPENROUTER_MODEL = "typesafe/jev-1.13"
OPENROUTER_PATH = "/api/alpha/decisions"
TYPESAFE_BASE_URL = "https://api.typesafe.ai"
TYPESAFE_MODEL = "jev-latest"
TYPESAFE_PATH = "/v1/systemone"
DEFAULT_TIMEOUT = 10.0

_configured_provider: str | None = None
_configured_base_url: str | None = None
_configured_model: str | None = None
_configured_typesafe_model: str | None = None
_configured_timeout: float | None = None


class JevError(RuntimeError):
    pass


def _normalize_provider(value: Any) -> str:
    raw = str(value or "openrouter").strip().lower().replace("_", "-")
    aliases = {
        "openrouter": "openrouter",
        "or": "openrouter",
        "typesafe": "typesafe",
        "type-safe": "typesafe",
        "direct": "typesafe",
        "typesafe-direct": "typesafe",
    }
    provider = aliases.get(raw)
    if provider is None:
        raise JevError("jev_provider must be 'openrouter' or 'typesafe'")
    return provider


def configure(
    *,
    provider: Any = None,
    base_url: Any = None,
    model: Any = None,
    typesafe_model: Any = None,
    timeout: Any = None,
) -> None:
    """Apply Hermes plugin transport settings captured during ``register(ctx)``."""
    global _configured_provider, _configured_base_url, _configured_model, _configured_typesafe_model, _configured_timeout

    _configured_provider = _normalize_provider(provider) if provider is not None else None

    raw_base = str(base_url or "").strip()
    _configured_base_url = raw_base.rstrip("/") if raw_base else None

    raw_model = str(model or "").strip()
    _configured_model = raw_model or None

    raw_typesafe_model = str(typesafe_model or "").strip()
    _configured_typesafe_model = raw_typesafe_model or None

    try:
        parsed_timeout = float(timeout) if timeout is not None else DEFAULT_TIMEOUT
    except (TypeError, ValueError):
        parsed_timeout = DEFAULT_TIMEOUT
    _configured_timeout = min(120.0, max(1.0, parsed_timeout))


@dataclass(frozen=True)
class JevResponse:
    model: str
    answers: dict[str, dict[str, Any]]
    usage: dict[str, Any]
    latency_ms: float
    request_id: str = ""
    provider: str = ""
    transport: str = "openrouter-decisions"


TransportResult = tuple[int, bytes] | tuple[int, bytes, Mapping[str, str]]
Transport = Callable[[str, dict[str, str], bytes, float], TransportResult]


class JevClient:
    def __init__(
        self,
        *,
        provider: str | None = None,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str | None = None,
        timeout: float | None = None,
        transport: Transport | None = None,
    ) -> None:
        selected_provider = provider or _configured_provider or os.getenv("HERMES_JEV_PROVIDER") or "openrouter"
        self.provider_kind = _normalize_provider(selected_provider)

        if self.provider_kind == "openrouter":
            self.api_key = api_key or os.getenv("OPENROUTER_API_KEY", "").strip()
            selected_base_url = base_url or _configured_base_url or os.getenv("OPENROUTER_BASE_URL") or OPENROUTER_BASE_URL
            selected_model = model or _configured_model or os.getenv("HERMES_JEV_MODEL") or OPENROUTER_MODEL
            self.path = OPENROUTER_PATH
            self.transport_name = "openrouter-decisions"
            self.provider_label = "OpenRouter"
            missing_key = "OPENROUTER_API_KEY is not configured"
        else:
            self.api_key = api_key or os.getenv("TYPESAFE_API_KEY", "").strip()
            selected_base_url = base_url or _configured_base_url or os.getenv("TYPESAFE_BASE_URL") or TYPESAFE_BASE_URL
            selected_model = model or _configured_typesafe_model or os.getenv("TYPESAFE_DEFAULT_MODEL") or TYPESAFE_MODEL
            self.path = TYPESAFE_PATH
            self.transport_name = "typesafe-system-one"
            self.provider_label = "TypeSafe"
            missing_key = "TYPESAFE_API_KEY is not configured"

        self.base_url = str(selected_base_url).rstrip("/")
        self.model = str(selected_model).strip()
        raw_timeout = timeout if timeout is not None else _configured_timeout
        if raw_timeout is None:
            raw_timeout = float(os.getenv("HERMES_JEV_TIMEOUT", str(DEFAULT_TIMEOUT)))
        self.timeout = min(120.0, max(1.0, float(raw_timeout)))
        self._transport = transport or self._urllib_transport

        if not self.api_key:
            raise JevError(missing_key)
        if not self.base_url.startswith("https://"):
            raise JevError("Jev base_url must use https://")
        if not self.model:
            raise JevError("Jev model is not configured")

    @staticmethod
    def _urllib_transport(url: str, headers: dict[str, str], body: bytes, timeout: float) -> TransportResult:
        request = urllib.request.Request(url, data=body, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310 - https required above
                return int(response.status), response.read(), dict(response.headers.items())
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", "replace")[:500]
            raise JevError(f"Jev provider returned HTTP {exc.code}: {detail}") from exc
        except (urllib.error.URLError, TimeoutError) as exc:
            raise JevError(f"Jev provider connection failed: {exc}") from exc

    @staticmethod
    def _unpack_transport(result: TransportResult) -> tuple[int, bytes, dict[str, str]]:
        if not isinstance(result, tuple) or len(result) not in {2, 3}:
            raise JevError("Jev transport returned an invalid result")
        status = int(result[0])
        raw = result[1]
        if not isinstance(raw, (bytes, bytearray)):
            raise JevError("Jev transport body must be bytes")
        headers: dict[str, str] = {}
        if len(result) == 3 and isinstance(result[2], Mapping):
            headers = {str(k).lower(): str(v) for k, v in result[2].items()}
        return status, bytes(raw), headers

    def system_one(self, *, state: Any, questions: dict[str, dict[str, Any]], model: str | None = None) -> JevResponse:
        if not questions:
            raise JevError("At least one question is required")
        payload = {"state": state, "model": model or self.model, "questions": questions}
        body = json.dumps(payload, separators=(",", ":"), ensure_ascii=False, default=str).encode("utf-8")
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "hermes-jev/0.1.5.5",
        }
        started = time.monotonic()
        result = self._transport(self.base_url + self.path, headers, body, self.timeout)
        latency_ms = (time.monotonic() - started) * 1000
        status, raw, response_headers = self._unpack_transport(result)
        if status < 200 or status >= 300:
            raise JevError(f"{self.provider_label} Jev API returned HTTP {status}: {raw.decode('utf-8', 'replace')[:500]}")
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise JevError(f"{self.provider_label} Jev API returned invalid JSON") from exc
        answers = data.get("answers")
        if not isinstance(answers, dict):
            raise JevError(f"{self.provider_label} Jev API response is missing answers")

        request_id = str(data.get("id") or "")
        provider = str(data.get("provider") or "")
        if self.provider_kind == "typesafe":
            request_id = response_headers.get("x-typesafe-request-id", request_id)
            provider = provider or "TypeSafe"

        return JevResponse(
            model=str(data.get("model") or model or self.model),
            answers=answers,
            usage=data.get("usage") if isinstance(data.get("usage"), dict) else {},
            latency_ms=latency_ms,
            request_id=request_id,
            provider=provider,
            transport=self.transport_name,
        )
