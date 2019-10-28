import pandas as pd

from pymarket.bids.processing import merge_same_price
from pymarket.transactions.processing import split_transactions_merged_players
from pymarket.transactions.transactions import TransactionManager
from collections import OrderedDict



class Mechanism():

    """Implements a standard interface for mechanisms

    Attributes
    -----------

    algo: Callable
        Algorithm to execute to solve the market.
    bids: pd.DataFrame
        Collection of bids to use, with processing.
    old_bids: pd.DataFrame
        Collection of bids previous to proecssing.
    maping: dict
        Map from the new bids to the old bids
    merge : bool
        Wheather to merge different players with
        the same price into one player. Useful for
        algorithms that require players to have different
        prices.

    Examples
    ---------

    Run p2p mechanism channging parameters with
    default parameters.

    >>> bm = pm.BidManager()
    >>> bm.add_bid(1, 3, 0)
    0
    >>> bm.add_bid(1, 0.5, 1)
    1
    >>> bm.add_bid(1, 1, 2, False)
    2
    >>> bm.add_bid(1, 2, 3, False)
    3
    >>> r = np.random.RandomState(420)
    >>> p2p = pm.mechanisms.p2p_random
    >>> mec = Mechanism(p2p, bm.get_df(), r=r)
    >>> trans, extra = mec.run()
    >>> extra
    {'trading_list': [[(0, 3), (1, 2)]]}
    >>> trans.get_df()
       bid  quantity  price  source  active
    0    0         1    2.5       3   False
    1    3         1    2.5       0   False
    2    1         0    0.0       2    True
    3    2         0    0.0       1    True

    >>> r = np.random.RandomState(420)
    >>> mec = Mechanism(p2p, bm.get_df(), r=r, p_coef=1)
    >>> trans, extra = mec.run()
    >>> extra
    {'trading_list': [[(0, 3), (1, 2)]]}
    >>> trans.get_df()
       bid  quantity  price  source  active
    0    0         1    3.0       3   False
    1    3         1    3.0       0   False
    2    1         0    0.0       2    True
    3    2         0    0.0       1    True
    """

    def __init__(self, algo, bids, *args, merge=False, **kwargs):
        """Creates a mechanisms with bids

        """
        self.algo = algo
        self.args = args
        self.kwargs = kwargs
        self.merge = merge
        self.bids = self._sanitize_bids(bids)

    def _sanitize_bids(self, bids):
        """
        Method to be overwritten by different
        mechanisms according to their needs
        in preprocessing.

        Parameters
        ----------
        bids: pd.DataFrame
            Collection of unprocess bids.

        Returns
        -------
        new_bids: pd.DataFrame
            The set of bids after processing.
        maping: dict
            Maping from new bids to old bids.


        Raises
        --------

        Examples
        ---------

        >>> bm = pm.BidManager()
        >>> bm.add_bid(1, 1, 0)
        0
        >>> bm.add_bid(0.5, 1, 1)
        1
        >>> mec = Mechanism(lambda: True, bm.get_df(), merge=True)
        >>> new_bids = mec._sanitize_bids(bm.get_df())
        >>> new_bids
           quantity  price  user  buying  time  divisible
        0       1.5      1   2.0     1.0   0.0        1.0
        >>> mec.maping
        {0: [0, 1]}
        """
        if self.merge:
            self.old_bids = bids
            new_bids, maping = merge_same_price(bids)
            # print(maping)
            self.maping = maping
        else:
            new_bids = bids

        return new_bids

    def _run(self):
        """Runs the mechanisms"""
        bids = self.bids
        N = bids.shape[0]
        if (bids.loc[bids['buying']].shape[0] not in [0, N]):
            trans, extra = self.algo(self.bids, *self.args, **self.kwargs)
            return trans, extra
        else:
            trans = TransactionManager()
            return trans, OrderedDict()

    def _cleanup(self, trans):
        """Makes the necessary adjustements
        to return the transactions in a proper format.

        If players where merged, all transactios with
        the merged player are splited into the corresponding
        amount of transactions for the original players.

        Parameters
        ----------
        trans : pd.DataFrame
            Collection of all the transactions executed
            in the market.


        Returns
        -------
        trans: pd.DataFrame
            The processed collection of transactions
            after the necesary adjustments.

        """

        if self.merge:
            trans = split_transactions_merged_players(
                trans, self.old_bids, self.maping)

        return trans

    def run(self):
        """Runs the mechanisms"""
        trans, extra = self._run()
        trans = self._cleanup(trans)
        return trans, extra
