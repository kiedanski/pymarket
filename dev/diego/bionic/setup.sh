#!/bin/bash

# Generic requirements for funtional curl, etc.
#echo "Provisioning virtual machine..."
#apt install --yes apt-transport-https
#apt install --yes ca-certificates
#apt install --yes software-properties-common
#apt install --yes curl

# pymarket repository specifics
echo "Installing pymarket and requirements..."

#apt install --yes python3-pip=9.0.1-2.3~ubuntu1.18.04.1
apt-get update
apt-get install --yes  python3-pip=9.0.1-2.3~ubuntu1.18.04.1
mkdir -p /home/vagrant
cd /home/vagrant
git clone https://github.com/gus0k/pymarket.git
cd pymarket
python3 setup.py install
python3 setup.py test
#python3 -m pip install https://github.com/gus0k/pymarket/archive/python3.5.zip
