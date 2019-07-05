import numpy as np
import pandas as pd
from typing import Tuple
from pymarket.bids import BidManager


def demand_curve_from_bids(bids: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
    """
    Creates a demand curve from a set of buying bids.
    It is the inverse cumulative distribution of quantity
    as a function of price.

    Parameters
    ----------
    bids
        Collection of all the bids in the market. The algorithm
        filters only the buying bids.

    Returns
    ---------
    demand_curve: np.ndarray
       Stepwise constant demand curve represented as a collection
       of the N rightmost points of each interval (N-1 bids). It is stored
       as a (N, 2) matrix where the first column is the x-coordinate
       and the second column is the y-coordinate.
       An extra point is added with x coordinate at infinity and
       price at 0 to represent the end of the curve.
    
    index : np.ndarray
        The order of the identifier of each bid in the demand
        curve.

    Examples
    ---------

    A minimal example, selling bid is ignored:

    >>> bm = pm.BidManager()
    >>> bm.add_bid(1, 1, 0, buying=True)
    0
    >>> bm.add_bid(1, 1, 1, buying=False)
    1
    >>> dc, index = pm.demand_curve_from_bids(bm.get_df())
    >>> dc
    array([[ 1.,  1.],
           [inf,  0.]])
    >>> index
    array([0])

    A larger example with reordering of bids:

    >>> bm = pm.BidManager()
    >>> bm.add_bid(1, 1, 0, buying=True)
    0
    >>> bm.add_bid(1, 1, 1, buying=False)
    1
    >>> bm.add_bid(3, 0.5, 2, buying=True)
    2
    >>> bm.add_bid(2.3, 0.1, 3, buying=True)
    3
    >>> dc, index = pm.demand_curve_from_bids(bm.get_df())
    >>> dc
    array([[1. , 1. ],
           [4. , 0.5],
           [6.3, 0.1],
           [inf, 0. ]])
    >>> index
    array([0, 2, 3])    

    """
    buying = bids[bids.buying == True]
    buying = buying.sort_values('price', ascending=False)
    buying['acum'] = buying.quantity.cumsum()
    demand_curve = buying[['acum', 'price']].values
    demand_curve = np.vstack([demand_curve, [np.inf, 0]])
    index = buying.index.values
    return demand_curve, index
    
def supply_curve_from_bids(bids):
    """
    Sorts selling bid by ascending price
    and creates an accumulation of them
    """
    selling = bids[bids.buying == False]
    selling = selling.sort_values('price')
    selling['acum'] = selling.quantity.cumsum()
    pairs = selling[['acum', 'price']].values
    pairs = np.vstack([pairs, [np.inf, np.inf]])
    index = selling.index.values
    return pairs, index


def get_value_stepwise(x, f):
    """
    Returns the value of a stepwise constant
    function defined by the right extrems
    of its interval
    Functions are assumed to be defined
    in (0, inf).
    :param x: x is the value to evaluate
    :param f: f is the function to be evaluated
    """
    if x < 0:
        return None

    for step in f:
        if x <= step[0]:
            return step[1] 


def intersect_stepwise(f, g, tiebreak=0.5):
    """
    Finds the intersection of
    two stepwise constants functions
    where f is assumed to be bigger at 0
    than g.
    If no intersection is found, None is returned
    tiebreak: if there is no intersection,
    is the lambda of a lienar combination between
    the two values
    """

    xs = sorted(list(set(g[:, 0]).union(set(f[:, 0]))))    
    fext = [get_value_stepwise(x, f) for x in xs]
    gext = [get_value_stepwise(x, g) for x in xs]
   
    x_ast = None
    for i in range(len(xs)):
        if (fext[i] > gext[i]) and (fext[i + 1] < gext[i + 1]):
            x_ast = xs[i]
        
    f_ast = np.argmax(f[:, 0] >= x_ast) if x_ast is not None else None
    g_ast = np.argmax(g[:, 0] >= x_ast) if x_ast is not None else None

    g_val = g[g_ast, 1]
    f_val  = f[f_ast, 1]
    
    intersect_domain_both = x_ast in f[:, 0] and x_ast in g[:, 0]
    if not intersect_domain_both:
        v = g_val if x_ast in f[:, 0] else f_val
    else:
        v = g_val * tiebreak + (1 - tiebreak) * f_val
    
    return x_ast, f_ast, g_ast, v


