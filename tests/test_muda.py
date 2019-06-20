from pymarket.transactions import TransactionManager
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


