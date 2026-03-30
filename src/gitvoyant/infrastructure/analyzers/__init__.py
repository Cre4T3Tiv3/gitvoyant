"""
Module: src/gitvoyant/infrastructure/analyzers/__init__.py

Language analyzer registry.

Maps file extensions to analyzer instances. Used by TemporalEvaluator to
resolve the correct analyzer for a given file path.

Version: 0.3.0
License: Apache 2.0
"""

from typing import Dict, List, Optional, Set

from gitvoyant.infrastructure.analyzers.base import Analyzer
from gitvoyant.infrastructure.analyzers.go import GoAnalyzer
from gitvoyant.infrastructure.analyzers.java import JavaAnalyzer
from gitvoyant.infrastructure.analyzers.javascript import JavaScriptAnalyzer
from gitvoyant.infrastructure.analyzers.python import PythonAnalyzer

_ANALYZERS: Dict[str, Analyzer] = {}

# Directories to exclude during file discovery, per language.
EXCLUSION_DIRS: Set[str] = {
    # Python
    ".venv", "__pycache__", "site-packages",
    # JavaScript / TypeScript
    "node_modules", "dist", ".next",
    # Java
    "target", ".gradle",
    # Go
    "vendor",
    # General
    "build",
}


def _register(analyzer: Analyzer) -> None:
    for ext in analyzer.file_extensions:
        _ANALYZERS[ext] = analyzer


_register(PythonAnalyzer())
_register(JavaScriptAnalyzer())
_register(JavaAnalyzer())
_register(GoAnalyzer())


def get_analyzer(file_path: str) -> Optional[Analyzer]:
    """Return the analyzer for a file path based on its extension, or None."""
    for ext, analyzer in _ANALYZERS.items():
        if file_path.endswith(ext):
            return analyzer
    return None


def supported_extensions(languages: Optional[List[str]] = None) -> List[str]:
    """Return file extensions for registered analyzers.

    Args:
        languages: If provided, restrict to these language names.
            If None, returns all registered extensions.
    """
    if languages is None:
        return list(_ANALYZERS.keys())
    return [
        ext for ext, analyzer in _ANALYZERS.items()
        if analyzer.language_name in languages
    ]


def is_excluded_dir(path_str: str) -> bool:
    """Return True if any path component matches an exclusion directory."""
    parts = path_str.replace("\\", "/").split("/")
    return any(part in EXCLUSION_DIRS for part in parts)


def get_registry() -> Dict[str, Analyzer]:
    """Return the full extension-to-analyzer mapping."""
    return dict(_ANALYZERS)
