from functools import wraps
import numpy as np

PRECISION = 8


def check_equal_price(f):
    """CHeck wheather there are two bids
    with the same price in the same side
    and in that case rises an error

    Parameters
    ----------
    f  :(function, mechanisms)
        Mechanisms to be tested


    Returns
    -------

    """
    @wraps(f)
    def wrapper(*args, **kwds):
        """

        Parameters
        ----------
        *args :

        **kwds :


        Returns
        -------

        """
        bids = args[0]

        buy = bids.loc[bids['buying'], :]
        sell = bids.loc[~bids['buying'], :]
        dfs = [buy, sell]

        for df in dfs:
            count = df.groupby(['price', 'user'])['user'].count()
            count = count > 1
            if count.any():
                raise NotImplementedError
        return f(*args, **kwds)
    return wrapper
