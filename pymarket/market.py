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
    'profits': calculate_profits,
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
        self.transactions = transactions
        self.extra = extra
        return transactions, extra

    def statistics(self, reservation_prices=None):
        """
        Computes the standard statistics of the market

        Parameters
        -----------
        reservation_prices (dict, optional):
            the reservation prices of the users. If there is none,
            the bid will be assumed truthfull
        
        Returns
        --------
        stats (dict):
            Dictionary with the different statistics calculated
        """
        stats = {}
        extras = {}
        if 'fees' in self.extra:
            extras['fees'] = self.extra['fees']
        extras['reservation_price'] = reservation_prices
        for stat in STATS:
            stats[stat] = STATS[stat](
                self.bm.get_df(),
                self.transactions.get_df(),
                **extras
            )
        self.stats = stats
        return stats

    def plot(self):
        """Plots both demand curves
        Returns
        -------
        TODO

        """
        df = self.bm.get_df()
        plot_demand_curves(df)
