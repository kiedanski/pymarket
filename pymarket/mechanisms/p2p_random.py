import pandas as pd
import networkx as nx
import numpy as np

from pymarket.transactions import TransactionManager
from pymarket.bids import BidManager
from pymarket.mechanisms import Mechanism


def p2p_random(bids, p_coef=0.5, r = None):
    """Computes all the trades using a P2P random trading
    process as describes in [CITA].

    Parameters
    ----------
    s :
        bids: BidManager class
    s :
        p_coef: coefficient to calculate the trading price, 1
        uses the buying price and 0 the selling price, else, linear combination.
    bids :
        
    p_coef :
         (Default value = 0.5)
    r :
         (Default value = None)

    Returns
    -------

    """
    r = np.random.RandomState() if r is None else r

    trans = TransactionManager()
    buying = bids[bids.buying == True]
    selling = bids[bids.buying == False]
    Nb, Ns = buying.shape[0], selling.shape[0]

    quantities = bids.quantity.values.copy()
    prices = bids.price.values.copy()
   
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
    general_trading_list = []
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

        general_trading_list.append(trading_list) 
        for (b, s) in trading_list:
            if prices[b] >= prices[s]:
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

    extra = {'trading_list': general_trading_list}
    return trans, extra

class P2PTrading(Mechanism):

    """Docstring for P2PTrading."""

    def __init__(self, bids, *args, **kwargs):
        """TODO: to be defined1.

        Parameters
        ----------
        bids : TODO
        *args : TODO


        """
        Mechanism.__init__(self, p2p_random, bids, *args, **kwargs)

        
