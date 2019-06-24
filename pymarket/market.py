from pymarket.bids import BidManager
from pymarket.mechanisms import *
from pymarket.transactions import TransactionManager
from pymarket.statistics import *
from pymarket.plot import plot_demand_curves

MECHANISM = {
    'huang': HuangAuction,        
    'muda': MudaAuction,
    'p2p': P2PTrading,
}

STATS = {
        
        'percentage_traded': percentage_traded,
        'percentage_welfare': percentage_welfare,
}

class Market():

    """General interface for calling the different
    market mechanisms"""

    def __init__(self):
        """TODO: to be defined1."""
        self.bm = BidManager()

    def accept_bid(self, *args):
        """Adds a bid to the bid manager
 
        Parameters
        ----------
        bid : TODO
 
        Returns
        -------
        TODO
 
        """
        self.bm.add_bid(*args) 
        return 1
     
    def run(self, algo, *args, **kwargs):
        """Runs a given mechanism with the current
        bids

        Parameters
        ----------
        algo : TODO

        Returns
        -------
        TODO

        """
        df = self.bm.get_df()
        mec = MECHANISM[algo](df, *args, **kwargs)
        transactions, extra = mec.run()
        stats = {}
        for stat in STATS:
            stats[stat] = STATS[stat](df, transactions.get_df())
        return transactions, extra, stats
    def plot(self):
        """Plots both demand curves
        Returns
        -------
        TODO

        """
        df = self.bm.get_df()
        plot_demand_curves(df)
