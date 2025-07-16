# 🔮 GitVoyant

**AI Agent Platform for Temporal Code Intelligence**  
*The missing evolution layer that AI code agents need*

<p align="center">
  <a href="https://github.com/Cre4T3Tiv3/gitvoyant" target="_blank">
    <img src="https://raw.githubusercontent.com/Cre4T3Tiv3/gitvoyant/main/docs/assets/gitvoyant_v0.2.0.jpeg" alt="GitVoyant v0.2.0" width="640"/>
  </a>
</p>

<p align="center">
  <a href="https://github.com/Cre4T3Tiv3/gitvoyant/actions/workflows/ci.yml" target="_blank">
    <img src="https://github.com/Cre4T3Tiv3/gitvoyant/actions/workflows/ci.yml/badge.svg?branch=main" alt="CI">
  </a>
  <a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/badge/python-3.11+-blue.svg" alt="Python: 3.11+">
  </a>
  <a href="https://github.com/Cre4T3Tiv3/gitvoyant/releases/tag/v0.2.0">
    <img src="https://img.shields.io/badge/version-v0.2.0-brightgreen" alt="Version: v0.2.0">
  </a>
  <a href="https://github.com/Cre4T3Tiv3/gitvoyant">
    <img src="https://img.shields.io/badge/status-stable-green.svg" alt="Status: Stable">
  </a>
  <a href="https://github.com/Cre4T3Tiv3/gitvoyant/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/License-Apache_2.0-blue.svg" alt="License: Apache 2.0">
  </a>
</p>

<p align="center">
  <a href="https://bytestacklabs.com">
    <img src="https://img.shields.io/badge/Made%20by-ByteStack%20Labs-2ea44f" alt="ByteStack Labs">
  </a>
  <a href="https://github.com/Cre4T3Tiv3/gitvoyant/stargazers">
    <img src="https://img.shields.io/github/stars/Cre4T3Tiv3/gitvoyant?style=social" alt="GitHub Stars">
  </a>
  <a href="#contributing" target="_blank">
    <img src="https://img.shields.io/badge/contributions-welcome-brightgreen.svg" alt="Contributions welcome">
  </a>
</p>

---

## 🚀 Quick Start

```bash
git clone https://github.com/Cre4T3Tiv3/gitvoyant.git
cd gitvoyant
make bootstrap
```

📖 **[Complete Setup Guide & Documentation →](USER_GUIDE.md)**

---

## 🏛️ Architecture

GitVoyant v0.2.0 is built using **Domain-Driven Design (DDD)** principles with Clean Architecture patterns, ensuring maintainable, extensible, and reliable code:

- **🎯 Domain Layer**: Rich entities (`TemporalEvaluation`) and value objects (`ComplexityTrend`, `ConfidenceRank`) with embedded business logic
- **🏗️ Application Layer**: Use cases orchestrating business workflows with clear separation of concerns
- **📡 Infrastructure Layer**: Core temporal intelligence engine with Git integration and statistical analysis
- **🎨 Presentation Layer**: CLI interface and AI agent integration with natural language capabilities

