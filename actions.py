"""
actions.py — Agent OS / MCP onchain action layer for VaultKeeper.

Same dry_run pattern as SignalPilot/PayLoop: safe to run live during
a demo, with a clear seam (_call_mcp_tool) for wiring in a real
Agent OS onchain tool call.
"""
import datetime
from .policy import Plan


def _log(msg: str) -> None:
    ts = datetime.datetime.utcnow().isoformat(timespec="seconds")
    print(f"[{ts}] {msg}")


def _call_mcp_tool(tool_name: str, payload: dict) -> dict:
    """
    Placeholder for a real Agent OS / MCP onchain tool call, e.g.:

        response = mcp_client.call_tool(
            server="binance-agent-os",
            tool=tool_name,
            arguments=payload,
        )
    """
    _log(f"[MCP CALL] tool={tool_name} payload={payload}")
    return {"status": "simulated", "tool": tool_name}


def execute(plan: Plan, dry_run: bool) -> None:
    if plan.action == "HOLD":
        _log(f"{plan.protocol_id}: HOLD — {plan.detail}")
        return

    payload = {"protocol": plan.protocol_id, "action": plan.action, "detail": plan.detail}
    if plan.amount_usd:
        payload["amount_usd"] = plan.amount_usd

    if dry_run:
        _log(f"{plan.protocol_id}: [DRY RUN] would {plan.action} — {payload}")
        return

    tool = "unstake_position" if plan.action == "EXIT" else "rebalance_position"
    result = _call_mcp_tool(tool, payload)
    _log(f"{plan.protocol_id}: executed {plan.action} -> {result}")
