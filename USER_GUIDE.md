# GitVoyant User Guide

GitVoyant v0.3.0 -- Setup, usage, CLI reference, and integration guidance.

---

## Overview

GitVoyant analyzes Git repositories to surface how code complexity evolves over time. It extracts commit history, computes cyclomatic complexity at each snapshot using language-specific parsers, fits linear regression to the resulting time series, and classifies the trend as IMPROVING, DECLINING, or STABLE with a statistical confidence score.

Supported languages: Python, JavaScript/TypeScript, Java, and Go. Language detection is automatic based on file extension. The `--language` flag restricts analysis to a single language when needed.

### Capabilities

- **Temporal analysis** -- Track complexity trends over configurable time windows with statistical confidence scoring.
- **AI agent integration** -- Conversational interface for repository analysis and interpretation.
- **Quality decay detection** -- Identify files whose complexity growth rate signals future maintenance burden.
- **Flexible input** -- Accepts local repository paths and remote Git URLs with automatic cloning and caching.

---

## Installation

### Prerequisites

GitVoyant requires Python 3.11+ and uses UV for package management.

**Install UV:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Install Python 3.11+ (if needed):**
Use [pyenv](https://github.com/pyenv/pyenv) or your OS package manager.

### Setup

1. **Clone and bootstrap:**
   ```bash
   git clone https://github.com/Cre4T3Tiv3/gitvoyant.git
   cd gitvoyant
   make bootstrap
   ```
   This creates a `.venv` via `uv`, installs core and CLI dependencies, and sets up the `gitvoyant` command in editable mode.

2. **Activate the environment:**
   ```bash
   source .venv/bin/activate
   ```

3. **Enable shell autocompletion (optional):**
   ```bash
   gitvoyant install-completion
   ```
   Follow the printed instructions for your shell.

### Model Configuration

The AI agent defaults to `claude-sonnet-4-5-20250929`. To use a different model, set `CLAUDE_MODEL` in `.env`:

```bash
# Supported models
CLAUDE_MODEL=claude-sonnet-4-5-20250929   # default
CLAUDE_MODEL=claude-opus-4-6
CLAUDE_MODEL=claude-sonnet-4-6
```

Temperature and max output tokens are also configurable:

```bash
CLAUDE_TEMPERATURE=0.1   # default
CLAUDE_MAX_TOKENS=8192   # default
```

---

## Makefile Command Reference

### Setup Commands

| Command | Description |
|---------|-------------|
| `make bootstrap` | Create `.venv` and install all dependencies |
| `make install` | Install core dependencies |
| `make dev` | Install development dependencies |
| `make cli` | Install CLI entry point in editable mode |
| `make cli-complete` | Install CLI with shell autocompletion |
| `make completions-debug` | Debug CLI app discovery for completion |

### Development Workflow

| Command | Description |
|---------|-------------|
| `make lint` | Run Ruff linting |
| `make format` | Format code using Ruff |
| `make test` | Run all tests (unit, integration, CLI, coverage) |
| `make test-unit` | Run unit tests |
| `make test-integration` | Run integration tests |
| `make test-cli` | Run CLI-level tests |
| `make test-coverage` | Run tests with coverage report |

### Utility

| Command | Description |
|---------|-------------|
| `make clean` | Remove temp and build artifacts |
| `make version` | Show version and system info |
| `make check-path` | Print current PYTHONPATH |
| `make check-uv` | Verify `uv` is installed |

---

## Usage

### Basic Commands

```bash
gitvoyant --help       # Show available commands and options
gitvoyant version      # Display version information
```

### Temporal Analysis

Analyze how code complexity evolves over time in a repository.

**Analyze entire repository (all supported languages):**
```bash
gitvoyant analyze temporal /path/to/repo
```

**Analyze a specific file:**
```bash
gitvoyant analyze temporal /path/to/repo main.py
```

**Restrict to a single language:**
```bash
gitvoyant analyze temporal /path/to/repo --language javascript
```

**Custom time window:**
```bash
gitvoyant analyze temporal /path/to/repo --window-days 90
```

**Remote repository:**
```bash
gitvoyant analyze temporal https://github.com/user/repo.git
```

Remote repositories are cloned automatically to a temporary directory. Subsequent runs reuse the existing clone.

#### Temporal Analysis Options

| Option | Default | Description |
|--------|---------|-------------|
| `--window-days` | 180 | Days of commit history to analyze |
| `--language` | (all) | Restrict analysis to a single language: `python`, `javascript`, `java`, or `go` |

### AI Agent Analysis

Launch an interactive agent session for conversational repository analysis.

```bash
gitvoyant analyze agent
```

The agent accepts natural language questions and runs temporal analysis to produce answers.

**Example interaction:**
```
You: What is the decay rate of src/gitvoyant/cli/analyze.py?

GitVoyant: Based on the analysis:
- The file shows a negative trend of -0.35 per month, indicating decreasing complexity over time.
- It has LOW exposure and a risk score of 0.00.
- The analysis is based on 11 commits.
- This file is well-maintained with improving code quality and minimal decay risk.
```

**Agent capabilities:**
- File-level decay pattern analysis
- Repository-wide health assessments
- Refactoring priority recommendations
- Trend interpretation and explanation

### Command Reference

#### Core Commands

| Command | Description |
|---------|-------------|
| `gitvoyant --help` | Show main help and available commands |
| `gitvoyant version` | Display version |
| `gitvoyant install-completion` | Set up shell autocompletion |

#### Analysis Commands

| Command | Description |
|---------|-------------|
| `gitvoyant analyze temporal <repo> [file]` | Run temporal complexity analysis |
| `gitvoyant analyze agent` | Launch interactive AI agent |

---

## Interpretation Guide

### Health Score

The overall repository health score is computed from all evaluated files. Higher positive scores indicate increasing complexity trends across the codebase.

### Temporal Score Indicators

The CLI displays a text marker alongside each file's temporal score:

| Marker | Score Range | Meaning |
|--------|-------------|---------|
| `[+]` green | < -0.25 | Decreasing complexity. Current practices are effective. |
| `[~]` yellow | -0.25 to +0.25 | Stable complexity. Monitor for changes. |
| `[-]` red | > +0.25 | Increasing complexity. Consider refactoring or targeted review. |

### Risk Indicators

- **High positive scores (> 1.0):** Files gaining complexity rapidly.
- **High-change files with positive trends:** Frequently modified files where each change adds complexity.
- **Legacy components with increasing scores:** Older files accumulating structural debt.

---

## Best Practices

### Regular Monitoring

- Run temporal analysis on a regular cadence against main repositories.
- Prioritize files with the highest positive temporal scores.
- Track trends across analysis runs to identify persistent patterns.

### AI Agent Usage

- Ask specific questions about files flagged by temporal analysis.
- Request refactoring priority rankings.
- Use the agent to interpret complex temporal patterns for team communication.

---

## Advanced Usage

### Custom Analysis Windows

Adjust the analysis timeframe to match project cadence:

```bash
# Short-term trend (30 days)
gitvoyant analyze temporal ./repo --window-days 30

# Long-term trend (1 year)
gitvoyant analyze temporal ./repo --window-days 365
```

### Batch Analysis

Analyze multiple repositories in sequence:

```bash
#!/bin/bash
repos=(
    "https://github.com/org/repo1.git"
    "https://github.com/org/repo2.git"
    "./local/repo3"
)

for repo in "${repos[@]}"; do
    echo "Analyzing $repo..."
    gitvoyant analyze temporal "$repo"
    echo "---"
done
```

### CI/CD Integration

Example GitHub Actions workflow:

```yaml
name: Code Quality Analysis
on: [push, pull_request]

jobs:
  gitvoyant-analysis:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
      with:
        fetch-depth: 0

    - name: Install UV
      run: curl -LsSf https://astral.sh/uv/install.sh | sh

    - name: Setup GitVoyant
      run: |
        git clone https://github.com/Cre4T3Tiv3/gitvoyant.git
        cd gitvoyant
        make bootstrap

    - name: Run Temporal Analysis
      run: |
        cd gitvoyant
        .venv/bin/gitvoyant analyze temporal ${{ github.workspace }}
```

### Programmatic Access

The temporal evaluation service can be used directly from Python:

```python
from gitvoyant import TemporalEvaluatorService

service = TemporalEvaluatorService()
result = await service.evaluate_repository("/path/to/repo")
```

---

## Troubleshooting

### Common Issues

**"UV not found" error:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Autocompletion not working:**
Run `gitvoyant install-completion` and follow the shell-specific instructions.

**CLI not found after bootstrap:**
Activate the virtual environment or add `.venv/bin` to your `PATH`:
```bash
source .venv/bin/activate
```

**Python version mismatch:**
GitVoyant requires Python 3.11+. Install via [pyenv](https://github.com/pyenv/pyenv) or your OS package manager.

**"Repository path does not exist":**
- Verify the path to the Git repository.
- Confirm the directory contains a `.git` folder.
- Check file permissions.

**"Path is not a Git repository":**
- Initialize Git if needed: `git init`
- Verify you are in the correct directory.
- Confirm `.git` exists and is not corrupted.

**Remote repository access failures:**
- Verify the Git URL is reachable.
- Check network connectivity.
- Confirm authentication credentials for private repositories.

**Python path issues:**
```bash
make check-path    # Inspect current PYTHONPATH
make clean         # Reset environment
make bootstrap     # Rebuild from scratch
```

### Getting Help

- `gitvoyant --help` for command reference.
- [GitHub Issues](https://github.com/Cre4T3Tiv3/gitvoyant/issues) for bug reports and feature requests.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup, guidelines, and contribution standards.

## License

GitVoyant v0.3.0 is licensed under [Apache 2.0](LICENSE).
