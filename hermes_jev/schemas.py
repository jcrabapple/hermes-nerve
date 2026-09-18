"""Hermes tool schemas for Hermes-Jev."""

JEV_DECIDE = {
    "name": "jev_decide",
    "description": (
        "Make one bounded typed decision with TypeSafe Jev. Use when the possible outcomes are known in advance "
        "and software needs a choice plus calibrated probabilities instead of generated prose."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "state": {"description": "JSON-compatible state Jev should evaluate."},
            "instructions": {"type": "string", "description": "Precise decision question."},
            "choices": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 2,
                "description": "Allowed output labels. Jev cannot return a label outside this set.",
            },
            "criteria": {
                "type": "object",
                "additionalProperties": {"description": "Optional description for a choice label."},
                "description": "Optional label-to-description mapping.",
            },
            "contract": {"type": "string", "description": "Stable contract name for receipts/evals."},
        },
        "required": ["state", "instructions", "choices"],
    },
}

JEV_RANK = {
    "name": "jev_rank",
    "description": (
        "Rank a bounded set of candidate labels using Jev probabilities. Useful for tool, skill, worker, model, "
        "queue, or option routing where every candidate is known."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "state": {"description": "JSON-compatible routing state."},
            "instructions": {"type": "string", "description": "What makes one candidate preferable."},
            "items": {
                "type": "object",
                "minProperties": 2,
                "additionalProperties": {"description": "Optional candidate description."},
                "description": "Candidate label -> description mapping.",
            },
            "contract": {"type": "string", "description": "Stable contract name for receipts/evals."},
        },
        "required": ["state", "instructions", "items"],
    },
}

JEV_VERIFY = {
    "name": "jev_verify",
    "description": (
        "Verify an execution result with a bounded PASS/RETRY/REPLAN/ESCALATE decision and probabilities. "
        "Use after work has run when the agent needs a cheap structured completion/recovery decision."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "state": {"description": "JSON-compatible evidence about the attempted work and result."},
            "instructions": {"type": "string", "description": "Verification goal and success conditions."},
            "contract": {"type": "string", "description": "Stable contract name for receipts/evals."},
        },
        "required": ["state", "instructions"],
    },
}
