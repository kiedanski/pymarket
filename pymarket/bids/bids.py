import pandas as pd

COLUMNS = ['quantity', 'price', 'user', 'buying', 'time',
        'divisible']

class BidManager:

    def __init__(self):
        self.n_bids = 0
        self.bids = []

    def add_bid(self, quantity: float, price: float, user: int, buying: bool,
            time: float, divisible=True):
        """
        Appends a bid to the bid list
        :param quantity: desired quantity, if divisible is `True`, then any
        fraction of it is acceptable
        :param price: limit price at which to trade
        :param user: user id
        :param buying: boolelan indicating if the bid is for buying or selling.
        :param time: time at which the offer was added
        :param divisible: whether the quantity is divisible or not.

        Returns:
        :bid_id: the id of the added bid or -1 if the bid was not added.

        """
        new_bid = (quantity, price, user, buying, time, divisible)
        self.bids.append(new_bid)
        self.n_bids += 1
        
        return self.n_bids - 1


    def get_df(self):
        """
        Creates a dataframe with the bids
        Returns:
        :df: Dataframe with all the bids
        """

        df = pd.DataFrame(self.bids, columns=COLUMNS)
        return df
