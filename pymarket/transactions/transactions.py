import pandas as pd
import numpy as np

COLUMNS = ['bid', 'quantity', 'price', 'source', 'active']

class TransactionManager:

    def __init__(self):
        self.n_trans = 0
        self.trans = []


    def add_transaction(self, bid, quantity, price, source, active):
        """
        Add a transaction to the transactions list
        :param bid: id of the bid
        :param quantity: transacted quantity
        :param price: transacted price
        :param source: second party in the trasaction, -1 if there is
        no clear second party.
        :param active: `True` if the bid is still active after the
        transaction.

        Returns:
        :trans_id: id of the added transaction, -1 if fails

        """

        new_trans = (bid, quantity, price, source, active)
        self.trans.append(new_trans)
        self.n_trans += 1

        return self.n_trans - 1


    def get_df(self):
        """
        Returns the transaction dataframe

        Returns:
        :df: dataframe with all the transactions

        """

        df = pd.DataFrame(self.trans, columns = COLUMNS)
        return df
