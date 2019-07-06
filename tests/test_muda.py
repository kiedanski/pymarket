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
    trans, fees = solve_market_side_with_exogenous_price(df, price, fees)

    true_fees = np.array([0, 20, 10])
    assert np.allclose(true_fees, fees)

    data_trans = [
        [0, 1, 50, -1, False],
        [1, 1, 50, -1, False],
        [2, 1, 50, -1, False],
        [3, 1, 50, -1, False],
        [6, 1, 50, -1, False],
        [11, 1, 50, -1, False],
        [7, 1, 50, -1, False],
        [12, 1, 50, -1, False],
    ]
    # Exclude the active colum full of Nones
    data_trans = np.array(data_trans).astype(float)
    df2 = trans.get_df().values.astype(float)
    #print(data_trans)
    #print(df2)
    #assert 0 == 1
    assert np.allclose(data_trans, df2)


def test_muda_dataset_1(bid_dataset_1):
    """TODO: Testing muda with the splits

    Parameters
    ----------
    bid_dataset_1 : dataframe from conftest

    Returns
    -------

    """
    df = bid_dataset_1
    r = np.random.RandomState(1234)

    trans, extra = muda(df, r)

    fee = extra['fees']

    true_trans = np.array([
        [1, 1, 6.3, -1, False],
        [3, 1, 6.3, -1, False],
        [4, 1, 6.3, -1, False],
        [7, 1, 6.3, -1, False],
        [8, 2, 6.3, -1, False],
        [6, 1, 4.65, -1, False],
        [0, 1, 4.65, -1, False]]).astype(float)
    df = trans.get_df().values.astype(float)
    print(extra['left'], extra['right'])

    assert np.allclose(df, true_trans)
    
    left = [1, 3, 4, 7, 8, 9]
    right = [0, 2, 5, 6, 10]
    assert extra['left'] == left
    assert extra['right'] == right
    assert np.allclose(extra['price_left'], 4.65)
    assert np.allclose(extra['price_right'], 6.3)

    fees = np.array([1.85, 0, 0, 0, 0, 0, 0, 2.3, 4.6, 0, 0])
    assert np.allclose(fees, fee)

