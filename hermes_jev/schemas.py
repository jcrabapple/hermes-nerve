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

JEV_ASSESS = {
    "name": "jev_assess",
    "description": (
        "Ask up to 16 native Jev typed questions about one state in a single API call. Supports noul (yes/no "
        "probability), choice (bounded labels), and score (ordered rubric). Use when several structured judgments "
        "share the same evidence so Hermes can avoid multiple model calls."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "state": {"description": "JSON-compatible state shared by all questions."},
            "questions": {
                "type": "object",
                "minProperties": 1,
                "maxProperties": 16,
                "description": (
                    "Question name -> Jev question object. Each object uses type noul, choice, or score; "
                    "choice criteria is a label map and score criteria is an ordered array."
                ),
                "additionalProperties": {
                    "oneOf": [
                        {
                            "type": "object",
                            "properties": {
                                "type": {"type": "string", "enum": ["choice"], "description": "Bounded label selection."},
                                "instructions": {"description": "Question-specific instructions/context."},
                                "criteria": {
                                    "type": "object",
                                    "minProperties": 2,
                                    "additionalProperties": {"description": "Description for this allowed choice label."},
                                    "description": "Required choice-label map with at least two labels.",
                                },
                            },
                            "required": ["type", "criteria"],
                        },
                        {
                            "type": "object",
                            "properties": {
                                "type": {"type": "string", "enum": ["score"], "description": "Ordered rubric score."},
                                "instructions": {"description": "Question-specific instructions/context."},
                                "criteria": {
                                    "type": "array",
                                    "minItems": 2,
                                    "items": {"description": "Ordered score/rubric label or description."},
                                    "description": "Required ordered rubric with at least two entries.",
                                },
                            },
                            "required": ["type", "criteria"],
                        },
                        {
                            "type": "object",
                            "properties": {
                                "type": {"type": "string", "enum": ["noul"], "description": "Yes/no probability judgment."},
                                "instructions": {"description": "Question-specific instructions/context."},
                                "criteria": {
                                    "type": "object",
                                    "additionalProperties": {"description": "Optional semantic description for noul outcomes."},
                                    "description": "Optional noul criteria object; no choice labels are required.",
                                },
                            },
                            "required": ["type"],
                        },
                    ]
                },
            },
            "contract": {"type": "string", "description": "Stable contract name for receipts/evals."},
        },
        "required": ["state", "questions"],
    },
}

JEV_CONTEXT_CURATE = {
    "name": "jev_context_curate",
    "description": (
        "Act as a context-value governor over explicit evidence units. Jev estimates four semantic dimensions per "
        "candidate (future need, exactness need, supersession, unresolved conflict); deterministic local policy then "
        "chooses KEEP_EXACT/PIN/ANCHOR/DROP. User/assistant text is never model-rewritten. ANCHOR is a deterministic "
        "rehydratable pointer, not a generated summary. Use mode=shadow to measure a plan without changing the copy."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "goal": {"type": "string", "description": "Ongoing goal the working context must continue to support."},
            "items": {
                "type": "array",
                "minItems": 1,
                "maxItems": 48,
                "description": "Ordered evidence units to evaluate.",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string", "description": "Unique stable evidence id used for anchors/rehydration."},
                        "kind": {
                            "type": "string",
                            "enum": ["user_text", "assistant_text", "tool_call", "tool_result", "observation", "artifact", "other"],
                        },
                        "content": {"type": "string", "description": "Original evidence content."},
                        "recoverable": {"type": "boolean", "description": "True only when local code knows the evidence can be rerun/refetched."},
                        "pinned": {"type": "boolean", "description": "Force a PIN without consulting Jev."},
                        "metadata": {
                            "type": "object",
                            "description": "Optional provenance/lifecycle metadata. lease and recovery_pointer are recognized when supplied.",
                        },
                    },
                    "required": ["id", "content"],
                },
            },
            "preserve_tail": {"type": "integer", "minimum": 0, "maximum": 12, "description": "Newest N items to PIN."},
            "preview_chars": {"type": "integer", "minimum": 160, "maximum": 4000, "description": "Maximum per-item preview sent to Jev."},
            "anchor_chars": {"type": "integer", "minimum": 40, "maximum": 1200, "description": "Original prefix retained inside an ANCHOR."},
            "stub_chars": {"type": "integer", "minimum": 40, "maximum": 1200, "description": "Deprecated alias for anchor_chars."},
            "min_confidence": {"type": "number", "minimum": 0, "maximum": 1, "description": "Deprecated 0.1.5.x compatibility field; action-specific policy is used instead."},
            "mode": {"type": "string", "enum": ["apply", "shadow"], "description": "shadow returns originals while recording proposed actions; apply changes the returned copy."},
            "policy": {
                "type": "object",
                "description": "Optional per-call overrides for deterministic curation thresholds.",
                "properties": {
                    "drop_max_needed": {"type": "number", "minimum": 0, "maximum": 1},
                    "drop_max_exact": {"type": "number", "minimum": 0, "maximum": 1},
                    "drop_min_superseded": {"type": "number", "minimum": 0, "maximum": 1},
                    "anchor_max_needed": {"type": "number", "minimum": 0, "maximum": 1},
                    "anchor_max_exact": {"type": "number", "minimum": 0, "maximum": 1},
                    "conflict_pin_min": {"type": "number", "minimum": 0, "maximum": 1},
                },
            },
            "contract": {"type": "string", "description": "Stable contract name for receipts/evals."},
        },
        "required": ["goal", "items"],
    },
}

