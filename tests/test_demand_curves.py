import pytest
import numpy as np
from pymarket.bids import *

def test_demand_curve_from_bids_0(bid_dataset_0):
    df = bid_dataset_0
    demand_curve, order = demand_curve_from_bids(df)
    
    data = np.array([
       [2, 4],
       [3, 3],
       [8, 1],
       [np.inf, 0]
        ])


    assert np.allclose(demand_curve, data)
    assert np.allclose(order, np.array([1, 0, 2]))

    xs = [-1   , 0 , 1 , 2 , 2.5 , 3 , 4 , 8 , 1000 , np.inf]
    ys = [None , 4 , 4 , 4 , 3   , 3 , 1 , 1 , 0    , 0]

    for x, y in zip(xs, ys):
        f_ = get_value_stepwise(x, demand_curve)
        if y is not None:
            assert np.allclose(f_, y)
        else:
            assert y == f_

def test_supply_curve_from_bids_0(bid_dataset_0):
    df = bid_dataset_0
    demand_curve, order = supply_curve_from_bids(df)
    
    data = np.array([
       [1, 1],
       [5, 2],
       [10, 6],
       [np.inf, np.inf]
        ])


    assert np.allclose(demand_curve, data)
    assert np.allclose(order, np.array([4, 3, 5]))

    xs = [-1   , 0 , 1 , 2 , 2.5 , 5 , 7 , 10 , 10.001 , np.inf]
    ys = [None , 1 , 1 , 2 , 2   , 2 , 6 , 6  , np.inf , np.inf]

    for x, y in zip(xs, ys):
        f_ = get_value_stepwise(x, demand_curve)
        if y is not None:
            assert np.allclose(f_, y)
        else:
            assert y == f_


def test_equilibrium_quantity_0(bid_dataset_0):
    df = bid_dataset_0

    demand_curve, _ = demand_curve_from_bids(df)
    supply_curve, _ = supply_curve_from_bids(df)
    
    equilibrium_quantity, demand_index, supply_index, price = intersect_stepwise(
            demand_curve, supply_curve)

    assert np.allclose(equilibrium_quantity, 3)
    assert np.allclose(demand_index, 1)
    assert np.allclose(supply_index, 1)
    assert np.allclose(price, 2)

def test_equilibrium_quantity_1(bid_dataset_1):
    df = bid_dataset_1

    demand_curve, _ = demand_curve_from_bids(df)
    supply_curve, _ = supply_curve_from_bids(df)
    
    equilibrium_quantity, demand_index, supply_index, price = intersect_stepwise(
            demand_curve, supply_curve)

    assert np.allclose(equilibrium_quantity, 6)
    assert np.allclose(demand_index, 5)
    assert np.allclose(supply_index, 3)
    assert np.allclose(price, 5)
