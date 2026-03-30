"""
Module: src/gitvoyant/infrastructure/analyzers/go.py

Go language analyzer using tree-sitter.

Extracts cyclomatic complexity and structural metrics from Go source files
via the tree-sitter-go grammar.

Version: 0.3.0
License: Apache 2.0
"""

import logging
from typing import Dict, List

import tree_sitter
import tree_sitter_go as tsg

from gitvoyant.infrastructure.analyzers.base import Analyzer

logger = logging.getLogger(__name__)

_GO_LANGUAGE = tree_sitter.Language(tsg.language())
_PARSER = tree_sitter.Parser(_GO_LANGUAGE)

# Node types that contribute to cyclomatic complexity.
_DECISION_TYPES = frozenset(
    {
        "if_statement",
        "for_statement",
        "expression_case",  # case clauses in switch
        "communication_case",  # case clauses in select
        "type_case",  # case clauses in type switch
    }
)

# Logical operators within binary_expression that add a branch.
_LOGICAL_OPS = frozenset({"&&", "||"})

# Node types counted as function/method declarations.
_FUNC_TYPES = frozenset(
    {
        "function_declaration",
        "method_declaration",
        "func_literal",
    }
)

# Node types counted as type definitions (struct, interface).
_TYPE_TYPES = frozenset(
    {
        "type_declaration",
    }
)


def _walk(node):
    yield node
    for child in node.children:
        yield from _walk(child)


class GoAnalyzer(Analyzer):
    """Analyzer for Go source files."""

    @property
    def file_extensions(self) -> List[str]:
        return [".go"]

    @property
    def language_name(self) -> str:
        return "go"

    def extract_metrics(self, content: str, commit) -> Dict:
        try:
            tree = _PARSER.parse(content.encode("utf-8"))
            complexity = self._cyclomatic_complexity(tree.root_node)
            function_count = sum(
                1 for n in _walk(tree.root_node) if n.type in _FUNC_TYPES
            )
            class_count = sum(1 for n in _walk(tree.root_node) if n.type in _TYPE_TYPES)
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
        """Calculate cyclomatic complexity from a Go tree-sitter parse tree.

        Counts: if, for (including range), expression/communication/type
        case clauses, and logical operators (&&, ||).
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
