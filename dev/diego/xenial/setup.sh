#!/bin/bash


echo `ps aux | grep [a]pt`

echo "Installing pymarket and requirements..."



apt-get update
apt-get install --yes python3-pip=8.1.1-2ubuntu0.4
apt-get install --yes pkg-config
apt-get install --yes libfreetype6-dev
apt-get install --yes libpng12-dev
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
python3 setup.py install
python3 setup.py test
#python3 -m pip install https://github.com/gus0k/pymarket/archive/python3.5.zip
