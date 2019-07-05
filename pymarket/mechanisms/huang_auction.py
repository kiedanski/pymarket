from pymarket.bids import BidManager
from pymarket.mechanisms import Mechanism
from pymarket.transactions import TransactionManager
from pymarket.bids.demand_curves import *


def update_quantity(quantity, gap):
    """Implements the footnote of the paper
    where the long side updates their
    trading quantities to match the short side
    Parms:

    Parameters
    ----------
    quantity :
        numpy array with the quantities
        traded
    gap :
        difference between the short and long side
        
        Returns:
        :quantity: updated quantities

    Returns
    -------

    """
    quantity = quantity * 1.0
    i_min = quantity[quantity > 0].argmin()
    v_min = quantity[quantity > 0].min()
    end = False
    N = len(quantity)
    while not end:
        if v_min < gap / N:
            quantity[i_min] = 0.0
            N -= 1
            gap -= v_min
            i_min = quantity[quantity > 0].argmin()
            v_min = quantity[quantity > 0].min()
        else:
            end = True
    quantity -= float(gap) / N
    max_ = quantity.max()
    quantity = np.clip(quantity, 0, max_)
    return quantity

def huang_auction(bids):
    """Implements the auction described in
    `DESIGN OF A MULTI-UNIT DOUBLE AUCTION E-MARKET`

    Parameters
    ----------
    s :
        bids: BidManager
        
        Returns:
        :trans : Transaction Manger
    bids :
        

    Returns
    -------

    """

    trans = TransactionManager()
    
    buy, b_index  = demand_curve_from_bids(bids)
    sell, s_index = supply_curve_from_bids(bids)

    q_, b_, s_, _ = intersect_stepwise(buy, sell)

    price_sell = sell[s_, 1]
    price_buy = buy[b_, 1]
   
    quantity_buy = bids.iloc[b_index[:b_], 0].values
    quantity_sell = bids.iloc[s_index[:s_], 0].values
    if b_ > 0 and s_ > 0:
       long_sellers = sell[s_ - 1, 0] > buy[b_ - 1, 0] 
       gap = sell[s_ - 1, 0] - buy[b_ - 1, 0] 
       if long_sellers:
            quantity_sell = update_quantity(quantity_sell, gap) 
       else:
           quantity_buy = update_quantity(quantity_buy, - gap)
            
       for i in range(s_):
           id_ = s_index[i]
           trans.add_transaction(id_, quantity_sell[i],
                   price_sell, -1, False)

       for i in range(b_):
           id_ = b_index[i]
           trans.add_transaction(id_, quantity_buy[i],
                   price_buy, -1, False)
           extra = {'price_sell': price_sell, 'price_buy': price_buy,
                   'quantity_traded': quantity_buy.sum()}
    return trans, extra

class HuangAuction(Mechanism):

    """Iinterface for the HuangAuction"""

    def __init__(self, bids, *args, **kwargs):
        """TODO: to be defined1.

        Parameters
        ----------
        bids : TODO


        """
        Mechanism.__init__(self, huang_auction,  bids, *args, merge=True, **kwargs)
        
