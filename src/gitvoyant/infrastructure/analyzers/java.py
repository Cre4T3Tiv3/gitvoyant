"""
Module: src/gitvoyant/infrastructure/analyzers/java.py

Java language analyzer using tree-sitter.

Extracts cyclomatic complexity and structural metrics from Java source files
via the tree-sitter-java grammar.

Version: 0.3.0
License: Apache 2.0
"""

import logging
from typing import Dict, List

import tree_sitter
import tree_sitter_java as tsj

from gitvoyant.infrastructure.analyzers.base import Analyzer

logger = logging.getLogger(__name__)

_JAVA_LANGUAGE = tree_sitter.Language(tsj.language())
_PARSER = tree_sitter.Parser(_JAVA_LANGUAGE)

# Node types that contribute to cyclomatic complexity.
_DECISION_TYPES = frozenset(
    {
        "if_statement",
        "for_statement",
        "enhanced_for_statement",
        "while_statement",
        "do_statement",
        "switch_block_statement_group",
        "catch_clause",
        "ternary_expression",
    }
)

# Logical operators within binary_expression that add a branch.
_LOGICAL_OPS = frozenset({"&&", "||"})

# Node types counted as function/method definitions.
_METHOD_TYPES = frozenset(
    {
        "method_declaration",
        "constructor_declaration",
    }
)

# Node types counted as class/interface definitions.
_CLASS_TYPES = frozenset(
    {
        "class_declaration",
        "interface_declaration",
        "enum_declaration",
    }
)


def _walk(node):
    yield node
    for child in node.children:
        yield from _walk(child)


class JavaAnalyzer(Analyzer):
    """Analyzer for Java source files."""

    @property
    def file_extensions(self) -> List[str]:
        return [".java"]

    @property
    def language_name(self) -> str:
        return "java"

    def extract_metrics(self, content: str, commit) -> Dict:
        try:
            tree = _PARSER.parse(content.encode("utf-8"))
            complexity = self._cyclomatic_complexity(tree.root_node)
            function_count = sum(
                1 for n in _walk(tree.root_node) if n.type in _METHOD_TYPES
            )
            class_count = sum(
                1 for n in _walk(tree.root_node) if n.type in _CLASS_TYPES
            )
        except Exception as e:
            logger.debug(f"Parse error in commit {commit.hexsha[:8]}: {e}")
            complexity = 0
            function_count = 0
            class_count = 0

        return {
            "timestamp": commit.committed_datetime,
            "complexity": complexity,
            "lines_of_code": len(content.splitlines()),
            "function_count": function_count,
            "class_count": class_count,
            "author": commit.author.name,
            "commit_hash": commit.hexsha,
        }

    @staticmethod
    def _cyclomatic_complexity(root_node) -> int:
        """Calculate cyclomatic complexity from a Java tree-sitter parse tree.

        Counts: if, for, enhanced-for, while, do-while, switch case groups,
        catch clauses, ternary expressions, and logical operators (&&, ||).
        """
        complexity = 1
        for node in _walk(root_node):
            if node.type in _DECISION_TYPES:
                complexity += 1
            elif node.type == "binary_expression":
                for child in node.children:
                    if child.type in _LOGICAL_OPS:
                        complexity += 1
        return complexity
