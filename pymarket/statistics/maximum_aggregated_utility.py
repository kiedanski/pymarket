import pulp
from pymarket.bids import BidManager


def maximum_aggregated_utility(bids, *args, reservation_prices=None):
    """Maximizes the total welfare

    Parameters
    ----------
    bids :
        
    *args :
        
    reservation_prices :
         (Default value = None)

    Returns
    -------

    
    """

    if reservation_prices is None:
        reservation_prices = {}

    model = pulp.LpProblem("Max aggregated utility", pulp.LpMaximize)
    buyers = bids.loc[bids['buying']].index.values
    sellers = bids.loc[~bids['buying']].index.values
    index = [(i, j) for i in buyers for j in sellers]

    for i, x in bids.iterrows():
        if i not in reservation_prices:
            reservation_prices[i] = x.price

    coeffs = {}
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
   
    variables = {}
    for var in qs:
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
    bids :
        
    transactions :
        
    reservation_prices :
         (Default value = None)
    **kwargs :
        

    Returns
    -------

    
    """
    if reservation_prices is None:
        reservation_prices = {}
    for i, x in bids.iterrows():
        if i not in reservation_prices:
            reservation_prices[i] = x.price

    _, objective, _ = maximum_aggregated_utility(bids, reservation_prices)

    tmp = bids.reset_index().rename(columns={'index': 'bid'})
    tmp.price = tmp.apply(
        lambda x: reservation_prices.get(x.user, x.price), axis=1)
    tmp = tmp[['bid', 'price', 'buying']]
    merged = transactions.merge(tmp, on='bid')

    welfare = merged.apply(lambda x: get_gain(x), axis=1).sum()

    if objective > 0:
        return welfare / objective
    else:
        return None


def get_gain(row):
    """Finds the gain of the row

    Parameters
    ----------
    row : TODO
        

    Returns
    -------

    
    """
    gap = row.price_y - row.price_x
    if not row.buying:
        gap = -gap
    return gap * row.quantity