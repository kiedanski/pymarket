import pandas as pd
import numpy as np


def calculate_profits(bids, transactions, reservation_prices=None, fees=None, **kwargs):
    """
    Extras from the transactions and the bids the profit
    of each player and the market maker

    Parameters
    -----------
    transactions (pandas dataframe):
        Transactions table with the result of running the market
    bids (pandas dataframe):
        Bids table with the submitted bids to the market
    reservation_prices (dict):
        The reservation price for each of the participants, if it is empty
        it is assumed that the bid was truthful and the reservation price
        was exactly the bidded one.
    fees (list, optional):
        A list of fees to pay for each player.

    Returns:
    profits (pandas dataframe):
        Table with the profits of each player and the marketmaker
    
    """
    users = sorted(bids.user.unique())
    buyers = bids.loc[bids['buying']].index.values
    sellers = bids.loc[~bids['buying']].index.values
    
    if reservation_prices is None:
        reservation_prices = {}
    for i, x in bids.iterrows():
        if i not in reservation_prices:
            reservation_prices[i] = x.price

    if fees is None:
        fees = np.zeros(bids.user.unique().shape[0])
   
    profit = {}
    for case in ['bid', 'reservation']:
        tmp = bids.reset_index().rename(columns={'index': 'bid'})
        tmp = tmp[['bid', 'price', 'buying', 'user']]
        if case == 'reservation':
            tmp.price = tmp.apply(
                lambda x: reservation_prices.get(x.user, x.price), axis=1)
        merged = transactions.merge(tmp, on='bid')
        merged['gain'] = merged.apply(lambda x: get_gain(x), axis=1)
        profit_player = merged.groupby('user')['gain'].sum()
        profit_player = np.array([profit_player.get(x, 0) for x in users])
        profit[f'player_{case}'] = profit_player

        if case == 'bid':
            mb = merged[merged.user.isin(buyers)]
            ms = merged[merged.user.isin(sellers)]
            profit_market = (
                (mb.price_x * mb.quantity).sum() -
                (ms.price_x * ms.quantity).sum()
            )
            profit_market += fees.sum()
            profit['market'] = profit_market

    return profit


def get_gain(row):
        """Finds the gain of the row

        Parameters
        ----------
        row : TODO

        Returns
        -------
        TODO

        """
        gap = row.price_y - row.price_x
        if not row.buying:
            gap = - gap
        return gap * row.quantity
