"""Hermes-Jev plugin registration."""

from .hermes_jev import gate, receipts, schemas, tools


def register(ctx):
    gate.configure(
        mode=ctx.get_config("gate_mode", "off"),
        min_confidence=ctx.get_config("min_confidence", 0.80),
    )
    receipts.configure(detail=ctx.get_config("receipt_detail", "hash"))
    ctx.register_tool(name="jev_decide", toolset="jev", schema=schemas.JEV_DECIDE, handler=tools.jev_decide)
    ctx.register_tool(name="jev_rank", toolset="jev", schema=schemas.JEV_RANK, handler=tools.jev_rank)
    ctx.register_tool(name="jev_verify", toolset="jev", schema=schemas.JEV_VERIFY, handler=tools.jev_verify)
    ctx.register_hook("pre_tool_call", gate.pre_tool_call)
