.PHONY: help install demo clean quick-start check-uv
.DEFAULT_GOAL := help

GREEN := \033[1;32m
YELLOW := \033[1;33m
BLUE := \033[1;34m
RED := \033[1;31m
NC := \033[0m

export PYTHONPATH := $(PYTHONPATH):$(PWD)

help:
	@echo "$(BLUE)🔮 GitVoyant - Temporal Code Intelligence$(NC)"
	@echo ""
	@echo "$(YELLOW)Available commands:$(NC)"
	@echo "  $(GREEN)help$(NC)        Show this help message"
	@echo "  $(GREEN)install$(NC)     Install dependencies"
	@echo "  $(GREEN)demo$(NC)        Run Flask discovery demo"
	@echo "  $(GREEN)clean$(NC)       Clean up cache files"
	@echo "  $(GREEN)quick-start$(NC) Install and run demo"
	@echo "  $(GREEN)check-uv$(NC)    Check if UV is installed"

check-uv:
	@if command -v uv >/dev/null 2>&1; then \
		echo "$(GREEN)✅ UV is installed and ready$(NC)"; \
	else \
		echo "$(RED)❌ UV not found. Installing...$(NC)"; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
		echo "$(GREEN)✅ UV installed. Please restart your shell$(NC)"; \
	fi

install: check-uv
	@echo "$(YELLOW)📦 Installing dependencies...$(NC)"
	uv sync
	@echo "$(GREEN)✅ Dependencies installed$(NC)"

demo: install
	@echo "$(YELLOW)🔍 Running GitVoyant demo...$(NC)"
	uv run python examples/flask_discovery_demo.py
	@echo "$(GREEN)✅ Demo complete$(NC)"

clean:
	@echo "$(YELLOW)🧹 Cleaning up...$(NC)"
	rm -rf __pycache__ src/__pycache__ src/core/__pycache__ examples/__pycache__
	@echo "$(GREEN)✅ Cleaned$(NC)"

quick-start: install demo
	@echo "$(GREEN)🚀 GitVoyant ready! Try: uv run python examples/flask_discovery_demo.py$(NC)"