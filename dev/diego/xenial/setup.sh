#!/bin/bash
echo "Installing pymarket and requirements..."

apt update & apt install --yes python3-pip=8.1.1-2ubuntu0.4 pkg-config libfreetype6-dev libpng12-dev
python3 -m pip -V

echo "Installing setupttools"
python3 -m pip install 'setuptools>=27.3'
echo "Checking setuptools"
python3 -m pip freeze | grep setuptools

mkdir -p /home/vagrant
cd /home/vagrant
git clone -b python3.5 https://github.com/gus0k/pymarket.git
setfacl -m u:vagrant:rwx /home/vagrant/pymarket
cd pymarket
#python3 setup.py install
#python3 setup.py test
#python3 -m pip install https://github.com/gus0k/pymarket/archive/python3.5.zip
