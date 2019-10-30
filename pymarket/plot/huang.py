import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from pymarket.plot.demand_curves import plot_demand_curves


def plot_huang_auction(bids, price_sell, price_buy, quantity_traded, ax=None):
    """Plots the results of the huang auction with some of the characteristics
    of such auction

    Parameters
    ----------
    bids (pandas dataframe):
        Table with all the bids submitted
    price_sell (list):
        The price at which all sellers sell
    price_buy (list):
        The price at which all players buy
    quantity traded (float):
        The total quantity traded

    Returns
    -------
    axe : matplotlib.axes._subplots.AxesSubplot
        The axe in which the figure was plotted.


    """
    bids = bids.get_df()
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 8))
    plot_demand_curves(bids, ax=ax)
    ax.axhline(price_sell, linestyle='--', c='k', label='Sell price')
    ax.axhline(price_buy, linestyle='-.', c='k', label='Buy price')
    ax.axvline(quantity_traded, linestyle='--', c='k', label='Quantity traded')
    ax.fill_between(
        np.arange(
            0,
            quantity_traded,
            0.01),
        y1=price_buy,
        y2=price_sell,
        alpha=0.3,
        label='Market profit')
    ax.legend()

    return ax
