import numpy as np
import pandas as pd
from pymarket.bids import BidManager, merge_same_price
from pymarket.transactions import TransactionManager, \
    split_transactions_merged_players
from pymarket.bids.demand_curves import *
from pymarket.mechanisms import Mechanism
from pymarket.utils.decorators import check_equal_price
from collections import OrderedDict


@check_equal_price
def muda(bids, r=None):
    """Implements the Vickrey MUDA as described in [1].

    The mechanism does not support two players in the
    same side of the market with the same price.

    Parameters
    ----------
    bids: pd.DataFrame
        Collection of bids to be used in the market
    r: np.random.RandomState
        A numpy random state generator. If not given,
        a new one will be created and the output will
        be random.

    Returns
    -------
    trans: TransactionManager
        A collection of all the transactions performed.

    extra: dict
        Dictionary with extra information provided by
        the mechanism.
        Keys:
        * left: players in the left market
        * right: players in the right market
        * price_left: clearing price of the left market
        * price_right: clearing price of the right_market
        * fees: Fees that players have to pay to participate


    Notes
    ------

    [1] Segal-Halevi, Erel, Avinatan Hassidim, and Yonatan Aumann. "MUDA:
    a truthful multi-unit double-auction mechanism." Thirty-Second AAAI
    Conference on Artificial Intelligence. 2018.

    Examples
    ---------

    A case in which the market puts all the players
    in the same side and no one trades.

    >>> bm = pm.BidManager()
    >>> bm.add_bid(1, 4, 0)
    0
    >>> bm.add_bid(1, 2, 1)
    1
    >>> bm.add_bid(1, 3, 2, False)
    2
    >>> bm.add_bid(1, 1, 3, False)
    3
    >>> r = np.random.RandomState(420)
    >>> trans, extra = muda(bm.get_df(), r)
    >>> extra
    OrderedDict([('left', []), ('right', [0, 1, 2, 3]), ('price_left', inf), ('price_right', 2.5), ('fees', array([0., 0., 0., 0.]))])
    >>> trans.get_df()
    Empty DataFrame
    Columns: [bid, quantity, price, source, active]
    Index: []

    A case in which there are 2 players in each side but the
    cleared prices makes it impossible to trade:

    >>> r = np.random.RandomState(69)
    >>> trans, extra = muda(bm.get_df(), r)
    >>> extra
    OrderedDict([('left', [1, 3]), ('right', [0, 2]), ('price_left', 1.5), ('price_right', 3.5), ('fees', array([0., 0., 0., 0.]))])
    >>> trans.get_df()
    Empty DataFrame
    Columns: [bid, quantity, price, source, active]
    Index: []

    A case with trade:

    >>> bm.add_bid(1, 5, 4)
    4
    >>> r = np.random.RandomState(69)
    >>> trans, extra = muda(bm.get_df(), r)
    >>> trans.get_df()
       bid  quantity  price  source  active
    0    3         1    3.5      -1   False
    1    4         1    3.5      -1   False
    2    2         1    3.0      -1   False
    3    0         1    3.0      -1   False
    >>> extra
    OrderedDict([('left', [1, 3, 4]), ('right', [0, 2]), ('price_left', 3.0), ('price_right', 3.5), ('fees', array([0., 0., 0., 0., 0.]))])

    """
    if r is None:
        r = np.random.RandomState()

    left = [i for i in bids.index if r.rand() > 0.5]
    right = [i for i in bids.index if i not in left]

    pl = find_competitive_price(bids.loc[left])
    pr = find_competitive_price(bids.loc[right])

    fees = np.zeros(bids.user.unique().shape[0])

    trans_left, fees = solve_market_side_with_exogenous_price(
        bids.loc[left], pr, fees)
    trans_right, fees = solve_market_side_with_exogenous_price(
        bids.loc[right], pl, fees)

    trans = trans_left.merge(trans_right)

    extra = OrderedDict([
        ('left', left),
        ('right', right),
        ('price_left', pl),
        ('price_right', pr),
        ('fees', fees),])
    return trans, extra


