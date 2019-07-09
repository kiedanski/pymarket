=====
Quickstart
=====

A minimal example
------------------

.. code:: python

    import pymarket as pm

    mar = pm.Market() # Creates a new market

    mar.accept_bid(1, 2, 0, True) # User 0 want to buy (True) 1 unit at price 2 
    mar.accept_bid(2, 1, 1, False) # User 1 wants to sell (False) 2 units at price 2

    transactions, extras = mar.run('p2p') # run the p2p mechanism with the 2 bids

    df = transactions.get_df() # obtain a dataframe with the summary of all transactions


