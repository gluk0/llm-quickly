# llm-quickly

A cookie-cutter FastAPI application for quickly serving LLMs.

## Prerequisites

- Python >= 3.8
- pip (Python package installer)
- Make

## Quick Start

The easiest way to get started is to use our setup script:

```bash
./utility/scripts/setup_env.sh
```

This script will:
1. Check your Python version
2. Create and activate a virtual environment
3. Set up your `.env` file from `.env.example`
4. Install all dependencies
5. Create necessary directories

## Manual Setup

If you prefer to set up manually, follow these steps:

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   make setup        # Install basic dependencies
   make dev-setup   # Install development dependencies
   ```

3. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

4. Download the TinyLlama model:
   ```bash
   make download-model
   ```

## Development

### Available Make Commands

- `make help` - Show all available commands
- `make setup` - Install basic dependencies
- `make dev-setup` - Install development dependencies
- `make test` - Run tests
- `make coverage` - Run tests with coverage report
- `make run` - Start the FastAPI application
- `make clean` - Clean up cache and temporary files
- `make lint` - Run code linting (flake8, mypy, black, isort)
- `make format` - Format code using black and isort
- `make download-model` - Download the TinyLlama model
- `make load-test` - Run load tests

### Running the Application

After setup is complete:

1. Update the `.env` file with your configurations
2. Run `make download-model` to download the TinyLlama model
3. Run `make test` to ensure everything is working
4. Start the application with `make run`

The API will be available at `http://localhost:8000`

### Code Quality

Run all checks with:
```bash
make lint
```

Format code with:
```bash
make format
```

### Testing

Run the test suite:
```bash
make test
```

For test coverage report:
```bash
make coverage
```

### Load Testing

To run load tests:
```bash
make load-test
```

## Directory Structure

```
llm-quickly/
├── app/                    # Main application code
│   ├── api/               # API routes and endpoints
│   └── core/              # Core functionality
├── models/                # Model storage
│   └── local/
│       └── tinyllama/     # TinyLlama model files
├── tests/                 # Test suite
├── utility/               # Utility scripts and tools
│   └── scripts/          # Helper scripts
└── logs/                  # Application logs
```

## Environment Variables

Copy `.env.example` to `.env` and update the following variables:
- Required environment variables will be listed here
- Add any specific configuration details

## Contributing

1. Ensure you have run `make dev-setup`
2. Make your changes
3. Run `make format` to format code
4. Run `make lint` to check for any issues
5. Run `make test` to ensure all tests pass
6. Submit your pull request
