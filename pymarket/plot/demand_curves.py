import matplotlib
matplotlib.use('Agg')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from pymarket.bids.demand_curves import demand_curve_from_bids, supply_curve_from_bids


def plot_demand_curves(bids, ax=None, margin_X=1.2, margin_Y=1.2):
    """Plots the demand curves.
    If ax is none, creates a new figure

    Parameters
    ----------
    bids
          Collection of bids to be used

    ax : TODO, optional
         (Default value = None)
    margin_X :
         (Default value = 1.2)
    margin_Y :
         (Default value = 1.2)

    Returns
    -------


    """

    if ax is None:
        fig, ax = plt.subplots()

    extra_X = 3
    extra_Y = 1

    dc = demand_curve_from_bids(bids)[0]
    sp = supply_curve_from_bids(bids)[0]

    x_dc = dc[:, 0]
    x_dc = np.concatenate([[0], x_dc])
    x_sp = np.concatenate([[0], sp[:, 0]])

    y_sp = sp[:, 1]
    y_dc = dc[:, 1]
    max_x = max(x_dc[-2], x_sp[-2])
    extra_X = max_x * margin_X

    x_dc[-1] = extra_X
    y_dc = np.concatenate([y_dc, [0]])
    max_point = y_dc.max() * margin_Y

    x_sp[-1] = extra_X
    y_sp[-1] = max_point
    y_sp = np.concatenate([y_sp, [y_sp[-1]]])

    ax.step(x_dc, y_dc, where='post', c='r', label='Demand')
    ax.step(x_sp, y_sp, where='post', c='b', label='Supply')
    ax.set_xlabel('Quantity')
    ax.set_ylabel('Price')
    ax.legend()
