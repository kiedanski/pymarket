import pulp
import pandas as pd
from pymarket.bids import BidManager
from collections import OrderedDict


def maximum_aggregated_utility(bids, *args, reservation_prices=None):
    """Maximizes the total welfare

    Parameters
    ----------
    bids : pd.DataFrame
       Collection of bids

    reservation_prices : dict of floats or None, (Default value = None)
        A maping from user ids to reservation prices. If no reservation
        price for a user is given, his bid will be assumed to be his
        true value.

    Returns
    -------
    status : str
        Status of the optimization problem. Desired output is 'Optimal'
    objective: float
        Maximum aggregated utility that can be obtained
    variables: dict
        A set of values achieving the objective. Maps a pair of bids
        to the quantity traded by them.

    Examples
    ---------

    >>> bm = pm.BidManager()
    >>> bm.add_bid(1, 3, 0)
    0
    >>> bm.add_bid(1, 2, 1)
    1
    >>> bm.add_bid(1.5, 1, 2, False)
    2
    >>> s, o, v = maximum_aggregated_utility(bm.get_df())
    >>> s
    'Optimal'
    >>> o
    2.5
    >>> v
    OrderedDict([((0, 2), 1.0), ((1, 2), 0.5)])

    If in reality the seller had 0 value for his commodity,
    the social welfare will be 1.5 units larger

    >>> bm = pm.BidManager()
    >>> bm.add_bid(1, 3, 0)
    0
    >>> bm.add_bid(1, 2, 1)
    1
    >>> bm.add_bid(1.5, 1, 2, False)
    2
    >>> rp = {2: 0}
    >>> s, o, v = maximum_aggregated_utility(bm.get_df(),
    ...        reservation_prices=rp)
    >>> s
    'Optimal'
    >>> o
    4.0
    >>> v
    OrderedDict([((0, 2), 1.0), ((1, 2), 0.5)])
    """

    if reservation_prices is None:
        reservation_prices = OrderedDict()

    model = pulp.LpProblem("Max aggregated utility", pulp.LpMaximize)
    buyers = bids.loc[bids['buying']].index.values
    sellers = bids.loc[~bids['buying']].index.values
    index = [(i, j) for i in buyers for j in sellers]

    for i, x in bids.iterrows():
        if i not in reservation_prices:
            reservation_prices[i] = x.price

    coeffs = OrderedDict()

    for x in index:
        coeffs[x] = reservation_prices[x[0]] - reservation_prices[x[1]]

    qs = pulp.LpVariable.dicts('q', index, lowBound=0, cat='Continuous')

    model += pulp.lpSum([qs[x[0], x[1]] * coeffs[x] for x in index])

    for b in buyers:
        model += pulp.lpSum(qs[b, j] for j in sellers) <= bids.iloc[b, 0]

    for s in sellers:
        model += pulp.lpSum(qs[i, s] for i in buyers) <= bids.iloc[s, 0]

    model.solve()

    status = pulp.LpStatus[model.status]
    objective = pulp.value(model.objective)

    variables = OrderedDict()
    sorted_keys = sorted(qs.keys())
    for var in sorted_keys:
        varval = qs[var].varValue
        variables[var] = varval

    return status, objective, variables


def percentage_welfare(bids, transactions, reservation_prices=None, **kwargs):
    """Percentage of the total welfare that could be achieved
    calculated based on the transaction lists

    Parameters
    ----------
    bids (pandas dataframe) :
        Table with all the submited bids
    transactions (pandas dataframe) :
        Table with all the transactions that ocurred in the market
    reservation_prices (dict, optional) :
        Reservation prices of the different participants. If None, the bids
        will be assumed to be the truthfull values.

    Returns
    -------
    ratio : float
        The ratio of the maximum social welfare achieved by the
        collection of transactions.

    Examples
    ---------
    Only bid 0 and 2 trade. That represents a net utility of 2
    which is 80% of the total max utility 2.5

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
    >>> percentage_welfare(bm.get_df(), tm.get_df())
    0.8
    """
    reservation_prices = OrderedDict()
    for i, x in bids.iterrows():
        if i not in reservation_prices:
            reservation_prices[i] = x.price

    _, objective, _ = maximum_aggregated_utility(bids, reservation_prices)

    tmp = bids.reset_index().rename(columns={'index': 'bid'})
    tmp = tmp[['bid', 'price', 'buying']]
    merged = transactions.merge(tmp, on='bid')

    buyers = merged.loc[merged['buying']]
    profit_buyers = (buyers.price_y - buyers.price_x) * buyers.quantity
    profit_buyers = profit_buyers.sum()

    sellers = merged.loc[~merged['buying']]
    profit_sellers = (sellers.price_x - sellers.price_y) * sellers.quantity
    profit_sellers = profit_sellers.sum()

    welfare = profit_buyers + profit_sellers

    if objective > 0:
        return welfare / objective
    else:
        return None
