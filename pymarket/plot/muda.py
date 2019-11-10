import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pymarket.plot.demand_curves import plot_demand_curves


def plot_both_side_muda(
        bids, left_players, right_players, left_price,
        right_price, FIGSIZE=(12, 6), **kwargs):
    """Plots the two sides in which MUDA divides the trades with the
    corresponding prices

    Parameters
    ----------
    bids (pandas dataframe):
        Table with all the bids submitted
    left (list):
        List of players in the left side
    right (list):
        List of players in the right side
    left_price (float):
        Price obtained from the left side to be used in the right side
    right_price (float):
        Price obtained from the right side to be used in the left side
    FIGSIZE (tuple):
        Tuple (width, height) of the figure to be created

    Returns
    -------
     axe : matplotlib.axes._subplots.AxesSubplot
        The axe in which the figure was plotted.
    """
    bids = bids.get_df()
    fig, ax = plt.subplots(1, 2, figsize=FIGSIZE)
    plot_demand_curves(bids[bids.index.isin(left_players)], ax=ax[0])
    ax[0].axhline(right_price, linestyle='--', c='k',
                  label='Trading price determined by right players')
    ax[0].legend()
    ax[0].set_title('Left players')

    plot_demand_curves(bids[bids.index.isin(right_players)], ax=ax[1])
    ax[1].axhline(
        left_price,
        linestyle='--',
        c='k',
        label='Trading price determined by left players')
    ax[1].legend()
    _ = ax[1].set_title('Right players')

    return ax
