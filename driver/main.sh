#!/bin/bash

# Install Dependencies
pip install --upgrade google-api-python-client
pip install --upgrade oauth2client
pip install --upgrade argparse
pip install --upgrade httplib2
pip install --upgrade pydrive

# Download Dataset
python /project/gdrive/download.py

# Train


# Test


# Upload data