def solve_market_side_with_exogenous_price(
    bids, price,
    fees):
    """
    Clears the market based on an external price.
    First it removes all biders that are not willing
    to trade at the given price, and then it fits
    the best allocation.
    Fees are calculated based on users that were
    willing but could not trade.

    Parameters
    ----------
    bids : pd.DataFrame
        Collection of bids to clear the market with
    price : float
        Price at which all the trades will ocurr
    fees: list of floats
        List of all the fees that players will have to pay.
        It gets updated.

    Returns
    -------
    trans: TransactionManager
        Collection of the transactions that clear the market
    fees: list of floats
        Fees to be paid by each player. Is a list where
        the fee of player with id `u` is located at `fees[u]`.

    Examples
    --------

    >>> bm = pm.BidManager()
    >>> bm.add_bid(1, 3, 0)
    0
    >>> bm.add_bid(1, 0.5, 1)
    1
    >>> bm.add_bid(1, 1, 2, False)
    2
    >>> bm.add_bid(1, 2, 3, False)
    3
    >>> fees = [0, 0, 0, 0]
    >>> trans, fees = solve_market_side_with_exogenous_price(bm.get_df(),2.5, fees)
    >>> trans.get_df()
       bid  quantity  price  source  active
    0    0         1    2.5      -1   False
    1    2         1    2.5      -1   False
    >>> fees
    [0, 0, 0.5, 0]

    """
    trans = TransactionManager()
    demand = bids.loc[bids['buying']]
    if demand.shape[0] > 0:
        demand = demand.query('price >= @price')
        demand = demand.sort_values('price', ascending=False)
    else:
        return trans, fees
    supply = bids.loc[~bids['buying']]
    if supply.shape[0] > 0:
        supply = supply.query('price <= @price')
        supply = supply.sort_values('price')
    else:
        return trans, fees
    supply_quantity = supply.quantity.sum()
    demand_quantity = demand.quantity.sum()

    # Deal with the short side of the demand
    supply_long = supply_quantity > demand_quantity
    long_side = supply if supply_long else demand
    short_side = demand if supply_long else supply
    total_quantity = demand_quantity if supply_long else supply_quantity
    if total_quantity > 0:

        long_side, l_index = get_trading_bids(long_side, total_quantity)
        short_side, s_index = get_trading_bids(short_side, total_quantity)

        for i, x in short_side.iterrows():
            if i <= s_index:
                t = (x.bid, x.quantity, price, -1, False)
                trans.add_transaction(*t)

        for i, x in long_side.iterrows():
            if i <= l_index:
                t = (x.bid, x.quantity, price, -1, False)
                trans.add_transaction(*t)

        trading_users_long_side = (
            long_side[long_side.index <= l_index]
            .user
            .unique()
        )
        for u in trading_users_long_side:
            fee = compute_fee(long_side, l_index, u, total_quantity, price)
            fees[u] = fee

    return trans, fees


