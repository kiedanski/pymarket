import numpy as np
from pymarket.bids import BidManager
from pymarket.transactions import TransactionManger
from pymarket.bids.demand_curves import *



def muda(bids, r=None):
    '''
    Implements MUDA as describes in paper...

    '''
    r     = np.random.RandomState() if r is None else None
    left  = [i for i in bids.index if r.rand() > 0.5]
    right = [i for i in bids.index if i not in left]

    pl = find_competitive_price(bids.loc[left])
    pr = find_competitive_price(bids.loc[right])
    
    trans = TransactionManger()
    fees = np.zeros(bids.users.unique().shape[0])
    trans, fees = solve_market_side_with_exogenous_price(bids.loc[left]  , pr , trans, fees, r)
    trans, fees = solve_market_side_with_exogenous_price(bids.loc[right] , pl , trans, fees, r)

    return trans, fees, left, right
def solve_market_side_with_exogenous_price(bids, price, trans, fees, r):
    """
    Finds who trades and at what price based on the
    exogeneous price
    """
    demand = bids[(bids.buying == True)  & (bids.price >= price)]
    demand = demand.sort_values('price', ascending=False)
    supply = bids[(bids.buying == False) & (bids.price <= price)]
    supply = supply.sort_values('price')

    supply_quantity = supply.quantity.sum()
    demand_quantity = demand.quantity.sum()
    
    ## Deal with the short side of the demand
    supply_long    = supply_quantity > demand_quantity
    long_side      = supply if supply_long else demand
    short_side     = demand if supply_long else supply
    total_quantity = demand_quantity if supply_long else supply_quantity
    if total_quantity > 0: 
        for i, x in short_side.iterrows():
            t = (x.name, x.quantity, price, -1, False)
            trans.add_transaction(*t)

        ## Deal with the long side of the demand
        ## Vickrey style
        trading_bids = long_side.index.values[:total_quantity] 
        trading_users = long_side.iloc[:total_quantity, :].user.unique()
        
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

    q_, b_, s_ = intersect_stepwise(buy, sell)

    price_sell = sell[s_, 1]
    price_buy  = buy[b_, 1]

    if q_ in buy[:, 0]:
        price = price_sell
    else:
        price = price_buy

    return price


if __name__ == '__main__':
    bm = BidManager()
    bm.add_bid(1, 100, 0, True, 0)
    bm.add_bid(1, 90, 0, True, 0)
    bm.add_bid(1, 80, 0, True, 0)
    bm.add_bid(1, 60, 0, True, 0)
    bm.add_bid(1, 40, 0, True, 0)
    bm.add_bid(1, 20, 0, True, 0)

    bm.add_bid(1, 10, 1, False, 0)
    bm.add_bid(1, 20, 1, False, 0)
    bm.add_bid(1, 40, 1, False, 0)
    bm.add_bid(1, 60, 1, False, 0)
    bm.add_bid(1, 70, 1, False, 0)
    
    bm.add_bid(1, 15, 2, False, 0)
    bm.add_bid(1, 25, 2, False, 0)
    bm.add_bid(1, 35, 2, False, 0)
    bm.add_bid(1, 45, 2, False, 0)
    bm.add_bid(1, 65, 2, False, 0)
    
    df = bm.get_df()
    r = np.random.RandomState()
    trans = TransactionManger()
    fees = np.zeros(3)
    tt, fees = solve_market_side_with_exogenous_price(df, 50, trans, fees, r)
    
    
