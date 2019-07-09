from pymarket.bids import BidManager
from pymarket.mechanisms import *
from pymarket.transactions import TransactionManager
from pymarket.statistics import *
from pymarket.plot import plot_demand_curves, plot_trades_as_graph, plot_both_side_muda, plot_huang_auction

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
    market mechanisms

    Parameters
    ----------

    Returns
    -------

    """

    def __init__(self):
        """TODO: to be defined1."""
        self.bm = BidManager()

    def accept_bid(self, *args):
        """Adds a bid to the bid manager

        Parameters
        ----------
        bid : TODO
            
        *args :
            

        Returns
        -------

        
        """
        bid_id = self.bm.add_bid(*args)
        return bid_id

    def run(self, algo, *args, **kwargs):
        """Runs a given mechanism with the current
        bids

        Parameters
        ----------
        algo : TODO
            
        *args :
            
        **kwargs :
            

        Returns
        -------

        
        """
        df = self.bm.get_df()
        mec = MECHANISM[algo](df, *args, **kwargs)
        transactions, extra = mec.run()
        self.transactions = transactions
        self.extra = extra
        return transactions, extra

    def statistics(self, reservation_prices=None, exclude=[]):
        """Computes the standard statistics of the market

        Parameters
        ----------
        reservation_prices (dict, optional) :
            the reservation prices of the users. If there is none,
            the bid will be assumed truthfull
        reservation_prices :
             (Default value = None)
        exclude :
            List of mechanisms to ignore will comuting statistics

        Returns
        -------
        stats : dict
            Dictionary with the differnt statistics. Currently:
                * percentage_welfare
                * percentage_traded
                * profits

        
        """
        stats = {}
        extras = {}
        if 'fees' in self.extra:
            extras['fees'] = self.extra['fees']
        extras['reservation_prices'] = reservation_prices
        for stat in STATS:
            if stat not in exclude:
                stats[stat] = STATS[stat](
                    self.bm.get_df(),
                    self.transactions.get_df(),
                    **extras
                )
        self.stats = stats
        return stats

    def plot(self):
        """Plots both demand curves"""
        df = self.bm.get_df()
        plot_demand_curves(df)

    def plot_method(self, method, ax=None):
        """Plots all trades as a bipartite graph.
        It makes sense only for P2P

        Parameters
        ----------
        method :
            
        ax :
             (Default value = None)

        Returns
        -------

        
        """

        trans = self.transactions
        bids = self.bm
        e = self.extra
        if method == 'p2p':
            ax = plot_trades_as_graph(bids, trans, ax)
        elif method == 'muda':
            
            left_players = e['left']
            right_players = e['right']
            left_price = e['price_left']
            right_price = e['price_right']
            ax = plot_both_side_muda(
                bids,
                left_players,
                right_players,
                left_price,
                right_price)
        elif method == 'huang':
            price_sell = e['price_sell']
            price_buy = e['price_buy']
            quantity_traded = e['quantity_traded']
            ax = plot_huang_auction(
                bids,
                price_sell,
                price_buy,
                quantity_traded,
                ax
            )

        return ax
