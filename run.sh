#!/bin/bash

# Check if the venv folder exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo ""
    echo "Virtual environment created."
    echo "Installing required libraries..."
    source venv/bin/activate
    pip install -r requirements.txt
    echo ""
    echo "Required libraries installed."
    echo ""
fi

# Check if the venv folder exists after creating it
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate

    # Launch main.py
    echo "Launching AI Script Coverage..."
    python3 main.py

    # Deactivate the virtual environment
    echo "Deactivating virtual environment..."
    deactivate
else
    echo "Failed to create virtual environment. Please check your Python installation and try again."
fi

read -p "Press any key to continue..." -n1 -s