import numpy as np
from pymarket.statistics import *

def test_maxiumum_traded_volume_dataset_0(bid_dataset_0):

    df = bid_dataset_0
    status, objective, variables = maximum_traded_volume(df)
    assert status == 'Optimal'
    assert np.allclose(objective, 4)
