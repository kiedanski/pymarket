import pytest
import pandas as pd
from pymarket.bids import BidManager


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

