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

Module: src/gitvoyant/application/use_cases/analyze_repo_use_case.py

Analyze Repository Use Case

Application layer use case for performing comprehensive temporal analysis
across multiple files within Git repositories. Provides repository-wide
evaluation capabilities with risk-based prioritization.

This use case coordinates multi-file analysis and aggregates results to
provide holistic repository quality assessment.

Author: Jesse Moses (@Cre4T3Tiv3) <jesse@bytestacklabs.com>

Version: 0.2.0

License: Apache 2.0
"""

from typing import Dict, List, Optional, Union

from gitvoyant.domain.services.temporal_evaluator_service import (
    TemporalEvaluatorService,
)

__version__ = "0.2.0"
__author__ = "Jesse Moses (@Cre4T3Tiv3) - jesse@bytestacklabs.com"


class AnalyzeRepoUseCase:
    """Use case for analyzing temporal patterns across repository files.

    Orchestrates repository-wide temporal evaluation by coordinating with the
    TemporalEvaluatorService to analyze multiple files and provide comprehensive
    quality assessment with risk-based prioritization.

    This use case implements the application layer logic for multi-file analysis,
    including file filtering, result aggregation, and risk-based sorting to
    highlight the most concerning files for immediate attention.

    Attributes:
        service (TemporalEvaluatorService): Domain service for temporal evaluation
            with configured analysis parameters.
    """

    def __init__(self, service: Optional[TemporalEvaluatorService] = None):
        """Initialize the analyze repository use case.

        Args:
            service (Optional[TemporalEvaluatorService]): Pre-configured temporal
                evaluator service. If None, creates a new service instance with
                default parameters.
        """
        self.service = service or TemporalEvaluatorService()

    async def execute(
        self, repo_path: str, max_files: int = 20
    ) -> Dict[str, Union[str, List[Dict]]]:
        """Execute comprehensive temporal analysis across repository files.

        Performs temporal evaluation on multiple Python files within the
        repository, analyzing complexity trends and quality patterns to
        identify files requiring attention. Results are sorted by decay
        risk to prioritize the most concerning files.

        Args:
            repo_path (str): Path to the Git repository root directory.
                Must be a valid Git repository with commit history.
            max_files (int, optional): Maximum number of files to analyze
                to prevent excessive processing time on large repositories.
                Defaults to 20.

        Returns:
            Dict[str, Union[str, List[Dict]]]: Repository analysis results containing:
                - repo_path (str): Resolved repository path
                - evaluations (List[Dict]): List of individual file analysis
                  results, sorted by quality decay forecast in descending order.
                  Each evaluation contains the same fields as single-file analysis.

        Note:
            The method automatically excludes common non-source directories
            like .venv and __pycache__ to focus analysis on relevant Python
            source files. Files with analysis errors are logged but excluded
            from results to ensure partial success on large repositories.

        Example:
            >>> use_case = AnalyzeRepoUseCase()
            >>> results = await use_case.execute("./my-repo", max_files=10)
            >>> evaluations = results["evaluations"]
            >>> print(f"Analyzed {len(evaluations)} files")
            >>> # Show highest risk files
            >>> for eval in evaluations[:3]:
            ...     file = eval["file_path"]
            ...     risk = eval["exposure_level"]
            ...     print(f"{file}: {risk} risk")
        """
        return await self.service.evaluate_repository(
            repo_path=repo_path, max_files=max_files
        )
