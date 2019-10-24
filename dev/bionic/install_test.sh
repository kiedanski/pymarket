#!/usr/bin/env bash

# install, upgrade etc.
pip3 install --user --upgrade pip
pip3 install --user pymarket

# Now to run the tests
git clone git://github.com/gus0k/pymarket
pushd pymarket
pip3 install --user -r requirements_dev.txt
make test
popd
