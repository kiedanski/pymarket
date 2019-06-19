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
    
    df = bm.get_df()
    return df

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
    bm.add_bid(1.1, 4, 9, False, 0)
    bm.add_bid(1, 6.1, 10, False, 0)
    
    df = bm.get_df()
    return df
