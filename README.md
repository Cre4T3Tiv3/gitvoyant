# 🔮 GitVoyant

**Researching Temporal Code Intelligence**

> Exploring the evolution layer that AI code agents need

<p align="center">
  <a href="https://github.com/Cre4T3Tiv3/gitvoyant" target="_blank">
    <img src="https://raw.githubusercontent.com/Cre4T3Tiv3/gitvoyant/main/docs/assets/gitvoyant_v0.1.0.jpeg" alt="GitVoyant social preview" width="640"/>
  </a>
</p>

<p align="center">
  <a href="https://github.com/Cre4T3Tiv3/gitvoyant">
    <img src="https://img.shields.io/badge/status-alpha-orange.svg" alt="Status: Alpha">
  </a>
  <a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python: 3.8+">
  </a>
  <a href="https://github.com/Cre4T3Tiv3/gitvoyant/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/License-Apache_2.0-blue.svg" alt="License: Apache 2.0">
  </a>
  <a href="https://bytestacklabs.com">
    <img src="https://img.shields.io/badge/Made%20by-ByteStack%20Labs-2ea44f" alt="ByteStack Labs">
  </a>
  <a href="#contributing" target="_blank">
    <img src="https://img.shields.io/badge/contributions-welcome-brightgreen.svg" alt="Contributions welcome">
  </a>
  <a href="https://github.com/pallets/flask">
    <img src="https://img.shields.io/badge/Validated-Flask%20Core-blue" alt="Flask Validated">
  </a>
  <a href="https://github.com/Cre4T3Tiv3/gitvoyant/stargazers">
    <img src="https://img.shields.io/github/stars/Cre4T3Tiv3/gitvoyant?style=social" alt="GitHub Stars">
  </a>
</p>

## 🏆 Key Discovery

**Flask Quality Engineering Recognition:**
- **File**: `src/flask/app.py` (foundation of Python web development)
- **Analysis**: 44 commits over 1095 days from 6 developers
- **Result**: Complexity trend: -1.46 units/month and Overall change: -26.5%
- **Pattern**: Quality engineering signature detected

*This suggests revealing temporal patterns that current AI tools might completely miss*

## The Missing Layer in AI Code Tools

Current AI code assistants analyze **snapshots**; what's wrong right now.
But AI agents need **evolution context**; how code changes over time.

**The Problem:**
- Static analysis catches present bugs
- Code reviews focus on current state  
- AI tools miss temporal patterns
- No understanding of quality evolution

**The Gap:**
```
Current AI: "This code is complex"
Missing: "This code is becoming simpler through quality engineering"
```

## What GitVoyant Explores

**Temporal Code Intelligence**: analyzing Git history to understand code evolution patterns that could enable smarter AI agents.

```python
from src.core.temporal_evaluator import TemporalEvaluator

evaluator = TemporalEvaluator("path/to/repo")
outcome = evaluator.evaluate_file_evolution("src/core/models.py")

print(f"Complexity trend: {outcome['complexity_trend_slope']:+.2f}/month")
print(f"Quality pattern: {outcome['risk_level']}")
# Output: Complexity trend: -1.46/month
# Output: Quality pattern: LOW
```

