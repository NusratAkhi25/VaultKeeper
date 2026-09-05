"""
positions.py — onchain position model + sample position feed for VaultKeeper.

In a real deployment, `fetch_positions()` would call a protocol
subgraph, an onchain RPC, or an Agent OS data tool. Here it returns a
fixed sample so the pipeline runs standalone for judges without
needing wallet credentials or live RPC access.
"""
from dataclasses import dataclass


@dataclass
class Position:
    protocol_id: str    # key matching config["target_allocation"]
    balance_usd: float
    apy: float           # current APY, percent
    liquidity_usd: float # protocol TVL/liquidity depth
    locked: bool          # True if funds are time-locked (can't unstake now)


def fetch_positions() -> list:
    """Sample onchain position feed — swap for a live data source."""
    return [
        Position("protocol_a_staking", balance_usd=3800.0, apy=5.2, liquidity_usd=12_000_000, locked=False),
        Position("protocol_b_vault", balance_usd=2900.0, apy=2.1, liquidity_usd=450_000, locked=False),
        Position("protocol_c_lp", balance_usd=3300.0, apy=8.7, liquidity_usd=90_000, locked=True),
    ]


def total_value(positions: list) -> float:
    return sum(p.balance_usd for p in positions)


def current_allocation(positions: list) -> dict:
    total = total_value(positions)
    if total == 0:
        return {p.protocol_id: 0.0 for p in positions}
    return {p.protocol_id: p.balance_usd / total for p in positions}
