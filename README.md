
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




<div>
<style>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>quantity</th>
      <th>price</th>
      <th>user</th>
      <th>buying</th>
      <th>time</th>
      <th>divisible</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0.2374</td>
      <td>1.0234</td>
      <td>0</td>
      <td>True</td>
      <td>0</td>
      <td>True</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0.1784</td>
      <td>1.1770</td>
      <td>1</td>
      <td>True</td>
      <td>0</td>
      <td>True</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0.6301</td>
      <td>1.5789</td>
      <td>2</td>
      <td>True</td>
      <td>0</td>
      <td>True</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0.1600</td>
      <td>1.8008</td>
      <td>3</td>
      <td>True</td>
      <td>0</td>
      <td>True</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0.7920</td>
      <td>1.5478</td>
      <td>4</td>
      <td>True</td>
      <td>0</td>
      <td>True</td>
    </tr>
  </tbody>
</table>
</div>



### Run a market algorithm


```python
transactions, extra = mar.run('p2p', r=r)
transactions = transactions.get_df()
transactions.head()
```




<div>
<style>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>bid</th>
      <th>quantity</th>
      <th>price</th>
      <th>source</th>
      <th>active</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>12</td>
      <td>0.0786</td>
      <td>1.28745</td>
      <td>28</td>
      <td>False</td>
    </tr>
    <tr>
      <th>1</th>
      <td>28</td>
      <td>0.0786</td>
      <td>1.28745</td>
      <td>12</td>
      <td>True</td>
    </tr>
    <tr>
      <th>2</th>
      <td>8</td>
      <td>0.0000</td>
      <td>0.00000</td>
      <td>23</td>
      <td>True</td>
    </tr>
    <tr>
      <th>3</th>
      <td>23</td>
      <td>0.0000</td>
      <td>0.00000</td>
      <td>8</td>
      <td>True</td>
    </tr>
    <tr>
      <th>4</th>
      <td>13</td>
      <td>0.4147</td>
      <td>1.98175</td>
      <td>22</td>
      <td>False</td>
    </tr>
  </tbody>
</table>
</div>



## Documentation and Examples

[Docs can be found here (click me!)](https://pymarket.readthedocs.io)

# Installation

```python
pip install pymarket
```


```python

```