**GitVoyant Discovers:**
- ✅ Quality engineering signatures (like Flask's complexity reduction)
- 🚨 Technical debt accumulation patterns  
- 📈 Maintenance trajectory predictions
- 👥 Team engineering effectiveness patterns
- 🔮 Temporal context for AI agents

## Real Analysis Results

**Validated on industry-standard repositories:**

| **Flask** | `app.py` | ✅ **Quality Engineering** | -1.46/month | Active optimization |
| **Research** | Various | 🔍 **Pattern Detection** | Ongoing | Alpha validation |

## 🤖 Agent Platform Vision

GitVoyant explores what could become **foundational infrastructure for AI code agents**.

### Why Agents Need Temporal Intelligence

**Current AI Code Tools:**
- Analyze current state only
- Miss evolution patterns  
- Can't predict quality trajectory
- Limited historical context

**Temporal-Enabled Agents Could:**
- Understand code evolution over time
- Recognize quality engineering patterns
- Predict maintenance challenges
- Learn from historical success patterns

### Research Direction

```python
# Future agent capabilities we're exploring
agent = GitVoyantAgent()

# Natural language temporal analysis
agent.query("Show me files with Flask-like quality patterns")
agent.predict("Where will complexity grow in the next 6 months?")
agent.recommend("How can we improve our temporal signature?")

# Autonomous code intelligence
agent.monitor_quality_trends()
agent.suggest_proactive_refactoring()
agent.identify_engineering_best_practices()
```

### The Platform Hypothesis

GitVoyant could provide the **temporal data layer** that enables:
- **Smarter code agents** with historical context
- **Predictive development assistance** 
- **Quality-aware automation**
- **Engineering pattern learning**

*Investigating: temporal intelligence → agent integration → autonomous code evolution*

## Quick Start

```bash
# Clone and setup in one command
git clone https://github.com/Cre4T3Tiv3/gitvoyant.git
cd gitvoyant
make quick-start
```

**That's it!** The demo visualization will be generated automatically.

### Available Commands

```bash
make help          # Show all available commands
make check-uv      # Verify UV package manager installation
make install       # Install project dependencies via UV
make demo          # Generate temporal evaluation visualization  
make clean         # Remove Python cache files and artifacts
make quick-start   # Complete setup: install deps + run demo
```

### Manual Installation

```bash
# Install UV (modern Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install GitVoyant
uv sync

# Run analysis
uv run examples/flask_discovery_demo.py
```

## Usage Examples

### Analyze Any Repository

```python
from src.core.temporal_evaluator import TemporalEvaluator

# Initialize evaluator
evaluator = TemporalEvaluator("path/to/your/repo")

# Get comprehensive evaluation
evaluation = evaluator.analyze_file_evolution("path/to/file.py")

print(f"Commits evaluated: {outcome['commits_evaluated']}")
print(f"Complexity trend: {outcome['complexity_trend_slope']:+.2f}/month")
print(f"Risk exposure level: {outcome['exposure_level']}")
```

### Generate Insights

```python
# Get actionable insights
discernment = evaluator.generate_discernment("path/to/file.py")

for insight in discernment:
    print(f"📊 {insight.description}")
    print(f"   Confidence: {insight.confidence:.0%}")
```

### Command Line Usage

```bash
# Analyze any file
uv run python -m src.core.temporal_evaluator . src/main.py

# Generate demo visualization
uv run examples/flask_discovery_demo.py
```

## Current Status: Alpha (v0.1.0)

🔮 **Research Validated:**
- ✅ Git history temporal evaluation working
- ✅ Quality pattern recognition (Flask validated)
- ✅ Complexity trend detection  
- ✅ Real production code validation
- ✅ Professional visualization
- ✅ Temporal signatures distinguishable

🚀 **Investigating Next (v0.2.0):**
- 🤖 Agent framework integration
- 💬 Natural language temporal queries
- 📊 Multi-file repository evaluation  
- 👥 Developer expertise correlation
- 🌐 Conversational code intelligence
- 🔍 Multi-language temporal patterns

## The Science Behind It

GitVoyant uses temporal pattern evaluation to identify code evolution signatures:

- **Temporal Complexity Analysis**: Tracks how cyclomatic complexity evolves
- **Quality Pattern Recognition**: Identifies improvement vs decay signatures
- **Change Pattern Analysis**: Maps modification patterns to quality outcomes  
- **Risk Correlation Modeling**: Predicts future maintenance burden
- **Developer Impact Assessment**: Analyzes how team changes affect code health

*Read more: [docs/temporal_analysis_explained.md](docs/temporal_analysis_explained.md)*

## Research Validation

GitVoyant has been tested against production repositories:

- **Flask Analysis**: Discovered quality engineering patterns (-25% complexity reduction)
- **Requests Analysis**: Confirmed stable maintenance patterns (0% growth)
- **Pattern Classification**: Distinguishes quality from decay signatures
- **Production Ready**: Handles real Git histories and large codebases

*Run `make demo` to see live validation results*

## Why This Research Matters

### Traditional Approach (Snapshot)
```
Code Review → Find Current Issues → Fix Current Issues
```
**Limitation**: Reactive, misses evolving patterns, no quality recognition

### Temporal Intelligence Approach (Evolution)
```
Historical Analysis → Recognize Quality Patterns → Guide Future Decisions
```
**Advantage**: Proactive, recognizes excellence, predicts trajectory, enables smarter agents

## Contributing to the Research

This explores uncharted territory in code intelligence. GitVoyant investigates how temporal evaluation could transform AI-assisted development.

**Current research areas:**
- Quality pattern recognition across languages
- Temporal intelligence for AI agent platforms
- Engineering effectiveness measurement
- Predictive code quality assessment

## Research Roadmap

### v0.2.0 - Agent Framework Investigation
- Natural language temporal queries
- Multi-file evolution analysis
- Developer effectiveness correlation
- Conversational code intelligence

### v0.3.0 - Multi-Language Temporal Patterns
- JavaScript/TypeScript evolution analysis
- Java quality pattern recognition
- Go code trajectory tracking
- Language-agnostic temporal insights

### v0.4.0 - Production Platform
- Web interface and dashboard
- REST API for agent integration
- CI/CD temporal monitoring
- Team collaboration insights

*Want early access to new features? ⭐ Star the repo for updates*

## License

Apache License 2.0 - see [LICENSE](LICENSE) for details.

## Research Collaboration

- 📖 **Documentation**: [docs/](docs/)
- 🐛 **Issues**: [GitHub Issues](https://github.com/Cre4T3Tiv3/gitvoyant/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/Cre4T3Tiv3/gitvoyant/discussions)
- 🔬 **Research**: [DISCOVERY.md](DISCOVERY.md)

---

## Author

**🔮 GitVoyant** by [Jesse Moses (@Cre4T3Tiv3)](https://github.com/Cre4T3Tiv3) at [ByteStack Labs](https://bytestacklabs.com)

*Investigating: Could temporal intelligence become the missing foundation layer for AI code agents?*

**🔮 Discover what temporal patterns reveal about your code's evolution**

---
