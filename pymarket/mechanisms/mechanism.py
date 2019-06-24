import pandas as pd


class Mechanism():

    """Implements a standard interface for mechanisms"""

    def __init__(self, algo,  bids, *args, **kwargs):
        """Creates a mechanisms with bids

        Parameters
        ----------
        bids : TODO
        args: extra possible arguments


        """
        self.algo = algo
        self.bids = self._sanitize_bids(bids) 
        self.args = args
        self.kwargs = kwargs

    def _sanitize_bids(self, bids):
        """Adapts the bids to a friendly format"

        Parameters
        ----------
        bids : TODO

        Returns
        -------
        TODO

        """
        return bids

    def _run(self):
        """Runs the mechanisms
        Returns
        -------
        TODO

        """
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
        TODO

        """
        return trans


    def run(self):
        """Runs the mechanisms
        Returns
        -------
        TODO

        """
        trans, extra = self._run()
        trans = self._cleanup(trans)
        return trans, extra
