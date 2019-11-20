#!/usr/bin/env bash

# Generic requirements for funtional curl, etc.
echo "Provisioning virtual machine..."
apt update --fix-missing
apt install --yes apt-transport-https
apt install --yes ca-certificates
apt install --yes software-properties-common
apt install --yes curl

# pymarket repository specifics
echo "Installing pymarket and requirements..."
apt-get install --yes --fix-missing python3-pip
