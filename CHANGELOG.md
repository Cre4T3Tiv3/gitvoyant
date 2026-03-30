# Changelog

All notable changes to GitVoyant are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.3.0] — 2026-03-29

### Multi-Language Temporal Analysis
- Extended temporal analysis to Python, JavaScript/TypeScript, Java, and Go
- Introduced `Analyzer` protocol (ABC) defining the interface for language-specific code analysis
- Created `PythonAnalyzer` by extracting `_extract_metrics()` and `_cyclomatic_complexity()` from `TemporalEvaluator`
- Created `JavaScriptAnalyzer` using tree-sitter-javascript (handles `.js`, `.jsx`, `.ts`)
- Created `JavaAnalyzer` using tree-sitter-java (handles `.java`)
- Created `GoAnalyzer` using tree-sitter-go (handles `.go`)
- Central analyzer registry mapping file extensions to analyzer instances
- `TemporalEvaluator` delegates to the resolved analyzer instead of calling `ast.parse` directly
- Automatic language detection by file extension
- `--language` CLI flag for restricting analysis to a single language
- `GITVOYANT_SUPPORTED_LANGUAGES` configuration option for limiting enabled languages
- Per-language directory exclusions: `node_modules`, `dist`, `.next`, `target`, `.gradle`, `vendor`, `build`
- File discovery in `TemporalEvaluatorService` and `langchain_bindings` now uses registry lookups instead of hardcoded `.py` checks

### Multi-Model Support
- Default model updated to `claude-sonnet-4-5-20250929`
- Verified support for `claude-opus-4-6` and `claude-sonnet-4-6`
- Model selection via `CLAUDE_MODEL` environment variable
- Agent runtime now consumes the full config contract via `get_claude_config()`, wiring `model`, `temperature`, and `max_tokens` through to `ChatAnthropic`
- Default `max_tokens` increased from 4000 to 8192 to match current model capabilities

### Dependency Upgrades
- `anthropic` minimum version raised from `0.18.0` to `0.80.0` (required for current model IDs and `models.list()` endpoint)
- `langchain-anthropic` minimum version raised from `0.1.0` to `1.0.0`
- `langchain` and `langchain-core` minimum versions raised from `0.1.0` to `0.3.0`
- Added `tree-sitter>=0.24.0`, `tree-sitter-javascript>=0.23.0`, `tree-sitter-java>=0.23.0`, `tree-sitter-go>=0.23.0`

### Schema and Output Changes
- Added `language` field to `TemporalEvaluation` domain entity
- Added `language` field to `EvaluationResponse` DTO
- Added `language` column to CLI Rich table output
- Updated all tool descriptions from "Python file" to "source file"
- CLI indicators changed from emoji to text markers: `[+]` (improving), `[-]` (declining), `[~]` (stable)
- Agent prompt strings rewritten: branded as "GitVoyant" instead of vendor name

### Bug Fixes
- `max_tokens` was configured in settings but never passed to `ChatAnthropic` in agent runtime; now wired through
- Corrected stale model identifiers that were returning HTTP 404 from the Anthropic API

### Documentation
- All markdown documentation (README, USER_GUIDE, CONTRIBUTING, CHANGELOG, COMPLEXITY_REQUIREMENTS, TEMPORAL_ANALYSIS_EXPLAINED) rewritten for declarative register, no speculative roadmaps, no performative language
- CITATION.cff rewritten: updated abstract, keywords, and version to reflect multi-language scope

### Removed
- All emoji characters across the entire codebase (source, docs, CI, CLI output, banner, agent prompts)
- All vendor attribution from documentation, user-facing strings, and CITATION.cff
- `docs/index.html` static architecture diagram (stale, duplicative of README)
- Speculative roadmap sections from CONTRIBUTING.md and CHANGELOG.md
- Badge wall from README.md

### Testing
- 63+ tests total
- 13 unit tests for `JavaScriptAnalyzer`
- 14 unit tests for `JavaAnalyzer`
- 12 unit tests for `GoAnalyzer`
- All three supported models verified end-to-end against the live Anthropic API through the full agent runtime

---

## [0.2.0] — 2025-07-15

### Architecture Transformation
- Complete rewrite using Domain-Driven Design (DDD) principles
- Clean Architecture with separation of presentation, application, domain, and infrastructure layers
- Rich domain entities: `TemporalEvaluation`, `Repository` with embedded business logic
- Value objects: `ComplexityTrend`, `ConfidenceRank`, `TimeTable` with validation and business rules
- Use cases: `AnalyzeFileUseCase`, `AnalyzeRepoUseCase` orchestrating business workflows

### AI Agent Platform
- LLM integration via LangChain and Anthropic agent runtime
- Conversational interface for natural language temporal analysis through AI agents
- Specialized tools: `temporal_analysis_tool`, `repo_evaluation_tool` for agent consumption
- LangGraph ReAct agent runtime with GitVoyant tools
- Context management with output suppression and response formatting

### Enhanced Temporal Intelligence
- Confidence scoring based on commit history depth (0.4-0.9 scale)
- Progressive disclosure: higher confidence with more temporal data points
- Low confidence warnings as reliability indicators for limited data
- Improved quality decay forecasting with confidence bounds
- Proper handling of insufficient data with graceful degradation

### CLI
- Rich formatting with color-coded metrics and styled tables
- Command structure: `gitvoyant analyze temporal` and `gitvoyant analyze agent`
- Comprehensive error messages and user guidance
- Smart resolution of local paths and remote Git URLs
- Structured rendering with risk-ranked file listings

### Quality
- 55%+ test coverage with unit, integration, and CLI tests
- Full type annotations throughout codebase
- Robust error recovery and partial result handling
- Structured logging with configurable levels
- Environment-based configuration with `.env` support

### Developer Experience
- UV package manager, Ruff linting and formatting
- Makefile with build automation
- Proper CLI installation with `gitvoyant` command
- Google-style docstrings throughout

### Technical Implementation
- Git integration via GitPython for commit history processing
- NumPy/Pandas for linear regression and trend analysis
- Python AST parsing for cyclomatic complexity calculation
- AsyncIO integration for service layer operations
- Immutable value objects and rich domain entities via dataclasses

### Removed (v0.1.0 Research Artifacts)
- Flask-specific research examples and results
- Research-oriented demonstration scripts
- Illustrative graphs and sample data
- REST API (simplified to CLI and agent interfaces)

### Migration from v0.1.0
- Core temporal evaluation algorithm preserved in full
- Research algorithms restructured into production architecture
- Same linear regression and complexity analysis foundation, now with confidence scoring
- IMPROVING/DECLINING/STABLE classification with statistical rigor

---

## [0.1.0] — 2025-07-01

### Initial Research Implementation
- First implementation of Git history-based quality analysis
- Flask repository analysis as discovery case
- 878-line research prototype demonstrating temporal intelligence viability
- Basic IMPROVING/DECLINING/STABLE quality pattern classification

### Core Algorithms
- AST-based cyclomatic complexity measurement across Git commits
- Statistical trend analysis via linear regression for complexity evolution
- Commit-by-commit code analysis and metrics extraction
- Quality pattern detection for positive and negative trends

### Research Validation
- Analysis of Flask, Django, and other open-source repositories
- Identification of quality engineering signatures in successful projects
- Demonstrated that temporal analysis provides insights unavailable to static tools
- Established temporal intelligence as a viable analytical approach

### Key Findings
- Historical analysis yields information inaccessible to point-in-time evaluation
- Deliberate complexity reduction patterns are observable in mature projects
- Quality decay forecasting is feasible from temporal data
- Approach validated as suitable for production AI agent platform
