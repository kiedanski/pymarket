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

