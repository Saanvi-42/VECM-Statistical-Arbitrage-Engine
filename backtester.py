import numpy as np
import pandas as pd

from basket_selector import find_cointegrated_baskets, choose_best_basket
from strategy import build_strategy
from config import EXIT_Z, TRANSACTION_COST


# Load the historical prices
prices = pd.read_csv(
    "prices.csv",
    index_col=0,
    parse_dates=True
)

prices = prices.dropna()

print("Looking for cointegrated baskets...\n")

# Find every basket that passes the Johansen test
baskets = find_cointegrated_baskets(prices)

print(f"Checked baskets: {len(baskets)} found\n")

# Save all basket results
basket_results = pd.DataFrame(baskets)

basket_results["stocks"] = basket_results["stocks"].apply(
    lambda x: ", ".join(x)
)

basket_results.to_csv("basket_results.csv", index=False)

# Display all candidate baskets
for i, basket in enumerate(baskets, start=1):
    print(
        f"{i}. {basket['stocks']}"
        f"\n   Rank            : {basket['rank']}"
        f"\n   Trace Statistic : {basket['trace_stat']:.2f}"
        f"\n   Max Eigen Stat  : {basket['max_eigen_stat']:.2f}\n"
    )

if len(baskets) == 0:
    raise ValueError("No cointegrated baskets were found.")

# Pick the best one
best = choose_best_basket(baskets)

pd.DataFrame(
    {
        "Stock": best["stocks"]
    }
).to_csv("selected_basket.csv", index=False)

print("Selected basket:")
print(best["stocks"])
print(f"Cointegration Rank : {best['rank']}")
print(f"Trace Statistic    : {best['trace_stat']:.2f}")
print(f"Max Eigen Statistic: {best['max_eigen_stat']:.2f}\n")

# Keep only the selected stocks
basket_prices = prices[list(best["stocks"])]

# Build the trading strategy
strategy, beta = build_strategy(basket_prices)

position = 0

daily_pnl = []
trade_dates = []

for i in range(1, len(strategy)):

    today = strategy.iloc[i]
    yesterday = strategy.iloc[i - 1]

    pnl = 0

    signal = today["Signal"]

    # Open a trade
    if position == 0:

        if signal == 1:
            position = 1

        elif signal == -1:
            position = -1

    # Long spread
    elif position == 1:

        pnl = today["Spread"] - yesterday["Spread"]

        if abs(today["ZScore"]) < EXIT_Z:
            pnl -= TRANSACTION_COST
            position = 0

    # Short spread
    elif position == -1:

        pnl = yesterday["Spread"] - today["Spread"]

        if abs(today["ZScore"]) < EXIT_Z:
            pnl -= TRANSACTION_COST
            position = 0

    daily_pnl.append(pnl)
    trade_dates.append(strategy.index[i])

# Save results
pnl = pd.Series(
    daily_pnl,
    index=trade_dates,
    name="PnL"
)

pnl.to_csv("pnl.csv")

print("Backtest finished.\n")

print(f"Total PnL: {round(pnl.sum(), 2)}")

if pnl.std() != 0:
    sharpe = pnl.mean() / pnl.std() * np.sqrt(252)
    print(f"Sharpe Ratio: {round(sharpe, 2)}")

wins = (pnl > 0).sum()
losses = (pnl < 0).sum()

print(f"Winning days: {wins}")
print(f"Losing days: {losses}")

if wins + losses > 0:
    print(f"Win Rate: {round(wins / (wins + losses) * 100, 1)}%")