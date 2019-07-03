import numpy as np
from pymarket.statistics import *

def test_maxiumum_aggregated_utility_dataset_0(bid_dataset_0):

    df = bid_dataset_0
    status, objective, variables = maximum_aggregated_utility(df)
    assert status == 'Optimal'
    assert np.allclose(objective, 6)
