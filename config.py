# Everything that might change is kept here.
# This makes the rest of the project much easier to maintain.

# Stocks we want to analyse
STOCKS = [
    "AAPL",
    "MSFT",
    "GOOGL",
    "META",
    "NVDA",
    "AMD",
    "AVGO",
    "QCOM"
]

# How much historical data to download
PERIOD = "5y"
# Number of stocks in each basket
BASKET_SIZE = 3

# Johansen test settings
DET_ORDER = 0
K_AR_DIFF = 1

# Strategy settings
LOOKBACK = 60
ENTRY_Z = 2.0
EXIT_Z = 0.5

# Backtest settings
STARTING_CAPITAL = 100000
TRANSACTION_COST = 0.001