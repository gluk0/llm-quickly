#!/bin/bash

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'
YELLOW='\033[1;33m'

echo "Checking Python version..."
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" = "$REQUIRED_VERSION" ]; then 
    echo -e "${GREEN}✓ Python version $PYTHON_VERSION is compatible${NC}"
else
    echo -e "${RED}✗ Python version $PYTHON_VERSION is not compatible. Please use Python >= $REQUIRED_VERSION${NC}"
    exit 1
fi

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi

source venv/bin/activate

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
make dev-setup

echo "Creating necessary directories..."
mkdir -p models/local/tinyllama
mkdir -p logs

echo -e "\n${GREEN}Environment setup complete!${NC}"
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Update the .env file with your configurations"
echo "2. Run 'make download-model' to download the TinyLlama model"
echo "3. Run 'make test' to ensure everything is working"
echo "4. Run 'make run' to start the application" 