"""Hermes-Jev plugin registration."""

from .hermes_jev import client, context, gate, ledger, receipts, schemas, tools
from .hermes_jev.context_engine import JevContextEngine


def register(ctx):
    # Compatibility with the user's hand-fixed 0.1.5.1 tree: model_id remains
    # accepted, while jev_model is the canonical non-reserved key going forward.
    legacy_model = ctx.get_config("model_id", "typesafe/jev-1.13")
    client.configure(
        provider=ctx.get_config("jev_provider", "openrouter"),
        model=ctx.get_config("jev_model", legacy_model),
        typesafe_model=ctx.get_config("typesafe_model", "jev-latest"),
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
    ctx.register_hook("pre_tool_call", gate.pre_tool_call)
    ctx.register_hook("post_tool_call", ledger.observe_tool_call)

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
