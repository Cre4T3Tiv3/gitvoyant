"""
Module: src/gitvoyant/domain/entities/repository.py

Repository Aggregate for Multi-File Temporal Evaluation

Domain entity representing a Git repository with aggregated temporal evaluation
results across multiple source files. Provides convenience methods for
analyzing quality distribution and identifying files with specific patterns.

This aggregate encapsulates the business logic for repository-level quality
assessment and provides derived properties for common quality queries.

Author: Jesse Moses (@Cre4T3Tiv3) <jesse@bytestacklabs.com>

Version: 0.2.0

License: Apache 2.0
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List

from .temporal_evaluation import TemporalEvaluation

__version__ = "0.2.0"
__author__ = "Jesse Moses (@Cre4T3Tiv3) - jesse@bytestacklabs.com"


@dataclass
class Repository:
    """Represents a repository with aggregated file evaluation results.

    Domain aggregate that encapsulates temporal evaluation results for multiple
    files within a Git repository. Provides derived properties for quality
    pattern analysis, health scoring, and risk assessment at the repository level.

    This entity follows Domain-Driven Design principles, providing a rich
    interface for repository-level quality intelligence without exposing
    internal implementation details.

    Attributes:
        path (str): Filesystem path to the repository root directory.
        name (str): Repository name or identifier for display and reference.
        evaluation_timestamp (datetime): When the evaluation was performed,
            useful for tracking evaluation history and cache management.
        file_analyses (List[TemporalEvaluation]): Collection of individual
            file evaluation results that comprise the repository assessment.
    """

    path: str
    name: str
    evaluation_timestamp: datetime = field(default_factory=datetime.now)
    file_analyses: List[TemporalEvaluation] = field(default_factory=list)

    @property
    def declining_files(self) -> List[TemporalEvaluation]:
        """Files showing declining quality patterns requiring attention.

        Identifies files with detected quality degradation patterns that may
        require refactoring, architectural review, or additional development
        resources to prevent further deterioration.

        Returns:
            List[TemporalEvaluation]: Files classified with DECLINING quality
                patterns based on temporal complexity analysis.

        Example:
            >>> repo = Repository(path="./project", name="MyProject")
            >>> declining = repo.declining_files
            >>> if declining:
            ...     print(f"{len(declining)} files need attention")
            ...     for file in declining[:5]:  # Show top 5
            ...         print(f"  {file.file_path}: {file.risk_level} risk")
        """
        return [
            evaluation
            for evaluation in self.file_analyses
            if evaluation.quality_pattern == "DECLINING"
        ]

    @property
    def improving_files(self) -> List[TemporalEvaluation]:
        """Files showing improving quality patterns worth studying.

        Identifies files demonstrating positive quality trends that can serve
        as examples of good engineering practices and potential patterns to
        replicate across other parts of the codebase.

        Returns:
            List[TemporalEvaluation]: Files classified with IMPROVING quality
                patterns based on temporal complexity analysis.

        Example:
            >>> repo = Repository(path="./project", name="MyProject")
            >>> improving = repo.improving_files
            >>> print(f"{len(improving)} files show quality improvements")
            >>> # Extract successful patterns for replication
        """
        return [
            evaluation
            for evaluation in self.file_analyses
            if evaluation.quality_pattern == "IMPROVING"
        ]

    @property
    def stable_files(self) -> List[TemporalEvaluation]:
        """Files showing stable quality patterns with consistent complexity.

        Identifies files that maintain consistent complexity levels over time,
        indicating stable code that may not require immediate attention but
        should be monitored for future changes.

        Returns:
            List[TemporalEvaluation]: Files classified with STABLE quality
                patterns based on temporal complexity analysis.
        """
        return [
            evaluation
            for evaluation in self.file_analyses
            if evaluation.quality_pattern == "STABLE"
        ]

    @property
    def total_files_evaluated(self) -> int:
        """Total number of files included in the repository evaluation.

        Returns:
            int: Count of files that were successfully analyzed and included
                in the repository assessment results.
        """
        return len(self.file_analyses)

    @property
    def overall_health_score(self) -> float:
        """Overall repository health score based on quality pattern distribution.

        Computes a normalized health score (0.0-10.0) based on the proportion
        of files showing improving, stable, and declining quality patterns.
        Higher scores indicate healthier repositories with more positive trends.

        Returns:
            float: Health score between 0.0 and 10.0, where 10.0 represents
                a repository with all files showing improving quality patterns.

        Note:
            The scoring algorithm weights improving files fully (1.0) and
            stable files partially (0.6), while declining files contribute
            negatively to the overall score. This encourages proactive
            quality improvement rather than mere stability.

        Example:
            >>> repo = Repository(path="./project", name="MyProject")
            >>> score = repo.overall_health_score
            >>> print(f"Repository health: {score:.1f}/10.0")
            >>> if score > 7.0:
            ...     print("Excellent quality trends!")
            >>> elif score < 4.0:
            ...     print("Quality concerns detected")
        """
        if not self.file_analyses:
            return 0.0

        improving_count = len(self.improving_files)
        stable_count = len(self.stable_files)
        total_files = self.total_files_evaluated

        if total_files == 0:
            return 0.0

        health_score = (improving_count * 1.0 + stable_count * 0.6) / total_files
        return health_score * 10

    @property
    def quality_distribution(self) -> Dict[str, int]:
        """Breakdown of files by quality pattern for analysis and reporting.

        Provides a summary count of files in each quality category, useful
        for dashboard displays, reporting, and trend analysis over time.

        Returns:
            Dict[str, int]: Dictionary with pattern counts:
                - improving: Number of files with improving quality
                - stable: Number of files with stable quality
                - declining: Number of files with declining quality

        Example:
            >>> repo = Repository(path="./project", name="MyProject")
            >>> distribution = repo.quality_distribution
            >>> print(f"Quality distribution:")
            >>> print(f"  Improving: {distribution['improving']}")
            >>> print(f"  Stable: {distribution['stable']}")
            >>> print(f"  Declining: {distribution['declining']}")
        """
        return {
            "improving": len(self.improving_files),
            "stable": len(self.stable_files),
            "declining": len(self.declining_files),
        }
