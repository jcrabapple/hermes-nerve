"""Hermes-Jev plugin registration."""

import logging
from pathlib import Path

from .hermes_jev import client, context, gate, ledger, receipts, schemas, tools, nervous
from .hermes_jev.context_engine import JevContextEngine
from .hermes_jev.provenance import VERSION

logger = logging.getLogger("hermes_jev")


def register(ctx):
    # Compatibility with the user's hand-fixed 0.1.5.1 tree: model_id remains
    # accepted, while jev_model is the canonical non-reserved key going forward.
    legacy_model = ctx.get_config("model_id", "typesafe/jev-1.13")
    client.configure(
        provider=ctx.get_config("jev_provider", "openrouter"),
        model=ctx.get_config("jev_model", legacy_model),
        typesafe_model=ctx.get_config("typesafe_model", "jev-latest"),
        opencode_model=ctx.get_config("opencode_model", "jev-1.13-free"),
        timeout=ctx.get_config("timeout_seconds", 10.0),
    )
    gate.configure(
        mode=ctx.get_config("gate_mode", "off"),
        min_confidence=ctx.get_config("min_confidence", 0.80),
        scope=ctx.get_config("gate_scope", "selective"),
    )
    receipts.configure(detail=ctx.get_config("receipt_detail", "hash"))
    ledger.configure(
        enabled=ctx.get_config("context_ledger_enabled", True),
        detail=ctx.get_config("context_ledger_detail", "sanitized"),
    )
    nervous.configure(
        enabled=ctx.get_config("nervous_enabled", True),
        admission_enabled=ctx.get_config("nervous_turn_admission", True),
        mode=ctx.get_config("nervous_mode", "correct_next"),
        challenge_confidence=ctx.get_config("nervous_challenge_confidence", 0.86),
        call_threshold=ctx.get_config("nervous_call_threshold", 0.58),
        max_provider_calls_per_turn=ctx.get_config("nervous_max_provider_calls_per_turn", 96),
        event_preview_chars=ctx.get_config("nervous_event_preview_chars", 1200),
        retain_recent_events=ctx.get_config("nervous_retain_recent_events", 64),
        emit_prompt_hint=ctx.get_config("nervous_emit_prompt_hint", False),
        local_learning=ctx.get_config("nervous_local_learning", True),
        local_learning_min_samples=ctx.get_config("nervous_local_learning_min_samples", 8),
        repeated_failure_local_replan_at=ctx.get_config("nervous_repeated_failure_local_replan_at", 3),
    )
    context.configure(
        preview_chars=ctx.get_config("context_preview_chars", 1200),
        anchor_chars=ctx.get_config("context_anchor_chars", 220),
        preserve_tail=ctx.get_config("context_preserve_tail", 4),
        mode=ctx.get_config("context_curation_mode", "shadow"),
        drop_max_needed=ctx.get_config("context_drop_max_needed", 0.20),
        drop_max_exact=ctx.get_config("context_drop_max_exact", 0.20),
        drop_min_superseded=ctx.get_config("context_drop_min_superseded", 0.75),
        anchor_max_needed=ctx.get_config("context_anchor_max_needed", 0.55),
        anchor_max_exact=ctx.get_config("context_anchor_max_exact", 0.45),
        conflict_pin_min=ctx.get_config("context_conflict_pin_min", 0.70),
    )

    ctx.register_tool(name="jev_decide", toolset="jev", schema=schemas.JEV_DECIDE, handler=tools.jev_decide)
    ctx.register_tool(name="jev_rank", toolset="jev", schema=schemas.JEV_RANK, handler=tools.jev_rank)
    ctx.register_tool(name="jev_verify", toolset="jev", schema=schemas.JEV_VERIFY, handler=tools.jev_verify)
    ctx.register_tool(name="jev_assess", toolset="jev", schema=schemas.JEV_ASSESS, handler=tools.jev_assess)
    ctx.register_tool(name="jev_context_curate", toolset="jev", schema=schemas.JEV_CONTEXT_CURATE, handler=tools.jev_context_curate)
    ctx.register_tool(name="jev_context_rehydrate", toolset="jev", schema=schemas.JEV_CONTEXT_REHYDRATE, handler=tools.jev_context_rehydrate)
    ctx.register_tool(name="jev_stats", toolset="jev", schema=schemas.JEV_STATS, handler=tools.jev_stats)
    ctx.register_tool(name="jev_nervous_event", toolset="jev", schema=schemas.JEV_NERVOUS_EVENT, handler=tools.jev_nervous_event)
    # v0.2.1: one composed pre-tool control seam. Local nervous control runs
    # first; the optional synchronous legacy gate is consulted only when the
    # local loop breaker does not already constrain the action.
    def _pre_tool_control(**kwargs):
        directive = nervous.pre_tool_call(**kwargs)
        if directive is not None:
            return directive
        return gate.pre_tool_call(**kwargs)

    ctx.register_hook("pre_tool_call", _pre_tool_control)
    ctx.register_hook("post_tool_call", ledger.observe_tool_call)
    # Admission and provider work are asynchronous; transform_tool_result is the
    # non-blocking model-context backchannel for confident challenges.
    ctx.register_hook("pre_llm_call", nervous.pre_llm_call)
    ctx.register_hook("post_tool_call", nervous.post_tool_call)
    ctx.register_hook("transform_tool_result", nervous.transform_tool_result)
    ctx.register_hook("pre_verify", nervous.pre_verify)
    ctx.register_hook("post_llm_call", nervous.post_llm_call)
    ctx.register_hook("on_session_end", nervous.on_session_end)

    # Registration is harmless until the user explicitly selects context.engine=jev.
    # Guard for older Hermes versions that do not yet expose the public ContextEngine slot.
    if bool(ctx.get_config("context_engine_register", True)) and hasattr(ctx, "register_context_engine"):
        engine = JevContextEngine(
            mode=ctx.get_config("context_engine_mode", "shadow"),
            threshold_percent=ctx.get_config("context_engine_threshold_percent", 0.72),
            protect_first_n=ctx.get_config("context_engine_protect_first_n", 3),
            protect_last_n=ctx.get_config("context_engine_protect_last_n", 6),
            shadow_trigger_percent=ctx.get_config("context_engine_shadow_trigger_percent", 0.55),
            fallback_builtin=ctx.get_config("context_engine_fallback_builtin", True),
        )
        ctx.register_context_engine(engine)

    logger.info(
        "Hermes-Jev %s loaded from %s; tools=8 hook_names=7 hook_callbacks=8 context_engine_register=%s",
        VERSION, Path(__file__).resolve().parent, bool(ctx.get_config("context_engine_register", True)),
    )
