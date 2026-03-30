# Complexity Requirements

## Overview

GitVoyant tracks multiple complexity metrics over time to build a comprehensive picture of code evolution.

## Primary Metrics

### 1. Cyclomatic Complexity

**Definition**: Number of linearly independent paths through code.

**Calculation**:
```
Complexity = 1 + number_of_decision_points
```

**Decision Points** (language-specific):
- Python: `if`/`elif`, `while`, `for`, `async for`, `except`, `and`, `or`
- JavaScript/TypeScript: `if`, `for`, `for-in`, `while`, `do-while`, `switch case`, `catch`, ternary (`?:`), `&&`, `||`
- Java: `if`, `for`, enhanced `for`, `while`, `do-while`, `switch case`, `catch`, ternary (`?:`), `&&`, `||`
- Go: `if`, `for` (including range), `switch case`, `select case`, `type case`, `&&`, `||`

**Interpretation**:
- **1-10**: Simple, easy to test
- **11-20**: Moderate complexity
- **21-50**: High complexity, consider refactoring
- **50+**: Very high risk, immediate attention needed

### 2. Lines of Code (LOC)

**Definition**: Total number of non-empty lines.

**Significance**: Correlates with maintenance effort. Growth rate indicates development velocity. Sudden spikes suggest rushed development.

### 3. Function Count

**Definition**: Number of function definitions.

**Usage**: Tracks code organization patterns. Helps identify monolithic growth. Correlates with modularity.

### 4. Class Count

**Definition**: Number of class definitions.

**Purpose**: Measures architectural complexity. Tracks object-oriented design evolution. Identifies abstraction patterns.

## Temporal Evaluation Metrics

### 1. Complexity Trend Slope

**Definition**: Rate of complexity change per time unit.

**Calculation**: Linear regression fitted to time-series complexity values produces a slope representing complexity change per month.

**Interpretation**:
- **Positive slope**: Increasing complexity (risk)
- **Negative slope**: Decreasing complexity (refactoring)
- **Zero slope**: Stable complexity (ideal)

### 2. Growth Rate

**Definition**: Percentage change in complexity over the evaluation window.

**Formula**:
```
growth_rate = (recent_avg_complexity - historical_avg_complexity) / historical_avg_complexity
```

Recent and historical averages are computed from the last 5 and first 5 data points in the evaluation window, respectively.

## Quality Decay Forecast

The quality decay forecast is derived from the complexity growth rate:

```
quality_decay_forecast = clamp(growth_rate * 2, 0.0, 1.0)
```

This produces a value between 0.0 and 1.0 representing the probability of future quality degradation.

### Risk Categories

- **0.0 - 0.4**: LOW risk
- **0.4 - 0.7**: MEDIUM risk
- **0.7 - 1.0**: HIGH risk

## Implementation Notes

### Handling Edge Cases

- **Minimum history**: At least 2 commits required for analysis; at least 5 for standard confidence. Files with fewer than 5 commits receive a low-confidence warning (confidence capped at 0.4).
- **Syntax errors**: On parse failure, complexity is recorded as 0 for that commit. Analysis continues with partial data.
- **File discovery**: Only files matching registered analyzer extensions (`.py`, `.js`, `.jsx`, `.ts`, `.java`, `.go`) are evaluated. Other file types are not processed.
- **Maximum commits**: At most 100 commits per file are evaluated within the analysis window.

**GitVoyant** by [Jesse Moses (@Cre4T3Tiv3)](https://github.com/Cre4T3Tiv3) at [ByteStack Labs](https://bytestacklabs.com)