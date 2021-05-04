#!/bin/bash

# Bash "strict mode", to help catch problems and bugs in the shell
# script. Every bash script you write should include this. See
# http://redsymbol.net/articles/unofficial-bash-strict-mode/ for
# details.
set -euo pipefail

# Tell apt we're never going to be able to give manual
# feedback:
export DEBIAN_FRONTEND=noninteractive

# Update lists
apt update

# Security updates
apt -y upgrade

# Install needed libraries
apt install -y --no-install-recommends python3-dev g++

# Delete cached files we don't need anymore:
apt clean
rm -rf /var/lib/apt/lists/*
