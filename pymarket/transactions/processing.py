"""
Some processing functions to deal with transactions
"""

import pandas as pd

from pymarket.transactions.transactions import TransactionManager


def split_transactions_merged_players(transactions, bids, maping, fees=None):
    """
    Splits the transactions of a market that used merged bids into the original
    bids
    Uses a proportional split, based on the offered (or asked) quantity by
    each player.

    Parameters
    ----------
    transactions: TransactionManager
        the transactions manager returned by the mechanism.
    bids: pandas dataframe
        the original bid dataframe where some players might be repeated
    maping: pandas dataframe
        A maping between the bids in the transaction dataframe and the original
        bids.

    Returns
    --------
    transactions_splited: pandas dataframe
        the result of splitting each merged bid in the transactions
        dataframe
    fees: dict or None
        dictionary obtained by splitting the fees equal to the transactions

    Examples
    -----------
    >>> bm = pm.BidManager()
    >>> tm = pm.TransactionManager()
    >>> bm.add_bid(1, 1, 0)
    0
    >>> bm.add_bid(2, 1, 1)
    1
    >>> tm.add_transaction(0, 1, 1, -1, False)
    0
    >>> tm_2 = split_transactions_merged_players(tm, bm.get_df(), {0:[0,1]})
    >>> tm_2.get_df()
       bid  quantity  price  source  active
    0    0  0.333333      1      -1   False
    1    1  0.666667      1      -1   False

    """

    trans = TransactionManager()
    new_rows = []
    for i, t in transactions.get_df().iterrows():
        rows = maping[t.bid]
        if True:  # TODO make more options available
            perc = bids.iloc[rows, :] / bids.iloc[rows, :].quantity.sum()
            perc = perc.quantity
        if len(rows) > 1 and fees is not None:
            fee = fees.pop(t.user, None)
        for r in rows:
            #t_ = pd.DataFrame(t).copy().T
            # print(r)
            t_ = t.copy().values
            # print(t_)
            t_[0] = r
            t_[1] *= perc[r]
            if len(rows) > 1 and fees is not None and fee is not None:
                fees[bids.iloc[r, :].user] = fee * perc[r]
            #t_.iloc[0, 0] = r
            #t_.iloc[0, 1] *= perc[r]
            # new_rows.append(t_)
            trans.add_transaction(*t_)
    #transactions_splited = pd.concat(new_rows)
    if fees is not None:
        return trans, fees
    else:
        return trans
