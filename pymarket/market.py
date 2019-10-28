from pymarket.bids import BidManager
from pymarket.mechanisms import *
from pymarket.transactions import TransactionManager
from pymarket.statistics import *
from pymarket.plot import plot_demand_curves, plot_trades_as_graph, plot_both_side_muda, plot_huang_auction
from collections import OrderedDict

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
    bm: BidManager
        All bids are stored in the bid manager
    transactions: TransactionManager
        The set of all tranasactions in the Market.
        This argument get updated after the market ran.
    extra: dict
        Extra information provided by the mechanisms.
        Gets updated after an execution of the run.

    Returns
    -------


    Examples
    ---------

    If everyone is buying, the transaction
    dataframe is returned empty as well as the extra
    dictionary.

    >>> mar = pm.Market()
    >>> mar.accept_bid(1, 2, 0, True)
    0
    >>> mar.accept_bid(2, 3, 1, True)
    1
    >>> trans, extra = mar.run('huang')
    >>> extra
    OrderedDict()
    >>> trans.get_df()
    Empty DataFrame
    Columns: [bid, quantity, price, source, active]
    Index: []

    If everyone is buying, the transaction
    dataframe is returned empty as well as the extra
    dictionary.

    >>> mar = pm.Market()
    >>> mar.accept_bid(1, 2, 0, False)
    0
    >>> mar.accept_bid(2, 3, 1, False)
    1
    >>> trans, extra = mar.run('huang')
    >>> extra
    OrderedDict()
    >>> trans.get_df()
    Empty DataFrame
    Columns: [bid, quantity, price, source, active]
    Index: []

    A very simple auction where nobody trades

    >>> mar = pm.Market()
    >>> mar.accept_bid(1, 3, 0, True)
    0
    >>> mar.accept_bid(1, 2, 1, False)
    1
    >>> trans, extra = mar.run('huang')
    >>> extra
    OrderedDict([('price_sell', 2.0), ('price_buy', 3.0), ('quantity_traded', 0)])
    >>> trans.get_df()
    Empty DataFrame
    Columns: [bid, quantity, price, source, active]
    Index: []

    """

    def __init__(self):
        """TODO: to be defined1."""
        self.bm = BidManager()
        self.transactions = TransactionManager()
        self.extra = OrderedDict()

    def accept_bid(self, *args):
        """Adds a bid to the bid manager

        Parameters
        ----------           
        *args :
            List of parameters requried to create a bid.
            See `BidManager` documentation.

        Returns
        -------
        bid_id: int
            The id of the new created bid in the BidManger
        
        """
        bid_id = self.bm.add_bid(*args)
        return bid_id

    def run(self, algo, *args, **kwargs):
        """Runs a given mechanism with the current
        bids

        Parameters
        ----------
        algo : str
            One of:
                * 'p2p'
                * 'huang'
                * 'muda'
            
        *args :
            Extra arguments to pass to the algorithm.

        **kwargs :
            Extra keyworded arguments to pass to the algorithm


        Returns
        -------
        transactions: TransactionManager
            The transaction manager holding all the transactions
            returned by the mechanism.
        extra: dict
            Dictionary with extra information returned by the
            executed method.

        
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
        stats = OrderedDict()
        extras = OrderedDict()
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
        """
        Plots a figure specific for a given method,
        reflecting the main characteristics of its solution.
        It requires that the algorithm has run before. 


        Parameters
        ----------
        method : str
            One of `p2p`, `muda`, `huang`
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
            try:
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
            except KeyError as e:
                print('Some of the parameters required were not found',
                'Make sure that the algorithm executed correctly.')
        elif method == 'huang':
            try:
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
            except KeyError as e:
                print('Some of the parameters required were not found',
                    'Make sure that the algorithm executed correctly.')
        return ax
