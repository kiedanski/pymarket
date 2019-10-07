#!/bin/bash

# Generic requirements for funtional curl, etc.
echo "Provisioning virtual machine..."
apt install --yes apt-transport-https
apt install --yes ca-certificates
apt install --yes software-properties-common
apt install --yes curl

# pymarket repository specifics
echo "Installing pymarket and requirements..."
apt install --yes python3-pip=8.1.1-2ubuntu0.4
