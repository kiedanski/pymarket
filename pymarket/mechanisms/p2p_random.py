import pandas as pd
import networkx as nx
import numpy as np

from pymarket.transactions import TransactionManager
from pymarket.bids import BidManager


def p2p_random(bids, p_coef=0.5, r = None):
    """
    Computes all the trades using a P2P random trading
    process as describes in [CITA].
    :params bids: BidManager class
    :params p_coef: coefficient to calculate the trading price, 1
    uses the buying price and 0 the selling price, else, linear combination.

    """
    r = np.random.RandomState() if r is None else r

    trans = TransactionManager()
    buying = bids[bids.buying == True]
    selling = bids[bids.buying == False]
    Nb, Ns = buying.shape[0], selling.shape[0]

    quantities = df.quantity.values.copy()
    prices = df.price.values.copy()
   
    inactive_buying = []
    inactive_selling = []

    # Enumerate all possible trades
    pairs = np.ones((Nb + Ns, Nb * Ns), dtype=bool)
    pairs_inv = []
    i = 0
    for b in buying.index:
        for s in selling.index:
            pairs[b, i] = False # Row b has 0s whenever the pair involves b
            pairs[s, i] = False # Same for s
            pairs_inv.append((b, s))
            i += 1 

    
    active = np.ones(Nb * Ns, dtype=bool)
    tmp_active = active.copy()

    # Loop while there is quantities to trade or not all
    # possibilities have been tried
    while quantities.sum() > 0 and tmp_active.sum() > 0:
        trading_list = []
        while tmp_active.sum() > 0: # We can select a pair
            where = np.where(tmp_active == 1)[0]
            x = r.choice(where)
            trade = pairs_inv[x]
            active[x] = False # Pair has already traded
            trading_list.append(trade)
            tmp_active &= pairs[trade[0], :] # buyer and seller already used
            tmp_active &= pairs[trade[1], :]

         
        for (b, s) in trading_list:
            if prices[b] > prices[s]:
                q = min(quantities[b], quantities[s])
                p = prices[b] * p_coef + (1 - p_coef) * prices[s]
                trans_b = (b, q, p, s, (quantities[b] - q) > 0)
                trans_s = (s, q, p, b, (quantities[s] - q) > 0)
                quantities[b] -= q
                quantities[s] -= q
            else:
                trans_b = (b, 0, 0, s, True)
                trans_s = (s, 0, 0, b, True)
            trans.add_transaction(*trans_b)
            trans.add_transaction(*trans_s)
       
        inactive_buying = [b for b in buying.index if quantities[b] == 0]
        inactive_selling = [s for s in selling.index if quantities[s] == 0]
       
        tmp_active = active.copy()
        for inactive in inactive_buying + inactive_selling:
            tmp_active &= pairs[inactive, :]

    return trans


if __name__ == '__main__':
    
    from utils import generate_random_bid
    from bids import BidManager

    bm = BidManager()
    [bm.add_bid(*generate_random_bid()) for _ in range(4)]
    df = bm.get_df()
    print(df[df.buying==True].shape[0], df.shape[0])
    y = p2p_random(df)
