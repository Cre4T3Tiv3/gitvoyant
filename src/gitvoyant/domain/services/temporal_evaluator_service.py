"""
Module: src/gitvoyant/domain/services/temporal_evaluator_service.py

GitVoyant v0.2.0 – TemporalEvaluatorService

Service layer exposing structured temporal intelligence over Git repositories.
Provides high-level orchestration for repository analysis, file evaluation,
decay forecasting, and insight generation for use by agents, CLI, or API layers.

This service abstracts the complexity of temporal evaluation infrastructure
and provides a clean interface for higher-level application components.

Author: Jesse Moses (@Cre4T3Tiv3) <jesse@bytestacklabs.com>

Version: 0.2.0

License: Apache 2.0
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional, Union

from gitvoyant.infrastructure.temporal_evaluator import (
    TemporalDiscernment,
    TemporalEvaluator,
)

__version__ = "0.2.0"
__author__ = "Jesse Moses (@Cre4T3Tiv3) - jesse@bytestacklabs.com"

logger = logging.getLogger(__name__)


class TemporalEvaluatorService:
    """High-level service orchestrating GitVoyant temporal analysis.

    Provides repository-level and file-level evaluation capabilities, quality
    decay forecasting, and insight generation. Serves as the primary interface
    between application layers and the underlying temporal evaluation infrastructure.

    This service handles error management, result aggregation, and provides
    consistent interfaces for different analysis modes including single-file
    evaluation, repository-wide analysis, and predictive quality assessment.

    Attributes:
        window_days (int): Default analysis window in days for temporal evaluation.
            Determines how far back in commit history to analyze for trends.
    """

    def __init__(self, window_days: int = 180):
        """Initialize the temporal evaluator service.

        Args:
            window_days (int, optional): Number of days of commit history to
                analyze by default. Larger windows provide more stable trends
                but may include less relevant historical data. Defaults to 180.
        """
        self.window_days = window_days

    async def evaluate_repository(
        self, repo_path: Union[str, Path], max_files: int = 50
    ) -> Dict[str, Union[str, List[Dict]]]:
        """Evaluate all Python files in a repository and rank by decay risk.

        Performs comprehensive temporal analysis across multiple files within
        a repository, identifying quality patterns and ranking files by their
        risk of quality decay. Results are sorted by decay risk to prioritize
        attention on the most concerning files.

        Args:
            repo_path (Union[str, Path]): Filesystem path to the Git repository
                root directory. Must be a valid Git repository with commit history.
            max_files (int, optional): Maximum number of files to evaluate to
                prevent excessive processing time on large repositories.
                Defaults to 50.

        Returns:
            Dict[str, Union[str, List[Dict]]]: Repository evaluation results containing:
                - repo_path (str): Resolved repository path
                - evaluations (List[Dict]): List of file evaluation results,
                  sorted by quality decay forecast in descending order

        Note:
            The method automatically excludes common non-source directories
            like .venv and __pycache__ to focus on relevant Python source files.
            Files with evaluation errors are logged but skipped to ensure
            partial results are still returned.

        Example:
            >>> service = TemporalEvaluatorService()
            >>> results = await service.evaluate_repository("./my-repo")
            >>> print(f"Evaluated {len(results['evaluations'])} files")
            >>> # Files are sorted by decay risk, highest first
        """
        path = Path(repo_path).resolve()
        evaluator = TemporalEvaluator(str(path), window_days=self.window_days)

        results = []
        for file in path.rglob("*.py"):
            if ".venv" in str(file) or "__pycache__" in str(file):
                continue

            try:
                outcome = evaluator.evaluate_file_evolution(str(file))
                if "error" not in outcome:
                    results.append(outcome)
            except Exception as e:
                logger.warning(f"[skip] {file}: {e}")
                continue

            if len(results) >= max_files:
                break

        results.sort(key=lambda x: x.get("quality_decay_forecast", 0), reverse=True)
        return {
            "repo_path": str(path),
            "evaluations": results,
        }

    async def evaluate_file(
        self, file_path: str, repo_path: str
    ) -> Dict[str, Union[str, float, int]]:
        """Evaluate a specific Python file for trend, exposure, and decay risk.

        Performs detailed temporal analysis on a single file, examining its
        complexity evolution, quality patterns, and risk characteristics over
        the configured analysis window.

        Args:
            file_path (str): Path to the target file for evaluation. Can be
                absolute or relative to the repository root.
            repo_path (str): Path to the Git repository containing the file.
                Must be a valid Git repository with commit history.

        Returns:
            Dict[str, Union[str, float, int]]: File evaluation results containing:
                - file_path (str): Resolved file path
                - complexity_trend_slope (float): Rate of complexity change
                - quality_decay_forecast (float): Risk prediction (0.0-1.0)
                - commits_evaluated (int): Number of commits analyzed
                - exposure_level (str): Risk classification (LOW/MEDIUM/HIGH)
                - error (str): Error message if evaluation failed

        Raises:
            Exception: Captured and returned as error field in result dictionary
                rather than propagated, ensuring graceful degradation.

        Example:
            >>> service = TemporalEvaluatorService()
            >>> result = await service.evaluate_file("src/main.py", "./repo")
            >>> if "error" not in result:
            ...     print(f"Risk level: {result['exposure_level']}")
            ...     print(f"Trend: {result['complexity_trend_slope']:+.2f}/month")
        """
        try:
            evaluator = TemporalEvaluator(repo_path, window_days=self.window_days)
            result = evaluator.evaluate_file_evolution(file_path)
            if "error" in result:
                raise ValueError(result["error"])
            return result
        except Exception as e:
            logger.error(f"[fail] evaluate_file: {file_path} – {e}")
            return {
                "file_path": file_path,
                "error": str(e),
                "quality_decay_forecast": 0.0,
                "commits_evaluated": 0,
            }

    def forecast_decay(self, file_path: str, repo_path: str) -> Optional[float]:
        """Predict the probability of future quality decay for a given file.

        Uses temporal patterns and complexity trends to estimate the likelihood
        of quality degradation in the specified file. This is a simplified
        predictive model that will be enhanced in future versions.

        Args:
            file_path (str): Path to the file for decay prediction.
            repo_path (str): Path to the Git repository containing the file.

        Returns:
            Optional[float]: Decay probability between 0.0 and 1.0, where
                higher values indicate greater risk of quality degradation.
                Returns None if prediction fails due to insufficient data
                or analysis errors.

        Note:
            The current implementation uses a simplified model based on
            complexity growth rates. Future versions will incorporate
            additional factors such as developer patterns, change frequency,
            and historical quality metrics.

        Example:
            >>> service = TemporalEvaluatorService()
            >>> risk = service.forecast_decay("src/utils.py", "./repo")
            >>> if risk is not None:
            ...     print(f"Decay risk: {risk:.1%}")
        """
        try:
            evaluator = TemporalEvaluator(repo_path, window_days=self.window_days)
            return evaluator.forecast_quality_decay(file_path)
        except Exception as e:
            logger.warning(f"[warn] forecast: {file_path} – {e}")
            return None

    def generate_insight(
        self, file_path: str, repo_path: str
    ) -> List[Dict[str, Union[str, float]]]:
        """Generate structured discernment signals for agentic tooling.

        Creates actionable insights and discernment signals based on temporal
        analysis results, formatted for consumption by AI agents, CLI tools,
        or other automated systems.

        Args:
            file_path (str): Path to the file for insight generation.
            repo_path (str): Path to the Git repository containing the file.

        Returns:
            List[Dict[str, Union[str, float]]]: List of insight dictionaries,
                each containing:
                - file_path (str): Target file path
                - type (str): Type of discernment (e.g., "complexity_growth")
                - severity (float): Severity level (0.0-1.0)
                - description (str): Human-readable description
                - confidence (float): Confidence in the insight (0.0-1.0)
                - detected_at (str): ISO timestamp of detection

        Note:
            Insights are generated based on configurable thresholds for
            complexity growth, quality decay risk, and other temporal patterns.
            The system focuses on actionable signals that can inform
            development decisions or automated quality management.

        Example:
            >>> service = TemporalEvaluatorService()
            >>> insights = service.generate_insight("src/api.py", "./repo")
            >>> for insight in insights:
            ...     print(f"{insight['type']}: {insight['description']}")
            ...     print(f"Severity: {insight['severity']:.2f}")
        """
        try:
            evaluator = TemporalEvaluator(repo_path, window_days=self.window_days)
            signals: List[TemporalDiscernment] = evaluator.generate_discernment(
                file_path
            )

            return [
                {
                    "file_path": i.file_path,
                    "type": i.discernment_type,
                    "severity": i.severity,
                    "description": i.description,
                    "confidence": i.confidence,
                    "detected_at": i.detected_at.isoformat(),
                }
                for i in signals
            ]

        except Exception as e:
            logger.warning(f"[warn] insight: {file_path} – {e}")
            return []
