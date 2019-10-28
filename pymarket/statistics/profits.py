import pandas as pd
import numpy as np
from collections import OrderedDict


def calculate_profits(
        bids,
        transactions,
        reservation_prices=None,
        fees=None,
        **kwargs):
    """Extras from the transactions and the bids the profit
    of each player and the market maker

    Parameters
    ----------
    bids : pd.DataFrame
        Collections of bids to be used

    transactions : pd.DataFrame
        Collection of transactions to be taken into account
    reservation_prices : dict, (Default value = None)
        Maping between users and their reservation prices. If None,
        it is assumed that each user bided truthfully and the
        information is extracted from the bid.
    fees : np.ndarray, (Default value = None)
        List of fees that each user has to pay to trade in the market.

    Returns
    -------
    profit: dict
        A dictionary with three values:
        * player_bid: A list with the profits of each user
        using their bids as reservation prices
        * player_reservation: Same as above but using
        their reservation prices, if none are provided,
        it is the same as `player_bid`
        * market: profit of the market maker


    Examples
    ---------
    >>> tm = pm.TransactionManager()
    >>> bm = pm.BidManager()
    >>> bm.add_bid(1, 3, 0)
    0
    >>> bm.add_bid(1, 2, 1)
    1
    >>> bm.add_bid(1.5, 1, 2, False)
    2
    >>> tm.add_transaction(0, 1, 2, 2, False)
    0
    >>> tm.add_transaction(2, 1, 2, 0, False)
    1
    >>> rp = {2: 0}
    >>> profits = calculate_profits(bm.get_df(), tm.get_df(),
    ...        reservation_prices=rp)
    >>> profits['player_bid']
    array([1., 0., 1.])
    >>> profits['player_reservation']
    array([1., 0., 2.])
    >>> profits['market']
    0.0
    """
    users = sorted(bids.user.unique())
    buyers = bids.loc[bids['buying']].index.values
    sellers = bids.loc[~bids['buying']].index.values

    if reservation_prices is None:
        reservation_prices = OrderedDict()
    for i, x in bids.iterrows():
        if i not in reservation_prices:
            reservation_prices[i] = x.price

    if fees is None:
        fees = np.zeros(bids.user.unique().shape[0])

    profit = OrderedDict()
    for case in ['bid', 'reservation']:
        tmp = bids.reset_index().rename(columns={'index': 'bid'}).copy()
        tmp = tmp[['bid', 'price', 'buying', 'user']]
        if case == 'reservation':
            tmp.price = tmp.apply(
                lambda x: reservation_prices.get(x.bid, x.price), axis=1)
        merged = transactions.merge(tmp, on='bid').copy()
        merged['gain'] = merged.apply(lambda x: get_gain(x), axis=1)
        profit_player = merged.groupby('user')['gain'].sum()
        # print(profit_player)
        profit_player = np.array([profit_player.get(x, 0) for x in users])
        profit['player_{}'.format(case)] = profit_player.astype('float64')

        if case == 'bid':
            # print(merged)
            mb = merged.loc[merged['buying']]
            ms = merged.loc[~merged['buying']]
            # print(ms)
            # print(ms.quantity.sum(), mb.quantity.sum())
            # print(ms.price_x * ms.quantity)
            profit_market = (mb.price_x * mb.quantity).values.sum()
            profit_market -= (ms.price_x * ms.quantity).values.sum()
            profit_market += fees.sum()
            profit['market'] = profit_market.astype('float64')

    return profit


def get_gain(row):
    """Finds the gain of the row

    Parameters
    ----------
    row : pandas row
       Row obtained by merging a transaction with a
       bid dataframe

    Returns
    -------
    gain
        The gain obtained by the row

    """
    gap = row.price_y - row.price_x
    if not row.buying:
        gap = - gap
    return gap * row.quantity
