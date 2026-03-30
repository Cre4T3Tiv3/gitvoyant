Temporal Code Intelligence platform. Time-series analysis on Git commit history to surface quality evolution, complexity trends, and maintenance risk before they become production incidents. Supports Python, JavaScript, Java, and Go.

---

## What It Does

Static analysis tools tell you a file is complex. GitVoyant tells you whether that complexity is growing, shrinking, or stable, and at what rate. The difference is temporal context: a file with high complexity and a declining trend is healthy engineering. A file with moderate complexity and an accelerating growth rate is a future incident.

GitVoyant extracts commit history for each file, computes cyclomatic complexity at every snapshot, fits linear regression to the complexity time series, and classifies the resulting pattern as IMPROVING, DECLINING, or STABLE. Each classification carries a statistical confidence score based on commit history depth.

## Supported Languages

| Language | Parser | Extensions |
|---|---|---|
| Python | Built-in `ast` module | `.py` |
| JavaScript/TypeScript | tree-sitter | `.js`, `.jsx`, `.ts` |
| Java | tree-sitter | `.java` |
| Go | tree-sitter | `.go` |

Language detection is automatic based on file extension. The `--language` flag restricts analysis to a single language when needed.

## How It Works

**Temporal evaluation pipeline:**

1. Discover source files across all supported languages in the repository.
2. Extract per-file complexity metrics across Git commit history within a configurable analysis window.
3. Track cyclomatic complexity evolution using language-specific AST analysis at each commit.
4. Fit linear regression to the complexity time series to compute trend slope (complexity change per month).
5. Score confidence based on data quality: 10+ commits yields 0.9 confidence; fewer than 5 triggers a low-confidence warning.
6. Forecast quality decay risk from the trend slope, bounded between 0 and 1.

**Architecture:** Domain-Driven Design with Clean Architecture separation. Domain layer (rich entities and value objects with embedded business logic), application layer (use case orchestration), infrastructure layer (Git integration, language-specific analyzers, and statistical analysis), and presentation layer (CLI and AI agent interface).

**Analyzer abstraction:** Each language has a dedicated analyzer implementing a common protocol. Python uses the standard library `ast` module. JavaScript, Java, and Go use tree-sitter grammars. All analyzers produce the same metric structure: cyclomatic complexity, function count, class count, and lines of code.

## Quick Start

```bash
git clone https://github.com/Cre4T3Tiv3/gitvoyant.git
cd gitvoyant
make bootstrap
```

Configure your environment:

```bash
cp .env.example .env
# Add your ANTHROPIC_API_KEY for AI agent features
```

The AI agent defaults to `claude-sonnet-4-5-20250929`. Set `CLAUDE_MODEL` in `.env` to use a different model. Supported: `claude-sonnet-4-5-20250929`, `claude-opus-4-6`, `claude-sonnet-4-6`.

## Usage

**CLI -- analyze a file:**

```bash
gitvoyant analyze temporal ./repo src/main.py
```

**CLI -- analyze a repository (all supported languages):**

```bash
gitvoyant analyze temporal ./repo
```

**CLI -- restrict to a single language:**

```bash
gitvoyant analyze temporal ./repo --language javascript
```

**CLI -- launch interactive AI agent:**

```bash
gitvoyant analyze agent
```

**Python -- programmatic access:**

```python
from gitvoyant import TemporalEvaluatorService

service = TemporalEvaluatorService()
result = await service.evaluate_repository(".")
```

## AI Agent

The AI agent provides conversational access to the temporal analysis engine. Ask questions in natural language; the agent runs the analysis and interprets the results.

```
You: "Which files need the most attention?"

GitVoyant: Analyzing repository temporal patterns...

src/api/handlers.py: 0.85 (HIGH RISK - complexity growing +2.3/month)
utils/data_processing.py: 0.72 (MEDIUM RISK - declining pattern detected)
core/business_logic.py: 0.68 (MEDIUM RISK - confidence: 0.4 - limited history)
```

## Test Coverage

63+ tests across unit tests (domain entities, value objects, language analyzers), integration tests (full workflow with real Git repositories), agent tests (AI agent interaction and tool integration), and CLI tests.

## Documentation

- [User Guide](USER_GUIDE.md) -- Setup, usage, and CLI reference
- [Contributing Guide](CONTRIBUTING.md) -- Development setup and contribution guidelines
- [Complexity Requirements](docs/COMPLEXITY_REQUIREMENTS.md) -- Complexity metrics specification
- [Temporal Analysis Explained](docs/TEMPORAL_ANALYSIS_EXPLAINED.md) -- Algorithm and methodology

## License

[Apache 2.0](LICENSE)
