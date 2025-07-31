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

Module: src/gitvoyant/infrastructure/temporal_evaluator.py

GitVoyant Temporal Evaluation Infrastructure

Core temporal evaluation engine for analyzing code complexity evolution through
Git commit history. This module implements the fundamental algorithms for
detecting quality patterns, computing complexity trends, and generating
predictive insights about code quality decay.

The TemporalEvaluator class provides comprehensive analysis of Python source
files using cyclomatic complexity metrics, temporal pattern recognition, and
statistical trend analysis to identify files at risk of quality degradation.

Author: Jesse Moses (@Cre4T3Tiv3) <jesse@bytestacklabs.com>

Version: 0.2.0

License: Apache 2.0
"""

import ast
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

import git
import numpy as np
import pandas as pd

__version__ = "0.2.0"
__author__ = "Jesse Moses (@Cre4T3Tiv3) - jesse@bytestacklabs.com"

from gitvoyant.infrastructure.config import get_settings

logger = logging.getLogger(__name__)
logger.propagate = False

settings = get_settings()

level = logging.INFO if settings.verbose_mode else logging.ERROR
logger.setLevel(level)

if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setLevel(level)
    formatter = logging.Formatter("%(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
else:
    for handler in logger.handlers:
        handler.setLevel(level)


@dataclass
class TemporalDiscernment:
    """Represents a temporal insight or pattern detected during analysis.

    Encapsulates actionable intelligence about code quality patterns, risk
    factors, and temporal trends discovered through commit history analysis.
    Used to generate structured insights for agent consumption and reporting.

    Attributes:
        file_path (str): Path to the file where the discernment was detected.
        discernment_type (str): Category of insight (e.g., "complexity_growth",
            "quality_decay"). Used for filtering and categorization.
        severity (float): Severity level from 0.0 to 1.0, where higher values
            indicate more critical issues requiring immediate attention.
        description (str): Human-readable description of the detected pattern
            or issue, suitable for reporting and user interfaces.
        confidence (float): Statistical confidence in the discernment from
            0.0 to 1.0, based on data quality and pattern strength.
        detected_at (datetime): Timestamp when the discernment was generated,
            useful for tracking insight evolution over time.
    """

    file_path: str
    discernment_type: str
    severity: float
    description: str
    confidence: float
    detected_at: datetime


class TemporalEvaluator:
    """Core engine for temporal code quality evaluation and pattern detection.

    Analyzes Git commit history to identify quality trends, complexity evolution,
    and risk patterns in Python source files. Uses cyclomatic complexity
    metrics and statistical analysis to detect temporal patterns and predict
    future quality decay.

    The evaluator implements GitVoyant's core temporal intelligence algorithms,
    providing file-level analysis with configurable time windows and robust
    error handling for production use.

    Attributes:
        repository_path (Path): Resolved path to the Git repository root.
        repo (git.Repo): GitPython repository object for commit access.
        window_days (int): Analysis window in days for temporal evaluation.
    """

    def __init__(self, repository_path: str, window_days: int = 180) -> None:
        """Initialize the temporal evaluator for a specific repository.

        Sets up Git repository access and configures the analysis window for
        temporal evaluation. Validates that the target path contains a valid
        Git repository with accessible commit history.

        Args:
            repository_path (str): Filesystem path to the Git repository root.
                Must be a valid Git repository with commit history.
            window_days (int, optional): Number of days of commit history to
                analyze. Larger windows provide more stable trends but may
                include less relevant historical data. Defaults to 180.

        Raises:
            git.exc.InvalidGitRepositoryError: If the path is not a valid Git
                repository or lacks proper Git metadata.
            Exception: For other Git access issues such as permissions or
                corruption.

        Example:
            >>> evaluator = TemporalEvaluator("/path/to/repo", window_days=90)
            >>> result = evaluator.evaluate_file_evolution("src/main.py")
        """
        logger.debug(
            f"Initializing TemporalEvaluator for repository: {repository_path}"
        )

        self.repository_path = Path(repository_path).resolve()
        logger.debug(f"Resolved repository path: {self.repository_path}")

        try:
            self.repo = git.Repo(repository_path)
            logger.debug("Git repository access established")
        except git.exc.InvalidGitRepositoryError as e:
            logger.error(f"Invalid Git repository at {repository_path}: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to access repository at {repository_path}: {e}")
            raise

        self.window_days = window_days
        logger.debug(f"Analysis window set to {window_days} days")

    def evaluate_file_evolution(self, file_path: str) -> Dict:
        """Evaluate temporal evolution of a specific file's complexity and quality.

        Performs comprehensive temporal analysis on a single file by examining
        its commit history, extracting complexity metrics at each commit, and
        computing statistical trends and quality patterns over time.

        Args:
            file_path (str): Path to the target file, either absolute or relative
                to the repository root. The file must exist in the current
                repository state and have sufficient commit history.

        Returns:
            Dict: Evaluation results containing:
                - file_path (str): Resolved file path
                - evaluation_window_days (int): Analysis window used
                - commits_evaluated (int): Number of commits analyzed
                - complexity_trend_slope (float): Rate of complexity change
                - current_complexity (int): Most recent complexity score
                - complexity_growth_rate (float): Relative growth rate
                - quality_decay_forecast (float): Risk prediction (0.0-1.0)
                - exposure_level (str): Risk classification (LOW/MEDIUM/HIGH)
                - evolution_timetable (List[Dict]): Chronological complexity data
                - confidence_warning (str): Warning if confidence is low (optional)
                - confidence_score (float): Statistical confidence (0.0-1.0) (optional)
                - error (str): Error message if evaluation failed

        Note:
            The method requires at least 2 commits within the analysis window
            and at least 3 successfully processed commits to generate reliable
            temporal trends. Files with insufficient history return error results.
            Results with < 5 commits include confidence warnings.

        Example:
            >>> evaluator = TemporalEvaluator("/path/to/repo")
            >>> result = evaluator.evaluate_file_evolution("src/api.py")
            >>> if "error" not in result:
            ...     trend = result["complexity_trend_slope"]
            ...     confidence = result.get("confidence_score", 1.0)
            ...     print(f"Complexity trend: {trend:+.2f} units/month (confidence: {confidence:.2f})")
        """
        logger.info(f"Starting temporal evaluation for: {file_path}")

        file_path_object = Path(file_path)
        if file_path_object.is_absolute():
            try:
                relative_path = file_path_object.relative_to(self.repository_path)
                logger.debug(f"Converted absolute path to relative: {relative_path}")
            except ValueError:
                error_message = (
                    f"File {file_path} is not in repository {self.repository_path}"
                )
                logger.error(error_message)
                return {"error": error_message}
        else:
            relative_path = Path(file_path)
            logger.debug(f"Using relative path: {relative_path}")

        logger.debug(
            f"Retrieving commit history for {relative_path} within {self.window_days} days"
        )
        try:
            commits = list(
                self.repo.iter_commits(
                    paths=str(relative_path),
                    since=datetime.now() - timedelta(days=self.window_days),
                    max_count=100,
                )
            )
            logger.debug(f"Found {len(commits)} commits for file")
        except Exception as e:
            error_message = f"Failed to retrieve commit history: {e}"
            logger.error(error_message)
            return {"error": error_message}

        if len(commits) < 2:
            error_message = "Insufficient commit history for temporal evaluation"
            logger.warning(
                f"{error_message} (found {len(commits)} commits, need at least 2)"
            )
            return {"error": error_message}

        logger.debug("Extracting temporal metrics from commits")
        evolution_data = []
        computed_commits = 0

        for commit in reversed(commits):
            try:
                content = self._get_file_at_commit(commit, relative_path)
                if content:
                    metrics = self._extract_metrics(content, commit)
                    evolution_data.append(metrics)
                    computed_commits += 1
            except Exception as e:
                logger.debug(f"Skipping commit {commit.hexsha[:8]}: {e}")
                continue

        logger.debug(f"Successfully processed {computed_commits} commits")

        if len(evolution_data) < 3:
            error_message = "Could not extract sufficient temporal data"
            logger.warning(
                f"{error_message} (processed {len(evolution_data)} commits, need at least 3)"
            )
            return {"error": error_message}
        elif len(evolution_data) < 5:
            logger.info(f"Low confidence analysis with {len(evolution_data)} commits")
            outcome = self._compute_temporal_discernment(
                evolution_data, str(relative_path)
            )
            outcome["confidence_warning"] = (
                "Low confidence due to limited commit history"
            )
            outcome["confidence_score"] = min(outcome.get("confidence_score", 0.5), 0.4)
            logger.info(
                f"Analysis complete for {file_path}: {outcome['commits_evaluated']} commits, "
                f"{outcome['complexity_trend_slope']:+.2f}/month trend, {outcome['exposure_level']} risk "
                f"(LOW CONFIDENCE)"
            )
            return outcome

        logger.debug("Computing temporal discernment")
        try:
            outcome = self._compute_temporal_discernment(
                evolution_data, str(relative_path)
            )
            logger.info(
                f"Analysis complete for {file_path}: {outcome['commits_evaluated']} commits, "
                f"{outcome['complexity_trend_slope']:+.2f}/month trend, {outcome['exposure_level']} risk"
            )
            return outcome
        except Exception as e:
            error_message = f"Failed to compute temporal discernment: {e}"
            logger.error(error_message)
            return {"error": error_message}

    def forecast_quality_decay(self, file_path: str) -> float:
        """Predict the probability of future quality decay for a file.

        Uses temporal patterns and complexity trends to estimate the likelihood
        of quality degradation. This method provides a simplified predictive
        model that will be enhanced in future versions with additional factors.

        Args:
            file_path (str): Path to the file for decay prediction.

        Returns:
            float: Decay probability between 0.0 and 1.0, where higher values
                indicate greater risk of quality degradation. Returns 0.0 if
                prediction fails due to insufficient data or analysis errors.

        Example:
            >>> evaluator = TemporalEvaluator("/path/to/repo")
            >>> risk = evaluator.forecast_quality_decay("src/utils.py")
            >>> print(f"Quality decay risk: {risk:.1%}")
        """
        logger.debug(f"Predicting quality decay for: {file_path}")

        evaluation = self.evaluate_file_evolution(file_path)
        if "error" in evaluation:
            logger.debug(
                f"Quality decay prediction failed due to evaluation error: {evaluation['error']}"
            )
            return 0.0

        risk_exposure_score = evaluation.get("quality_decay_forecast", 0.0)
        logger.debug(
            f"Quality decay prediction for {file_path}: {risk_exposure_score:.3f}"
        )
        return risk_exposure_score

    def generate_discernment(self, file_path: str) -> List[TemporalDiscernment]:
        """Generate structured discernment signals for the specified file.

        Creates actionable insights based on temporal analysis results,
        identifying patterns and risk factors that warrant attention. Insights
        are prioritized by severity to focus on the most critical issues.

        Args:
            file_path (str): Path to the file for insight generation.

        Returns:
            List[TemporalDiscernment]: List of discernment objects sorted by
                severity (highest first), each containing structured insight
                data about detected patterns, risks, and recommendations.

        Note:
            Current discernment types include:
            - complexity_growth: Rapidly increasing complexity patterns
            - quality_decay: High risk of future quality degradation

            Additional discernment types will be added in future versions
            to cover more temporal patterns and risk factors.

        Example:
            >>> evaluator = TemporalEvaluator("/path/to/repo")
            >>> insights = evaluator.generate_discernment("src/api.py")
            >>> for insight in insights:
            ...     print(f"{insight.discernment_type}: {insight.description}")
            ...     print(f"Severity: {insight.severity:.2f}")
        """
        logger.debug(f"Generating discernment for: {file_path}")

        evaluation = self.evaluate_file_evolution(file_path)
        if "error" in evaluation:
            logger.debug(
                f"Insight generation failed due to evaluation error: {evaluation['error']}"
            )
            return []

        discernment = []

        base_confidence = 0.85
        if "confidence_warning" in evaluation:
            base_confidence = evaluation.get("confidence_score", 0.4)

        complexity_slope = evaluation.get("complexity_trend_slope", 0)
        if complexity_slope > 0.5:
            severity = min(complexity_slope / 2.0, 1.0)
            insight = TemporalDiscernment(
                file_path=file_path,
                discernment_type="complexity_growth",
                severity=severity,
                description=f"Complexity growing rapidly (+{complexity_slope:.1f}/month)",
                confidence=base_confidence,
                detected_at=datetime.now(),
            )
            discernment.append(insight)
            logger.debug(
                f"Generated complexity_growth insight: severity={severity:.2f}, confidence={base_confidence:.2f}"
            )

        decay_prediction = evaluation.get("quality_decay_forecast", 0)
        if decay_prediction > 0.7:
            insight = TemporalDiscernment(
                file_path=file_path,
                discernment_type="quality_decay",
                severity=decay_prediction,
                description=f"High risk of quality decay ({decay_prediction:.0%})",
                confidence=base_confidence * 0.95,
                detected_at=datetime.now(),
            )
            discernment.append(insight)
            logger.debug(
                f"Generated quality_decay insight: severity={decay_prediction:.2f}, confidence={base_confidence * 0.95:.2f}"
            )

        discernment.sort(key=lambda x: x.severity, reverse=True)
        logger.debug(f"Generated {len(discernment)} discernment for {file_path}")

        return discernment

    def _get_file_at_commit(self, commit, relative_path: Path) -> Optional[str]:
        """Retrieve file content at a specific commit in the repository history.

        Extracts the content of a file as it existed at a particular commit,
        enabling temporal analysis of code evolution. Handles encoding issues
        and missing files gracefully.

        Args:
            commit: GitPython commit object representing the target revision.
            relative_path (Path): Repository-relative path to the target file.

        Returns:
            Optional[str]: File content as a string if successfully retrieved,
                None if the file doesn't exist at that commit or cannot be
                decoded properly.

        Note:
            Uses UTF-8 decoding with error tolerance to handle files with
            encoding issues. Binary files or files with severe encoding
            problems will return None and be skipped in analysis.
        """
        try:
            blob = commit.tree / str(relative_path)
            content = blob.data_stream.read().decode("utf-8", errors="ignore")
            return content
        except Exception as e:
            logger.debug(
                f"Could not retrieve file {relative_path} at commit {commit.hexsha[:8]}: {e}"
            )
            return None

    def _extract_metrics(self, content: str, commit) -> Dict:
        """Extract complexity and structural metrics from file content.

        Parses Python source code to compute cyclomatic complexity and
        count structural elements like functions and classes. Provides
        the foundational metrics for temporal trend analysis.

        Args:
            content (str): Python source code content to analyze.
            commit: GitPython commit object for metadata extraction.

        Returns:
            Dict: Metrics dictionary containing:
                - timestamp (datetime): Commit timestamp
                - complexity (int): Cyclomatic complexity score
                - lines_of_code (int): Total lines in the file
                - function_count (int): Number of function definitions
                - class_count (int): Number of class definitions
                - author (str): Commit author name
                - commit_hash (str): Full commit SHA hash

        Note:
            Syntax errors in the source code result in zero complexity
            and structural counts, allowing analysis to continue with
            partial data rather than failing completely.
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

    def _cyclomatic_complexity(self, tree) -> int:
        """Calculate cyclomatic complexity of a Python AST.

        Implements cyclomatic complexity calculation by counting decision
        points in the code including conditionals, loops, boolean operations,
        and exception handlers. Uses the standard formula starting with
        base complexity of 1.

        Args:
            tree: Python AST (Abstract Syntax Tree) to analyze.

        Returns:
            int: Cyclomatic complexity score, where higher values indicate
                more complex code with more decision paths.

        Note:
            The implementation counts:
            - If statements, while loops, for loops (including async)
            - Boolean operations (and/or) based on operand count
            - Exception handlers (except clauses)

            This provides a standard cyclomatic complexity metric suitable
            for tracking complexity trends over time.
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

    def _compute_temporal_discernment(
        self, evolution_data: List[Dict], file_path: str
    ) -> Dict:
        """Compute temporal trends and risk assessment from evolution data.

        Analyzes the collected temporal metrics to identify complexity trends,
        predict quality decay risk, and classify exposure levels. This is the
        core algorithm that transforms raw commit data into actionable insights.

        Args:
            evolution_data (List[Dict]): Chronological list of complexity metrics
                extracted from commit history, each containing timestamp and
                structural measurements.
            file_path (str): Path to the file being analyzed for result annotation.

        Returns:
            Dict: Comprehensive temporal analysis results containing trend
                analysis, risk predictions, detailed evolution timeline, and
                confidence scoring based on data quality.

        Note:
            The algorithm uses linear regression for trend analysis and a
            simplified model for quality decay prediction. Confidence scoring
            is based on the number of data points available for analysis.
            Future versions will incorporate more sophisticated machine learning
            approaches and additional risk factors.
        """
        logger.debug(
            f"Computing temporal discernment from {len(evolution_data)} data points"
        )

        data_frame = pd.DataFrame(evolution_data)

        data_frame["timestamp"] = pd.to_datetime(
            data_frame["timestamp"], utc=True
        ).dt.tz_convert(None)
        data_frame = data_frame.sort_values("timestamp")

        logger.debug(
            f"Data span: {data_frame['timestamp'].min()} to {data_frame['timestamp'].max()}"
        )
        logger.debug(
            f"Complexity range: {data_frame['complexity'].min()} to {data_frame['complexity'].max()}"
        )

        complexity_trend = np.polyfit(
            range(len(data_frame)), data_frame["complexity"], 1
        )[0]
        logger.debug(f"Calculated complexity trend slope: {complexity_trend:.3f}")

        recent_complexity = data_frame["complexity"].tail(5).mean()
        historical_complexity = data_frame["complexity"].head(5).mean()

        if historical_complexity > 0:
            complexity_growth_rate = (
                recent_complexity - historical_complexity
            ) / historical_complexity
        else:
            complexity_growth_rate = 0

        logger.debug(f"Complexity growth rate: {complexity_growth_rate:.3f}")

        quality_decay_forecast = min(max(complexity_growth_rate * 2, 0), 1)

        if quality_decay_forecast > 0.7:
            exposure_level = "HIGH"
        elif quality_decay_forecast > 0.4:
            exposure_level = "MEDIUM"
        else:
            exposure_level = "LOW"

        commit_count = len(data_frame)
        if commit_count >= 10:
            confidence_score = 0.9
        elif commit_count >= 7:
            confidence_score = 0.75
        elif commit_count >= 5:
            confidence_score = 0.6
        else:
            confidence_score = 0.4

        logger.debug(
            f"Quality decay prediction: {quality_decay_forecast:.3f}, risk level: {exposure_level}, "
            f"confidence: {confidence_score:.2f}"
        )

        outcome = {
            "file_path": file_path,
            "evaluation_window_days": self.window_days,
            "commits_evaluated": len(data_frame),
            "complexity_trend_slope": complexity_trend,
            "current_complexity": data_frame["complexity"].iloc[-1],
            "complexity_growth_rate": complexity_growth_rate,
            "quality_decay_forecast": quality_decay_forecast,
            "exposure_level": exposure_level,
            "confidence_score": confidence_score,
            "evolution_timetable": data_frame[
                ["timestamp", "complexity", "author"]
            ].to_dict("records"),
        }

        return outcome


def expedited_analysis(
    repository_path: str, file_path: str, window_days: int = 180
) -> Dict:
    """Perform quick temporal evaluation for a single file.

    Convenience function that creates a TemporalEvaluator instance and
    performs file evaluation in a single call. Useful for one-off analysis
    or integration with external tools.

    Args:
        repository_path (str): Path to the Git repository root directory.
        file_path (str): Path to the target file for evaluation.
        window_days (int, optional): Analysis window in days. Defaults to 180.

    Returns:
        Dict: Evaluation results identical to TemporalEvaluator.evaluate_file_evolution(),
            or error dictionary if analysis fails. Includes confidence scoring
            and warnings for low-confidence results.

    Example:
        >>> from gitvoyant.infrastructure.temporal_evaluator import expedited_analysis
        >>> result = expedited_analysis("/path/to/repo", "src/main.py", 90)
        >>> if "error" not in result:
        ...     confidence = result.get("confidence_score", 1.0)
        ...     print(f"Risk: {result['exposure_level']} (confidence: {confidence:.2f})")
    """
    logger.debug(f"Running expedited evaluation for {file_path} in {repository_path}")

    try:
        evaluator = TemporalEvaluator(repository_path, window_days=window_days)
        outcome = evaluator.evaluate_file_evolution(file_path)
        logger.debug(f"Expedited evaluation completed for {file_path}")
        return outcome
    except Exception as e:
        error_message = f"Expedited evaluation failed: {e}"
        logger.error(error_message)
        return {"error": error_message}


def forecast_decay(repository_path: str, file_path: str) -> float:
    """Predict quality decay risk for a specific file.

    Convenience function for quick decay forecasting without creating
    a full TemporalEvaluator instance. Uses default analysis window.

    Args:
        repository_path (str): Path to the Git repository root directory.
        file_path (str): Path to the target file for prediction.

    Returns:
        float: Decay risk probability between 0.0 and 1.0, or 0.0 if
            prediction fails.

    Example:
        >>> from gitvoyant.infrastructure.temporal_evaluator import forecast_decay
        >>> risk = forecast_decay("/path/to/repo", "src/api.py")
        >>> if risk > 0.5:
        ...     print("High decay risk detected!")
    """
    logger.debug(f"Running decay forecast for {file_path} in {repository_path}")

    try:
        evaluator = TemporalEvaluator(repository_path)
        risk_exposure_score = evaluator.forecast_quality_decay(file_path)
        logger.debug(
            f"Decay forecast completed for {file_path}: {risk_exposure_score:.3f}"
        )
        return risk_exposure_score
    except Exception as e:
        logger.warning(f"Decay forecast failed for {file_path}: {e}")
        return 0.0


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(levelname)s - %(name)s - %(message)s"
    )

    logger.info("🔮 GitVoyant Temporal Code Intelligence v0.2.0")
    logger.info("This is just the beginning...")
    logger.info("")
    logger.info("Module loaded successfully. Key components:")
    logger.info("  • TemporalEvaluator: Core evaluation engine")
    logger.info("  • TemporalDiscernment: Insight representation")
    logger.info("  • expedited_analysis(): Quick single-file evaluation")
    logger.info("  • forecast_decay(): Risk prediction utility")
    logger.info("")
    logger.info("Example usage:")
    logger.info("  from src.infrastructure.temporal_evaluator import TemporalEvaluator")
    logger.info("  evaluator = TemporalEvaluator('/path/to/repo')")
    logger.info("  outcome = evaluator.evaluate_file_evolution('src/main.py')")
    logger.info("")
    logger.info("For more examples, see: examples/flask_discovery_demo")
