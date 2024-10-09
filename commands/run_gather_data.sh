#!/bin/bash

# Ensure that the utils folder is treated as a package by checking if __init__.py exists
if [ ! -f ../utils/__init__.py ]; then
  echo "utils/__init__.py not found, creating one..."
  touch ../utils/__init__.py
fi

# Set Python path to the root directory to ensure proper package importing
export PYTHONPATH=$(dirname "$PWD")

# Navigate to the root directory
cd ..

# Run the gather_data.py script
echo "Running gather_data.py..."
python3 utils/gather_data.py

# Report status of the script execution
if [ $? -eq 0 ]; then
    echo "gather_data.py ran successfully!"
else
    echo "gather_data.py encountered an error."
fi