def get_trading_bids(
    bids,
    quantity_traded):
    """
    Finds the index of the rightmost trading
    bid in a side of the market.
    If the bid has to be split, it does so, and
    returns the a new bid dataframe with two bids
    in stade of the original one.

    Parameters
    ----------
    bids : pd.DataFrame
        Collection of bids in one side of the market
        Precondition: the dataframe is sorted by
        price. Reverse order for buying and selling
        side.

    quantity_traded : float
        Total quantity that the side of the market
        can trade.

    Returns
    -------
    bids_trading: pd.DataFrame
        Same as `bids`, but the index (which represent the
        bid identifier) is added as the first column.
        If a bid had to be splitted, that bid is replaced by two, with
        the quantity in both summing up to the original
        quantity. The index is reseted but both splitted
        bids retain the oringal bid number in the column.

    bid_index: int
        Index of the `worst` bid that gets to trade.

    Examples
    ---------

    No splitting needed

    >>> bm = pm.BidManager()
    >>> bm.add_bid(1, 3, 0)
    0
    >>> bm.add_bid(1, 2, 1)
    1
    >>> bm.get_df()
       quantity  price  user  buying  time  divisible
    0         1      3     0    True     0       True
    1         1      2     1    True     0       True
    >>> bids, index = get_trading_bids(bm.get_df(), 1)
    >>> bids
       bid  quantity  price  user  buying  time  divisible
    0    0         1      3     0    True     0       True
    1    1         1      2     1    True     0       True
    >>> index
    0

    Splitting needed:


    >>> bm = pm.BidManager()
    >>> bm.add_bid(1, 3, 0)
    0
    >>> bm.add_bid(1, 2, 1)
    1
    >>> bm.get_df()
       quantity  price  user  buying  time  divisible
    0         1      3     0    True     0       True
    1         1      2     1    True     0       True
    >>> bids, index = get_trading_bids(bm.get_df(), 0.3)
    >>> bids
       bid quantity price user buying time divisible
    0    0      0.3     3    0   True    0      True
    1    0      0.7     3    0   True    0      True
    2    1        1     2    1   True    0      True
    >>> index
    0

    """

    if bids.quantity.sum() > quantity_traded:
        bid_index = np.argmax(bids.quantity.cumsum().values >= quantity_traded)
    else:
        bid_index = bids.shape[0] - 1

    quantity_but_last = bids.iloc[: bid_index, :].quantity.sum()
    diff = quantity_traded - quantity_but_last
    if diff < bids.iloc[bid_index, :].quantity:
        new_row = pd.DataFrame(bids.iloc[bid_index, :]).T

        bids_trading = (pd.concat([
            bids.iloc[: bid_index, :],
            new_row,
            bids.iloc[bid_index:, :]
        ])
            .copy()
            .rename_axis('bid')
            .reset_index()
        )

        bids_trading.iloc[bid_index, 1] = diff
        bids_trading.iloc[bid_index + 1, 1] -= diff
    else:
        bids_trading = bids.copy().rename_axis('bid').reset_index()

    return bids_trading, bid_index


def compute_fee(
    df,
    index,
    user,
    quantity,
    price):
    """Computes the fee that a user has to pay by
    not letting others trade

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe for one side of the market
        resulting from reseting the index
        of a bid dataframe, getting the bid
        as the first column in addition to all the
        standard ones.
        Precondition: all bids should be willing
        to trade at the trading price.
    index : int
        Index of the last trading bid
    user : int
        User identifier for which the fee should be computed
    quantity : float
        Total quantity that the side of the
        market trades
    price : float
        Price at which the market clears.

    Returns
    -------
    fee : float
        Fee that user `ùser` will have to pay
        for not letting others trade as well.
    Examples
    --------

    >>> bm = pm.BidManager()
    >>> bm.add_bid(1, 1, 1)
    0
    >>> bm.add_bid(1, 2, 3)
    1
    >>> compute_fee(bm.get_df(), 0, 1, 1, 2.5)
    0.5
    """
    trades_without_user = df[(df.user != user)]
    if trades_without_user.shape[0] == 0:
        fee = 0
    else:
        if trades_without_user.quantity.sum() > quantity:
            new_index = np.argmax(
                trades_without_user.quantity.cumsum().values >= quantity)
        else:
            new_index = trades_without_user.shape[0] - 1

        new_winning = trades_without_user.iloc[: new_index + 1, :].copy()
        diff = quantity - new_winning.iloc[:-1, :].quantity.sum()
        if diff < new_winning.iloc[new_index, :].quantity:
            new_winning.iloc[new_index, 1] = diff

        pure_new = new_winning[new_winning.index > index]
        fee = (pure_new.price - price) * pure_new.quantity
        fee = np.abs(fee.sum())
    return fee


def find_competitive_price(bids):
    """
    Finds the unique trading price of the intersection
    of supply and demand.

    Parameters
    ----------
    bids: pd.DataFrame
        Collection of bids to process the
        mechanism with.

    Returns
    -------
    price : float
        The price at which the market clears.

    Notes
    ------
    See also: intersect_stepwise.
    """

    buy, _ = demand_curve_from_bids(bids)
    sell, _ = supply_curve_from_bids(bids)

    q_, b_, s_, price = intersect_stepwise(buy, sell)

    return price


class MudaAuction(Mechanism):

    """Interface for MudaAuction.

    Parameters
    -----------
    bids
        Collection of bids to run the mechanism
        with.
    """

    def __init__(self, bids, *args, **kwargs):
        """TODO: to be defined1. """
        Mechanism.__init__(self, muda, bids, *args, **kwargs)
