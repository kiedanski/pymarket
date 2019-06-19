import numpy as np
from bids import BidManager


def demand_curve_from_bids(bids):
    """
    Sorts buying bids by descending price
    and creates an accumulation of them
    """
    buying = bids[bids.buying == True]
    buying = buying.sort_values('price', ascending=False)
    buying['acum'] = buying.quantity.cumsum()
    pairs = buying[['acum', 'price']].values
    pairs = np.vstack([pairs, [np.inf, 0]])
    index = buying.index.values
    return pairs, index
    
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
        if x < step[0]:
            return step[1] 


def intersect_stepwise(f, g):
    """
    Finds the intersection of
    two stepwise constants functions
    where f is assumed to be bigger at 0
    than g.
    If no intersection is found, None is returned
    """

    xs = sorted(list(set(g[:, 0]).union(set(f[:, 0]))))    
    fext = [get_value_stepwise(x, f) for x in xs]
    gext = [get_value_stepwise(x, g) for x in xs]
    
    x_ast = None
    for i in range(len(xs)):
        if i == len(xs) - 1:
            x_ast = np.inf
        elif (fext[i] > gext[i]) and (fext[i + 1] < gext[i + 1]):
            x_ast = i + 1 
            break
    x_ast = xs[x_ast] if x_ast is not None else None
    f_ast = np.argmax(f[:, 0] >= x_ast) if x_ast is not None else None
    g_ast = np.argmax(g[:, 0] >= x_ast) if x_ast is not None else None

    return x_ast, f_ast, g_ast


if __name__ == '__main__':
    bm = BidManager()
    bm.add_bid(1, 3, 0, True, 0)
    bm.add_bid(2, 4, 1, True, 0)
    bm.add_bid(5, 1, 2, True, 0)

    bm.add_bid(4, 2, 3, False, 0)
    bm.add_bid(1, 1, 4, False, 0)
    bm.add_bid(5, 6, 5, False, 0)
    
    df = bm.get_df()

    buy, ib0 = demand_curve_from_bids(df)
    sell, is0 = supply_curve_from_bids(df)

    bm1 = BidManager()
    bm1.add_bid(2, 2.5, 0, True, 0)
    bm1.add_bid(2, 5, 1, True, 0)
    bm1.add_bid(2, 3, 2, True, 0)

    bm1.add_bid(2, 4, 3, False, 0)
    bm1.add_bid(1, 1, 4, False, 0)
    bm1.add_bid(2, 2, 5, False, 0)
    
    df1 = bm1.get_df()

    buy1, ib1 = demand_curve_from_bids(df1)
    sell1, ib2 = supply_curve_from_bids(df1)
