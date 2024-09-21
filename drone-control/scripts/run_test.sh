#!/bin/bash

# Run the Python test script for controlling the drone
echo "Running the drone test script..."

# Make sure you have the correct Python environment activated if using virtualenv or conda
# Example:
# source your-venv/bin/activate

# Run the drone test script
python3 drone_test.py

# Check if the script ran successfully
if [ $? -eq 0 ]; then
    echo "Drone test script completed successfully."
else
    echo "Drone test script failed. Please check for errors."
fi