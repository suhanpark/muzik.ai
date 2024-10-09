#!/bin/bash

# Ensure that the utils folder is treated as a package by checking if __init__.py exists
if [ ! -f ../utils/__init__.py ]; then
  echo "utils/__init__.py not found, creating one..."
  touch ../utils/__init__.py
fi

# Set Python path to the root directory to ensure proper package importing
export PYTHONPATH=$(dirname "$PWD")

# Navigate back to the root directory to run tests
cd ..

# Run tests using unittest's discovery mode, searching for tests in the 'tests' folder
echo "Running tests..."
python3 -m unittest discover -s tests

# Check for the exit status of the unittest command to report if tests passed or failed
if [ $? -eq 0 ]; then
    echo "All tests passed successfully!"
else
    echo "Some tests failed."
fi
