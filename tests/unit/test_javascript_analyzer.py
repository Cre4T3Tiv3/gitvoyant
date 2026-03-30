"""
Module: tests/unit/test_javascript_analyzer.py

Unit tests for the JavaScript/TypeScript language analyzer.

Validates cyclomatic complexity computation and structural metric extraction
using tree-sitter-javascript against known code samples.

Version: 0.3.0
License: Apache 2.0
"""

from types import SimpleNamespace
from datetime import datetime, timezone

import pytest

from gitvoyant.infrastructure.analyzers.javascript import JavaScriptAnalyzer


@pytest.fixture
def analyzer():
    return JavaScriptAnalyzer()


def _fake_commit(hexsha="abcdef1234567890", author="Test Author"):
    """Create a minimal commit-like object for testing."""
    return SimpleNamespace(
        committed_datetime=datetime(2025, 1, 1, tzinfo=timezone.utc),
        hexsha=hexsha,
        author=SimpleNamespace(name=author),
    )


def test_file_extensions(analyzer):
    assert ".js" in analyzer.file_extensions
    assert ".jsx" in analyzer.file_extensions
    assert ".ts" in analyzer.file_extensions


def test_language_name(analyzer):
    assert analyzer.language_name == "javascript"


def test_simple_function_complexity(analyzer):
    """A function with no branches has complexity 1."""
    code = "function hello() { return 42; }"
    metrics = analyzer.extract_metrics(code, _fake_commit())
    assert metrics["complexity"] == 1
    assert metrics["function_count"] == 1
    assert metrics["class_count"] == 0


def test_if_statement_complexity(analyzer):
    """An if statement adds 1 to complexity."""
    code = """
function check(x) {
    if (x > 0) {
        return x;
    }
    return 0;
}
"""
    metrics = analyzer.extract_metrics(code, _fake_commit())
    assert metrics["complexity"] == 2  # 1 base + 1 if


def test_multiple_branches(analyzer):
    """Multiple decision points accumulate."""
    code = """
function process(x) {
    if (x > 10) { return 'big'; }
    for (let i = 0; i < x; i++) { console.log(i); }
    while (x > 0) { x--; }
}
"""
    metrics = analyzer.extract_metrics(code, _fake_commit())
    # 1 base + 1 if + 1 for + 1 while = 4
    assert metrics["complexity"] == 4


def test_switch_case_complexity(analyzer):
    """Each switch case adds to complexity."""
    code = """
function route(action) {
    switch(action) {
        case 'a': return 1;
        case 'b': return 2;
        case 'c': return 3;
    }
}
"""
    metrics = analyzer.extract_metrics(code, _fake_commit())
    # 1 base + 3 cases = 4
    assert metrics["complexity"] == 4


def test_logical_operators_complexity(analyzer):
    """&& and || each add 1 to complexity."""
    code = """
function validate(x) {
    if (x > 0 && x < 100 || x === -1) {
        return true;
    }
    return false;
}
"""
    metrics = analyzer.extract_metrics(code, _fake_commit())
    # 1 base + 1 if + 1 && + 1 || = 4
    assert metrics["complexity"] == 4


def test_catch_clause_complexity(analyzer):
    """catch clauses add to complexity."""
    code = """
function safe() {
    try {
        doSomething();
    } catch(e) {
        handleError(e);
    }
}
"""
    metrics = analyzer.extract_metrics(code, _fake_commit())
    # 1 base + 1 catch = 2
    assert metrics["complexity"] == 2


def test_ternary_expression_complexity(analyzer):
    """Ternary expressions add to complexity."""
    code = "const x = a > 0 ? 'yes' : 'no';"
    metrics = analyzer.extract_metrics(code, _fake_commit())
    # 1 base + 1 ternary = 2
    assert metrics["complexity"] == 2


def test_arrow_function_counted(analyzer):
    """Arrow functions are counted as functions."""
    code = "const add = (a, b) => a + b;"
    metrics = analyzer.extract_metrics(code, _fake_commit())
    assert metrics["function_count"] == 1


def test_class_counted(analyzer):
    """Class declarations are counted."""
    code = """
class Foo {
    bar() { return 1; }
    baz() { return 2; }
}
"""
    metrics = analyzer.extract_metrics(code, _fake_commit())
    assert metrics["class_count"] == 1
    assert metrics["function_count"] == 2  # methods


def test_metrics_structure(analyzer):
    """Verify all expected keys are present."""
    code = "const x = 1;"
    commit = _fake_commit()
    metrics = analyzer.extract_metrics(code, commit)
    assert "timestamp" in metrics
    assert "complexity" in metrics
    assert "lines_of_code" in metrics
    assert "function_count" in metrics
    assert "class_count" in metrics
    assert "author" in metrics
    assert "commit_hash" in metrics
    assert metrics["author"] == "Test Author"


def test_empty_file(analyzer):
    """An empty file has complexity 1 (base)."""
    metrics = analyzer.extract_metrics("", _fake_commit())
    assert metrics["complexity"] == 1
    assert metrics["function_count"] == 0
