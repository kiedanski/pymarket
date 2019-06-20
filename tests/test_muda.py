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
           [0  , 1 , 50 , -1 , False]  ,
           [1  , 1 , 50  , -1 , False]  ,
           [2  , 1 , 50  , -1 , False]  ,
           [3  , 1 , 50  , -1 , False]  ,
           [6  , 1 , 50  , -1 , False] ,
           [7  , 1 , 50  , -1 , False] ,
           [11 , 1 , 50  , -1 , False] ,
           [12 , 1 , 50  , -1 , False] ,
            ]
    # Exclude the active colum full of Nones
    data_trans = np.array(data_trans).astype(float)
    df2 = trans.get_df().values.astype(float)
    print(data_trans)
    print(df2)
    assert np.allclose(data_trans, df2)
