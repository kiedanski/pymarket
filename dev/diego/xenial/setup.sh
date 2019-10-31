#!/bin/bash


echo "Installing pymarket and requirements..."

apt-get update
apt-get install --yes python3-pip=8.1.1-2ubuntu0.4
mkdir -p /home/vagrant
cd /home/vagrant
git clone -b python3.5 https://github.com/gus0k/pymarket.git
cd pymarket
python3 setup.py install
python3 setup.py test
#python3 -m pip install https://github.com/gus0k/pymarket/archive/python3.5.zip
