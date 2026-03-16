#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# if [ ! -f .env ]; then
#     echo "Creating .env file from .env.example..."
#     cp .env.example .env
# fi

echo "Installing dependencies..."
# pip install -r requirements.txt

echo "Starting ASR Service..."
python -m app.main
