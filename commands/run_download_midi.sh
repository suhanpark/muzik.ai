#!/bin/bash

# Ensure the utils folder is treated as a package by checking if __init__.py exists
if [ ! -f ./utils/__init__.py ]; then
  echo "utils/__init__.py not found, creating one..."
  touch ./utils/__init__.py
fi

# Set the PYTHONPATH to the root directory to ensure proper package importing
export PYTHONPATH=$(pwd)
export GOOGLE_APPLICATION_CREDENTIALS="credentials/muzik_service_account.json"

# Run the gather_data.py script
echo "Downloading midi from bucket..."
python3 utils/download_files.py

# Report the status of the script execution
if [ $? -eq 0 ]; then
    echo "download_files.py ran successfully!"
else
    echo "download_files.py encountered an error."
fi
