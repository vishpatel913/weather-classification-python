#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Define the virtual environment directory name
VENV_NAME="venv"

echo "Creating and activating virtual environment..."
python3 -m venv "$VENV_NAME"
source "$VENV_NAME/bin/activate"

