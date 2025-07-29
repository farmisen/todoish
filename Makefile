.PHONY: help setup install-deps lint format format-check type-check test clean all dev-check fix

# Note: If you see "make: function definition file not found", this is due to a shell
# function overriding the make command. Use ./make.sh as a workaround.

# Folders to lint and type-check
SRC_FOLDERS = src/ tests/

# Default target
all: lint type-check

help:
	@echo "Available commands:"
	@echo "  make setup        - Install uv and create Python 3.12 virtual environment"
	@echo "  make install-deps - Install project with dev dependencies"
	@echo "  make lint         - Run Ruff linter"
	@echo "  make format       - Format code with Ruff (includes tests)"
	@echo "  make format-check - Check code formatting"
	@echo "  make fix          - Auto-fix code issues (format + safe linting fixes)"
	@echo "  make type-check   - Run Pyright type checker"
	@echo "  make test         - Run pytest tests"
	@echo "  make clean        - Remove cache files"
	@echo "  make all          - Run lint and type-check"
	@echo "  make dev-check    - Run all checks (format-check, lint, type-check)"

setup:
	@echo "🔧 Setting up todoish development environment..."
	@# Check for Python 3.12
	@echo "🐍 Checking for Python 3.12..."
	@if ! python3.12 --version >/dev/null 2>&1; then \
		echo "❌ Error: Python 3.12 is not installed or not in PATH"; \
		echo ""; \
		echo "Please install Python 3.12 from:"; \
		echo "  - https://www.python.org/downloads/"; \
		echo "  - Or use your system package manager"; \
		echo ""; \
		exit 1; \
	fi
	@echo "✅ Python 3.12 found: $$(python3.12 --version)"
	@# Check if uv is installed
	@if ! command -v uv >/dev/null 2>&1; then \
		echo "📦 Installing uv..."; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
		echo "✅ uv installed successfully!"; \
		echo ""; \
		echo "⚠️  Please restart your shell or run:"; \
		echo "    source ~/.cargo/env"; \
		echo ""; \
		echo "Then run 'make setup' again."; \
		exit 1; \
	fi
	@echo "✅ uv is installed"
	@# Create virtual environment with Python 3.12
	@echo "🐍 Creating Python 3.12 virtual environment..."
	@uv venv --python 3.12
	@echo "✅ Virtual environment created"
	@echo ""
	@echo "📝 Next steps:"
	@echo "1. Activate the virtual environment:"
	@echo "   source .venv/bin/activate  # On Unix/macOS"
	@echo "   .venv\\Scripts\\activate     # On Windows"
	@echo ""
	@echo "2. Install the project dependencies:"
	@echo "   ./make.sh install-deps"

install-deps:
	uv pip install -e ".[dev]"

lint:
	@echo "Running Ruff linter..."
	uv run ruff check $(SRC_FOLDERS)

format:
	@echo "Formatting code with Ruff..."
	uv run ruff format $(SRC_FOLDERS)
	uv run ruff check $(SRC_FOLDERS) --fix

format-check:
	@echo "Checking code formatting..."
	uv run ruff format $(SRC_FOLDERS) --check

fix:
	@echo "🔧 Auto-fixing code issues..."
	@echo "Running Ruff formatter..."
	uv run ruff format $(SRC_FOLDERS)
	@echo "Running Ruff linter with safe fixes..."
	uv run ruff check $(SRC_FOLDERS) --fix
	@echo "✅ Safe fixes applied!"
	@echo ""
	@echo "Note: Some issues may require manual fixes:"
	@echo "- Type errors (run 'make type-check' to see them)"
	@echo "- Complex linting issues (run 'make lint' to see remaining)"
	@echo ""
	@echo "For unsafe fixes, run: uv run ruff check --fix --unsafe-fixes"

type-check:
	@echo "Running Pyright type checker..."
	uv run pyright $(SRC_FOLDERS)

test:
	@echo "Running tests..."
	uv run pytest

clean:
	@echo "Cleaning cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +

# Development workflow
dev-check: format-check lint type-check
	@echo "✅ All checks passed!"