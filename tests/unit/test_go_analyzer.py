"""
Module: tests/unit/test_go_analyzer.py

Unit tests for the Go language analyzer.

Validates cyclomatic complexity computation and structural metric extraction
using tree-sitter-go against known code samples.

Version: 0.3.0
License: Apache 2.0
"""

from types import SimpleNamespace
from datetime import datetime, timezone

import pytest

from gitvoyant.infrastructure.analyzers.go import GoAnalyzer


@pytest.fixture
def analyzer():
    return GoAnalyzer()


def _fake_commit(hexsha="abcdef1234567890", author="Test Author"):
    return SimpleNamespace(
        committed_datetime=datetime(2025, 1, 1, tzinfo=timezone.utc),
        hexsha=hexsha,
        author=SimpleNamespace(name=author),
    )


def test_file_extensions(analyzer):
    assert analyzer.file_extensions == [".go"]


def test_language_name(analyzer):
    assert analyzer.language_name == "go"


def test_simple_function_complexity(analyzer):
    code = """package main

func hello() int {
    return 42
}
"""
    metrics = analyzer.extract_metrics(code, _fake_commit())
    assert metrics["complexity"] == 1
    assert metrics["function_count"] == 1


def test_if_statement_complexity(analyzer):
    code = """package main

func check(x int) int {
    if x > 0 {
        return x
    }
    return 0
}
"""
    metrics = analyzer.extract_metrics(code, _fake_commit())
    assert metrics["complexity"] == 2


def test_for_loop_complexity(analyzer):
    code = """package main

func loop(x int) {
    for i := 0; i < x; i++ {
        fmt.Println(i)
    }
}
"""
    metrics = analyzer.extract_metrics(code, _fake_commit())
    # 1 base + 1 for = 2
    assert metrics["complexity"] == 2


def test_range_loop_complexity(analyzer):
    code = """package main

func iter(items []int) {
    for _, v := range items {
        process(v)
    }
}
"""
    metrics = analyzer.extract_metrics(code, _fake_commit())
    # 1 base + 1 for (range) = 2
    assert metrics["complexity"] == 2


def test_switch_case_complexity(analyzer):
    code = """package main

func route(x int) int {
    switch x {
    case 1:
        return 10
    case 2:
        return 20
    case 3:
        return 30
    }
    return 0
}
"""
    metrics = analyzer.extract_metrics(code, _fake_commit())
    # 1 base + 3 expression_case = 4
    assert metrics["complexity"] == 4


def test_select_complexity(analyzer):
    code = """package main

func sel(ch chan int, done chan bool) {
    select {
    case msg := <-ch:
        handle(msg)
    case <-done:
        return
    }
}
"""
    metrics = analyzer.extract_metrics(code, _fake_commit())
    # 1 base + 2 communication_case = 3
    assert metrics["complexity"] == 3


def test_logical_operators_complexity(analyzer):
    code = """package main

func validate(x int) bool {
    if x > 0 && x < 100 || x == -1 {
        return true
    }
    return false
}
"""
    metrics = analyzer.extract_metrics(code, _fake_commit())
    # 1 base + 1 if + 1 && + 1 || = 4
    assert metrics["complexity"] == 4


def test_method_declaration_counted(analyzer):
    code = """package main

type Foo struct {}

func (f Foo) Bar() int { return 1 }
func (f Foo) Baz() int { return 2 }
"""
    metrics = analyzer.extract_metrics(code, _fake_commit())
    assert metrics["function_count"] == 2
    assert metrics["class_count"] == 1  # type_declaration


def test_multiple_branches(analyzer):
    code = """package main

func process(x int) {
    if x > 10 {
        return
    }
    for i := 0; i < x; i++ {
        fmt.Println(i)
    }
    if x > 0 && x < 5 {
        doWork()
    }
}
"""
    metrics = analyzer.extract_metrics(code, _fake_commit())
    # 1 base + 1 if + 1 for + 1 if + 1 && = 5
    assert metrics["complexity"] == 5


def test_metrics_structure(analyzer):
    code = "package main"
    commit = _fake_commit()
    metrics = analyzer.extract_metrics(code, commit)
    assert "timestamp" in metrics
    assert "complexity" in metrics
    assert "lines_of_code" in metrics
    assert "function_count" in metrics
    assert "class_count" in metrics
    assert "author" in metrics
    assert "commit_hash" in metrics
