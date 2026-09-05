"""
policy.py — allocation and risk policy for VaultKeeper.

Turns a list of Positions into a list of Plans (actions to take):
  - EXIT  a position that fails a risk check (low APY, thin liquidity, locked)
  - REBALANCE a position whose actual weight has drifted too far from target
  - HOLD everything else

Each decision carries its reasons so a demo can narrate exactly why
the agent chose what it chose.
"""
from dataclasses import dataclass
from typing import List
from .positions import Position, current_allocation


@dataclass
class Plan:
    protocol_id: str
    action: str          # EXIT | REBALANCE | HOLD
    detail: str
    amount_usd: float = 0.0


def evaluate(positions: List[Position], config: dict) -> List[Plan]:
    risk = config["risk"]
    targets = config["target_allocation"]
    actual = current_allocation(positions)
    plans = []

    for pos in positions:
        # Risk checks first — these override allocation drift.
        if pos.apy < risk["min_apy"]:
            plans.append(Plan(pos.protocol_id, "EXIT", f"APY {pos.apy}% below floor {risk['min_apy']}%", pos.balance_usd))
            continue
        if pos.liquidity_usd < risk["min_liquidity_usd"]:
            plans.append(Plan(pos.protocol_id, "EXIT", f"liquidity ${pos.liquidity_usd:,.0f} below floor", pos.balance_usd))
            continue
        if pos.locked:
            plans.append(Plan(pos.protocol_id, "HOLD", "position is time-locked, cannot act now"))
            continue

        target = targets.get(pos.protocol_id, 0.0)
        weight = actual.get(pos.protocol_id, 0.0)
        drift = weight - target

        if weight > risk["max_protocol_exposure"]:
            plans.append(Plan(pos.protocol_id, "REBALANCE", f"exposure {weight:.1%} exceeds max {risk['max_protocol_exposure']:.0%}"))
        elif abs(drift) > risk["rebalance_drift_threshold"]:
            direction = "trim" if drift > 0 else "top up"
            plans.append(Plan(pos.protocol_id, "REBALANCE", f"{direction} — actual {weight:.1%} vs target {target:.1%}"))
        else:
            plans.append(Plan(pos.protocol_id, "HOLD", f"within target ({weight:.1%} vs {target:.1%})"))

    return plans
