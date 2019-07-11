
# PyMarket

[![Build Status](https://travis-ci.org/gus0k/pymarket.svg?branch=master)](https://travis-ci.org/gus0k/pymarket)

[![Documentation Status](https://readthedocs.org/projects/pymarket/badge/?version=latest)](https://pymarket.readthedocs.io/en/latest/?badge=latest)

[![PyPI version](https://badge.fury.io/py/pymarket.svg)](https://badge.fury.io/py/pymarket)

PyMarket is a python library designed to ease the simulation and
comparison of different market mechanisms.

Marketplaces can be proposed to solve a diverse array of problems. They
are used to sell ads online, bandwith spectrum, energy, etc.
PyMarket provides a simple environment to try, simulate and compare different
market mechanisms, a task that is inherent to the process of establishing a new
market.

As an example, Local Energy Markets (LEMs) have been proposed to syncronize energy consumption
with surplus of renewable generation. Several mechanisms have been proposed for such a market:
from double sided auctions to p2p trading. 

This library aims to provide a simple interface for such process, making results reproducible.

## Getting Started


```python
import pymarket as pm
import numpy as np

r = np.random.RandomState(1234)

mar = pm.Market()
bids = pm.datasets.uniform_bidders.generate(20, 20, 1, 1, r)
for b in bids:
    mar.accept_bid(*b)
    
mar.plot()
```


![png](README_files/README_4_0.png)


### Access the bids


```python
bids = mar.bm.get_df()
bids.head()
```




       quantity   price  user  buying  time  divisible
    0    0.2374  1.0234     0    True     0       True
    1    0.1784  1.1770     1    True     0       True
    2    0.6301  1.5789     2    True     0       True
    3    0.1600  1.8008     3    True     0       True
    4    0.7920  1.5478     4    True     0       True



### Run a market algorithm


```python
transactions, extra = mar.run('p2p', r=r)
transactions = transactions.get_df()
transactions.head()
```




       bid  quantity   price  source  active
    0   16    0.0000  0.0000      34    True
    1   34    0.0000  0.0000      16    True
    2    0    0.0000  0.0000      23    True
    3   23    0.0000  0.0000       0    True
    4   12    0.0786  1.3828      26   False



## Documentation and Examples

[Docs can be found here (click me!)](https://pymarket.readthedocs.io)

# Installation

```python
pip install pymarket
```
