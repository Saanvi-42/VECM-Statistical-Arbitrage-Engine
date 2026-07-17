import pandas as pd
from itertools import combinations
from statsmodels.tsa.vector_ar.vecm import coint_johansen

from config import DET_ORDER, K_AR_DIFF, BASKET_SIZE


def find_cointegrated_baskets(prices, basket_size=BASKET_SIZE):
    # Stores every basket that passes the Johansen test
    valid_baskets = []

    stocks = list(prices.columns)

    # Try every possible combination
    for basket in combinations(stocks, basket_size):

        sample = prices[list(basket)]

        try:
            result = coint_johansen(
                sample,
                det_order=DET_ORDER,
                k_ar_diff=K_AR_DIFF
            )

            rank = 0

            # Compare the trace statistic against the 95% critical values
            for stat, critical in zip(result.lr1, result.cvt[:, 1]):
                if stat > critical:
                    rank += 1
                else:
                    break

            if rank > 0:
                valid_baskets.append({
                    "stocks": basket,
                    "rank": rank,
                    "trace_stat": float(result.lr1[0]),
                    "max_eigen_stat": float(result.lr2[0])
                })

        # Ignore baskets that fail because of numerical issues
        except Exception:
            continue

    return valid_baskets


def choose_best_basket(valid_baskets):
    if len(valid_baskets) == 0:
        return None

    # Highest rank first, then strongest trace statistic
    valid_baskets.sort(
        key=lambda x: (
            x["rank"],
            x["trace_stat"]
        ),
        reverse=True
    )

    return valid_baskets[0]