import numpy as np
import pandas as pd
from pymarket.bids import BidManager, merge_same_price
from pymarket.transactions import TransactionManager, \
    split_transactions_merged_players
from pymarket.bids.demand_curves import *
from pymarket.mechanisms import Mechanism
from pymarket.utils.decorators import check_equal_price


@check_equal_price
def muda(bids, r=None):
    '''
    Implements MUDA as describes in paper...

    '''
    if r is None:
        r = np.random.RandomState()
        print('Es None')
    
    
    #r = np.random.RandomState() if r is None else r
    left = [i for i in bids.index if r.rand() > 0.5]
    right = [i for i in bids.index if i not in left]

    pl = find_competitive_price(bids.loc[left])
    pr = find_competitive_price(bids.loc[right])

    fees = np.zeros(bids.user.unique().shape[0])

    trans_left, fees = solve_market_side_with_exogenous_price(
        bids.loc[left], pr, fees, r)
    trans_right, fees = solve_market_side_with_exogenous_price(
        bids.loc[right], pl, fees, r)

    trans = trans_left.merge(trans_right)

    extra = {
            'left': left,
            'right': right,
            'price_left': pl,
            'price_right': pr,
            'fees': fees
            }
    return trans, extra


def solve_market_side_with_exogenous_price(bids, price, fees, r):
    """
    Finds who trades and at what price based on the
    exogeneous price
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
    # print(total_quantity)
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

        # trading_bids = [maping[x] for x in long_side.index if x <= l_index]

        # trans = split_transactions_merged_players(trans, df, maping)

        trading_users_long_side = (
            long_side[long_side.index <= l_index]
            .user
            .unique()
        )
        # fees_ = {}
        for u in trading_users_long_side:

            fee = compute_fee(long_side, l_index, u, total_quantity, price)
            if supply_long:
                fees[u] = -fee
            else:
                fees[u] = fee
        # print(fees_)
        # trans, fees_ = split_transactions_merged_players(
        # trans, df, maping, fees_)
        # for k, v in fees_.items():
        #    fees[k] = v

    return trans, fees


def get_trading_bids(bids, quantity_traded):
    """
    Finds the index of the rightmost trading
    bid and splits it in two if the quantity
    traded falls in the middle of the bid

    Parameters
    ----------
    bids: bids of one side of the market
    quantity_traded: quantity that clears the market

    Returns
    -------
    bids_trading: dataframe
        dataframe that is a copy of bids but might
        have the rightmost bid splitted in half
    bid_index: int
        index of the last trading bid in the returned dataset

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


def compute_fee(df, index, user, quantity, price):
    """
    Compute the fee that a user has to pay by
    not letting others trade

    Parameters
    ----------

    df: dataframe
        Dataframe resulting from reseting the index
        of a bid dataframe
    index: int
        Index of the last trading bid
    user: int
        User for which the fee should be computed
    quantity: int
        Total quantity to be traded
    price: int
        Price at which trade ocurrs

    Returns
    --------

    fee: float
        Fee to be paid by the user
    """

    trades_without_user = df[(df.user != user)]
    if trades_without_user.shape[0] == 0:
        # Only one player in the side of the market
        fee = 0
    else:
        if trades_without_user.quantity.sum() > quantity:
            new_index = np.argmax(
                trades_without_user.quantity.cumsum().values >= quantity)
        else:
            new_index = trades_without_user.shape[0] - 1

        new_winning = trades_without_user.iloc[: new_index + 1, :].copy()
        # print('------------', index, quantity, price)
        # print(trades_without_user, '\n', new_index, '\n', new_winning)
        diff = quantity - new_winning.iloc[:-1, :].quantity.sum()
        if diff < new_winning.iloc[new_index, :].quantity:
            new_winning.iloc[new_index, 1] = diff

        pure_new = new_winning[new_winning.index > index]
        #  print('PUREEEE NEWWWW', index, pure_new)

        fee = (pure_new.price - price) * pure_new.quantity
        fee = fee.sum()

    return fee


def find_competitive_price(bids):
    """
    Finds the unique trading price of the intersection
    of supply and demand
    """

    buy, _ = demand_curve_from_bids(bids)
    sell, _ = supply_curve_from_bids(bids)

    q_, b_, s_, price = intersect_stepwise(buy, sell)

    return price


class MudaAuction(Mechanism):

    """Docstring for MudaAuction. """

    def __init__(self, bids, *args, **kwargs):
        """TODO: to be defined1. """
        Mechanism.__init__(self, muda, bids, *args, **kwargs)
