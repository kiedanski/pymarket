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
date: 17 May 2019
bibliography: paper.bib
---

# Summary

PyMarket is a python library designed to ease the simulation and
comparison of different market mechanisms.

Marketplaces can be proposed to solve a diverse array of problems. They
are used to sell ads online, bandwith spectrum, energy, etc.
PyMarket provides a simple environment to try, simulate and compare different
market mechanisms, a task that is inherent to the process of establishing a new
market.

As an example, Local Energy Markets (LEMs) have been proposed to syncronize energy consumption
with surplus of renewable generation. Several mechanisms have been proposed for such a market:
from double sided auctions to peer to peer trading. 

This library aims to provide a simple interface for such process, making results reproducible. In doing so,
it exposes a `Market` interface that accepts bids, runs market mechanisms algorithms to clear the market,
produces statistics about the results and plots the results.
An intuitive procedure is provided to implement new mechanisms and compare them with the existing ones.

Algorithms implemented in this library have been used by the authors [@horta2017, @kiedanski2019] as well as other researchers
in the field [@mengelkamp2017]. Moreover, the library is a key enabler of ongoing research in the LEMs.



# Acknowledgements

The code was developed in the context of Diego Kiedanski's PhD at Telecom ParisTech.

# References