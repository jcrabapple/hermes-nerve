"""Dependency-free Jev client supporting OpenRouter, TypeSafe direct, and OpenCode Zen."""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Callable

OPENROUTER_BASE_URL = "https://openrouter.ai"
OPENROUTER_MODEL = "typesafe/jev-1.13"
OPENROUTER_PATH = "/api/alpha/decisions"
TYPESAFE_BASE_URL = "https://api.typesafe.ai"
TYPESAFE_MODEL = "jev-latest"
TYPESAFE_PATH = "/v1/systemone"
OPENCODE_BASE_URL = "https://opencode.ai"
OPENCODE_MODEL = "jev-1.13"
OPENCODE_PATH = "/zen/v1/systemone"
SUPPORTED_PROVIDERS = frozenset({"openrouter", "typesafe", "opencode"})
PROVIDER_API_KEY_ENV = {
    "openrouter": "OPENROUTER_API_KEY",
    "typesafe": "TYPESAFE_API_KEY",
    "opencode": "OPENCODE_API_KEY",
}
DEFAULT_TIMEOUT = 10.0

_configured_provider: str | None = None
_configured_base_url: str | None = None
_configured_model: str | None = None
_configured_typesafe_model: str | None = None
_configured_opencode_model: str | None = None
_configured_timeout: float | None = None


class JevError(RuntimeError):
    pass


def configure(*, provider: Any = None, base_url: Any = None, model: Any = None,
              typesafe_model: Any = None, opencode_model: Any = None, timeout: Any = None) -> None:
    global _configured_provider, _configured_base_url, _configured_model, _configured_typesafe_model, _configured_opencode_model, _configured_timeout
    raw_provider = str(provider or "").strip().lower()
    _configured_provider = raw_provider if raw_provider in SUPPORTED_PROVIDERS else None
    raw_base = str(base_url or "").strip()
    _configured_base_url = raw_base.rstrip("/") if raw_base else None
    raw_model = str(model or "").strip()
    _configured_model = raw_model or None
    raw_ts_model = str(typesafe_model or "").strip()
    _configured_typesafe_model = raw_ts_model or None
    raw_opencode_model = str(opencode_model or "").strip()
    _configured_opencode_model = raw_opencode_model or None
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


class JevClient:
    def __init__(
        self,
        *,
        provider: str | None = None,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str | None = None,
        timeout: float | None = None,
        transport: Callable[[str, dict[str, str], bytes, float], tuple] | None = None,
    ) -> None:
        selected_provider = str(provider or _configured_provider or os.getenv("HERMES_JEV_PROVIDER") or "openrouter").strip().lower()
        if selected_provider not in SUPPORTED_PROVIDERS:
            raise JevError("jev provider must be 'openrouter', 'typesafe', or 'opencode'")
        self.provider_kind = selected_provider

        if selected_provider == "opencode":
            self.api_key = api_key or os.getenv(PROVIDER_API_KEY_ENV[selected_provider], "").strip()
            selected_base_url = base_url or _configured_base_url or os.getenv("OPENCODE_BASE_URL") or OPENCODE_BASE_URL
            self.model = model or _configured_opencode_model or os.getenv("HERMES_JEV_OPENCODE_MODEL") or OPENCODE_MODEL
            if self.model != OPENCODE_MODEL:
                raise JevError("OpenCode Hermes-Jev access currently supports only paid model 'jev-1.13'")
            self.path = OPENCODE_PATH
            self.transport_name = "opencode-zen-system-one"
        elif selected_provider == "typesafe":
            self.api_key = api_key or os.getenv(PROVIDER_API_KEY_ENV[selected_provider], "").strip()
            selected_base_url = base_url or _configured_base_url or os.getenv("TYPESAFE_BASE_URL") or TYPESAFE_BASE_URL
            self.model = model or _configured_typesafe_model or os.getenv("HERMES_JEV_TYPESAFE_MODEL") or TYPESAFE_MODEL
            self.path = TYPESAFE_PATH
            self.transport_name = "typesafe-system-one"
        else:
            self.api_key = api_key or os.getenv(PROVIDER_API_KEY_ENV[selected_provider], "").strip()
            selected_base_url = base_url or _configured_base_url or os.getenv("OPENROUTER_BASE_URL") or OPENROUTER_BASE_URL
            self.model = model or _configured_model or os.getenv("HERMES_JEV_MODEL") or OPENROUTER_MODEL
            self.path = OPENROUTER_PATH
            self.transport_name = "openrouter-decisions"
        missing = f"{PROVIDER_API_KEY_ENV[selected_provider]} is not configured"

        self.base_url = str(selected_base_url).rstrip("/")
        raw_timeout = timeout if timeout is not None else _configured_timeout
        if raw_timeout is None:
            raw_timeout = float(os.getenv("HERMES_JEV_TIMEOUT", str(DEFAULT_TIMEOUT)))
        self.timeout = min(120.0, max(1.0, float(raw_timeout)))
        self._transport = transport or self._urllib_transport
        if not self.api_key:
            raise JevError(missing)
        if not self.base_url.startswith("https://"):
            raise JevError("Jev base_url must use https://")

    @staticmethod
    def _urllib_transport(url: str, headers: dict[str, str], body: bytes, timeout: float) -> tuple[int, bytes, dict[str, str]]:
        request = urllib.request.Request(url, data=body, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310 - https required above
                return int(response.status), response.read(), {str(k).lower(): str(v) for k, v in response.headers.items()}
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", "replace")[:500]
            raise JevError(f"Jev API returned HTTP {exc.code}: {detail}") from exc
        except (urllib.error.URLError, TimeoutError) as exc:
            raise JevError(f"Jev API connection failed: {exc}") from exc

    def system_one(self, *, state: Any, questions: dict[str, dict[str, Any]], model: str | None = None) -> JevResponse:
        if not questions:
            raise JevError("At least one question is required")
        payload = {"state": state, "model": model or self.model, "questions": questions}
        body = json.dumps(payload, separators=(",", ":"), ensure_ascii=False, default=str).encode("utf-8")
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "hermes-jev/0.2.2.dev2",
        }
        started = time.monotonic()
        raw_result = self._transport(self.base_url + self.path, headers, body, self.timeout)
        latency_ms = (time.monotonic() - started) * 1000
        if not isinstance(raw_result, tuple) or len(raw_result) not in {2, 3}:
            raise JevError("Jev transport returned an invalid response tuple")
        status, raw = raw_result[0], raw_result[1]
        response_headers = raw_result[2] if len(raw_result) == 3 and isinstance(raw_result[2], dict) else {}
        response_headers = {str(k).lower(): str(v) for k, v in response_headers.items()}
        if int(status) < 200 or int(status) >= 300:
            raise JevError(f"Jev API returned HTTP {status}: {bytes(raw).decode('utf-8', 'replace')[:500]}")
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise JevError("Jev API returned invalid JSON") from exc
        answers = data.get("answers")
        if not isinstance(answers, dict):
            raise JevError("Jev API response is missing answers")
        request_id = str(data.get("id") or "")
        if self.provider_kind == "typesafe":
            request_id = response_headers.get("x-typesafe-request-id", request_id)
        return JevResponse(
            model=str(data.get("model") or model or self.model),
            answers=answers,
            usage=data.get("usage") if isinstance(data.get("usage"), dict) else {},
            latency_ms=latency_ms,
            request_id=request_id,
            provider=str(data.get("provider") or ("OpenCode Zen" if self.provider_kind == "opencode" else "TypeSafe")),
            transport=self.transport_name,
        )
