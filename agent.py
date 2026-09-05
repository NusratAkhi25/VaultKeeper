"""
agent.py — VaultKeeper main loop.

Usage:
    python -m vaultkeeper.agent --config config.yaml --once
"""
import argparse
import yaml

from .positions import fetch_positions, current_allocation, total_value
from .policy import evaluate
from .actions import execute


def run_once(config: dict) -> None:
    positions = fetch_positions()
    allocation = current_allocation(positions)

    print(f"Portfolio value: ${total_value(positions):,.2f}")
    for protocol_id, weight in allocation.items():
        target = config["target_allocation"].get(protocol_id, 0.0)
        print(f"  {protocol_id}: {weight:.1%} (target {target:.1%})")

    plans = evaluate(positions, config)
    for plan in plans:
        execute(plan, dry_run=config["dry_run"])


def main():
    parser = argparse.ArgumentParser(description="VaultKeeper onchain workflow agent")
    parser.add_argument("--config", default="config.yaml")
    parser.add_argument("--once", action="store_true", help="run a single evaluation pass and exit")
    args = parser.parse_args()

    with open(args.config) as f:
        config = yaml.safe_load(f)

    run_once(config)


if __name__ == "__main__":
    main()
