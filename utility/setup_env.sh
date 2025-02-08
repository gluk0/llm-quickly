#!/bin/bash

set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color
YELLOW='\033[1;33m'

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" = "$REQUIRED_VERSION" ]; then 
    echo -e "${GREEN}✓ Python version $PYTHON_VERSION is compatible${NC}"
else
    echo -e "${RED}✗ Python version $PYTHON_VERSION is not compatible. Please use Python >= $REQUIRED_VERSION${NC}"
    exit 1
fi

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
    echo -e "${GREEN}✓ Poetry installed${NC}"
else
    echo -e "${GREEN}✓ Poetry already installed${NC}"
fi

# Configure Poetry to create virtual environment in project directory
poetry config virtualenvs.in-project true

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from .env.example..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo -e "${GREEN}✓ Created .env file${NC}"
        echo -e "${YELLOW}! Please update the .env file with your configurations${NC}"
    else
        echo -e "${RED}✗ .env.example file not found${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✓ .env file exists${NC}"
fi

echo "Installing dependencies..."
poetry install

echo "Creating necessary directories..."
mkdir -p models/local/tinyllama
mkdir -p logs

echo -e "\n${GREEN}Environment setup complete!${NC}"
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Update the .env file with your configurations"
echo "2. Run 'poetry run make download-model' to download the TinyLlama model"
echo "3. Run 'poetry run make test' to ensure everything is working"
echo "4. Run 'poetry run make run' to start the application" 