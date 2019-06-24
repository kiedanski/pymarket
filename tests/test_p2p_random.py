import numpy as np
from pymarket.bids import *
from pymarket.transactions import *

from pymarket.mechanisms import p2p_random


def test_p2p_random_dataset_0(bid_dataset_0):
    """ Tests the p2p-random mechanisms in the dataset
    0 with several possible orders

    Order of trading:

    Seed = 1234
    Round 0 :
        1-3 : q=2, p=3
        2-4 : q=1, p=1
        0-5 : q=0, p=0
    Round 1 :
        2-3 : q=0, p=0
    Round 2 :
        0-3 : q=1, p=2.5
        2-5 : q=0, p=0 

    Parameters
    ----------
    bid_dataset_0 : dataframe created from the bid_0 dataset

    Returns
    -------
    

    """
    df = bid_dataset_0
    r = np.random.RandomState(1234)
    trans, extra = p2p_random(df, r=r)

    trading_list = [
            [(1 , 3)  , (2 , 4)  , (0 , 5)] ,
            [(2 , 3)] ,
            [(0 , 3)  , (2 , 5)]
            ]

    assert trading_list == extra['trading_list']

    true_trans = [[1, 2, 3.0, 3, False],
             [3, 2, 3.0, 1, True],
            [2, 1, 1.0, 4, True],
             [4, 1, 1.0, 2, False],
             [0, 0, 0.0, 5, True],
             [5, 0, 0.0, 0, True],
             [2, 0, 0.0, 3, True],
             [3, 0, 0.0, 2, True],
             [0, 1, 2.5, 3, False],
             [3, 1, 2.5, 0, True],
             [2, 0, 0.0, 5, True],
             [5, 0, 0.0, 2, True],]

    true_trans = np.array(true_trans).astype(float)
    
    df = trans.get_df().values.astype(float)
    assert np.allclose(df, true_trans)

