import pandas as pd

from vecm_engine import (
    fit_johansen,
    compute_spread,
    compute_zscore,
    generate_signal
)

from config import LOOKBACK, ENTRY_Z


def build_strategy(prices):
    # Estimate the hedge ratios
    beta, rank = fit_johansen(prices)

    if rank == 0:
        raise ValueError("The selected basket is not cointegrated.")

    # Build the spread
    spread = compute_spread(prices, beta)

    # Standardise it
    zscore = compute_zscore(
        spread,
        window=LOOKBACK
    )

    # Convert z-scores into trading signals
    signals = zscore.apply(
        lambda z: generate_signal(
            z,
            entry=ENTRY_Z
        )
        if pd.notna(z)
        else 0
    )

    strategy = pd.DataFrame(index=prices.index)

    strategy["Spread"] = spread
    strategy["ZScore"] = zscore
    strategy["Signal"] = signals

    return strategy, beta