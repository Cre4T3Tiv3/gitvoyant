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

Module: src/gitvoyant/application/use_cases/analyze_file_use_case.py

Analyze File Use Case

Application layer use case for performing temporal analysis on individual
files within Git repositories. Provides a clean interface between the
presentation layer and domain services for single-file evaluation.

This use case encapsulates the business logic for file-level temporal
analysis, including parameter validation and result formatting.

Author: Jesse Moses (@Cre4T3Tiv3) <jesse@bytestacklabs.com>

Version: 0.2.0

License: Apache 2.0
"""

from pathlib import Path
from typing import Dict, Union

from gitvoyant.domain.services.temporal_evaluator_service import (
    TemporalEvaluatorService,
)

__version__ = "0.2.0"
__author__ = "Jesse Moses (@Cre4T3Tiv3) - jesse@bytestacklabs.com"


class AnalyzeFileUseCase:
    """Use case for analyzing temporal patterns in individual source files.

    Orchestrates single-file temporal evaluation by coordinating with the
    TemporalEvaluatorService to provide complexity trend analysis, quality
    pattern detection, and risk assessment for specific files.

    This use case follows the Clean Architecture pattern, providing a clear
    boundary between application logic and domain services while maintaining
    a simple interface for presentation layer consumers.

    Attributes:
        service (TemporalEvaluatorService): Domain service for temporal evaluation
            configured with the specified analysis window.
    """

    def __init__(self, window_days: int = 180):
        """Initialize the analyze file use case.

        Args:
            window_days (int, optional): Number of days of commit history to
                analyze for temporal patterns. Larger windows provide more
                stable trends but may include less relevant data. Defaults to 180.
        """
        self.service = TemporalEvaluatorService(window_days=window_days)

    async def execute(
        self,
        repo_path: Union[str, Path],
        file_path: Union[str, Path],
    ) -> Dict[str, Union[str, float, int]]:
        """Execute temporal analysis for a specific file.

        Performs comprehensive temporal evaluation of a single file, analyzing
        its complexity evolution, quality patterns, and risk characteristics
        over the configured analysis window.

        Args:
            repo_path (Union[str, Path]): Path to the Git repository containing
                the target file. Must be a valid Git repository with commit history.
            file_path (Union[str, Path]): Path to the target file for analysis.
                Can be absolute or relative to the repository root.

        Returns:
            Dict[str, Union[str, float, int]]: Analysis results containing:
                - file_path (str): Resolved file path
                - complexity_trend_slope (float): Rate of complexity change per month
                - quality_decay_forecast (float): Risk prediction (0.0-1.0)
                - commits_evaluated (int): Number of commits analyzed
                - exposure_level (str): Risk classification (LOW/MEDIUM/HIGH)
                - current_complexity (int): Most recent complexity score
                - complexity_growth_rate (float): Relative growth rate
                - evolution_timetable (List[Dict]): Chronological complexity data
                - error (str): Error message if analysis failed

        Example:
            >>> use_case = AnalyzeFileUseCase(window_days=90)
            >>> result = await use_case.execute("./repo", "src/main.py")
            >>> if "error" not in result:
            ...     trend = result["complexity_trend_slope"]
            ...     risk = result["exposure_level"]
            ...     print(f"Trend: {trend:+.2f}/month, Risk: {risk}")
        """
        return await self.service.evaluate_file(
            repo_path=str(repo_path),
            file_path=str(file_path),
        )
