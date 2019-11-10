import pandas as pd


class BidManager(object):
    """A class used to store and manipulate a collection
    of all the bids in the market.

    Attributes
    -----------
    col_names : :obj:`list` of :obj:`str`
        Column names for the different attributes in the dataframe
        to be created. Currently and in order: `quantity`, `price`,
        `user`, `buying`, `time`, `divisible`.
    n_bids : int
        Number of bids currently stored. Used as a unique identifier
        for each bid within a BidManager.
    bids : :obj:`list` of :obj:`tuple`
        A list where all the recieved bids are stored.
    """

    col_names = [
        'quantity',
        'price',
        'user',
        'buying',
        'time',
        'divisible',
    ]

    def __init__(self):
        self.n_bids = 0
        self.bids = []

    def add_bid(
        self,
        quantity,
        price,
        user,
        buying=True,
        time = 0,
        divisible=True
    ):
        """Appends a bid to the bid list

        Parameters
        ----------
        quantity: float
            Quantity of good desired. If `divisible=True` then any
            fraction of the good is an acceptable outcome of the
            market.
        price: float
            Uniform price offered in the market for each unit of the the good.
        user: int
            Identifier of the user submitting the bid.
        buying: bool
            `True` if the bid is for buying the good and `False`otherwise.
            Default is `True`.
        time : float
            Instant at which the offer was made. This is relevant only if the
            market mechanism has perferences for earlier bids. Default is `0`
        divisible : bool
            `True` is the user accepts a fraction of the asked quantity as
            a result and `False` otherwise.

        Returns
        -------
        int
            Unique identifier of the added bid.

        Examples
        --------
        >>> bm = pm.BidManager()
        >>> bm.add_bid(2, 1, 0)
        0
        """
        new_bid = (quantity, price, user, buying, time, divisible)
        self.bids.append(new_bid)
        self.n_bids += 1

        return self.n_bids - 1

    def get_df(self):
        """Creates a dataframe with the bids

        Parameters
        ----------

        Returns
        -------
        pd.DataFrame
            Dataframe with each row a different bid
            and each column each of the different attributes.

        Examples
        ---------
        >>> bm = pm.BidManager()
        >>> bm.add_bid(2, 1, 0)
        0
        >>> bm.add_bid(1, 3, 1, buying=False)
        1
        >>> print(bm.get_df())
           quantity  price  user  buying  time  divisible
        0         2      1     0    True     0       True
        1         1      3     1   False     0       True
        """

        df = pd.DataFrame(self.bids, columns=self.col_names)
        return df
