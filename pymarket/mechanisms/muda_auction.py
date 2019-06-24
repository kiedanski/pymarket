import numpy as np
from pymarket.bids import BidManager
from pymarket.transactions import TransactionManager
from pymarket.bids.demand_curves import *
from pymarket.mechanisms import Mechanism



def muda(bids, r=None):
    '''
    Implements MUDA as describes in paper...

    '''
    r     = np.random.RandomState() if r is None else r
    left  = [i for i in bids.index if r.rand() > 0.5]
    right = [i for i in bids.index if i not in left]

    pl = find_competitive_price(bids.loc[left])
    pr = find_competitive_price(bids.loc[right])
    
    trans = TransactionManager()
    fees = np.zeros(bids.user.unique().shape[0])
    trans, fees = solve_market_side_with_exogenous_price(bids.loc[left]  , pr , trans, fees, r)
    trans, fees = solve_market_side_with_exogenous_price(bids.loc[right] , pl , trans, fees, r)

    extra = {
            'left': left,
            'right': right,
            'price_left': pl,
            'price_right': pr,
            'fees': fees
            }
    return trans, extra
def solve_market_side_with_exogenous_price(bids, price, trans, fees, r):
    """
    Finds who trades and at what price based on the
    exogeneous price
    """
    demand = bids[(bids.buying == True)  & (bids.price >= price)]
    demand = demand.sort_values('price', ascending=False)
    supply = bids[(bids.buying == False) & (bids.price <= price)]
    supply = supply.sort_values('price')
    print(demand, supply)
    supply_quantity = supply.quantity.sum()
    demand_quantity = demand.quantity.sum()
    
    ## Deal with the short side of the demand
    supply_long    = supply_quantity > demand_quantity
    long_side      = supply if supply_long else demand
    short_side     = demand if supply_long else supply
    total_quantity = demand_quantity if supply_long else supply_quantity
    print(supply_long, total_quantity)
    if total_quantity > 0: 
        total_quantity = int(total_quantity)
        for i, x in short_side.iterrows():
            t = (x.name, x.quantity, price, -1, False)
            trans.add_transaction(*t)

        ## Deal with the long side of the demand
        ## Vickrey style
        trading_bids = long_side.index.values[:total_quantity] 
        trading_users = long_side.iloc[:total_quantity, :].user.unique()
        print(trading_bids) 
        ## Compute fee of each user
        for u in trading_users:
            trades_by_user = long_side[(long_side.user == u)]
            exclude_index = long_side.index.isin(trades_by_user.index)
            trading_without_u = long_side[~exclude_index].iloc[:total_quantity, :]
            new_bids          = trading_without_u[~trading_without_u.index.isin(trading_bids)]
            fee               = (new_bids.price - price).sum()
            for i, x in trades_by_user[trades_by_user.index.isin(trading_bids)].iterrows():
                t = (x.name, x.quantity, price, -1, False)
                trans.add_transaction(*t)
            if supply_long:
                fees[u] = -fee
            else:
                fees[u] = fee

    return trans, fees
            

def find_competitive_price(bids):
    """
    Finds the unique trading price of the intersection
    of supply and demand
    """
        
    buy, b_index  = demand_curve_from_bids(bids)
    sell, s_index = supply_curve_from_bids(bids)

    q_, b_, s_, price = intersect_stepwise(buy, sell)

    return price

class MudaAuction(Mechanism):

    """Docstring for MudaAuction. """

    def __init__(self, bids, *args, **kwargs):
        """TODO: to be defined1. """
        Mechanism.__init__(self, muda, bids, *args, **kwargs)


        

