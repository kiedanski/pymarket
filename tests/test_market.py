import numpy as np
from pymarket import Market


def test_market_init():
    """Tests that the market can be initialized
    and bids added
    Returns
    -------
    TODO

    """

    # Initialize the dataset
    mar = Market()

    mar.accept_bid(1, 4, 0, True, 0)
    mar.accept_bid(1, 3, 1, True, 0)
    mar.accept_bid(1, 2, 2, True, 0)
    mar.accept_bid(1, 1, 3, True, 0)
    mar.accept_bid(1, 1, 10, False, 0)
    mar.accept_bid(1, 2, 11, False, 0)
    mar.accept_bid(1, 3, 12, False, 0)
    
    algos = ['huang', 'muda', 'p2p']
    
    trans = {}
    extras = {}
    stats = {}
    ## Run the three algorithms
    for al in algos:
        if al != 'huang':
            r = np.random.RandomState(1234)
            tr, ex = mar.run(al, r=r)
            st = mar.statistics()
        else:
            tr, ex = mar.run(al)
            st = mar.statistics()
        trans[al] = tr
        extras[al] = ex
        stats[al] = st
    
    for al in algos:
        print(al, extras[al])
        print(al, trans[al].get_df())
        print(al, stats[al])
    #### Test MUDA
    ####################

    true_trans = np.array([
       [4 , 1.0 , 3.0 , -1 , False] ,
       [1 , 1.0 , 3.0 , -1 , False] ,
       [5 , 1.0 , 2.0 , -1 , False] ,
       [0 , 1.0 , 2.0 , -1 , False] ,
        ]).astype(float)

    res_trans = trans['muda'].get_df().astype(float)
    assert np.allclose(true_trans, res_trans)
    assert np.allclose(stats['muda']['percentage_traded'], 2/3)
    assert np.allclose(stats['muda']['percentage_welfare'], 1)
    ###################3


    #### Test HUANG
    ###################

    
    true_trans = np.array([
       [4 , 1.0 , 2.0 , -1 , False] ,
       [0 , 1.0 , 3.0 , -1 , False] ,
        ]).astype(float)

    res_trans = trans['huang'].get_df().astype(float)
    assert np.allclose(true_trans, res_trans)
    assert np.allclose(stats['huang']['percentage_traded'], 1/3)
    assert np.allclose(stats['huang']['percentage_welfare'], 1/2)
    #### Test P2P
    ###################



    true_trans = np.array([
       [1 , 1.0 , 2.0 , 4 , False] ,
       [4 , 1.0 , 2.0 , 1 , False] ,
       [3 , 0   , 0   , 6 , True]  ,
       [6 , 0   , 0   , 3 , True]  ,
       [0 , 1   , 3   , 5 , False] ,
       [5 , 1   , 3   , 0 , False] ,
       [2 , 0   , 0   , 6 , True]  ,
       [6 , 0   , 0   , 2 , True]  ,

        ]).astype(float)

    res_trans = trans['p2p'].get_df().astype(float)
    assert np.allclose(true_trans, res_trans)
    assert np.allclose(stats['p2p']['percentage_traded'], 2/3)
    assert np.allclose(stats['p2p']['percentage_welfare'], 1)


    ##################
