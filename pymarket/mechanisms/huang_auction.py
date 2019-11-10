from pymarket.bids import BidManager
from pymarket.mechanisms import Mechanism
from pymarket.transactions import TransactionManager
from pymarket.bids.demand_curves import *
from collections import OrderedDict


def update_quantity(quantity, gap):
    """Implements the footnote in page 8 of [1],
    where the long side updates their
    trading quantities to match the short side.

    Parameters
    ----------
    quantity: np.ndarray
        List of the quantities to be traded by each
        player.
    gap: float
        Difference between the short and long side

    Returns
    -------
    quantity: np.ndarray
        Updated list of quantities to be traded
        by each player

    Notes
    ------
    [1] Huang, Pu, Alan Scheller–Wolf, and Katia Sycara. "Design of a multi–unit
    double auction e–market." Computational Intelligence 18.4 (2002): 596-617.

    Examples
    ---------
    All keep trading, with less quantity

    >>> l, g = np.array([1, 2, 3]), 0.6
    >>> update_quantity(l, g)
    array([0.8, 1.8, 2.8])

    The gap is to big for small trader:

    >>> l,g = np.array([1, 0.5, 2]), 1.8
    >>> update_quantity(l, g)
    array([0.35, 0.  , 1.35])

    """
    quantity = quantity * 1.0
    i_min = np.nanargmin(quantity)
    v_min = np.nanmin(quantity)
    #i_min = quantity[quantity > 0].argmin()
    #v_min = quantity[quantity > 0].min()
    end = False
    N = len(quantity)
    while not end:
        if v_min < gap / N:
            quantity[i_min] = np.nan
            N -= 1
            gap -= v_min
            i_min = np.nanargmin(quantity)
            v_min = np.nanmin(quantity)
            #i_min = quantity[quantity > 0].argmin()
            #v_min = quantity[quantity > 0].min()
        else:
            end = True
    quantity = np.nan_to_num(quantity)
    quantity -= float(gap) / N
    max_ = quantity.max()
    quantity = np.clip(quantity, 0, max_)
    return quantity


def huang_auction(bids):
    """Implements the auction described in [1]

    Parameters
    ----------
    bids: pd.DataFrame
        Collection of all the bids to take
        into account by the mechanism

    Returns
    -------
    trans : TransactionManager
        Collection of all the trasactions cleared
        by the mechanism

    extra : dict
        Extra information provided by the mecanism.
        Keys:
        * price_sell: price at which sellers traded
        * price_buy: price at which the buyers traded
        * quantity_traded: the total quantity traded


    Notes
    ------
    [1] Huang, Pu, Alan Scheller–Wolf, and Katia Sycara. "Design of a multi–unit
    double auction e–market." Computational Intelligence 18.4 (2002): 596-617.

    Examples
    --------
    No trade because price setters don't trade:

    >>> bm = pm.BidManager()
    >>> bm.add_bid(1, 3, 0)
    0
    >>> bm.add_bid(2, 1, 1)
    1
    >>> bm.add_bid(2, 2, 2, False)
    2
    >>> trans, extra = huang_auction(bm.get_df())
    >>> trans.get_df()
    Empty DataFrame
    Columns: [bid, quantity, price, source, active]
    Index: []
    >>> extra
    OrderedDict([('price_sell', 2.0), ('price_buy', 3.0), ('quantity_traded', 0)])

    Adding small bids at the beginning, those can trade
    because they don't define de market price:

    >>> bm.add_bid(0.3, 1, 3, False)
    3
    >>> bm.add_bid(0.2, 3.3, 4)
    4
    >>> trans, extra = huang_auction(bm.get_df())
    >>> trans.get_df()
       bid  quantity  price  source  active
    0    3       0.2    2.0      -1   False
    1    4       0.2    3.0      -1   False
    >>> extra
    OrderedDict([('price_sell', 2.0), ('price_buy', 3.0), ('quantity_traded', 0.2)])

    """

    # print(bids)

    trans = TransactionManager()

    buy, b_index = demand_curve_from_bids(bids)
    sell, s_index = supply_curve_from_bids(bids)

    q_, b_, s_, _ = intersect_stepwise(buy, sell)

    if b_ is None or s_ is None:
        price_sell = None
        price_buy = None
        quantity_bid = np.array([0, 0])
    else:

        price_sell = sell[s_, 1]
        price_buy = buy[b_, 1]

        buying_bids = bids.loc[bids['buying']].sort_values(
            'price', ascending=False)
        selling_bids = bids.loc[~bids['buying']
                                ].sort_values('price', ascending=True)

        # Filter only the trading bids.
        buying_bids = buying_bids.iloc[: b_, :]
        selling_bids = selling_bids.iloc[: s_, :]

        # print(selling_bids, buying_bids)

        quantity_buy = buying_bids.quantity.values
        quantity_sell = selling_bids.quantity.values

    if b_ is not None and b_ > 0 and s_ is not None and s_ > 0:


        #long_sellers = sell[s_ - 1, 0] > buy[b_ - 1, 0]
        #gap = sell[s_ - 1, 0] - buy[b_ - 1, 0]
        gap = quantity_sell.sum() - quantity_buy.sum()
        if gap > 0:
            quantity_sell = update_quantity(quantity_sell, gap)
        else:
            quantity_buy = update_quantity(quantity_buy, - gap)

        for (i, x), q in zip(selling_bids.iterrows(), quantity_sell):
            # print(i)
            t = (i, q, price_sell, -1, False)
            trans.add_transaction(*t)

        for (i, x), q in zip(buying_bids.iterrows(), quantity_buy):
            # print(i)
            t = (i, q, price_buy, -1, False)
            trans.add_transaction(*t)

    #    for i in range(s_):
    #        id_ = s_index[i]
    #        trans.add_transaction(id_, quantity_sell[i],
    #                price_sell, -1, False)

    #    for i in range(b_):
    #        id_ = b_index[i]
    #        trans.add_transaction(id_, quantity_buy[i],
    #                price_buy, -1, False)
    
    if b_ is None or s_ is None:
        extra = OrderedDict()
    else:
        extra = OrderedDict([('price_sell', price_sell), ('price_buy', price_buy),
                 ('quantity_traded', quantity_buy.sum())])
    # print(trans.get_df())
    return trans, extra


class HuangAuction(Mechanism):

    """Iinterface for the HuangAuction

    Parameters
    -----------
    bids: pd.DataFrame
        Collection of bids to use in the market
    merge: bool
        Wheather to merge players with the
        same price. Always `True`

    """

    def __init__(self, bids, *args, **kwargs):
        """
        """
        Mechanism.__init__(
            self,
            huang_auction,
            bids,
            *args,
            merge=True,
            **kwargs)
