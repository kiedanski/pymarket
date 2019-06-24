from pymarket.mechanisms import *
from pymarket.bids import *
from pymarket.transactions import *

def test_huang_auction_with_dataset_0(bid_dataset_0):
    """Test the huang auction with dataset 0

    Parameters
    ----------
    bid_dataset_0 : TODO

    Returns
    -------
    TODO

    """

    df = bid_dataset_0
    trans, extra = huang_auction(df)
    
    df = trans.get_df().sort_values('bid').values.astype(float)

    true_trans = np.array([
        [1, 1, 3, -1, False],
        [4, 1, 2, -1, False]
        ]).astype(float)

    assert np.allclose(true_trans, df)

def test_huang_auction_with_dataset_3(bid_dataset_3):
    """Test the huang auction with dataset 3

    Parameters
    ----------
    bid_dataset_3 : TODO

    Returns
    -------
    TODO

    """

    df = bid_dataset_3
    trans, extra = huang_auction(df)
    
    df = trans.get_df().sort_values('bid').values.astype(float)

    true_trans = np.array([
        [0 , 0.8 , 3   , -1 , False] ,
        [1 , 0   , 3   , -1 , False] ,
        [2 , 1.7 , 3   , -1 , False] ,
        [4 , 1   , 2.5 , -1 , False] ,
        [5 , 1.5 , 2.5 , -1 , False]
        ]).astype(float)

    assert np.allclose(true_trans, df)
