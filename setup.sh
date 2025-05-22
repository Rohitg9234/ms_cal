#!/bin/bash

# Create the conda environment
conda create --name cal_sync python=3.11 -y

# Activate the environment
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate cal_sync

# Install dependencies
python -m pip install msal requests
