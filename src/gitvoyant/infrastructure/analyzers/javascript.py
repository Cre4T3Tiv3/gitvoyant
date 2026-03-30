"""
Module: src/gitvoyant/infrastructure/analyzers/javascript.py

JavaScript/TypeScript language analyzer using tree-sitter.

Extracts cyclomatic complexity and structural metrics from JavaScript and
TypeScript source files via the tree-sitter-javascript grammar.

Version: 0.3.0
License: Apache 2.0
"""

import logging
from typing import Dict, List

import tree_sitter
import tree_sitter_javascript as tsjs

from gitvoyant.infrastructure.analyzers.base import Analyzer

logger = logging.getLogger(__name__)

_JS_LANGUAGE = tree_sitter.Language(tsjs.language())
_PARSER = tree_sitter.Parser(_JS_LANGUAGE)

# Node types that contribute to cyclomatic complexity.
_DECISION_TYPES = frozenset({
    "if_statement",
    "for_statement",
    "for_in_statement",
    "while_statement",
    "do_statement",
    "switch_case",
    "catch_clause",
    "ternary_expression",
})

# Logical operators within binary_expression that add a branch.
_LOGICAL_OPS = frozenset({"&&", "||"})

# Node types counted as function definitions.
_FUNCTION_TYPES = frozenset({
    "function_declaration",
    "function_expression",
    "arrow_function",
    "method_definition",
    "generator_function_declaration",
})

# Node types counted as class definitions.
_CLASS_TYPES = frozenset({
    "class_declaration",
})


def _walk(node):
    """Yield all nodes in the tree rooted at *node*."""
    yield node
    for child in node.children:
        yield from _walk(child)


class JavaScriptAnalyzer(Analyzer):
    """Analyzer for JavaScript and TypeScript source files."""

    @property
    def file_extensions(self) -> List[str]:
        return [".js", ".jsx", ".ts"]

    @property
    def language_name(self) -> str:
        return "javascript"

    def extract_metrics(self, content: str, commit) -> Dict:
        try:
            tree = _PARSER.parse(content.encode("utf-8"))
            complexity = self._cyclomatic_complexity(tree.root_node)
            function_count = sum(
                1 for n in _walk(tree.root_node) if n.type in _FUNCTION_TYPES
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
        """Calculate cyclomatic complexity from a tree-sitter parse tree.

        Counts decision points: if, for, for-in, while, do-while,
        switch cases, catch clauses, ternary expressions, and logical
        operators (&&, ||).
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
