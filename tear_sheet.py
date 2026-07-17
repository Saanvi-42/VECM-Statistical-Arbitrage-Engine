import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Read the daily PnL from the backtest
pnl = pd.read_csv(
    "pnl.csv",
    index_col=0,
    parse_dates=True
).squeeze()

# Running total of profits
cumulative = pnl.cumsum()

# Rolling Sharpe ratio over 60 trading days
rolling_sharpe = (
    pnl.rolling(60).mean()
    / pnl.rolling(60).std()
) * np.sqrt(252)

# Drawdown
running_max = cumulative.cummax()
drawdown = cumulative - running_max

print("\nPerformance Summary")
print("-" * 30)

print(f"Total Return : {round(cumulative.iloc[-1], 2)}")

if pnl.std() != 0:
    sharpe = pnl.mean() / pnl.std() * np.sqrt(252)
    print(f"Sharpe Ratio: {round(sharpe, 2)}")

print(f"Max Drawdown: {round(drawdown.min(), 2)}")

# Create the charts
fig, axes = plt.subplots(3, 1, figsize=(12, 10))

# Cumulative returns
axes[0].plot(cumulative, color="green")
axes[0].set_title("Cumulative PnL")
axes[0].set_ylabel("PnL")
axes[0].grid(alpha=0.3)

# Rolling Sharpe
axes[1].plot(rolling_sharpe, color="royalblue")
axes[1].set_title("Rolling Sharpe Ratio")
axes[1].set_ylabel("Sharpe")
axes[1].grid(alpha=0.3)

# Drawdown
axes[2].fill_between(
    drawdown.index,
    drawdown,
    0,
    color="firebrick",
    alpha=0.35
)

axes[2].set_title("Drawdown")
axes[2].set_ylabel("PnL")
axes[2].grid(alpha=0.3)

plt.tight_layout()

plt.savefig("tear_sheet.png", dpi=300)

plt.show()

print("\nSaved tear_sheet.png")