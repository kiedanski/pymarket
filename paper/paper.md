---
title: 'PyMarket - A simple library for simulating markets in Python'
tags:
  - Python
  - Market
  - Mechanism Design
authors:
  - name: Diego Kiedanski
    orcid: 0000-0001-8041-9685
    affiliation: 1
  - name: Daniel Kofman
    orcid: 0000-0002-7337-050X
    affiliation: 1
  - name: José Horta
    affiliation: 2
affiliations:
 - name: Telecom ParisTech
   index: 1
 - name: ICT4V
   index: 2
date: 16 July 2019
bibliography: paper.bib
---

# Summary

PyMarket is a python library aimed to ease the design, simulation and comparison of different market mechanisms.

Marketplaces have been proposed to solve a diverse array of problems. They are currently used to sell ads online, allocate bandwidth spectrum, exchange energy, etc. PyMarket provides a simple environment to try, simulate, compare and visualize different market mechanisms; a task that is inherent to the process of market design.

This library was not intended for its use in financial domain, where mature tools already exist[^1] such as [@simulation],[@builder]. Instead, it was targeted for the engineering domain in which markets are sometimes used for interfacing the interaction of multi-agent systems.

As an example, Local Energy Markets (LEMs) have been proposed to synchronize energy consumption with surplus of renewable generation. Several mechanisms have been proposed for such markets: from discrete-time double sided auctions to continuous peer to peer trading.

This library aims to provide a simple interface for such process, making results reproducible. In doing so, it exposes a Market interface that accepts bids, runs market clearing algorithms, and produces statistics  and plots (Figure \ref{figure}) from the results. Moreover, an intuitive procedure is provided to implement new market mechanisms and compare them with existing ones.

![png\label{figure}](../README_files/README_4_0.png)

Algorithms implemented in this library have been used by the authors [@horta2017] [@kiedanski2019] as well as other researchers in the field [@mengelkamp2017]. Moreover, the library is a key enabler of ongoing research in the LEMs.

# List of Implemented Algorithms
* Huang et.al. Double Auction [@huangauction].
* MUDA [@segal2018muda].
* P2P random trading based on [@blouin2001decentralized], [@mengelkamp2017].


# Acknowledgements

The code was developed in the context of Diego Kiedanski's PhD at Telecom ParisTech.

[^1]: See also: https://github.com/fiquant/marketsimulator


# References
