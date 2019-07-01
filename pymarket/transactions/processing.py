"""
Some processing functions to deal with transactions
"""

import pandas as pd


def split_transactions_merged_players(transactions, bids, maping):
    """
    Splits the transactions of a market that used merged bids into the original
    bids

    Parametes
    ----------
    transactions: pandas dataframe
        the transactions obtained by running a market mechanism
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

    """

    new_rows = []
    for i, t in transactions.iterrows():
        rows = maping[t.bid]
        if True:  # TODO make more options available
            perc = bids.iloc[rows, :] / bids.iloc[rows, :].quantity.sum()
            perc = perc.quantity
        for r in rows:
            t_ = pd.DataFrame(t).copy().T
            t_.iloc[0, 0] = r
            t_.iloc[0, 1] *= perc[r]
            new_rows.append(t_)

    transactions_splited = pd.concat(new_rows)

    return transactions_splited
