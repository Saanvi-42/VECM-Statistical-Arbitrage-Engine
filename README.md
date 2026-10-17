# VECM Statistical Arbitrage Engine

## Overview

## What this project does

Prices of some stocks in the market are often times linked to one another, 
in a way where one cannot rise or fall at the expense of the other. They 
form a relationship that can be mathematically expressed. This engine finds 
out the relations (if there exist any) among a given set of stocks, and gives 
us a mathematical equation in which all stocks are linked via coefficients. 
The result of that expression is a value we expect to stay within a normal 
range, and if it drifts more than 2 standard deviations away from its average, 
we bet on it resetting back.

## Why VECM over simple pairs trading

Despite the mathematical relation we might find between two stocks, exceptional 
cases may exist. Cases where one company receives specific news — like a fraud 
scandal or major acquisition — which may cause its stock to permanently move 
away from the other. In such a case, our bet fails because the relationship 
actually broke, and did not just temporarily drift.

The 6 stock engine functions such that, even if one relationship breaks or one 
stock goes rogue, our net profit still exists because we benefit from the other 
relationships.

## Why these stocks

I chose these 6 stocks because they fall into two natural groups that share 
the same economic environment.

AAPL, MSFT and GOOGL are all tech companies. They are affected by the same 
market cycles, same consumer trends and same regulatory environment. This makes 
it likely that a long run relationship exists between them.

JPM, GS and BAC are all banks. They are all affected by the same Federal Reserve 
interest rate decisions, same economic cycles and same lending environment.

Splitting into two sector groups also reduces the risk of a relationship breaking 
down, since stocks within the same sector are more likely to be cointegrated than 
stocks across different sectors.
## System Architecture

![System Architecture](architecture.png)

## Features

a. Downloads historical stock price data from Yahoo Finance.

b. Tests different stock baskets for cointegration using the Johansen test.

c. Selects the strongest basket based on the cointegration rank and trace statistic.

d. Constructs a spread using the estimated hedge ratios.

e. Generates buy and sell signals using the spread's Z-score.

f. Backtests the trading strategy.

g. Generates performance metrics and a tear sheet.


## Project Structure
.
├── config.py
├── download_data.py
├── basket_selector.py
├── vecm_engine.py
├── strategy.py
├── backtester.py
├── tear_sheet.py
├── requirements.txt
├── README.md
├── prices.csv
├── basket_results.csv
├── selected_basket.csv
├── pnl.csv
└── tear_sheet.png

## Requirements

Install the required libraries using:
pip install -r requirements.txt


Required packages:

a. numpy

b. pandas

c. matplotlib

d. statsmodels

e. yfinance

## Running the Project

1] Download historical data
python download_data.py

This downloads historical stock prices and stores them in `prices.csv`.

2] Run the backtest
python backtester.py

This script:

a. Finds all valid cointegrated baskets.

b. Selects the strongest basket.

c. Builds the trading strategy.

d. Runs the backtest.

e. Saves the daily PnL as `pnl.csv`.

3] Generate the performance report
python tear_sheet.py

This creates the performance summary and saves the charts as `tear_sheet.png`.

## Methodology

The implementation follows these steps:

a. Download historical stock prices.

b. Generate all possible three-stock baskets.

c. Apply the Johansen cointegration test to every basket.

d. Select the basket with the highest cointegration rank. If more than one basket has the same rank, the trace statistic is used as a tie-breaker.

e. Estimate the hedge ratios using the first cointegrating eigenvector.

f. Construct the spread.

g. Calculate the rolling Z-score of the spread.

h. Generate trading signals.

i. Backtest the strategy.

j. Evaluate the results using cumulative PnL, Sharpe ratio and drawdown.

## Trading Strategy

The strategy assumes that the spread between cointegrated stocks is mean reverting.

The trading rules are simple:

a. Go long when the Z-score falls below -2.

b. Go short when the Z-score rises above +2.

c. Exit the position when the absolute Z-score becomes smaller than 0.5.

## Output Files

| File | Description |
|------|-------------|
| prices.csv | Historical stock prices |
| basket_results.csv | Cointegration statistics for valid baskets |
| selected_basket.csv | Selected basket used in the strategy |
| pnl.csv | Daily profit and loss |
| tear_sheet.png | Performance charts |

## Performance Metrics

The backtest reports the following metrics:

a. Total Profit and Loss (PnL)

b. Sharpe Ratio

c. Winning Days

d. Losing Days

e. Win Rate

f. Maximum Drawdown

The tear sheet also provides plots of cumulative PnL, rolling Sharpe ratio and drawdown.

## Limitations

This project is a simplified implementation of a statistical arbitrage strategy.

Some limitations are:

a. Results depend on the historical data available from Yahoo Finance.

b. Transaction costs are modeled in a simplified manner.

c. Fixed entry and exit thresholds are used throughout the backtest.

d. Position sizing and risk management are kept simple.

## License

This project was developed for educational purposes. demonstrating the application of VECM, cointegration analysis, and quantitative trading concepts.
