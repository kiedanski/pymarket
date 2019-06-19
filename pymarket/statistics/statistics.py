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

    print(index)

    model += pulp.lpSum(
            [qs[x[0], x[1]] * (bids.iloc[x[0], 1] - bids.iloc[x[1], 1]) for x in index])

    for b in buyers:
        model += pulp.lpSum(qs[b, j] for j in sellers) <= bids.iloc[b, 0]
    
    for s in sellers:
        model += pulp.lpSum(qs[i, s] for i in buyers) <= bids.iloc[s, 0]
    
    model.solve()

    print(pulp.LpStatus[model.status])
    print(pulp.value(model.objective))
    
    tot = 0
    for var in qs:
        varval = qs[var].varValue
        tot += varval

    print(tot)
def maximum_traded_volume(bids):
    """
    """

    model = pulp.LpProblem("Max aggregated utility", pulp.LpMaximize)
    buyers = bids[bids.buying == True].index.values
    sellers = bids[bids.buying == False].index.values

    index = [(i, j) for i in buyers for j in sellers if bids.iloc[i, 1]
            >= bids.iloc[j, 1]]

    qs = pulp.LpVariable.dicts('q', index, lowBound=0, cat='Continuous')

    print(index)

    model += pulp.lpSum([qs[x[0], x[1]] for x in index])

    for b in buyers:
        model += pulp.lpSum(qs[b, j] for j in sellers if (b, j) in index) <= bids.iloc[b, 0]
    
    for s in sellers:
        model += pulp.lpSum(qs[i, s] for i in buyers if (i, s) in index) <= bids.iloc[s, 0]
    
    model.solve()

    print(pulp.LpStatus[model.status])
    print(pulp.value(model.objective))
    

if  __name__ == '__main__':

    
    bm = BidManager()
    bm.add_bid(1, 3, 0, True, 0)
    bm.add_bid(2, 4, 1, True, 0)
    bm.add_bid(5, 1, 2, True, 0)

    bm.add_bid(4, 2, 3, False, 0)
    bm.add_bid(1, 1, 4, False, 0)
    bm.add_bid(5, 6, 5, False, 0)
    
    df = bm.get_df()
    maximum_aggregated_utility(df) 
    print('--------------------')
    maximum_traded_volume(df) 
    
