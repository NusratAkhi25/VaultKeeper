# VaultKeeper
**Binance Agent OS Mini Hackathon — Track A: Onchain Workflows**

VaultKeeper is an AI agent that automates **staking and DeFi allocation** — it monitors yield across a set of onchain positions (staking pools, vaults, liquidity positions), evaluates each against risk and target-allocation rules, and executes rebalancing actions automatically.

## What it does

1. **Position Monitor** — tracks a portfolio of onchain positions: current APY, TVL/liquidity depth, and lock-up status for each.
2. **Allocation Policy** — compares current allocation against target weights and risk limits (max per-protocol exposure, minimum APY threshold, minimum liquidity floor) to decide what needs to move.
3. **Onchain Actions** — executes the resulting plan — stake, unstake, claim rewards, or rebalance between protocols — via Agent OS / MCP onchain tool calls, gated behind a `dry_run` flag for safe demoing.

## Architecture

```
 ┌────────────────┐     ┌───────────────────┐     ┌──────────────────────┐
 │ Position Monitor│────▶│  Allocation Policy │────▶│  Onchain Action Layer│
 │ (APY, TVL, lock) │     │ (target weights,   │     │  (Agent OS / MCP)     │
 │                  │     │  risk limits)       │     │                       │
 └────────────────┘     └───────────────────┘     └──────────┬───────────┘
                                                                │
                              ┌─────────────────────────────────┼─────────────────────┐
                              ▼                                 ▼                      ▼
                        Stake into protocol           Unstake / withdraw       Claim + compound rewards
```

## Files

- `vaultkeeper/positions.py` — position data model + sample onchain position feed
- `vaultkeeper/policy.py` — target allocation, risk limits, and rebalance decision logic
- `vaultkeeper/actions.py` — Agent OS / MCP onchain action layer (paper-execute by default)
- `vaultkeeper/agent.py` — main loop wiring monitor → policy → actions
- `config.yaml` — target allocation weights, risk thresholds, dry-run toggle

## Running it

```bash
pip install -r requirements.txt
python -m vaultkeeper.agent --config config.yaml --once
```

`dry_run: true` by default — planned actions are logged as "[DRY RUN] would execute" instead of firing.

## Demo script (for the submission video)

1. Show `config.yaml` — target allocation across protocols (e.g. 40% Protocol A staking, 35% Protocol B vault, 25% Protocol C LP) and risk limits (min APY, max per-protocol exposure).
2. Run the agent against the sample position feed — show current vs. target allocation drift.
3. Walk through the log output: which positions are under/over target, and the resulting stake/unstake/rebalance plan.
4. Flip `dry_run: false` against a testnet to show one action actually firing.
5. Close on the architecture diagram, mapping each stage to an Agent OS onchain tool call.

## Why this fits Track A — Onchain Workflows

VaultKeeper is a minimal but complete staking/DeFi allocation loop: it doesn't just call a "stake" function on request, it *evaluates* a portfolio against policy and *decides* what onchain action is warranted — the same shape needed for any autonomous yield-management agent, with clear extension points for new protocols or risk rules.

## Roadmap (post-hackathon)

- Pull live APY/TVL data from real protocol subgraphs instead of the sample feed
- Add gas-cost-aware batching so small rebalances don't fire on every cycle
- Cross-wire with PayLoop so protocol fees or performance fees settle automatically after a rebalance
