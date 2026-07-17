import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

from config import STOCKS, PERIOD


print("Downloading historical prices...\n")

# Download adjusted closing prices
prices = yf.download(
    STOCKS,
    period=PERIOD,
    auto_adjust=True,
    progress=True,
    threads=False
)["Close"]

# Remove any dates where one or more stocks are missing
prices = prices.dropna()

# Save for the rest of the project
prices.to_csv("prices.csv")

print("Download complete.")
print(f"Rows: {len(prices)}")
print(f"Columns: {len(prices.columns)}\n")

print(prices.head())

# Plot everything on the same scale
normalised = prices / prices.iloc[0]

plt.figure(figsize=(12, 6))

for stock in STOCKS:
    plt.plot(normalised.index, normalised[stock], label=stock)

plt.title("Normalised Stock Prices")
plt.xlabel("Date")
plt.ylabel("Price (Normalised)")
plt.legend()
plt.grid(alpha=0.3)

plt.tight_layout()
plt.show()