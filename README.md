# VECM Statistical Arbitrage Engine

## Overview

This project implements a statistical arbitrage engine using a Vector Error Correction Model (VECM). The engine identifies groups of cointegrated stocks, builds a mean reversion trading strategy, backtests it on historical market data, and generates a performance report.

The project uses historical stock prices downloaded from Yahoo Finance and applies the Johansen cointegration test to find baskets of stocks that share a long term relationship. A trading strategy is then created using the spread and its Z-score.

## Features

- Downloads historical stock price data using Yahoo Finance
- Finds cointegrated stock baskets using the Johansen cointegration test
- Selects the strongest basket based on cointegration rank and trace statistic
- Builds a VECM-based spread using hedge ratios
- Generates trading signals using Z-score thresholds
- Backtests the strategy on historical data
- Produces performance metrics and a visual tear sheet

## Project Structure

 config.py               # Project configuration and parameters
 download_data.py        # Downloads historical stock prices
 basket_selector.py      # Finds cointegrated stock baskets
 vecm_engine.py          # VECM and spread calculations
 strategy.py             # Builds the trading strategy
 backtester.py           # Runs the backtest
 tear_sheet.py           # Generates performance charts
 requirements.txt        # Python dependencies
 README.md

├── prices.csv                # Downloaded price data
├── selected_basket.csv       # Selected cointegrated basket
├── pnl.csv                   # Daily profit and loss
└── tear_sheet.png            # Performance report

## Requirements

Install the required libraries using:
pip install -r requirements.txt


Required packages:

- numpy
- pandas
- matplotlib
- statsmodels
- yfinance

## How to Run

### Step 1: Download historical data
python download_data.py
This downloads historical stock prices and saves them as `prices.csv`.

### Step 2: Run the backtest
python backtester.py


This will:

- Find all valid cointegrated baskets
- Select the best basket
- Build the trading strategy
- Run the backtest
- Save the daily PnL as `pnl.csv`

### Step 3: Generate the performance report
python tear_sheet.py
This creates a performance summary and saves the charts as `tear_sheet.png`.
## Methodology

The project follows these steps:

1. Download historical stock prices.
2. Generate every possible basket of three stocks.
3. Apply the Johansen cointegration test to each basket.
4. Select the basket with the highest cointegration rank. If multiple baskets have the same rank, the Johansen trace statistic is used as a tie-breaker.
5. Estimate normalized hedge ratios from the first Johansen cointegrating eigenvector.
6. Compute the spread for the selected basket.
7. Calculate the rolling Z-score of the spread.
8. Generate buy and sell signals based on the Z-score.
9. Backtest the trading strategy.
10. Evaluate performance using cumulative PnL, rolling Sharpe ratio, and drawdown.

## Trading Strategy

The strategy assumes that the spread between cointegrated stocks tends to revert to its historical average.

Trading rules:

- Enter a long spread position when the Z-score falls below -2.
- Enter a short spread position when the Z-score rises above +2.
- Exit the trade when the absolute Z-score falls below 0.5.

## Output Files

| File | Description |
|------|-------------|
| prices.csv | Historical stock prices |
| selected_basket.csv | Selected cointegrated basket |
| pnl.csv | Daily profit and loss from the backtest |
| tear_sheet.png | Performance charts |

## Performance Metrics

The backtest reports:

- Total Profit and Loss (PnL)
- Sharpe Ratio
- Winning Days
- Losing Days
- Win Rate
- Maximum Drawdown

The tear sheet visualizes cumulative PnL, rolling Sharpe ratio, and drawdown over time.

## Limitations

- Historical data is downloaded from Yahoo Finance and updates over time, so results may vary slightly between runs.
- Transaction costs are simplified.
- The strategy uses fixed entry and exit thresholds.
- The project is intended for educational purposes and is not investment advice.


## Future Improvements

Some possible extensions include:

- Dynamic position sizing
- Portfolio optimization
- Walk-forward validation
- Additional risk management techniques
- More advanced basket selection methods
- Live market data integration

## Author

Developed as a statistical arbitrage project demonstrating the application of VECM, cointegration analysis, and quantitative trading concepts.