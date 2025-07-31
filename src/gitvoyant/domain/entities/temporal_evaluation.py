"""
# Copyright 2025 ByteStack Labs
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

Module: src/gitvoyant/domain/entities/temporal_evaluation.py

Temporal Evaluation Entity - Core Domain Model

Domain entity representing the temporal evolution analysis of a single source
file within a Git repository. This module implements the core business logic
for temporal quality assessment based on GitVoyant's research methodology.

The TemporalEvaluation entity encapsulates all metrics, patterns, and insights
derived from analyzing a file's commit history, complexity evolution, and
quality trends over time.

Author: Jesse Moses (@Cre4T3Tiv3) <jesse@bytestacklabs.com>

Version: 0.2.0

License: Apache 2.0
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from ..value_objects.complexity_tenor import ComplexityTrend
from ..value_objects.confidence_rank import ConfidenceRank
from ..value_objects.time_table import TimeTable

__version__ = "0.2.0"
__author__ = "Jesse Moses (@Cre4T3Tiv3) - jesse@bytestacklabs.com"


@dataclass
class TemporalEvaluation:
    """Represents the comprehensive temporal evolution analysis of a source file.

    This domain entity encapsulates all aspects of a file's quality evolution
    over time, including complexity trends, developer activity patterns, risk
    assessments, and derived quality classifications. It serves as the primary
    data structure for temporal intelligence in GitVoyant.

    The entity follows Domain-Driven Design principles, providing rich behavior
    through properties and methods that encode business logic for quality
    pattern recognition and risk assessment.

    Attributes:
        file_path (str): Relative or absolute path to the evaluated source file
            within the repository context.
        repository_path (str): Filesystem path to the root directory of the
            Git repository containing the evaluated file.
        complexity_tenor (ComplexityTrend): Value object representing the rate
            and direction of complexity change over the evaluation period.
        confidence_rank (ConfidenceRank): Statistical confidence level in the
            evaluation results, ranging from 0.0 to 1.0.
        time_table (TimeTable): Temporal scope of the evaluation, defining
            the start and end dates of the analysis window.
        commits_evaluated (int): Total number of commits analyzed during the
            evaluation process for this specific file.
        developer_count (int): Number of unique developers who made changes
            to the file within the evaluation window.
        change_frequency (float): Average frequency of changes per day,
            calculated over the evaluation period.
        quality_pattern (str): Categorical classification of the overall quality
            trend. Valid values: "IMPROVING", "DECLINING", "STABLE".
        risk_level (str): Risk assessment classification based on complexity
            trends and quality patterns. Valid values: "LOW", "MEDIUM", "HIGH".
        exposure_level (str): Research-derived exposure classification providing
            additional risk context beyond the basic risk level.
        evaluation_timestamp (datetime): Timestamp when the evaluation was
            completed, useful for tracking analysis history and cache validity.
        analysis_duration_ms (Optional[int]): Duration of the evaluation process
            in milliseconds, useful for performance monitoring and optimization.
        git_history_depth (int): Total number of commits retrieved from Git
            history during the analysis, may exceed commits_evaluated due to
            filtering and processing constraints.
    """

    file_path: str
    repository_path: str
    complexity_tenor: ComplexityTrend
    confidence_rank: ConfidenceRank
    time_table: TimeTable
    commits_evaluated: int
    developer_count: int
    change_frequency: float
    quality_pattern: str
    risk_level: str
    exposure_level: str
    evaluation_timestamp: datetime = field(default_factory=datetime.now)
    analysis_duration_ms: Optional[int] = None
    git_history_depth: int = 0

    @property
    def is_quality_improving(self) -> bool:
        """Indicates whether the file exhibits improving quality patterns.

        Provides a boolean interface for quality pattern assessment, enabling
        easy filtering and categorization of files showing positive trends.

        Returns:
            bool: True if the quality pattern is classified as "IMPROVING",
                indicating decreasing complexity and positive quality trends.
                False for "STABLE" or "DECLINING" patterns.

        Example:
            >>> evaluation = TemporalEvaluation(...)
            >>> if evaluation.is_quality_improving:
            ...     print("File shows positive quality trends")
            ...     # Consider replicating patterns elsewhere
        """
        return self.quality_pattern == "IMPROVING"

    @property
    def monthly_complexity_change(self) -> float:
        """Calculates the average complexity change per month.

        Provides direct access to the complexity trend slope, representing
        the rate of complexity change over time. Negative values indicate
        improving quality (decreasing complexity), while positive values
        suggest quality degradation.

        Returns:
            float: Rate of complexity change per month. Negative values
                indicate complexity reduction (quality improvement), positive
                values indicate complexity increase (quality degradation).

        Example:
            >>> evaluation = TemporalEvaluation(...)
            >>> change = evaluation.monthly_complexity_change
            >>> if change < -1.0:
            ...     print(f"Significant quality improvement: {change:.2f}/month")
            >>> elif change > 1.0:
            ...     print(f"Quality concern: +{change:.2f} complexity/month")
        """
        return self.complexity_tenor.slope

    @staticmethod
    def _classify_pattern(tenor_slope: float) -> str:
        """Classify quality pattern based on complexity trend slope.

        Provides standardized classification logic for converting numerical
        complexity trends into categorical quality patterns. This method
        implements the core business rules for pattern recognition in
        GitVoyant's temporal analysis framework.

        The classification thresholds are based on empirical analysis of
        quality patterns across diverse codebases and represent statistically
        significant boundaries that distinguish meaningful quality changes
        from normal variation.

        Args:
            tenor_slope (float): Rate of complexity change over time, where
                negative values indicate decreasing complexity (improvement)
                and positive values indicate increasing complexity (degradation).
                Units are typically complexity points per month.

        Returns:
            str: Quality pattern classification:
                - "IMPROVING": slope < -0.5 (significant complexity reduction)
                - "DECLINING": slope > 0.5 (significant complexity increase)
                - "STABLE": -0.5 <= slope <= 0.5 (minimal complexity change)

        Business Rules:
            The threshold values (-0.5, +0.5) encode business logic for
            distinguishing significant quality changes from normal variation:
            - Thresholds filter out noise in complexity measurements
            - Values are based on statistical analysis of real-world patterns
            - Classification enables consistent quality assessment across files

        Example:
            >>> slope = -0.8  # Decreasing complexity
            >>> pattern = TemporalEvaluation.classify_pattern(slope)
            >>> print(pattern)  # "IMPROVING"

            >>> slope = 0.2   # Minor complexity increase
            >>> pattern = TemporalEvaluation.classify_pattern(slope)
            >>> print(pattern)  # "STABLE"

            >>> slope = 1.2   # Significant complexity increase
            >>> pattern = TemporalEvaluation.classify_pattern(slope)
            >>> print(pattern)  # "DECLINING"

        Note:
            This static method can be used independently of TemporalEvaluation
            instances for classification tasks or validation during entity
            construction. The method encapsulates domain knowledge about
            what constitutes meaningful quality change.
        """
        if tenor_slope < -0.5:
            return "IMPROVING"
        elif tenor_slope > 0.5:
            return "DECLINING"
        return "STABLE"
