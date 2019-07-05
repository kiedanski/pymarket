import pulp
from pymarket.bids import BidManager


def maximum_traded_volume(bids, *args, reservation_prices={}):
    """

    Parameters
    ----------
    bids :
        
    *args :
        
    reservation_prices :
         (Default value = {})

    Returns
    -------

    """

    model = pulp.LpProblem("Max aggregated utility", pulp.LpMaximize)
    buyers = bids.loc[bids['buying']].index.values
    sellers = bids.loc[~bids['buying']].index.values

    index = [(i, j) for i in buyers for j in sellers
             if bids.iloc[i, 1] >= bids.iloc[j, 1]]

    qs = pulp.LpVariable.dicts('q', index, lowBound=0, cat='Continuous')

    model += pulp.lpSum([qs[x[0], x[1]] for x in index])

    for b in buyers:
        model += pulp.lpSum(qs[b, j] for j in sellers if (b, j) in index) <= bids.iloc[b, 0]
    
    for s in sellers:
        model += pulp.lpSum(qs[i, s] for i in buyers if (i, s) in index) <= bids.iloc[s, 0]
    
    model.solve()

    status = pulp.LpStatus[model.status]
    objective = pulp.value(model.objective)
    variables = {}
    for q in qs:
        v = qs[q].varValue
        variables[q] = v

    return status, objective, variables


def percentage_traded(bids, transactions, reservation_prices={}, **kwargs):
    """Calculates from the transaction dataframe
    the percentage of the total maximum possible
    traded quantity.

    Parameters
    ----------
    bids : TODO
        
    transactions : TODO
        
    reservation_prices :
         (Default value = {})
    **kwargs :
        

    Returns
    -------

    
    """
    _, objective, _ = maximum_traded_volume(bids)
    
    total_traded = transactions.quantity.sum() / 2

    if objective > 0:
        return total_traded / objective
    else:
        return None
