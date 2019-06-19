import numpy as np


def generate_random_bid(r=None):

    if r is None:
        r = np.random.RandomState()

    q = r.uniform(0, 2)
    p = r.uniform(0, 2)
    user = r.randint(0, 1000000)
    time = 0
    buying = r.rand() < 0.5
    divisible = True

    return q, p, user, buying, time, divisible
