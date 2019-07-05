import pandas as pd

from pymarket.bids.processing import merge_same_price
from pymarket.transactions.processing import split_transactions_merged_players


class Mechanism():

    """Implements a standard interface for mechanisms"""

    def __init__(self, algo,  bids, *args,  merge=False, **kwargs):
        """Creates a mechanisms with bids

        If 'merge', then bids with the same price in the
        same side will be merged

        Parameters
        ----------
        bids : TODO
        args: extra possible arguments


        """
        self.algo = algo
        self.args = args
        self.kwargs = kwargs
        self.merge = merge
        self.bids = self._sanitize_bids(bids)

    def _sanitize_bids(self, bids):
        """Adapts the bids to a friendly format

        Parameters
        ----------
        bids : TODO
            

        Returns
        -------

        
        """
        if self.merge:
            self.old_bids = bids
            new_bids, maping = merge_same_price(bids)
            self.maping = maping
        else:
            new_bids = bids

        return new_bids

    def _run(self):
        """Runs the mechanisms"""
        trans, extra = self.algo(self.bids, *self.args, **self.kwargs)
        return trans, extra
    
    def _cleanup(self,  trans):
        """Makes the necessary adjustements
        to return the transactions in a proper format

        Parameters
        ----------
        trans : TODO
            

        Returns
        -------

        
        """

        if self.merge:
            trans = split_transactions_merged_players(trans, self.old_bids, self.maping)

        return trans

    def run(self):
        """Runs the mechanisms"""
        trans, extra = self._run()
        trans = self._cleanup(trans)
        return trans, extra
