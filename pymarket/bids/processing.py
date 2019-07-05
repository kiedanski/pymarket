"""
Implements processing techniques applied to bids before
mechanisms can use them
"""
import numpy as np
import pandas as pd
from pymarket.bids import BidManager


def new_player_id(index):
    """Helper function for
    merge_same price
    Maps list of one user to
    the exact user and list of several
    users to a new value
    
    Paramters
    -----------
    index: int
        First identifier to use for the
        new fake players

    Parameters
    ----------
    index :
        

    Returns
    -------

    
    """

    def new_id(users):
        """Maps a list of users
        to the only value if the length
        is 1, or to the current value of the
        closured index
        
        Paramters
        ----------
        users: list
            list of user indentifiers
        
        Returns:
        new_index: int
            The new index to use

        Parameters
        ----------
        users :
            

        Returns
        -------

        
        """
        nonlocal index
        if len(users) > 1:
            new_index = index
            index += 1
        else:
            new_index = users[0]

        return new_index
    return new_id


def merge_same_price(df : pd.DataFrame, prec=5):
    """Takes a bid where there are two players
    in the same side of the market with the same
    price and merges them into a new player with
    aggregated quantity

    Parameters
    ----------
    df : pandas dataframe
        Dataframe with bids where there are at least
        two players in the same side of the market
        with the same price
    prec :
         (Default value = 5)

    Returns
    -------

    
    """

    id_gen = new_player_id(df.user.max() + 1)
    columns = df.columns.copy()

    df = df.copy().reset_index().rename(columns={'index': 'bid'})
    print(df)

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