📊 **[→ View Interactive Architecture Diagram](https://Cre4T3Tiv3.github.io/gitvoyant/)**

> **Architecture Philosophy**: Clean boundaries between domain logic, infrastructure, and presentation layers enable independent evolution and testing of each component.

---

## 🧪 Quality & Testing Excellence

<p align="center">
  <img src="https://raw.githubusercontent.com/Cre4T3Tiv3/gitvoyant/main/docs/assets/gitvoyant_code_cov_71_percent_v0_2_0.png" alt="Test Coverage: 55+%" width="100%"/>
</p>

**Current Test Coverage: 55+%**
- ✅ **Unit Tests**: Domain entities, value objects, and core algorithms
- ✅ **Integration Tests**: Full workflow testing with real Git repositories  
- ✅ **Agent Tests**: AI agent interaction and tool integration
- ✅ **CLI Tests**: Command-line interface and intuitive output formatting

*Comprehensive test suite ensures reliability across temporal analysis, Git integration, and AI agent workflows.*

---

## 🤖 AI Agent Intelligence in Action

**Live Temporal Intelligence**: The Claude-powered agent provides conversational access to GitVoyant's temporal analysis engine:

```bash
💬 You: "Which files in this repo need the most attention?"
🤖 Claude: Analyzing repository temporal patterns...

📦 Repository decay risks:
src/api/handlers.py: 0.85 (HIGH RISK - complexity growing +2.3/month)
utils/data_processing.py: 0.72 (MEDIUM RISK - declining pattern detected)  
core/business_logic.py: 0.68 (MEDIUM RISK - confidence: 0.4 - limited history)
```

> **Note**: Currently supports **Claude AI only**. Multi-LLM support (GPT-4, Gemini, Local LLMs) planned for v0.3.0.

---

## 🚀 What's New in v0.2.0

### ✅ Enhanced Temporal Intelligence Engine

* 🔬 **Confidence Scoring**: Statistical confidence based on commit history depth
* ⚠️ **Low Confidence Warnings**: Transparent reliability indicators for limited data
* 📊 **Progressive Disclosure**: Higher confidence with more temporal data points
* 🎯 **Improved Risk Assessment**: Enhanced quality decay forecasting algorithms

### ✅ Stable & Reliable Platform

* 🏗️ **Domain-Driven Architecture**: Clean separation with rich domain entities
* 🔮 **Claude + LangChain** integration for natural language interaction
* 🧠 **AI Agent Runtime**: Conversational temporal intelligence analysis
* 📊 **Comprehensive Testing**: 55+% test coverage across all layers

---

## 📸 GitVoyant CLI in Action

### 🎨 CLI Interface

_GitVoyant provides a Rich-formatted CLI experience:_

<p align="center">
  <img src="https://raw.githubusercontent.com/Cre4T3Tiv3/gitvoyant/main/docs/assets/gitvoyant_cmd_v0_2_0.png" alt="GitVoyant CLI" width="100%"/>
</p>

**Visual Features:**
- 📋 **Command Structure**: Organized help system with clear options
- 🔍 **Auto-Completion**: Shell completion support for enhanced productivity
- 📊 **Typography**: Clean terminal formatting with proper spacing

---

### 🔬 Temporal Analysis

_Deep temporal analysis with statistical confidence and visual indicators._

<p align="center">
  <img src="https://raw.githubusercontent.com/Cre4T3Tiv3/gitvoyant/main/docs/assets/gitvoyant_analyze_temporal_cmd_v0_2_0.png" alt="Temporal Analysis" width="100%"/>
</p>

**What You See:**
- 🔮 **Banner**: Welcome message with version and branding
- 📊 **Info Grid**: Repository stats with 🔍📊📂 indicators
  - 🔍 Repository path
  - 📊 Health score (-0.35 = improving complexity)
  - 📂 Number of evaluated files
- 📋 **Results Table**: Color-coded temporal scores
  - 🟢 **Green Circle**: -0.35 indicates decreasing complexity
  - File paths in cyan
  - Clean table formatting

**Status Messages:**
- 💙 **Info**: "Initializing temporal analysis..." in cyan
- ✅ **Success**: "Temporal evaluation complete" in green with checkmark

---

### 🧠 AI Agent

_Conversational temporal intelligence powered by Claude AI._

<p align="center">
  <img src="https://raw.githubusercontent.com/Cre4T3Tiv3/gitvoyant/main/docs/assets/gitvoyant_analyze_agent_cmd_v0_2_0.png" alt="AI Agent Temporal Analysis" width="100%"/>
</p>

**Agent Experience:**
- 🧠 **Natural Language**: Ask questions in plain English about code quality
- 💬 **Interactive Dialog**: Real-time conversation with temporal analysis
- 📊 **Detailed Analysis**: Specific decay rates, risk scores, and recommendations

**Conversation Flow:**
```
💬 You: What is the decay rate of src/gitvoyant/cli/analyze.py?

🤖 Claude: Based on the analysis:
- The file shows a negative trend of -0.35 per month, indicating decreasing complexity over time
- It has LOW exposure and a risk score of 0.00
- The analysis is based on 11 commits
- Overall, this file appears to be well-maintained with improving code quality and minimal decay risk
```

**Agent Capabilities:**
- 🔍 **File-Specific Analysis**: Deep dive into individual file patterns
- 📈 **Trend Interpretation**: Explains what temporal patterns mean
- 💡 **Actionable Insights**: Provides specific recommendations
- 📊 **Statistical Context**: Includes commit counts and confidence levels

---

### 🎯 CLI Design

GitVoyant implements modern terminal UI principles:

#### **🎨 Visual Design**
- **Indicators**: 🔍📊📂 for quick scanning
- **Color Coding**: Green/yellow/red for pattern recognition
- **Typography**: Clean spacing and alignment

#### **⚡ User Experience**
- **Feedback**: Status messages during operations
- **Completion**: Shell auto-completion support
- **Responsive**: Adapts to terminal width
- **Consistency**: Unified experience across commands

#### **🔍 Information Design**
- **Hierarchy**: Key information first
- **Scannable**: Tables with clear headers
- **Contextual**: Descriptive help and options
- **Transparent**: Clear status for remote operations

---

## 🔍 Core Capabilities

### 1️⃣ Temporal File Evaluation with Confidence

```python
from gitvoyant import TemporalEvaluatorService
service = TemporalEvaluatorService()
evaluation = await service.analyze_file("src/main.py")

print(f"Quality Pattern: {evaluation.quality_pattern}")
print(f"Complexity Trend: {evaluation.complexity_tenor.slope:.2f}/month")
print(f"Confidence: {evaluation.confidence_score:.2f}")

if evaluation.confidence_warning:
    print(f"⚠️ {evaluation.confidence_warning}")
```

---

### 2️⃣ Repository-Level Assessment

```python
repo = await service.analyze_repository(".")
print(f"Health Score: {repo.overall_health_score}/10.0")
print(f"Quality Distribution: {repo.quality_distribution}")

# Identify files with quality improvement patterns
improving = repo.improving_files
print(f"Files showing improvement: {len(improving)}")
```

---

### 3️⃣ Claude + LangChain Integration

```python
from gitvoyant.application.agent_runtime import create_gitvoyant_agent
agent = create_gitvoyant_agent()

response = agent.invoke({
    "input": "Which files in this repository need attention?"
})
print(response["output"])
```

---

### 4️⃣ CLI Interface

```bash
# Analyze a specific file
gitvoyant analyze temporal ./repo src/main.py

# Launch interactive AI agent
gitvoyant analyze agent

# Get help
gitvoyant --help
```

📖 **[Complete CLI Reference →](USER_GUIDE.md#command-reference)**

---

## 🔬 How Temporal Intelligence Works

GitVoyant's core algorithm implements sophisticated temporal pattern recognition:

### **1. Commit History Analysis**
```python
# Extract complexity metrics across Git history
commits = repo.iter_commits(paths=file_path, since=analysis_window)
evolution_data = [extract_metrics(commit) for commit in commits]
```

### **2. Cyclomatic Complexity Tracking**
```python
def _cyclomatic_complexity(self, ast_tree):
    complexity = 1  # Base complexity
    for node in ast.walk(ast_tree):
        if isinstance(node, (ast.If, ast.While, ast.For)):
            complexity += 1
        elif isinstance(node, ast.BoolOp):
            complexity += len(node.values) - 1
    return complexity
```

### **3. Linear Regression Trend Analysis**
```python
# Compute temporal trend using statistical analysis
complexity_trend = np.polyfit(range(len(data)), complexity_values, 1)[0]
quality_pattern = classify_pattern(complexity_trend)  # IMPROVING/DECLINING/STABLE
```

### **4. Confidence Scoring & Risk Assessment**
```python
# Enhanced confidence scoring based on data quality
if commit_count >= 10: confidence_score = 0.9
elif commit_count >= 7: confidence_score = 0.75
elif commit_count >= 5: confidence_score = 0.6
else: confidence_score = 0.4  # Low confidence warning

# Quality decay forecasting
quality_decay_forecast = min(max(complexity_growth_rate * 2, 0), 1)
```

**Key Innovation**: GitVoyant transforms raw commit data into actionable temporal intelligence through statistical analysis, pattern recognition, and predictive modeling.

---

## 🤖 The Missing Layer in AI Code Tools

```txt
Static AI: "This file has high complexity."
GitVoyant: "This file is reducing complexity monthly, this is quality engineering."
```

---

## 📦 Installation & Setup

### Quick Installation

```bash
git clone https://github.com/Cre4T3Tiv3/gitvoyant.git
cd gitvoyant
make bootstrap
```

### Environment Configuration

```bash
cp .env.example .env
# Edit .env with your ANTHROPIC_API_KEY
```

⚠️ **Note**: Requires `ANTHROPIC_API_KEY` for full AI agent features

📖 **[Complete Installation Guide →](USER_GUIDE.md#installation)**

---

## 📖 Documentation

- **[User Guide](USER_GUIDE.md)** - Complete setup, usage, and troubleshooting
- **[Temporal Analysis Explained](docs/TEMPORAL_ANALYSIS_EXPLAINED.md)** - Deep dive into the science

---

## 🗺️ Roadmap

### 🎯 v0.3.0 – Multi-LLM & Enhanced Intelligence (Q3 2025)

* 🤖 **Multi-LLM Support**: GPT-4, Gemini, Claude, Local LLMs (Ollama)
* 🔬 **Advanced Algorithms**: R-squared confidence, trend stability metrics
* 🌍 **Multi-Language Support**: JavaScript, Java, Go temporal patterns
* 📊 **Enhanced Metrics**: Maintainability index, technical debt scoring
* 🔍 **Pattern Mining**: Cross-repository quality pattern discovery

### 🚀 v0.4.0 – Enterprise Platform (Q4 2025)

* 🌐 **Web Dashboard**: Interactive temporal visualization and insights
* 🔔 **CI/CD Integration**: GitHub Actions, GitLab CI temporal monitoring
* 👥 **Team Analytics**: Developer impact analysis and collaboration patterns
* 📈 **Predictive Models**: ML-enhanced quality decay forecasting
* 🎯 **Custom Patterns**: Organization-specific quality pattern recognition

### 🌟 v0.5.0 – AI-Native Development (Q1 2026)

* 🧠 **Agent Ecosystem**: Specialized agents for different analysis domains
* 🔮 **Temporal Recommendations**: AI-powered refactoring suggestions
* 📚 **Knowledge Base**: Historical pattern learning and recommendation
* 🤝 **IDE Integration**: VSCode, IntelliJ temporal intelligence plugins
* 🌐 **Community Platform**: Shared pattern libraries and best practices

---

## 📌 Current Limitations & Future Work

### **AI Integration**
- ✅ Claude AI (Anthropic) - Full support
- 🚧 GPT-4, Gemini, Local LLMs - Planned for v0.3.0

### **Language Support**  
- ✅ Python - Complete temporal analysis
- 🚧 JavaScript, Java, Go - Research in progress

### **Confidence & Statistics**
- ✅ Commit-based confidence scoring
- 🚧 R-squared trend stability - Enhanced algorithms planned

---

## 🔬 The Science Behind It

GitVoyant uses temporal pattern evaluation to identify code evolution signatures:

* **📈 Temporal Complexity Analysis** – Tracks cyclomatic complexity evolution with linear regression
* **🎯 Quality Pattern Recognition** – Classifies IMPROVING/DECLINING/STABLE patterns with confidence scoring  
* **📊 Change Pattern Analysis** – Maps modification patterns to quality outcomes
* **🔮 Risk Correlation Modeling** – Predicts future maintenance burden with decay forecasting
* **👥 Developer Impact Assessment** – Analyzes how team changes affect code health
* **📏 Statistical Confidence** – Progressive disclosure based on temporal data quality

📖 *Learn more: [Temporal Analysis Explained](docs/TEMPORAL_ANALYSIS_EXPLAINED.md)*

---

## 🔬 Research Validation

* ✅ **Temporal Pattern Recognition**: IMPROVING/DECLINING/STABLE classification with statistical rigor
* ✅ **Confidence Scoring**: Progressive disclosure based on temporal data quality (55+% test coverage)
* ✅ **Statistical Analysis**: Linear regression trend analysis with R-squared validation
* ✅ **Real-World Ready**: Handles real Git histories and large projects with graceful degradation
* ✅ **Domain-Driven Design**: Rich entities and value objects encoding business logic

---

## 🧭 Why This Research Matters

### Traditional (Snapshot)

```
Code Review → Find Current Issues → Fix Current Issues
```

🟥 Limitation: Reactive and blind to positive evolution

---

### GitVoyant (Temporal)

```
History Analysis → Pattern Recognition → Confidence Assessment → Future Guidance
```

✅ Advantage: Proactive insights, quality discovery, predictive power, statistical honesty

---

## 🧪 Contributing

GitVoyant advances the **temporal intelligence** layer for AI-assisted development.

### Development Setup

```bash
git clone https://github.com/Cre4T3Tiv3/gitvoyant.git
cd gitvoyant
make bootstrap
make dev
```

📖 **[Complete Development Guide →](USER_GUIDE.md#development-workflow)**

### Research Areas

* 🔬 Cross-language quality pattern mining
* 🤖 Agent training via historical code context  
* 📊 Predictive engineering effectiveness models
* 🔄 CI-integrated code health monitoring
* 📈 Statistical confidence and trend stability
* 🧠 Multi-LLM temporal intelligence integration

---

## 📄 License

GitVoyant v0.2.0 is licensed under Apache 2.0.
See [`LICENSE`](LICENSE)

---

## 👤 Author

**🔮 GitVoyant** by [Jesse Moses (@Cre4T3Tiv3)](https://github.com/Cre4T3Tiv3) at [ByteStack Labs](https://bytestacklabs.com)

> Could *temporal intelligence with statistical confidence* be the missing foundation for AI-native engineering?

---

## 🎯 Get Started Now

```bash
git clone https://github.com/Cre4T3Tiv3/gitvoyant.git
cd gitvoyant
make bootstrap
gitvoyant analyze temporal . --help
```

📖 **[Complete User Guide →](USER_GUIDE.md)**

---

<p align="center">
  <strong>GitVoyant v0.2.0 - Where Temporal Intelligence Meets AI Engineering</strong><br>
  <em>Built with Domain-Driven Design • Powered by Statistical Analysis • Enhanced by AI</em>
</p>