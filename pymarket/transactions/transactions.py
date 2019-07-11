import pandas as pd
import numpy as np


class TransactionManager:
    """
    An interaface to store and
    manage all transactions.
    Transactions are the minimal unit to represent
    the outcome of a market.

    Attributes
    -----------
    name_col: list of str
        Name of the columns to use in the dataframe
        returned.
    n_trans: int
        Number of transactions currently in the Manager
    trans: list of tuples
        List of the actual transactions available
    """

    name_col = ['bid', 'quantity', 'price', 'source', 'active']

    def __init__(self):
        """
        """
        self.n_trans = 0
        self.trans = []

    def add_transaction(self, bid, quantity, price, source, active):
        """Add a transaction to the transactions list

        Parameters
        ----------
        bid : int
            Unique identifier of the bid
        quantity : float
            transacted quantity
        price : float
            transacted price
        source : int
            Identifier of the second party in the trasaction,
            -1 if there is no clear second party, such as
            in a double auction.
        active :
            True` if the bid is still active after the
            transaction.

        Returns
        --------
        trans_id: int
            id of the added transaction, -1 if fails

        Examples
        ---------

        >>> tm = pm.TransactionManager()
        >>> tm.add_transaction(1, 0.5, 2.1, -1, False)
        0
        >>> tm.trans
        [(1, 0.5, 2.1, -1, False)]
        >>> tm.n_trans
        1
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
        df: pd.DataFrame
            A pandas dataframe representing all the transactions
            stored.

        Examples
        ---------
        >>> tm = pm.TransactionManager()
        >>> tm.add_transaction(1, 0.5, 2.1, -1, False)
        0
        >>> tm.add_transaction(5, 0, 0, 3, True)
        1
        >>> tm.get_df()
           bid  quantity  price  source  active
        0    1       0.5    2.1      -1   False
        1    5       0.0    0.0       3    True
        """

        df = pd.DataFrame(self.trans, columns=self.name_col)
        return df

    def merge(self, other):
        """
        Merges two transaction managers with each other
        There are no checks on whether the new
        TransactionManger is consisten after the
        merge.

        Parameters
        ----------
        other : TransactionManager
            A different transaction manager to merge
            with

        Returns
        -------
        trans : TransactionManager
            A new transaction Manager
            with the transactions of the two.

        Examples
        ---------
        >>> tm_1 = pm.TransactionManager()
        >>> tm_1.add_transaction(1, 0.5, 2.1, -1, False)
        0
        >>> tm_2 = pm.TransactionManager()
        >>> tm_2.add_transaction(5, 0, 0, 3, True)
        0
        >>> tm_3 = tm_1.merge(tm_2)
        >>> tm_3.get_df()
           bid  quantity  price  source  active
        0    1       0.5    2.1      -1   False
        1    5       0.0    0.0       3    True

        """

        assert isinstance(other, TransactionManager)

        trans = TransactionManager()
        for t in self.trans:
            trans.add_transaction(*t)
        for t in other.trans:
            trans.add_transaction(*t)

        return trans
