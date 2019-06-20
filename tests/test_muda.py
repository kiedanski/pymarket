from pymarket.transactions import TransactionManager
from pymarket.mechanisms import *
import numpy as np


def test_example_1(bid_dataset_muda_example_1):
    """Test the example 1 presented in the MUDA
    paper

    Parameters
    ----------
    bid_dataset_muda_example_1 : Dataframe
        dataset with 3 biders from conftest

    Returns
    -------

    """
    df = bid_dataset_muda_example_1
    r = np.random.RandomState(1234)
    
    fees = np.zeros(df.user.unique().shape[0])
    trans = TransactionManager()
    price = 50
    trans, fees = solve_market_side_with_exogenous_price(df, price, trans, fees, r)

    true_fees = np.array([0, 20, 10])
    assert np.allclose(true_fees, fees)

    data_trans = [
           [0  , 1 , 100 , -1 , True]  ,
           [1  , 1 , 90  , -1 , True]  ,
           [2  , 1 , 80  , -1 , True]  ,
           [3  , 1 , 60  , -1 , True]  ,
           [6  , 1 , 10  , -1 , False] ,
           [7  , 1 , 20  , -1 , False] ,
           [11 , 1 , 15  , -1 , False] ,
           [12 , 1 , 25  , -1 , False] ,
            ]
    # Exclude the active colum full of Nones
    assert np.allclose(data_trans[:, :-1], trans.get_df().values[:, :-1])
