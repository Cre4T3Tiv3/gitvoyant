"""
Module: src/gitvoyant/infrastructure/analyzers/python.py

Python language analyzer using the built-in ast module.

Extracts cyclomatic complexity and structural metrics from Python source files.
This is a direct extraction of the logic previously embedded in TemporalEvaluator.

Version: 0.3.0
License: Apache 2.0
"""

import ast
import logging
from typing import Dict, List

from gitvoyant.infrastructure.analyzers.base import Analyzer

logger = logging.getLogger(__name__)


class PythonAnalyzer(Analyzer):
    """Analyzer for Python source files using the standard library ast module."""

    @property
    def file_extensions(self) -> List[str]:
        return [".py"]

    @property
    def language_name(self) -> str:
        return "python"

    def extract_metrics(self, content: str, commit) -> Dict:
        """Extract complexity and structural metrics from Python source.

        Args:
            content: Python source code string.
            commit: GitPython commit object.

        Returns:
            Dict containing timestamp, complexity, lines_of_code,
            function_count, class_count, author, and commit_hash.
        """
        try:
            tree = ast.parse(content)
            complexity = self._cyclomatic_complexity(tree)
            function_count = len(
                [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
            )
            class_count = len(
                [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
            )
        except SyntaxError as e:
            logger.debug(f"Syntax error in commit {commit.hexsha[:8]}: {e}")
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
    def _cyclomatic_complexity(tree) -> int:
        """Calculate cyclomatic complexity of a Python AST.

        Counts decision points: if, while, for, async for, boolean
        operators, and exception handlers. Base complexity is 1.
        """
        complexity = 1
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
            elif isinstance(node, ast.ExceptHandler):
                complexity += 1
        return complexity
