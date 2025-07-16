# Contributing to GitVoyant

Welcome to GitVoyant! 🔮 We're excited that you're interested in contributing to the **AI Agent Platform for Temporal Code Intelligence**.

GitVoyant v0.2.0 is a production-ready platform that provides the missing evolution layer for AI code agents. Your contributions help advance the future of temporal intelligence in software development.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Research Areas](#research-areas)
- [Submitting Changes](#submitting-changes)
- [Testing](#testing)
- [Documentation](#documentation)
- [Community](#community)

## Code of Conduct

This project adheres to a code of conduct that promotes a welcoming, inclusive environment for all contributors. By participating, you agree to uphold these standards and help create a positive community focused on advancing temporal code intelligence.

## Getting Started

### Prerequisites

- **Python 3.11+** (Required)
- **[UV package manager](https://astral.sh/uv/)** (Recommended for fast dependency management)
- **Git**
- **ANTHROPIC_API_KEY** (For full AI agent features)
- Basic understanding of Git history analysis and code complexity metrics

### Quick Setup

```bash
# Clone the repository
git clone https://github.com/Cre4T3Tiv3/gitvoyant.git
cd gitvoyant

# Bootstrap complete development environment
make bootstrap
```

This will create a `.venv`, install all dependencies, and set up the CLI (`gitvoyant`) in editable mode.

## Development Setup

### Using UV (Recommended)

```bash
# Install UV if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Complete setup with virtual environment
make bootstrap

# Activate environment
source .venv/bin/activate

# Or add to PATH
export PATH="$(pwd)/.venv/bin:$PATH"
```

### Environment Configuration

```bash
cp .env.example .env
# Edit .env with your ANTHROPIC_API_KEY for AI agent features
```

## How to Contribute

### 🤖 AI Agent Enhancement

GitVoyant v0.2.0 is an **AI Agent Platform**. Contributions in this area are especially valuable:

- **Multi-LLM Support**: Extend beyond Claude to GPT-4, Gemini, Local LLMs (planned v0.3.0)
- **Agent Tools**: Enhance `temporal_analysis_tool` and `repo_evaluation_tool`
- **Natural Language Interface**: Improve conversational capabilities
- **Agent Runtime**: Optimize LangGraph ReAct agent performance
- **Context Management**: Better response formatting and output handling

### 🏗️ Architecture Contributions

GitVoyant uses **Domain-Driven Design** with Clean Architecture:

- **Domain Layer**: Enhance rich entities (`TemporalEvaluation`) and value objects (`ComplexityTrend`)
- **Application Layer**: Improve use cases and business workflow orchestration
- **Infrastructure Layer**: Optimize Git integration and statistical analysis
- **Presentation Layer**: Enhance Rich CLI formatting and user experience

### 🔬 Temporal Intelligence Research

- **Confidence Scoring**: Improve statistical confidence algorithms (currently 0.4-0.9 scale)
- **Pattern Recognition**: Enhance IMPROVING/DECLINING/STABLE classification
- **Language Support**: Extend beyond Python to JavaScript, Java, Go (v0.3.0 roadmap)
- **Statistical Models**: Add R-squared validation and trend stability metrics
- **Quality Decay Forecasting**: Improve predictive capabilities

### 🐛 Bug Reports

When reporting bugs, please include:

1. **Environment**: Python version, OS, UV version, GitVoyant version
2. **Repository Context**: Type and size of repository being analyzed
3. **Command Used**: Exact CLI command that caused the issue
4. **Expected vs Actual**: What temporal patterns you expected vs what GitVoyant found
5. **Agent Context**: If using AI agent, include conversation context

Use this template:

```markdown
## Bug Description
Brief description of the issue

## Environment
- GitVoyant version: v0.2.0
- Python version: 3.11+
- Operating System: 
- UV version:
- Repository analyzed:

## Steps to Reproduce
1. Run command: `gitvoyant analyze temporal /path/to/repo`
2. Expected: Clean temporal analysis output
3. Actual: Error or unexpected pattern

## CLI Output
```
[Paste complete CLI output including any error messages]
```

## Additional Context
Any other relevant information about the codebase being analyzed
```

### 🚀 Feature Requests

We're particularly interested in features that advance the AI agent platform:

**v0.3.0 Planned Features** (Contributions Welcome):
- **Multi-LLM Support**: GPT-4, Gemini, Claude, Local LLMs (Ollama)
- **Advanced Algorithms**: R-squared confidence, trend stability metrics
- **Multi-Language Support**: JavaScript, Java, Go temporal patterns
- **Enhanced Metrics**: Maintainability index, technical debt scoring

**v0.4.0 Enterprise Features**:
- **Web Dashboard**: Interactive temporal visualization
- **CI/CD Integration**: GitHub Actions, GitLab CI monitoring
- **Team Analytics**: Developer impact analysis
- **Predictive Models**: ML-enhanced quality forecasting

## Research Areas

### Current Focus (v0.2.0 → v0.3.0)

- 🤖 **Multi-LLM Integration**: Expanding beyond Claude AI
- 📊 **Statistical Enhancement**: R-squared validation and confidence improvements
- 🌍 **Language Expansion**: JavaScript, TypeScript, Java, Go support
- 🔬 **Advanced Patterns**: Cross-repository quality pattern discovery
- 📈 **Predictive Models**: Enhanced quality decay forecasting

### Future Research Directions

- **Agent Ecosystem**: Specialized agents for different analysis domains
- **Enterprise Platform**: Web dashboards and CI/CD integration
- **Knowledge Base**: Historical pattern learning and recommendations
- **IDE Integration**: VSCode, IntelliJ plugins for real-time temporal intelligence

## Development Workflow

### Makefile Commands (v0.2.0)

**Setup & Installation:**
```bash
make bootstrap      # 🔁 Complete setup: .venv + dependencies + CLI
make install        # 📦 Install core dependencies only
make dev           # 🧪 Install development dependencies
make cli           # 📦 Install CLI entry point in editable mode
```

**Development & Testing:**
```bash
make lint          # 🔍 Run Ruff linting
make format        # ✨ Format code using Ruff
make test          # 🧪 Run all tests (55+% coverage)
make test-unit     # 🔬 Run unit tests only
make test-cli      # 💻 Run CLI-level tests
make test-coverage # 📊 Run tests with coverage report
```

**Utilities:**
```bash
make clean         # 🧹 Remove temp and build artifacts
make version       # 📋 Show version and system info
make check-uv      # 🔍 Ensure UV is installed
```

## Submitting Changes

### Pull Request Process

1. **Fork and Branch**: Create a feature branch from `main`
   ```bash
   git checkout -b feature/multi-llm-support
   # or
   git checkout -b fix/confidence-scoring-bug
   ```

2. **Development Setup**: Ensure proper development environment
   ```bash
   make bootstrap  # Complete setup
   make dev       # Development dependencies
   ```

3. **Test Your Changes**: Ensure compatibility with existing functionality
   ```bash
   make test              # Run full test suite
   make lint              # Check code quality
   
   # Test CLI functionality
   gitvoyant analyze temporal . --help
   gitvoyant analyze agent    # Test AI agent (requires ANTHROPIC_API_KEY)
   ```

4. **Document Your Changes**: Update relevant documentation
   - Code changes → Update docstrings
   - New features → Update USER_GUIDE.md
   - Architecture changes → Update README.md
   - Breaking changes → Update CHANGELOG.md

5. **Submit PR**: Include:
   - Clear description of temporal intelligence improvements
   - Before/after analysis results if applicable
   - Test coverage for new features
   - Documentation updates
   - Future roadmap implications

### Commit Message Format

Use clear, descriptive commit messages that reflect the production nature of v0.2.0:

```
feat: add GPT-4 support to agent runtime
feat: enhance confidence scoring with R-squared validation  
fix: resolve CLI error handling for remote repositories
docs: update temporal analysis examples in USER_GUIDE
test: add integration tests for multi-file analysis
refactor: optimize domain entity validation logic
```

## Testing

### Running Tests (55+% Coverage)

```bash
# Full test suite
make test

# Specific test categories
make test-unit         # Domain entities, value objects, algorithms
make test-integration  # Full workflow with real Git repositories
make test-cli          # CLI interface and Rich formatting
make test-coverage     # Generate coverage report
```

### Testing AI Agent Features

```bash
# Requires ANTHROPIC_API_KEY in .env
gitvoyant analyze agent

# Test temporal analysis
gitvoyant analyze temporal . 
gitvoyant analyze temporal https://github.com/user/repo.git
```

### Validation Testing

When contributing new analysis capabilities:

1. **Test on Known Repositories**: Validate against popular open-source projects
2. **Statistical Accuracy**: Verify confidence scoring and trend analysis
3. **Agent Integration**: Ensure AI tools work correctly with new features
4. **CLI Experience**: Test Rich formatting and user experience
5. **Performance**: Validate with large repositories and long Git histories

## Documentation

### Technical Documentation

- **Architecture**: Document DDD patterns and Clean Architecture decisions
- **Domain Logic**: Explain business rules in domain entities and value objects
- **Agent Integration**: Document LangChain/Claude integration patterns
- **Statistical Methods**: Explain confidence scoring and trend analysis algorithms

### User Documentation

- **USER_GUIDE.md**: Update for new features and CLI changes
- **CLI Help**: Ensure `--help` text is comprehensive and accurate
- **Agent Capabilities**: Document new AI agent features and conversations
- **Examples**: Provide real-world usage examples

### Code Documentation

- Use Google-style docstrings for all public methods
- Include type hints throughout the codebase
- Document statistical assumptions and limitations
- Explain temporal analysis concepts for newcomers

## Quality Standards

### Code Quality (v0.2.0 Standards)

- **Type Safety**: Full type annotations using Python 3.11+ features
- **Domain-Driven Design**: Rich entities with embedded business logic
- **Clean Architecture**: Clear separation of concerns across layers
- **Test Coverage**: Maintain 55+% coverage, aim for 70+%
- **Error Handling**: Robust error recovery and graceful degradation

### Performance Standards

- **Large Repository Support**: Handle repositories with 1000+ commits
- **Memory Efficiency**: Optimize for repositories with extensive history
- **Agent Response Time**: Keep AI agent interactions under 10 seconds
- **CLI Responsiveness**: Rich formatting should not impact performance

## Community

### Getting Help

- **GitHub Discussions**: [Research questions and feature discussions](https://github.com/Cre4T3Tiv3/gitvoyant/discussions)
- **GitHub Issues**: [Bug reports and feature requests](https://github.com/Cre4T3Tiv3/gitvoyant/issues)
- **ByteStack Labs**: [Technical support and collaboration](https://bytestacklabs.com)

### Collaboration Opportunities

GitVoyant welcomes academic and industry collaborations:

- **University Research**: Student projects on temporal code analysis and AI agents
- **Industry Partnerships**: Enterprise temporal intelligence integration
- **AI Research**: Multi-LLM support and agent framework development
- **Open Source**: Contributing to the temporal intelligence ecosystem

### Recognition

Contributors who advance GitVoyant's AI agent platform will be:

- Acknowledged in release notes and documentation
- Featured as collaborators in the project
- Invited to co-author research publications
- Recognized in the temporal intelligence community

---

## Roadmap Alignment

### v0.3.0 Contribution Opportunities (Q3 2025)

**High Priority:**
- Multi-LLM support (GPT-4, Gemini, Local LLMs)
- Enhanced statistical models with R-squared validation
- JavaScript/TypeScript temporal pattern analysis
- Advanced confidence metrics and trend stability

**Medium Priority:**
- Java and Go language support
- Enhanced maintainability index calculations
- Cross-repository pattern discovery
- Improved agent conversation capabilities

### v0.4.0 Enterprise Features (Q4 2025)

**Platform Development:**
- Web dashboard with interactive visualizations
- CI/CD integration and monitoring
- Team analytics and developer impact analysis
- Enterprise deployment and scaling

---

## Questions?

GitVoyant v0.2.0 represents a significant evolution from research prototype to production AI agent platform. If you have questions about:

- **Architecture**: How DDD and Clean Architecture principles are applied
- **AI Integration**: Claude agent runtime and LangChain implementation
- **Temporal Intelligence**: Statistical methods and confidence scoring
- **Roadmap**: Multi-LLM support and enterprise features
- **Collaboration**: Research partnerships and industry integration

Feel free to [open a discussion](https://github.com/Cre4T3Tiv3/gitvoyant/discussions) or reach out to [@Cre4T3Tiv3](https://github.com/Cre4T3Tiv3).

---

**🔮 Together, let's build the temporal intelligence foundation that AI code agents need to understand how code evolves over time.**

---

*GitVoyant v0.2.0 by [Jesse Moses (@Cre4T3Tiv3)](https://github.com/Cre4T3Tiv3) at [ByteStack Labs](https://bytestacklabs.com)*

*Could temporal intelligence with statistical confidence be the missing foundation for AI-native engineering?*

---
