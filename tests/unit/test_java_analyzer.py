"""
Module: tests/unit/test_java_analyzer.py

Unit tests for the Java language analyzer.

Validates cyclomatic complexity computation and structural metric extraction
using tree-sitter-java against known code samples.

Version: 0.3.0
License: Apache 2.0
"""

from types import SimpleNamespace
from datetime import datetime, timezone

import pytest

from gitvoyant.infrastructure.analyzers.java import JavaAnalyzer


@pytest.fixture
def analyzer():
    return JavaAnalyzer()


def _fake_commit(hexsha="abcdef1234567890", author="Test Author"):
    return SimpleNamespace(
        committed_datetime=datetime(2025, 1, 1, tzinfo=timezone.utc),
        hexsha=hexsha,
        author=SimpleNamespace(name=author),
    )


def test_file_extensions(analyzer):
    assert analyzer.file_extensions == [".java"]


def test_language_name(analyzer):
    assert analyzer.language_name == "java"


def test_simple_method_complexity(analyzer):
    code = """
public class Foo {
    public int bar() {
        return 42;
    }
}
"""
    metrics = analyzer.extract_metrics(code, _fake_commit())
    assert metrics["complexity"] == 1
    assert metrics["function_count"] == 1
    assert metrics["class_count"] == 1


def test_if_statement_complexity(analyzer):
    code = """
public class Foo {
    public int check(int x) {
        if (x > 0) {
            return x;
        }
        return 0;
    }
}
"""
    metrics = analyzer.extract_metrics(code, _fake_commit())
    assert metrics["complexity"] == 2


def test_multiple_branches(analyzer):
    code = """
public class Foo {
    public void process(int x) {
        if (x > 10) { return; }
        for (int i = 0; i < x; i++) { System.out.println(i); }
        while (x > 0) { x--; }
    }
}
"""
    metrics = analyzer.extract_metrics(code, _fake_commit())
    # 1 base + 1 if + 1 for + 1 while = 4
    assert metrics["complexity"] == 4


def test_switch_case_complexity(analyzer):
    code = """
public class Foo {
    public int route(int action) {
        switch(action) {
            case 1: return 10;
            case 2: return 20;
            case 3: return 30;
        }
        return 0;
    }
}
"""
    metrics = analyzer.extract_metrics(code, _fake_commit())
    # 1 base + 3 case groups = 4
    assert metrics["complexity"] == 4


def test_logical_operators_complexity(analyzer):
    code = """
public class Foo {
    public boolean validate(int x) {
        if (x > 0 && x < 100 || x == -1) {
            return true;
        }
        return false;
    }
}
"""
    metrics = analyzer.extract_metrics(code, _fake_commit())
    # 1 base + 1 if + 1 && + 1 || = 4
    assert metrics["complexity"] == 4


def test_catch_clause_complexity(analyzer):
    code = """
public class Foo {
    public void safe() {
        try {
            doSomething();
        } catch(Exception e) {
            log(e);
        }
    }
}
"""
    metrics = analyzer.extract_metrics(code, _fake_commit())
    # 1 base + 1 catch = 2
    assert metrics["complexity"] == 2


def test_do_while_complexity(analyzer):
    code = """
public class Foo {
    public void loop(int x) {
        do { x++; } while (x < 10);
    }
}
"""
    metrics = analyzer.extract_metrics(code, _fake_commit())
    # 1 base + 1 do-while = 2
    assert metrics["complexity"] == 2


def test_enhanced_for_complexity(analyzer):
    code = """
public class Foo {
    public void iter(int[] items) {
        for (int item : items) {
            process(item);
        }
    }
}
"""
    metrics = analyzer.extract_metrics(code, _fake_commit())
    # 1 base + 1 enhanced-for = 2
    assert metrics["complexity"] == 2


def test_ternary_complexity(analyzer):
    code = """
public class Foo {
    public int pick(int x) {
        return x > 0 ? 1 : 0;
    }
}
"""
    metrics = analyzer.extract_metrics(code, _fake_commit())
    # 1 base + 1 ternary = 2
    assert metrics["complexity"] == 2


def test_constructor_counted(analyzer):
    code = """
public class Foo {
    public Foo() {}
    public void bar() {}
}
"""
    metrics = analyzer.extract_metrics(code, _fake_commit())
    assert metrics["function_count"] == 2  # constructor + method
    assert metrics["class_count"] == 1


def test_interface_counted(analyzer):
    code = """
public interface Baz {
    void doIt();
}
"""
    metrics = analyzer.extract_metrics(code, _fake_commit())
    assert metrics["class_count"] == 1


def test_metrics_structure(analyzer):
    code = "public class Empty {}"
    commit = _fake_commit()
    metrics = analyzer.extract_metrics(code, commit)
    assert "timestamp" in metrics
    assert "complexity" in metrics
    assert "lines_of_code" in metrics
    assert "function_count" in metrics
    assert "class_count" in metrics
    assert "author" in metrics
    assert "commit_hash" in metrics
