#!/usr/bin/env bash

# install test etc.
python3 -m pip install pymarket --user
git clone https://github.com/gus0k/pymarket
cd pymarket
python3 -m pytest
