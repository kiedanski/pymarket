import pulp
import pandas as pd
from pymarket.bids import BidManager
from collections import OrderedDict


def maximum_traded_volume(bids, *args, reservation_prices=OrderedDict()):
    """

    Parameters
    ----------
    bids : pd.DataFrame
       Collections of bids

    reservation_prices : dict of floats or None, (Default value = None)
        A maping from user ids to reservation prices. If no reservation
        price for a user is given, his bid will be assumed to be his
        true value.

    Returns
    -------
    status : str
        Status of the optimization problem. Desired output is 'Optimal'
    objective: float
        Maximum tradable volume that can be obtained
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
    >>> s, o, v = maximum_traded_volume(bm.get_df())
    >>> s
    'Optimal'
    >>> o
    1.5
    >>> v
    OrderedDict([((0, 2), 0.5), ((1, 2), 1.0)])

    """

    model = pulp.LpProblem("Max aggregated utility", pulp.LpMaximize)
    buyers = bids.loc[bids['buying']].index.values
    sellers = bids.loc[~bids['buying']].index.values

    index = [(i, j) for i in buyers for j in sellers
             if bids.iloc[i, 1] >= bids.iloc[j, 1]]

    qs = pulp.LpVariable.dicts('q', index, lowBound=0, cat='Continuous')

    model += pulp.lpSum([qs[x[0], x[1]] for x in index])

    for b in buyers:
        model += pulp.lpSum(qs[b, j]
                            for j in sellers if (b, j) in index) <= bids.iloc[b, 0]

    for s in sellers:
        model += pulp.lpSum(qs[i, s]
                            for i in buyers if (i, s) in index) <= bids.iloc[s, 0]

    model.solve()

    status = pulp.LpStatus[model.status]
    objective = pulp.value(model.objective)
    variables = OrderedDict()
    sorted_keys = sorted(qs.keys())
    for q in sorted_keys:
        v = qs[q].varValue
        variables[q] = v

    return status, objective, variables


def percentage_traded(bids, transactions, reservation_prices=OrderedDict(), **kwargs):
    """Calculates from the transaction dataframe
    the percentage of the total maximum possible
    traded quantity.

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
    Only bid 0 and 2 trade 1 unit. That represents
    the 66% of all that could have been traded.

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
    >>> percentage_traded(bm.get_df(), tm.get_df())
    0.6666666666666666

    """
    _, objective, _ = maximum_traded_volume(bids)

    total_traded = transactions.quantity.sum() / 2

    if objective > 0:
        return total_traded / objective
    else:
        return None
