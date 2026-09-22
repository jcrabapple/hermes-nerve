#!/usr/bin/env python3
"""Dependency-free live smoke for a running Hermes Reflex Laya sidecar."""
from __future__ import annotations

import argparse
import json
import os
import urllib.request


def request_json(url: str, *, token: str = "", payload=None, timeout: float = 10.0):
    headers = {"Accept": "application/json"}
    data = None
    method = "GET"
    if payload is not None:
        data = json.dumps(payload, separators=(",", ":")).encode()
        headers["Content-Type"] = "application/json"
        method = "POST"
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return int(response.status), json.loads(response.read())


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--base-url", default=os.getenv("HERMES_REFLEX_LAYA_BASE_URL", "http://127.0.0.1:8765"))
    p.add_argument("--token", default=os.getenv("HERMES_REFLEX_LAYA_TOKEN", ""))
    p.add_argument("--timeout", type=float, default=10.0)
    args = p.parse_args()
    base = args.base_url.rstrip("/")
    status, health = request_json(base + "/healthz", token=args.token, timeout=args.timeout)
    if status != 200 or not health.get("ok"):
        raise SystemExit(f"health failed: status={status} payload={health}")
    payload = {
        "state": {"goal": "Keep a Hermes worker on a productive trajectory", "signal": "same failing test repeated twice"},
        "questions": {
            "trajectory": {
                "type": "choice",
                "instructions": "What should the supervisor do?",
                "criteria": {
                    "WATCH": "Continue without changing the plan.",
                    "REPLAN": "Change the plan before repeating the same work.",
                },
            }
        },
    }
    status, result = request_json(base + "/v1/systemone", token=args.token, payload=payload, timeout=args.timeout)
    answer = (result.get("answers") or {}).get("trajectory") or {}
    if status != 200 or answer.get("choice") not in {"WATCH", "REPLAN"}:
        raise SystemExit(f"decision failed: status={status} payload={result}")
    if result.get("provider") != "Laya" or result.get("transport") != "laya-local-http":
        raise SystemExit(f"unexpected provenance: {result}")
    print(json.dumps({"ok": True, "health": health, "decision": result}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
