import pytest
from pymarket.bids import BidManager


@pytest.fixture(scope='module')
def bid_dataset_0():
    """
    Simple bid dataset in which demand intersects supply
    """

    bm = BidManager()
    bm.add_bid(1, 3, 0, True, 0)
    bm.add_bid(2, 4, 1, True, 0)
    bm.add_bid(5, 1, 2, True, 0)

    bm.add_bid(4, 2, 3, False, 0)
    bm.add_bid(1, 1, 4, False, 0)
    bm.add_bid(5, 6, 5, False, 0)
        
    return bm.get_df()


@pytest.fixture(scope='module')
def bidlist_dataset_0():
    """
    Simple bid dataset made of bid of lists.
    Same as `bid_dataset_0` in which demand intersects supply
    """

    bm = BidManager()
    bm.add_bid(1, 3, 0, True, 0)
    bm.add_bid(2, 4, 1, True, 0)
    bm.add_bid(5, 1, 2, True, 0)

    bm.add_bid(4, 2, 3, False, 0)
    bm.add_bid(1, 1, 4, False, 0)
    bm.add_bid(5, 6, 5, False, 0)
    
    return bm.get_df()

@pytest.fixture(scope='module')
def bid_dataset_1():
    """
    Larger test case, supply intersects demand
    """

    bm = BidManager()

    bm.add_bid(1, 6.7, 0, True, 0)
    bm.add_bid(1, 6.6, 1, True, 0)
    bm.add_bid(1, 6.5, 2, True, 0)
    bm.add_bid(1, 6.4, 3, True, 0)
    bm.add_bid(1, 6.3, 4, True, 0)
    bm.add_bid(1, 6, 5, True, 0)

    bm.add_bid(1, 1, 6, False, 0)
    bm.add_bid(1, 2, 7, False, 0)
    bm.add_bid(2, 3, 8, False, 0)
    bm.add_bid(2, 4, 9, False, 0)
    bm.add_bid(1, 6.1, 10, False, 0)
    
    return bm.get_df()

@pytest.fixture(scope='module')
def bid_dataset_muda_example_1():
    """Simple example with 3 biders as described
    in the MUDA paper
    Returns
    -------
    df : pandas.DataFrame
        dataframe with all the bids

    """
    bm = BidManager()
    bm.add_bid(1, 100, 0, True, 0)
    bm.add_bid(1, 90, 0, True, 0)
    bm.add_bid(1, 80, 0, True, 0)
    bm.add_bid(1, 60, 0, True, 0)
    bm.add_bid(1, 40, 0, True, 0)
    bm.add_bid(1, 20, 0, True, 0)

    bm.add_bid(1, 10, 1, False, 0)
    bm.add_bid(1, 20, 1, False, 0)
    bm.add_bid(1, 40, 1, False, 0)
    bm.add_bid(1, 60, 1, False, 0)
    bm.add_bid(1, 70, 1, False, 0)
    
    bm.add_bid(1, 15, 2, False, 0)
    bm.add_bid(1, 25, 2, False, 0)
    bm.add_bid(1, 35, 2, False, 0)
    bm.add_bid(1, 45, 2, False, 0)
    bm.add_bid(1, 65, 2, False, 0)
    
    return bm.get_df()


@pytest.fixture(scope='module')
def bid_dataset_3():
    
    bm = BidManager()
    bm.add_bid(1   , 6 , 0 , True , 0)
    bm.add_bid(0.1 , 5 , 1 , True , 0)
    bm.add_bid(1.9 , 4 , 2 , True , 0)
    bm.add_bid(1   , 3 , 3 , True , 0)

    bm.add_bid(1   , 1   , 4 , False , 0)
    bm.add_bid(1.5 , 2   , 5 , False , 0)
    bm.add_bid(1   , 2.5 , 6 , False , 0)
    bm.add_bid(1   , 4   , 7 , False , 0)

    return bm.get_df()
