import pandas as pd
import numpy as np

COLUMNS = ['bid', 'quantity', 'price', 'source', 'active']

class TransactionManager:
    """ """

    def __init__(self):
        self.n_trans = 0
        self.trans = []


    def add_transaction(self, bid, quantity, price, source, active):
        """Add a transaction to the transactions list

        Parameters
        ----------
        bid :
            id of the bid
        quantity :
            transacted quantity
        price :
            transacted price
        source :
            second party in the trasaction, -1 if there is
            no clear second party.
        active :
            True` if the bid is still active after the
            transaction.
            
            Returns:
            :trans_id: id of the added transaction, -1 if fails

        Returns
        -------

        """

        new_trans = (bid, quantity, price, source, active)
        self.trans.append(new_trans)
        self.n_trans += 1

        return self.n_trans - 1

    def get_df(self):
        """Returns the transaction dataframe

        Parameters
        ----------

        Returns
        -------
        
            df: dataframe with all the transactions

        """

        df = pd.DataFrame(self.trans, columns=COLUMNS)
        return df

    def merge(self, other):
        """Merges two transaction managers with each other

        Parameters
        ----------
        other : TransactionManager
            

        Returns
        -------

        
        """

        assert isinstance(other, TransactionManager)

        trans = TransactionManager()
        for t in self.trans:
            trans.add_transaction(*t)
        for t in other.trans:
            trans.add_transaction(*t)
        
        return trans
