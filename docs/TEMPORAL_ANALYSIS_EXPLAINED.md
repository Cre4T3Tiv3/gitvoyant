# Temporal Evaluation Explained

Traditional static analysis examines code at a single point in time. GitVoyant introduces temporal evaluation, tracking how code evolves over time to identify quality trajectories before they become production incidents.

## Core Concepts

### Temporal Complexity Evolution

Code complexity has momentum. Files that show steady complexity growth tend to continue growing. Stable files tend to remain stable. The rate of complexity change is more predictive of future maintenance burden than absolute complexity at any single snapshot.

### Quality Decay Signatures

Certain patterns in code evolution correlate with future maintenance problems: rapid complexity spikes during deadline-driven development, consistent upward trends without refactoring, high-frequency modifications in already-complex areas, and multiple contributor patterns compressing into the same timeframe.

### Predictive Modeling

GitVoyant uses temporal pattern evaluation to identify files at risk of quality decay.

```
Quality Decay Risk = f(
    complexity_trend,
    change_frequency,
    author_diversity,
    modification_patterns
)
```

## Algorithm

### Phase 1: Temporal Data Extraction

Git history is extracted for target files. Complexity metrics are calculated at each commit using language-specific parsers (Python via built-in `ast`, JavaScript/Java/Go via tree-sitter). Trends, spikes, and anomalies are identified from the resulting time series.

### Phase 2: Risk Assessment

Linear regression is fitted to the complexity time series to compute trend slope (complexity change per month). Volatility is measured as the standard deviation of complexity changes between commits. Patterns are mapped to known quality decay indicators.

### Phase 3: Classification

Each file is classified as IMPROVING (negative slope, complexity decreasing), DECLINING (positive slope, complexity increasing), or STABLE (slope near zero). A statistical confidence score is assigned based on commit history depth: 10+ commits yields 0.9 confidence; fewer than 5 triggers a low-confidence warning.

## Why Temporal Evaluation

Static analysis identifies current issues. Temporal analysis identifies trajectories. A file with high complexity and a declining trend is healthy engineering in progress. A file with moderate complexity and an accelerating growth rate is a future incident. The distinction is invisible to any tool that only examines the current snapshot.

## Validation

Analysis of the Flask repository identified a -26% complexity reduction across the evaluation window, consistent with known refactoring patterns in the project history. Initial testing across multiple open-source repositories suggests correlation between temporal patterns and reported maintenance burden.

Validation is ongoing. Results should be interpreted as directional indicators, not deterministic predictions.

## Limitations

- Requires at least 5 commits for meaningful evaluation. Fewer than 5 commits produces a low-confidence warning.
- Python, JavaScript, Java, and Go are supported. Other languages are not currently analyzed.
- Results are strongest on active repositories with regular commit cadence. Repositories with sparse or irregular commit history produce less reliable trend data.
- Temporal evaluation measures structural complexity via cyclomatic complexity. It does not measure semantic complexity, test coverage, or runtime behavior.

**GitVoyant** by [Jesse Moses (@Cre4T3Tiv3)](https://github.com/Cre4T3Tiv3) at [ByteStack Labs](https://bytestacklabs.com)