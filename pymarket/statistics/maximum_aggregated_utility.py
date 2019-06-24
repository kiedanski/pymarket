import pulp
from pymarket.bids import BidManager

def maximum_aggregated_utility(bids):
    """
    Maximizes the sum of the utilities
    """

    model = pulp.LpProblem("Max aggregated utility", pulp.LpMaximize)
    buyers = bids[bids.buying == True].index.values
    sellers = bids[bids.buying == False].index.values

    index = [(i, j) for i in buyers for j in sellers]

    qs = pulp.LpVariable.dicts('q', index, lowBound=0, cat='Continuous')

    model += pulp.lpSum(
            [qs[x[0], x[1]] * (bids.iloc[x[0], 1] - bids.iloc[x[1], 1]) for x in index])

    for b in buyers:
        model += pulp.lpSum(qs[b, j] for j in sellers) <= bids.iloc[b, 0]
    
    for s in sellers:
        model += pulp.lpSum(qs[i, s] for i in buyers) <= bids.iloc[s, 0]
    
    model.solve()

    status = pulp.LpStatus[model.status]
    objective  = pulp.value(model.objective)
   
    variables = {}
    for var in qs:
        varval = qs[var].varValue
        variables[var] =  varval

    return status, objective, variables

def percentage_welfare(bids, transactions):
    """Percentage of the total welfare that could be achieved
    calculated based on the transaction lists

    Parameters
    ----------
    bids : TODO
    transactions : TODO

    Returns
    -------
    TODO

    """

    _, objective, _  = maximum_aggregated_utility(bids)

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
            gap =- gap
        return gap * row.quantity

    tmp = bids.reset_index().rename(columns={'index':'bid'})
    tmp = tmp[['bid', 'price', 'buying']]
    merged = transactions.merge(tmp, on='bid')

    welfare = merged.apply(lambda x: get_gain(x), axis=1).sum()

    if objective > 0:
        return welfare / objective
    else:
        return None
        
