#!/bin/bash

set -e

VENV_NAME="venv"

echo "Creating and activating virtual environment..."
python3 -m venv "$VENV_NAME"
source "$VENV_NAME/bin/activate"

