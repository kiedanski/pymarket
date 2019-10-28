import numpy as np
import pandas as pd
from pymarket.bids import BidManager


def demand_curve_from_bids(bids):
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
       An extra point is a))dded with x coordinate at infinity and
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
    buying = bids[bids.buying]
    buying = buying.sort_values('price', ascending=False)
    buying['acum'] = buying.quantity.cumsum()
    demand_curve = buying[['acum', 'price']].values
    demand_curve = np.vstack([demand_curve, [np.inf, 0]])
    index = buying.index.values.astype('int64')
    return demand_curve, index


def supply_curve_from_bids(bids):
    """
    Creates a supply curve from a set of selling bids.
    It is the cumulative distribution of quantity
    as a function of price.

    Parameters
    ----------
    bids: pd.DataFrame
        Collection of all the bids in the market. The algorithm
        filters only the selling bids.

    Returns
    ---------
    supply_curve: np.ndarray
       Stepwise constant demand curve represented as a collection
       of the N rightmost points of each interval (N-1 bids). It is stored
       as a (N, 2) matrix where the first column is the x-coordinate
       and the second column is the y-coordinate.
       An extra point is added with x coordinate at infinity and
       price at infinity to represent the end of the curve.

    index : np.ndarray
        The order of the identifier of each bid in the supply
        curve.

    Examples
    ---------

    A minimal example, selling bid is ignored:

    >>> bm = pm.BidManager()
    >>> bm.add_bid(1, 3, 0, False)
    0
    >>> bm.add_bid(2.1, 3, 3, True)
    1
    >>> sc, index = pm.supply_curve_from_bids(bm.get_df())
    >>> sc
    array([[ 1.,  3.],
           [inf, inf]])
    >>> index
    array([0])

    A larger example with reordering:

    >>> bm = pm.BidManager()
    >>> bm.add_bid(1, 3, 0, False)
    0
    >>> bm.add_bid(2.1, 3, 3, True)
    1
    >>> bm.add_bid(0.2, 1, 3, False)
    2
    >>> bm.add_bid(1.7, 6, 4, False)
    3
    >>> sc, index = pm.supply_curve_from_bids(bm.get_df())
    >>> sc
    array([[0.2, 1. ],
           [1.2, 3. ],
           [2.9, 6. ],
           [inf, inf]])
    >>> index
    array([2, 0, 3])


    """
    selling = bids[bids.buying == False]
    selling = selling.sort_values('price')
    selling['acum'] = selling.quantity.cumsum()
    supply_curve = selling[['acum', 'price']].values
    supply_curve = np.vstack([supply_curve, [np.inf, np.inf]])
    index = selling.index.values.astype('int64')
    return supply_curve, index


def get_value_stepwise(x, f):
    """
    Returns the value of a stepwise constant
    function defined by the right extrems
    of its interval
    Functions are assumed to be defined
    in (0, inf).

    Parameters
    ----------
    x: float
        Value in which the function is to be
        evaluated
    f: np.ndarray
        Stepwise function represented as a 2 column
        matrix. Each row is the rightmost extreme
        point of each constant interval. The first column
        contains the x coordinate and is sorted increasingly.
        f is assumed to be defined only in the interval
        :math: (0, \infty)
    Returns
    --------
    float or None
        The image of x under f: `f(x)`. If `x` is negative,
        then None is returned instead. If x is outside
        the range of the function (greater than `f[-1, 0]`),
        then the method returns None.

    Examples
    ---------
    >>> f = np.array([
    ...     [1, 1],
    ...     [3, 4]])
    >>> [pm.get_value_stepwise(x, f)
    ...     for x in [-1, 0, 0.5, 1, 2, 3, 4]]
    [None, 1, 1, 1, 4, 4, None]

    """
    if x < 0:
        return None

    for step in f:
        if x <= step[0]:
            return step[1]


def intersect_stepwise(
        f,
        g,
        k=0.5
    ):
    """
    Finds the intersection of
    two stepwise constants functions
    where f is assumed to be bigger at 0
    than g.
    If no intersection is found, None is returned.

    Parameters
    ----------
    f: np.ndarray
        Stepwise constant function represented as
        a 2 column matrix where each row is the rightmost
        point of the constat interval. The first column
        is sorted increasingly.
        Preconditions: f is non-increasing.

    g: np.ndarray
        Stepwise constant function represented as
        a 2 column matrix where each row is the rightmost
        point of the constat interval. The first column
        is sorted increasingly.
        Preconditions: g is non-decreasing and
        `f[0, 0] > g[0, 0]`
    k : float
        If the intersection is empty or an interval,
        a convex combination of the y-values of f and g
        will be returned and k will be used to determine
        hte final value. `k=1` will be the value of g
        while `k=0` will be the value of f.

    Returns
    --------
    x_ast : float or None
        Axis coordinate of the intersection of both
        functions. If the intersection is empty,
        then it returns None.
    f_ast : int or None
        Index of the rightmost extreme
        of the interval of `f` involved in the
        intersection. If the intersection is
        empty, returns None
    g_ast : int or None
        Index of the rightmost extreme
        of the interval of `g` involved in the
        intersection. If the intersection is
        empty, returns None.
    v : float or None
        Ordinate of the intersection if it
        is uniquely identified, otherwise
        the k-convex combination of the
        y values of `f` and `g` in the last
        point when they were both defined.

    Examples
    ---------
    Simple intersection with diferent domains

    >>> f = np.array([[1, 3], [3, 1]])
    >>> g = np.array([[2,2]])
    >>> pm.intersect_stepwise(f, g)
    (1, 0, 0, 2)

    Empty intersection, returning the middle value

    >>> f = np.array([[1,3], [2, 2.5]])
    >>> g = np.array([[1,1], [2, 2]])
    >>> pm.intersect_stepwise(f, g)
    (None, None, None, 2.25)
    """
    x_max = np.min([f.max(axis=0)[0], g.max(axis=0)[0]])
    xs = sorted([x for x in set(g[:, 0]).union(set(f[:, 0])) if x <= x_max])
    fext = [get_value_stepwise(x, f) for x in xs]
    gext = [get_value_stepwise(x, g) for x in xs]
    x_ast = None
    for i in range(len(xs) - 1):
        if (fext[i] > gext[i]) and (fext[i + 1] < gext[i + 1]):
            x_ast = xs[i]

    f_ast = np.argmax(f[:, 0] >= x_ast) if x_ast is not None else None
    g_ast = np.argmax(g[:, 0] >= x_ast) if x_ast is not None else None

    g_val = g[g_ast, 1] if g_ast is not None else get_value_stepwise(xs[-1], g)
    f_val = f[f_ast, 1] if f_ast is not None else get_value_stepwise(xs[-1], f)

    intersect_domain_both = x_ast in f[:, 0] and x_ast in g[:, 0]
    if not (intersect_domain_both) and (x_ast is not None):
        v = g_val if x_ast in f[:, 0] else f_val
    else:
        v = g_val * k + (1 - k) * f_val

    return x_ast, f_ast, g_ast, v
