"""
Module: src/gitvoyant/infrastructure/analyzers/base.py

Analyzer protocol defining the interface for language-specific code analysis.

All language analyzers implement this protocol to provide cyclomatic complexity
computation and structural metric extraction from source code content at
specific Git commits.

Version: 0.3.0
License: Apache 2.0
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, List


class Analyzer(ABC):
    """Abstract base for language-specific code analyzers.

    Each implementation handles AST parsing and cyclomatic complexity
    computation for a single programming language. The analyzer is
    resolved at runtime based on file extension via the language registry.
    """

    @property
    @abstractmethod
    def file_extensions(self) -> List[str]:
        """Return the file extensions this analyzer handles (e.g. ['.py'])."""
        ...

    @property
    @abstractmethod
    def language_name(self) -> str:
        """Return a human-readable language name (e.g. 'python')."""
        ...

    @abstractmethod
    def extract_metrics(self, content: str, commit) -> Dict:
        """Extract complexity and structural metrics from source content.

        Args:
            content: Source code as a string.
            commit: GitPython commit object for metadata extraction.

        Returns:
            Dict with keys: timestamp, complexity, lines_of_code,
            function_count, class_count, author, commit_hash.
        """
        ...
