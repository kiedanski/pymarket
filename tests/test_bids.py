import pytest
import pandas as pd
import numpy as np
from pymarket.bids import BidManager
from pymarket.bids.processing import merge_same_price


def test_bids(bid_dataset_0):
    """
    Check that the bid_dataset_0
    is exactly as expected
    """
    df = bid_dataset_0
    
    data = [
      [ 1 , 3 , 0 , True  , 0 , True],
      [ 2 , 4 , 1 , True  , 0 , True],
      [ 5 , 1 , 2 , True  , 0 , True],
      [ 4 , 2 , 3 , False , 0 , True],
      [ 1 , 1 , 4 , False , 0 , True],
      [ 5 , 6 , 5 , False , 0 , True],
            ]
    columns = ['quantity', 'price', 'user', 'buying', 'time', 'divisible']
    df2 = pd.DataFrame(data, columns=columns)

    assert df2.equals(df)


def test_merge_same_price():
    """    Test the merge_same_price
    functionalty with repeated
    price in both sides and equal
    price for the repated price.
    """

    bm = BidManager()

    bm.add_bid(1, 100, 0, True, 0)
    bm.add_bid(3, 100, 1, True, 0)
    bm.add_bid(2.3, 85, 2, True, 0)
    bm.add_bid(2.1, 90, 7, True, 0)
    bm.add_bid(0.4, 90, 8, True, 0)

    bm.add_bid(0.5, 90, 4, False, 0)
    bm.add_bid(4.2, 1, 5, False, 0)
    bm.add_bid(0.1, 90, 6, False, 0)
    df = bm.get_df()

    df_new, maping = merge_same_price(df)

    X_original = np.array([
        [2.3, 85, 2, True, 0, True],
        [4.2, 1, 5, False, 0, True],
        [2.5, 90, 9, True, 0, True],
        [4, 100, 10, True, 0, True],
        [0.6, 90, 11, False, 0, True],
    ]).astype(float)
    
    maping_original = {
        0: [2], 1: [3, 4], 2: [0, 1], 3: [6], 4: [5, 7]
    }

    X_new = df_new.sort_values('user').values.astype(float)

    assert np.allclose(X_original, X_new)
    for k in maping_original:
        assert maping_original[k] == maping[k]