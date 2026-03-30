# Contributing to GitVoyant

GitVoyant is a temporal code intelligence platform with multi-language support for Python, JavaScript, Java, and Go. This document describes how to contribute.

## Getting Started

### Prerequisites

- Python 3.11+
- [UV package manager](https://astral.sh/uv/)
- Git
- ANTHROPIC_API_KEY (for AI agent features)

### Setup

```bash
git clone https://github.com/Cre4T3Tiv3/gitvoyant.git
cd gitvoyant
make bootstrap
source .venv/bin/activate
cp .env.example .env
```

`make bootstrap` creates a virtual environment, installs all dependencies, and sets up the `gitvoyant` CLI in editable mode.

## Architecture

GitVoyant uses Domain-Driven Design with Clean Architecture separation.

- **Domain Layer** — Rich entities (`TemporalEvaluation`, `ComplexityTrend`) and value objects with embedded business logic.
- **Application Layer** — Use case orchestration and workflow coordination.
- **Infrastructure Layer** — Git integration, language-specific analyzers (Python via `ast`, JavaScript/Java/Go via tree-sitter), and statistical analysis.
- **Presentation Layer** — Typer CLI with Rich formatting and LangGraph-based AI agent.

Contributions should respect this separation. Domain logic belongs in the domain layer. Infrastructure concerns (parsers, Git operations, external APIs) belong in infrastructure.

## Areas of Contribution

### Language Analyzers

Each supported language has a dedicated analyzer implementing the `Analyzer` protocol in `infrastructure/analyzers/base.py`. Adding a new language means implementing `extract_metrics()` and `file_extensions`, writing unit tests, and registering the analyzer in `infrastructure/analyzers/__init__.py`.

### Temporal Intelligence

- Confidence scoring algorithms (currently 0.4-0.9 scale based on commit count)
- IMPROVING/DECLINING/STABLE classification refinement
- R-squared validation and trend stability metrics
- Quality decay forecasting improvements

### AI Agent

- Multi-LLM support (GPT-4, Gemini, local models via Ollama)
- Agent tool enhancements (`temporal_analysis_tool`, `repo_evaluation_tool`)
- Context management and response formatting

### Bug Reports

When reporting bugs, include the GitVoyant version, Python version, OS, the exact CLI command used, and the complete output including any error messages. Describe what you expected versus what occurred.

### Feature Requests

Open a GitHub Issue describing the problem or gap, the proposed solution, and how it integrates with the existing architecture.

## Development Workflow

### Branch and Test

```bash
git checkout -b feature/your-change
make test          # Full test suite (63 tests)
make lint          # Code quality
```

### Commit Messages

```
feat: add R-squared confidence validation
fix: resolve CLI error handling for remote repositories
docs: update temporal analysis methodology
test: add integration tests for Go analyzer
refactor: optimize domain entity validation
```

### Pull Request Process

1. Create a feature branch from `main`.
2. Write tests for new functionality.
3. Run `make test` and `make lint` before submitting.
4. Update relevant documentation (USER_GUIDE.md for new features, CHANGELOG.md for breaking changes).
5. Submit with a clear description of changes and rationale.

## Testing

```bash
make test              # Full suite
make test-unit         # Domain entities, value objects, analyzers
make test-integration  # Full workflow with real Git repositories
make test-cli          # CLI interface
make test-coverage     # Coverage report
```

When contributing new analysis capabilities, validate against known repositories with established complexity patterns.

## Quality Standards

- Full type annotations using Python 3.11+ features.
- Google-style docstrings for all public methods.
- Maintain existing test coverage; expand for new features.
- Robust error handling with graceful degradation.
- Domain-Driven Design patterns respected across all layers.

## Documentation

- Code changes: update docstrings.
- New features: update USER_GUIDE.md.
- Architecture changes: update README.md.
- Breaking changes: update CHANGELOG.md.

## Contact

For questions about architecture, contribution scope, or temporal intelligence methods, open an issue or contact [@Cre4T3Tiv3](https://github.com/Cre4T3Tiv3).