JEV_CONTEXT_REHYDRATE = {
    "name": "jev_context_rehydrate",
    "description": (
        "Restore sanitized evidence previously replaced by a Hermes-Jev context ANCHOR or DROP decision. "
        "This is a local evidence-ledger operation and does not call Jev/OpenRouter."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "evidence_id": {"type": "string", "description": "Evidence id from a JEV_CONTEXT_ANCHOR or curation decision."},
            "contract": {"type": "string", "description": "Optional receipt/eval contract name."},
        },
        "required": ["evidence_id"],
    },
}

JEV_STATS = {
    "name": "jev_stats",
    "description": (
        "Return bounded local Hermes-Jev telemetry for the active profile. The default is a compact summary to avoid "
        "injecting a very large tool result into the main model context. Use section to request receipts, gate, context, "
        "nervous, quality, outcomes, or all; include_recent is opt-in. This tool never calls Jev/OpenRouter."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "section": {
                "type": "string",
                "enum": ["summary", "receipts", "gate", "context", "nervous", "quality", "outcomes", "all"],
                "description": "Telemetry section to return (default summary).",
            },
            "recent_limit": {
                "type": "integer",
                "minimum": 0,
                "maximum": 20,
                "description": "Recent rows per requested section when include_recent=true (default 3).",
            },
            "include_recent": {
                "type": "boolean",
                "description": "Include bounded recent arrays. False by default to keep model context small.",
            },
        },
    },
}

JEV_NERVOUS_EVENT = {
    "name": "jev_nervous_event",
    "description": (
        "Emit one structured material decision into the asynchronous Hermes-Jev nervous system. "
        "Use only for an accountable decision with materially different alternatives, a recovery/completion boundary, "
        "or a consequential action. Routine reads and ordinary tool calls are observed automatically and should not call this tool."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "type": {"type": "string", "description": "Decision/event type such as DECISION, STRATEGY, ROUTING, RECOVERY, COMPLETION_CANDIDATE, COMMIT, or PRIORITIZATION."},
            "goal": {"type": "string", "description": "Accountable objective this decision advances."},
            "choices": {"type": "array", "items": {"type": "string"}, "description": "Bounded material alternatives when known."},
            "hermes_decision": {"type": "string", "description": "Hermes's proposed choice, included in the original event."},
            "criteria": {"type": "object", "description": "Optional label descriptions for bounded choices."},
            "state": {"description": "Compact JSON-compatible state relevant to the decision."},
            "evidence": {"description": "Compact evidence supporting the proposed decision."},
            "strategy": {"type": "string"},
            "hypothesis": {"type": "string"},
            "materiality": {"type": "number", "minimum": 0, "maximum": 1},
            "uncertainty": {"type": "number", "minimum": 0, "maximum": 1},
            "novelty": {"type": "number", "minimum": 0, "maximum": 1},
            "consequence": {"type": "number", "minimum": 0, "maximum": 1},
            "risk": {"type": "number", "minimum": 0, "maximum": 1},
            "reversible": {"type": "boolean"},
            "contradiction": {"type": "boolean"},
            "strategy_changed": {"type": "boolean"},
            "repeated_failure": {"type": "boolean"},
            "completion_candidate": {"type": "boolean"},
            "turn_id": {"type": "string", "description": "Optional Hermes turn correlation id; current turn is inferred when omitted."},
            "session_id": {"type": "string", "description": "Optional Hermes session correlation id."},
            "state_version": {"type": "string", "description": "Optional state/version identifier for stale-response protection."},
            "decision_version": {"type": "string", "description": "Optional decision version identifier."},
        },
        "required": ["type", "goal"],
    },
}
