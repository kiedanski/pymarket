"""
Implements processing techniques applied to bids before
mechanisms can use them
"""
import numpy as np
import pandas as pd
from typing import Callable, List
from pymarket.bids import BidManager


def new_player_id(index : int) -> Callable[[List[int]], int]:
    """Helper function for
    merge_same_price
    Creates a function that returns consecutive integers.
    
    Paramters
    -----------
    index
        First identifier to use for the
        new fake players

    Returns
    -------
    Callable
        Function that maps a list
        of user ids into a new user id.

    Examples
    ----------
    >>> id_gen = new_player_id(6)
    >>> id_gen([3])
    3
    >>> id_gen([5])
    5 
    >>> id_gen([0, 1])
    6
    >>> id_gen([2, 4])
    7

    """

    def new_id(users: List[int]) -> int:
        """
        Generates a unique identifier for a
        list of users. If the list has
        only one user, then the id is mantained
        else, a new user id is created for the 
        whole list.
        
        Paramters
        ----------
        users
            List of 1 or more user's identifiers.
            Precondition: all elements of users
            are smaller than index.
        Returns
        -------
        int
            The old identifier if in the list
            there was only one player
            and or the next new consecutive
            identifier if there where more
            than one.

        """
        nonlocal index
        if len(users) > 1:
            new_index = index
            index += 1
        else:
            new_index = users[0]

        return new_index

    return new_id


def merge_same_price(df : pd.DataFrame, prec: float=5) -> pd.DataFrame:
    """
    Process a collection of bids by merging in each
    side (buying or selling) all players with the same
    price into a new user with their aggregated quantity

    Parameters
    ----------
    df
        Collection of bids to process
    prec
        Number of digits to use after the comma
        while comparing floating point prices
        as equal.

    Returns
    -------
    dataframe_new: pd.DataFrame
        The new collection of bids where
        players with the same price have
        been merged into one.
    
    final_maping : dict
        Maping from new bids index to the
        old bids index.

    Exampels
    ---------
    >>> bm = BidManager()
    >>> bm.add_bid(0.3, 1, 0)
    0
    >>> bm.add_bid(0.7, 1, 1)
    1
    >>> bm.add_bid(2, 1, 2, False)
    2
    >>> bm.add_bid(1, 2.444446, 3, False)
    3
    >>> bm.add_bid(3, 2.444447, 4, False)
    4
    >>> bm.get_df()
        quantity     price  user  buying  time  divisible
    0       0.3  1.000000     0    True     0       True
    1       0.7  1.000000     1    True     0       True
    2       2.0  1.000000     2   False     0       True
    3       1.0  2.444446     3   False     0       True
    4       3.0  2.444447     4   False     0       True
    >>> bids, index = pm.merge_same_price(bm.get_df(), 5)
    >>> bids
        quantity     price  user  buying  time  divisible
    0       1.0  1.00000     5    True     0       True
    1       2.0  1.00000     2   False     0       True
    2       4.0  2.44445     6   False     0       True
    >>> index
    {0: [0, 1], 1: [2], 2: [3, 4]}
    
    """

    id_gen = new_player_id(df.user.max() + 1)
    columns = df.columns.copy()

    df = df.copy().reset_index().rename(columns={'index': 'bid'})

    buy = df.loc[df['buying'], :]
    sell = df.loc[~df['buying'], :]

    dataframes = [buy, sell]

    agg_fun = {
        'bid': list,
        'user': list,
        'quantity': sum,
        'buying': lambda x: x.sample(1),
        'time': lambda x: x.sample(1),
        'divisible': lambda x: x.sample(1),
    }

    dataframe_new = []
    user_to_bid = {}
    for df_ in dataframes:
        rounded_prices = df_.price.apply(lambda x: np.round(x, prec))
        df_new = df_.groupby(rounded_prices).agg(agg_fun).reset_index()
        df_new.user = df_new.user.apply(id_gen)
        maping = df_new.set_index('user').bid.to_dict()
        for k, v in maping.items():
            user_to_bid[k] = v

        dataframe_new.append(df_new)

    dataframe_new = pd.concat(dataframe_new)[columns].reset_index(drop=True)
    index_to_user = dataframe_new.user.to_dict()

    final_maping = {}
    for k, v in index_to_user.items():
        final_maping[k] = user_to_bid[v]

    return dataframe_new, final_maping
