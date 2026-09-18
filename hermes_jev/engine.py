"""Provider-independent decision runtime. Jev is the first backend."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from .client import JevClient
from .privacy import redact
from .receipts import write_receipt


class DecisionProvider(Protocol):
    def system_one(self, *, state: Any, questions: dict[str, dict[str, Any]], model: str | None = None): ...


@dataclass(frozen=True)
class DecisionResult:
    value: str
    confidence: float
    probabilities: dict[str, float]
    model: str
    latency_ms: float
    contract: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "value": self.value,
            "confidence": self.confidence,
            "probabilities": self.probabilities,
            "model": self.model,
            "latency_ms": round(self.latency_ms, 3),
            "contract": self.contract,
        }


class DecisionEngine:
    def __init__(self, provider: DecisionProvider | None = None) -> None:
        self.provider = provider or JevClient()

    def decide(
        self,
        *,
        state: Any,
        instructions: str,
        choices: list[str],
        criteria: dict[str, Any] | None = None,
        contract: str = "decision/v1",
    ) -> DecisionResult:
        labels = [str(item).strip() for item in choices if str(item).strip()]
        if len(labels) < 2 or len(set(labels)) != len(labels):
            raise ValueError("choices must contain at least two unique non-empty labels")
        safe_state = redact(state)
        mapped = {label: (criteria or {}).get(label) for label in labels}
        response = self.provider.system_one(
            state=safe_state,
            questions={"decision": {"type": "choice", "instructions": instructions, "criteria": mapped}},
        )
        answer = response.answers.get("decision") or {}
        value = str(answer.get("choice") or "")
        probabilities = {str(k): float(v) for k, v in (answer.get("probabilities") or {}).items()}
        if value not in mapped:
            raise ValueError(f"provider returned out-of-contract choice: {value!r}")
        confidence = float(answer.get("confidence", probabilities.get(value, 0.0)))
        result = DecisionResult(value, confidence, probabilities, response.model, response.latency_ms, contract)
        write_receipt(contract=contract, state=safe_state, result=result.as_dict(), model=response.model, latency_ms=response.latency_ms)
        return result

    def rank(self, *, state: Any, instructions: str, items: dict[str, Any], contract: str = "rank/v1") -> dict[str, Any]:
        result = self.decide(
            state=state,
            instructions=instructions,
            choices=list(items),
            criteria=items,
            contract=contract,
        )
        ranking = sorted(result.probabilities.items(), key=lambda pair: (-pair[1], pair[0]))
        return {**result.as_dict(), "ranking": [{"label": label, "probability": prob} for label, prob in ranking]}

    def verify(self, *, state: Any, instructions: str, contract: str = "verify/v1") -> DecisionResult:
        return self.decide(
            state=state,
            instructions=instructions,
            choices=["PASS", "RETRY", "REPLAN", "ESCALATE"],
            criteria={
                "PASS": "Evidence satisfies the requested outcome with no material unresolved issue.",
                "RETRY": "The approach is valid but execution should be tried again with the same plan.",
                "REPLAN": "The current approach is insufficient; change the plan before trying again.",
                "ESCALATE": "Human judgment, permission, missing information, or an external dependency is required.",
            },
            contract=contract,
        )
