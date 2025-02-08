.PHONY: setup test run clean lint format download-model load-test help

PYTHON := python3
PIP := pip3
PYTEST := pytest
APP_MODULE := app.api.main:app

help:
	@echo "Available commands:"
	@echo "make setup         - Install all dependencies"
	@echo "make dev-setup    - Install development dependencies"
	@echo "make test         - Run tests"
	@echo "make coverage     - Run tests with coverage report"
	@echo "make run          - Run the FastAPI application"
	@echo "make clean        - Clean up cache and temporary files"
	@echo "make lint         - Run code linting"
	@echo "make format       - Format code"
	@echo "make download-model - Download the TinyLlama model"
	@echo "make load-test    - Run load tests"

setup:
	$(PIP) install -r requirements.txt

dev-setup: setup
	$(PIP) install -r requirements-dev.txt
	$(PIP) install black flake8 isort mypy

test:
	$(PYTEST) tests/ -v

coverage:
	$(PYTEST) tests/ --cov=app --cov-report=term-missing

run:
	uvicorn $(APP_MODULE) --reload --host 0.0.0.0 --port 8000

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

lint:
	flake8 app/ tests/
	black --check app/ tests/
format:
	black app/ tests/
	isort app/ tests/

download-model:
	./utility/scripts/download_model.sh

load-test:
	locust -f utility/scripts/load/locustfile.py 