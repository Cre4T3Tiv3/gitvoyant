.PHONY: help install dev lint format test test-unit test-integration test-cli test-coverage clean version check-uv cli cli-complete check-path bootstrap completions-debug
.DEFAULT_GOAL := help

GREEN := \033[1;32m
YELLOW := \033[1;33m
BLUE := \033[1;34m
RED := \033[1;31m
CYAN := \033[1;36m
NC := \033[0m

PROJECT_NAME := gitvoyant
VERSION := 0.2.0
PYTHON_VERSION := 3.11
AUTHOR := Jesse Moses (@Cre4T3Tiv3) - jesse@bytestacklabs.com

export PYTHONPATH := $(PWD)/src

# Define virtual environment paths
VENV_DIR := .venv
VENV_BIN := $(VENV_DIR)/bin
PYTHON := $(VENV_BIN)/python
UV := uv

help: ## 📖 Show this help message
	@echo "$(BLUE)🔮 GitVoyant v$(VERSION) - Temporal Code Intelligence CLI$(NC)"
	@echo ""
	@echo "$(YELLOW)🔧 Setup Commands:$(NC)"
	@echo "  $(GREEN)make bootstrap$(NC)      - 🔁 Create .venv and install everything via UV"
	@echo "  $(GREEN)make install$(NC)        - Install production dependencies via UV"
	@echo "  $(GREEN)make dev$(NC)            - Install dev dependencies (tests, docs, lint)"
	@echo "  $(GREEN)make cli$(NC)            - Install CLI entry point (editable mode)"
	@echo "  $(GREEN)make cli-complete$(NC)   - Install CLI + shell autocompletion"
	@echo ""
	@echo "$(YELLOW)🧪 Dev Workflow:$(NC)"
	@echo "  $(GREEN)make lint$(NC)           - Run Ruff lint checks"
	@echo "  $(GREEN)make format$(NC)         - Auto-format using Ruff"
	@echo "  $(GREEN)make test$(NC)           - Run all tests"
	@echo ""
	@echo "$(YELLOW)📦 Version Info:$(NC)"
	@echo "  $(GREEN)make version$(NC)        - Show environment info"

check-uv: ## 🔍 Ensure UV is installed
	@command -v uv >/dev/null 2>&1 || { \
		echo "$(RED)❌ UV not found — installing...$(NC)"; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
		exit 1; }

$(VENV_DIR): check-uv
	@echo "$(CYAN)🔧 Creating virtual environment...$(NC)"
	$(UV) venv $(VENV_DIR)

# Create a marker file to track when dev dependencies are installed
$(VENV_DIR)/.dev-installed: $(VENV_DIR)
	@echo "$(CYAN)📦 Installing dev dependencies...$(NC)"
	$(UV) sync --dev
	@touch $(VENV_DIR)/.dev-installed

bootstrap: $(VENV_DIR) ## 🔁 Create .venv and install all tools/dev deps
	@echo "$(CYAN)🚀 Bootstrapping GitVoyant environment using UV...$(NC)"
	$(UV) sync --dev
	@touch $(VENV_DIR)/.dev-installed
	@echo "$(GREEN)✅ Bootstrap complete. You can now run 'gitvoyant'.$(NC)"
	@echo "$(YELLOW)👉 Tip: add .venv/bin to your PATH to run 'gitvoyant' without activating the venv.$(NC)"
	@echo "$(CYAN)   Option 1:$(NC) Run: 'source .venv/bin/activate' before using gitvoyant"
	@echo "$(CYAN)   Option 2:$(NC) Add the following to your shell config file (e.g., ~/.bashrc or ~/.zshrc):"
	@echo "         export PATH=\"$$(pwd)/.venv/bin:\$$PATH\""
	@echo "$(YELLOW)💡 To enable CLI autocompletion, run:$(NC)"
	@echo "   gitvoyant install-completion"
	@echo "   # This will print tailored setup instructions for your shell"

install: $(VENV_DIR) ## 📦 Install production dependencies
	$(UV) sync

dev: $(VENV_DIR)/.dev-installed ## 🧪 Install all dev dependencies

cli: $(VENV_DIR) ## 📦 Install CLI entry point (editable mode)
	$(UV) pip install -e .

cli-complete: cli ## 🚀 Install CLI + shell autocompletion
	@echo "$(CYAN)🔧 Installing CLI with autocompletion...$(NC)"
	@echo "$(YELLOW)💡 Run the following to enable autocompletion:$(NC)"
	@echo "   gitvoyant install-completion"

completions-debug: $(VENV_DIR)/.dev-installed ## 🧪 Debug CLI app loading for completion
	@echo "$(CYAN)Testing Typer CLI discovery for autocompletion...$(NC)"
	$(UV) run python -c 'from gitvoyant.cli.cli import get_app; print(get_app())'

lint: $(VENV_DIR)/.dev-installed ## 🔍 Run Ruff linting
	$(VENV_BIN)/ruff check src/

format: $(VENV_DIR)/.dev-installed ## ✨ Auto-format using Ruff
	$(VENV_BIN)/ruff format src/
	$(VENV_BIN)/ruff check --fix src/

test: test-unit test-integration test-cli test-coverage ## 🧪 Run all tests

test-unit: $(VENV_DIR)/.dev-installed ## 🔬 Run unit tests
	PYTHONPATH=$(PWD)/src $(VENV_BIN)/pytest -v tests/unit

test-integration: $(VENV_DIR)/.dev-installed ## 🔗 Run integration tests
	PYTHONPATH=$(PWD)/src $(VENV_BIN)/pytest -v tests/integration

test-cli: $(VENV_DIR)/.dev-installed ## 💻 Run CLI tests
	$(UV) pip install -e .
	PYTHONPATH=$(PWD)/src $(VENV_BIN)/pytest -v tests/cli

test-coverage: $(VENV_DIR)/.dev-installed ## 📊 Run tests with coverage report
	PYTHONPATH=$(PWD)/src $(VENV_BIN)/pytest --cov=gitvoyant --cov-report=term-missing --cov-fail-under=70

version: ## 📋 Show system details
	@echo "Project:   $(PROJECT_NAME)"
	@echo "Version:   $(VERSION)"
	@echo "Python:    $(PYTHON_VERSION)"
	@echo "Platform:  $(shell python -c 'import platform; print(platform.system())')"
	@echo "UV:        $(shell uv --version 2>/dev/null || echo 'Not installed')"

clean: ## 🧹 Remove cache and temp files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .ruff_cache .pytest_cache .coverage dist/ build/ $(VENV_DIR)

check-path: ## 🧪 Print current PYTHONPATH for debugging
	@echo "$(CYAN)PYTHONPATH is:$(NC) $(PYTHONPATH)"