import pandas as pd
import numpy as np

from pymarket import Market
from pymarket.transactions import TransactionManager, split_transactions_merged_players
from pymarket.bids.processing import merge_same_price
from pymarket.mechanisms.muda_auction import solve_market_side_with_exogenous_price


def test_split_transactions():
    """
    Test the reconstruction
    of the transaction list
    of a merged bids dataframe
    """

    mar = Market()

    mar.bm.add_bid(1, 100, 0, True, 0)
    mar.bm.add_bid(3, 100, 1, True, 0)
    mar.bm.add_bid(2.3, 85, 2, True, 0)
    mar.bm.add_bid(2.1, 90, 7, True, 0)
    mar.bm.add_bid(0.4, 90, 8, True, 0)

    mar.bm.add_bid(0.5, 90, 4, False, 0)
    mar.bm.add_bid(4.2, 1, 5, False, 0)
    mar.bm.add_bid(0.1, 90, 6, False, 0)

    df = mar.bm.get_df()
    df_, maping = merge_same_price(df)

    trans, fee = solve_market_side_with_exogenous_price(df_, 95, np.arange(df_.shape[0] + 1))

    new_trans = split_transactions_merged_players(trans, df, maping)

    X_obtained = new_trans.get_df().sort_values('bid').values.astype('float')

    X_true = np.array([
        [0, 1, 95, -1, False],
        [1, 3, 95, -1, False],
        [6, 4, 95, -1, False]
    ]).astype(float)

    assert np.allclose(X_obtained, X_true)
