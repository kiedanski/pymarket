# -*- coding: utf-8 -*-
"""
Implements processing techniques applied to bids before
mechanisms can use them
"""
import numpy as np
import pandas as pd
from pymarket.bids import BidManager
from collections import OrderedDict


def new_player_id(index):
    """Helper function for merge_same_price.
    Creates a function that returns consecutive integers.

    Parameters
    -----------
    index: int
        First identifier to use for the
        new fake players

    Returns
    -------
    Callable : function
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
    new_player_id.index = index
    def new_id(users):
        """
        Generates a unique identifier for a
        list of users. If the list has
        only one user, then the id is mantained
        else, a new user id is created for the
        whole list.

        Parameters
        ----------
        users: list of int
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

        #nonlocal index
        if len(users) > 1:
            new_index = new_player_id.index
            new_player_id.index += 1
        else:
            new_index = users[0]

        return new_index

    return new_id


def merge_same_price(df, prec=5):
    """
    Process a collection of bids by merging in each
    side (buying or selling) all players with the same
    price into a new user with their aggregated quantity

    Parameters
    ----------
    df : pd.DataFrame
        Collection of bids to process
    prec: float
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

    Examples
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
       quantity    price  user  buying  time  divisible
    0       1.0  1.00000     5    True     0       True
    1       2.0  1.00000     2   False     0       True
    2       4.0  2.44445     6   False     0       True
    >>> index
    {0: [0, 1], 1: [2], 2: [3, 4]}


    >>> mar = pm.Market()
    >>> mar.accept_bid(250, 200, 0, True) # CleanRetail
    0
    >>> mar.accept_bid(300, 110, 1, True) # El4You
    1
    >>> mar.accept_bid(120, 100, 2, True) # EVcharge
    2
    >>> mar.accept_bid( 80,  90, 3, True) # QualiWatt
    3
    >>> mar.accept_bid( 40,  85, 4, True) # IntelliWatt
    4
    >>> mar.accept_bid( 70,  75, 1, True) # El4You
    5
    >>> mar.accept_bid( 60,  65, 0, True) # CleanRetail
    6
    >>> mar.accept_bid( 45,  40, 4, True) # IntelliWatt
    7
    >>> mar.accept_bid( 30,  38, 3, True) # QualiWatt
    8
    >>> mar.accept_bid( 35,  31, 4, True) # IntelliWatt
    9
    >>> mar.accept_bid( 25,  24, 0, True) # CleanRetail
    10
    >>> mar.accept_bid( 10,  21, 1, True) # El4You
    11

    >>> mar.accept_bid(120,   0, 5, False) # RT
    12
    >>> mar.accept_bid(50,    0, 6, False) # WeTrustInWind
    13
    >>> mar.accept_bid(200,  15, 7, False) # BlueHydro
    14
    >>> mar.accept_bid(400,  30, 5, False) # RT
    15
    >>> mar.accept_bid(60, 32.5, 8, False) # KøbenhavnCHP
    16
    >>> mar.accept_bid(50,   34, 8, False) # KøbenhavnCHP
    17
    >>> mar.accept_bid(60,   36, 8, False) # KøbenhavnCHP
    18
    >>> mar.accept_bid(100,37.5, 9, False) # DirtyPower
    19
    >>> mar.accept_bid(70,   39, 9, False) # DirtyPower
    20
    >>> mar.accept_bid(50,   40, 9, False) # DirtyPower
    21
    >>> mar.accept_bid(70,   60, 5, False) # RT
    22
    >>> mar.accept_bid(45,   70, 5, False) # RT
    23
    >>> mar.accept_bid(50,  100, 10, False) # SafePeak
    24
    >>> mar.accept_bid(60,  150, 10, False) # SafePeak
    25
    >>> mar.accept_bid(50,  200, 10, False) # SafePeak
    26
    >>> bids, index = pm.merge_same_price(mar.bm.get_df())
    >>> mar.bm.get_df()
        quantity  price  user  buying  time  divisible
    0        250  200.0     0    True     0       True
    1        300  110.0     1    True     0       True
    2        120  100.0     2    True     0       True
    3         80   90.0     3    True     0       True
    4         40   85.0     4    True     0       True
    5         70   75.0     1    True     0       True
    6         60   65.0     0    True     0       True
    7         45   40.0     4    True     0       True
    8         30   38.0     3    True     0       True
    9         35   31.0     4    True     0       True
    10        25   24.0     0    True     0       True
    11        10   21.0     1    True     0       True
    12       120    0.0     5   False     0       True
    13        50    0.0     6   False     0       True
    14       200   15.0     7   False     0       True
    15       400   30.0     5   False     0       True
    16        60   32.5     8   False     0       True
    17        50   34.0     8   False     0       True
    18        60   36.0     8   False     0       True
    19       100   37.5     9   False     0       True
    20        70   39.0     9   False     0       True
    21        50   40.0     9   False     0       True
    22        70   60.0     5   False     0       True
    23        45   70.0     5   False     0       True
    24        50  100.0    10   False     0       True
    25        60  150.0    10   False     0       True
    26        50  200.0    10   False     0       True



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
    user_to_bid = OrderedDict()
    for df_ in dataframes:
        rounded_prices = df_.price.apply(lambda x: np.round(x, prec))
        df_new = df_.groupby(rounded_prices).agg(agg_fun).reset_index()
        # print(df_new)
        df_new.user = df_new.user.apply(id_gen)
        #maping = df_new.set_index('user').bid.to_dict()
        # for k, v in maping.items():
        #    user_to_bid[k] = v

        dataframe_new.append(df_new)

    dataframe_new = pd.concat(dataframe_new).reset_index(drop=True)
    final_maping = dataframe_new.bid.to_dict()
    # print(final_maping)
    dataframe_new = dataframe_new[columns]
    # print('-------------')
    # print(dataframe_new)
    #index_to_user = dataframe_new.user.to_dict()

    #final_maping =
    # for k, v in index_to_user.items():
    #    final_maping[k] = user_to_bid[v]

    return dataframe_new, final_maping
