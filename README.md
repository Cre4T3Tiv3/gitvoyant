Temporal Code Intelligence platform. Time-series analysis on Git commit history to surface quality evolution, complexity trends, and maintenance risk before they become production incidents.

<p align="center">
  <a href="https://github.com/Cre4T3Tiv3/gitvoyant" target="_blank">
    <img src="https://raw.githubusercontent.com/Cre4T3Tiv3/gitvoyant/main/docs/assets/gitvoyant_v0.2.0.jpeg" alt="GitVoyant v0.2.0" width="640"/>
  </a>
</p>

<p align="center">
  <a href="https://github.com/Cre4T3Tiv3/gitvoyant/releases/tag/v0.2.0">
    <img src="https://img.shields.io/badge/version-v0.2.0-brightgreen" alt="Version: v0.2.0">
  </a>
  <a href="https://github.com/Cre4T3Tiv3/gitvoyant/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/License-Apache_2.0-blue.svg" alt="License: Apache 2.0">
  </a>
  <a href="https://orcid.org/0009-0006-0322-7974">
    <img src="https://img.shields.io/badge/ORCID-0009--0006--0322--7974-A6CE39?logo=orcid&logoColor=white" alt="ORCID: 0009-0006-0322-7974">
  </a>
  <a href="https://bytestacklabs.com">
    <img src="https://img.shields.io/badge/Made%20by-ByteStack%20Labs-2ea44f" alt="ByteStack Labs">
  </a>
</p>

---

## What It Does

Static analysis tools tell you a file is complex. GitVoyant tells you whether that complexity is growing, shrinking, or stable, and at what rate. The difference is temporal context: a file with high complexity and a declining trend is healthy engineering. A file with moderate complexity and an accelerating growth rate is a future incident.

GitVoyant extracts commit history for each file, computes cyclomatic complexity at every snapshot, fits linear regression to the complexity time series, and classifies the resulting pattern as IMPROVING, DECLINING, or STABLE. Each classification carries a statistical confidence score based on commit history depth.

## How It Works

**Temporal evaluation pipeline:**

1. Extract per-file complexity metrics across Git commit history within a configurable analysis window.
2. Track cyclomatic complexity evolution using AST-based static analysis at each commit.
3. Fit linear regression to the complexity time series to compute trend slope (complexity change per month).
4. Score confidence based on data quality: 10+ commits yields 0.9 confidence; fewer than 5 triggers a low-confidence warning.
5. Forecast quality decay risk from the trend slope, bounded between 0 and 1.

**Architecture:** Domain-Driven Design with Clean Architecture separation. Domain layer (rich entities and value objects with embedded business logic), application layer (use case orchestration), infrastructure layer (Git integration and statistical analysis), and presentation layer (CLI and AI agent interface).

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

## Usage

**CLI — analyze a file:**

```bash
gitvoyant analyze temporal ./repo src/main.py
```

**CLI — launch interactive AI agent:**

```bash
gitvoyant analyze agent
```

**Python — programmatic access:**

```python
from gitvoyant import TemporalEvaluatorService

service = TemporalEvaluatorService()
evaluation = await service.analyze_file("src/main.py")

print(f"Quality Pattern: {evaluation.quality_pattern}")
print(f"Complexity Trend: {evaluation.complexity_tenor.slope:.2f}/month")
print(f"Confidence: {evaluation.confidence_score:.2f}")
```

**Repository-level assessment:**

```python
repo = await service.analyze_repository(".")
print(f"Health Score: {repo.overall_health_score}/10.0")
print(f"Files showing improvement: {len(repo.improving_files)}")
```

## AI Agent

The Claude-powered agent provides conversational access to the temporal analysis engine. Ask questions in natural language; the agent runs the analysis and interprets the results.

```
You: "Which files need the most attention?"

GitVoyant: Analyzing repository temporal patterns...

src/api/handlers.py: 0.85 (HIGH RISK - complexity growing +2.3/month)
utils/data_processing.py: 0.72 (MEDIUM RISK - declining pattern detected)
core/business_logic.py: 0.68 (MEDIUM RISK - confidence: 0.4 - limited history)
```

Currently supports Claude AI only. Multi-LLM support planned for v0.3.0.

## Test Coverage

55+% coverage across unit tests (domain entities, value objects, core algorithms), integration tests (full workflow with real Git repositories), agent tests (AI agent interaction and tool integration), and CLI tests.

## Documentation

- [User Guide](USER_GUIDE.md) — Complete setup, usage, and CLI reference
- [Contributing Guide](CONTRIBUTING.md) — Development setup and contribution guidelines
- [Complexity Requirements](docs/COMPLEXITY_REQUIREMENTS.md) — Deep dive into complexity metrics
- [Temporal Analysis Explained](docs/TEMPORAL_ANALYSIS_EXPLAINED.md) — The science behind the engine

## License

[Apache 2.0](LICENSE)
