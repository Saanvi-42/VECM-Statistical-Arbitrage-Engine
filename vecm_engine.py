import pandas as pd
from statsmodels.tsa.vector_ar.vecm import coint_johansen

from config import DET_ORDER, K_AR_DIFF


def fit_johansen(prices):
    """
    Fits the Johansen cointegration test and returns the
    primary cointegrating vector (hedge ratios) along with
    the estimated cointegration rank.
    """

    result = coint_johansen(
        prices,
        det_order=DET_ORDER,
        k_ar_diff=K_AR_DIFF
    )

    trace_stats = result.lr1
    critical_values = result.cvt[:, 1]  # 95% critical values

    rank = 0

    # Estimate cointegration rank
    for stat, critical in zip(trace_stats, critical_values):
        if stat > critical:
            rank += 1
        else:
            break

    if rank == 0:
        return None, 0

    # First cointegrating vector
    beta = result.evec[:, 0]

    # Normalize so the first asset has weight 1
    beta = beta / beta[0]

    return beta, rank


def compute_spread(prices, beta):
    """
    Constructs the stationary spread using the hedge ratios.
    """

    spread = prices.dot(beta)

    return pd.Series(
        spread,
        index=prices.index,
        name="Spread"
    )


def compute_zscore(spread, window=60):
    """
    Computes the rolling Z-score of the spread.
    """

    mean = spread.rolling(window).mean()
    std = spread.rolling(window).std(ddof=0)

    zscore = (spread - mean) / std

    return zscore


def generate_signal(zscore, entry=2.0):
    """
    Generates trading signals based on the Z-score.

    Returns:
        1  -> Long Spread
       -1  -> Short Spread
        0  -> No Position
    """

    if zscore > entry:
        return -1

    if zscore < -entry:
        return 1

    return 0