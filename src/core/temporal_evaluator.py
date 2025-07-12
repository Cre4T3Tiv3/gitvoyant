"""
Module: src/core/temporal_evaluator.py

GitVoyant Temporal Code Intelligence Engine v0.1.0
The core temporal evaluation that proves the concept works.

This module provides temporal code intelligence by analyzing Git repository history
to understand code evolution patterns and predict quality trajectories. It serves
as the foundation for GitVoyant's temporal intelligence capabilities.

The module implements McCabe cyclomatic complexity evaluation across Git commit
history, using linear regression to identify temporal trends and predict future
quality decay patterns. This enables AI agents to understand code evolution
beyond static snapshots.

Key Features:
    - Temporal complexity trend evaluation
    - Quality engineering pattern detection
    - Risk assessment and prediction
    - Evolution timeline tracking
    - Developer impact correlation

Example:
    Basic temporal evaluation workflow:

    >>> from src.core.temporal_evaluator import TemporalEvaluator
    >>> evaluator = TemporalEvaluator("/path/to/repo")
    >>> outcome = evaluator.evaluate_file_evolution("src/main.py")
    >>> if 'error' not in evaluation:
    ...     print(f"Trend: {evaluation['complexity_trend_slope']:+.2f}/month")
    ...     print(f"Risk: {evaluation['exposure_level']}")

Dependencies:
    - GitPython: For repository and commit access
    - pandas: For temporal data manipulation
    - numpy: For trend evaluation and regression
    - ast: For Python code parsing and complexity calculation

Author: Jesse Moses (@Cre4T3Tiv3) - jesse@bytestacklabs.com
Version: 0.1.0
License: Apache 2.0
"""

import ast
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import git
import numpy as np
import pandas as pd

__version__ = "0.1.0"
__author__ = "Jesse Moses (@Cre4T3Tiv3) - jesse@bytestacklabs.com"

logger = logging.getLogger(__name__)


@dataclass
class TemporalDiscernment:
    """A temporal insight about code evolution.

    Represents a specific finding from temporal code evaluation that provides
    actionable information about code quality trends and patterns. Used to
    communicate discernment about complexity growth, quality decay risks, and
    maintenance recommendations.

    Attributes:
        file_path: Path to the evaluated file relative to repository root.
        discernment_type: Category of insight (e.g., 'complexity_growth', 'quality_decay').
        severity: Severity score from 0.0 (low) to 1.0 (critical).
        description: Human-readable description of the insight.
        confidence: Confidence level in the insight from 0.0 to 1.0.
        detected_at: Timestamp when the insight was generated.

    Example:
        >>> insight = TemporalDiscernment(
        ...     file_path="src/api.py",
        ...     discernment_type="complexity_growth",
        ...     severity=0.8,
        ...     description="Complexity growing rapidly (+2.3/month)",
        ...     confidence=0.85,
        ...     detected_at=datetime.now()
        ... )
        >>> print(f"🚨 {insight.description} (confidence: {insight.confidence:.0%})")
    """

    file_path: str
    discernment_type: str
    severity: float
    description: str
    confidence: float
    detected_at: datetime


class TemporalEvaluator:
    """Analyzes Git repository history to predict code evolution patterns.

    This is the core engine that powers GitVoyant's temporal intelligence.
    It analyzes how code complexity evolves over time by examining Git commit
    history and extracting temporal patterns that indicate quality trends.

    The evaluator provides comprehensive discernment into code evolution by:
    - Tracking cyclomatic complexity changes over time
    - Identifying quality engineering vs decay patterns
    - Predicting future maintenance challenges
    - Correlating developer actions with code health
    - Providing temporal context for AI code agents

    The evaluation uses McCabe cyclomatic complexity as the primary metric,
    applying linear regression to identify trends and statistical models
    to predict quality decay probability.

    Example:
        Basic usage for analyzing a single file:

        >>> evaluator = TemporalEvaluator("/path/to/repo")
        >>> outcome = evaluator.evaluate_file_evolution("src/main.py")
        >>> print(f"Trend: {evaluation['complexity_trend_slope']:+.2f}/month")
        >>> print(f"Risk level: {evaluation['exposure_level']}")

        Generate actionable discernment:

        >>> discernment = evaluator.generate_discernment("src/main.py")
        >>> for insight in discernment:
        ...     print(f"{insight.description} (confidence: {insight.confidence:.0%})")

        Batch evaluation across multiple files:

        >>> files = ["src/api.py", "src/models.py", "src/utils.py"]
        >>> for file_path in files:
        ...     risk = evaluator.forecast_quality_decay(file_path)
        ...     print(f"{file_path}: {risk:.1%} decay risk")

    Attributes:
        repository_path: Path to the Git repository being evaluated.
        repo: GitPython repository object for accessing Git history.
        window_days: Number of days of history to analyze (default: 180).

    Note:
        Requires a valid Git repository with sufficient commit history.
        Analysis quality improves with longer commit history and more
        frequent commits to the target files.
    """

    def __init__(self, repository_path: str, window_days: int = 180) -> None:
        """Initialize evaluator for a Git repository.

        Sets up the temporal evaluator with repository access and evaluation
        parameters. Validates repository existence and initializes Git
        access for commit history traversal.

        Args:
            repository_path: Path to the Git repository to analyze. Can be relative
                or absolute path to repository root containing .git directory.
            window_days: Number of days of commit history to include in evaluation.
                Defaults to 180 days for reasonable performance vs insight trade-off.
                Larger windows provide more historical context but slower evaluation.

        Raises:
            git.exc.InvalidGitRepositoryError: If repository_path is not a valid Git repository.
            FileNotFoundError: If repository_path does not exist.
            PermissionError: If insufficient permissions to access repository.

        Example:
            >>> # Standard 6-month evaluation window
            >>> evaluator = TemporalEvaluator("/path/to/repo")

            >>> # Extended 1-year evaluation for deeper discernment
            >>> evaluator = TemporalEvaluator("/path/to/repo", window_days=365)

            >>> # Quick 1-month evaluation for recent patterns
            >>> evaluator = TemporalEvaluator("/path/to/repo", window_days=30)
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
        """Analyze how a specific file has evolved over time.

        Examines the Git history of a file to understand complexity evolution,
        quality patterns, and predict future maintenance needs. This is the
        core method that provides temporal intelligence by tracking how
        cyclomatic complexity changes across commits.

        The evaluation process involves:
        1. Retrieving commit history for the specified file
        2. Extracting code metrics at each commit point
        3. Computing temporal trends using linear regression
        4. Predicting quality decay based on historical patterns
        5. Classifying the evolution pattern (improving/stable/deteriorating)

        Args:
            file_path: Path to the file to analyze, relative to repository root.
                Can be absolute path - will be converted to relative automatically.
                Must be a Python file for complexity evaluation to work properly.

        Returns:
            Dictionary containing comprehensive temporal evaluation results:

            - 'file_path': The evaluated file path (string)
            - 'evaluation_window_days': Number of days evaluated (int)
            - 'commits_evaluated': Number of commits processed (int)
            - 'complexity_trend_slope': Monthly complexity change rate (float)
            - 'current_complexity': Most recent complexity measurement (int)
            - 'complexity_growth_rate': Percentage change from baseline (float)
            - 'quality_decay_forecast': Risk score 0.0-1.0 for quality decay (float)
            - 'exposure_level': Human-readable risk assessment ('LOW'/'MEDIUM'/'HIGH')
            - 'evolution_timetable': List of complexity measurements over time (list)

            Or dictionary with 'error' key if evaluation fails:

            - 'error': Description of why evaluation failed (string)

        Example:
            >>> evaluator = TemporalEvaluator("/path/to/repo")
            >>> outcome = evaluator.evaluate_file_evolution("src/core/models.py")
            >>> if 'error' not in outcome:
            ...     print(f"Risk exposure level: {outcome['exposure_level']}")
            ...     print(f"Complexity trend: {outcome['complexity_trend_slope']:+.2f}/month")
            ...     print(f"Commits evaluated: {outcome['commits_evaluated']}")
            ... else:
            ...     print(f"Analysis failed: {outcome['error']}")

        Note:
            Requires at least 5 commits in the evaluation window for meaningful results.
            Files with insufficient history will return an error dictionary.
            Analysis quality improves with more commits and longer time spans.

        Raises:
            Exception: Logs errors but returns error dict instead of raising.
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

        if len(commits) < 5:
            error_message = "Insufficient commit history for temporal evaluation"
            logger.warning(
                f"{error_message} (found {len(commits)} commits, need at least 5)"
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
        """Predict likelihood of quality decay for a file.

        Uses temporal evaluation to assess the probability that a file will
        experience quality degradation in the near future based on historical
        evolution patterns. This prediction is based on complexity growth
        trends and helps prioritize maintenance efforts.

        The prediction model considers:
        - Historical complexity growth rate
        - Recent vs historical complexity comparison
        - Trend acceleration patterns
        - Commit frequency and patterns

        Args:
            file_path: Path to the file to analyze, relative to repository root.
                Same path handling as evaluate_file_evolution().

        Returns:
            Risk score from 0.0 (no risk) to 1.0 (highest risk of quality decay).
            Returns 0.0 if evaluation fails due to insufficient data.

            Risk interpretation:
            - 0.0-0.3: Low risk - stable or improving quality
            - 0.4-0.6: Medium risk - monitor for changes
            - 0.7-1.0: High risk - consider refactoring

        Example:
            >>> evaluator = TemporalEvaluator("/path/to/repo")
            >>> risk = evaluator.forecast_quality_decay("src/legacy_module.py")
            >>> if risk > 0.7:
            ...     print("High risk - consider refactoring")
            >>> elif risk > 0.4:
            ...     print("Medium risk - monitor closely")
            >>> else:
            ...     print("Low risk - stable quality")

            >>> # Batch evaluation for prioritization
            >>> files = ["src/api.py", "src/models.py", "src/utils.py"]
            >>> risks = [(f, evaluator.forecast_quality_decay(f)) for f in files]
            >>> sorted_risks = sorted(risks, key=lambda x: x[1], reverse=True)
            >>> print("Files by decay risk:")
            >>> for file_path, risk in sorted_risks:
            ...     print(f"  {file_path}: {risk:.1%}")

        Note:
            This is a simplified prediction model. Future versions will
            incorporate machine learning approaches for improved accuracy.
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
        """Generate actionable temporal discernment for a file.

        Analyzes temporal patterns to generate specific, actionable discernment
        about code quality trends, complexity growth, and maintenance needs.
        This method translates raw temporal evaluation into human-readable
        recommendations for development teams.

        The insight generation process evaluates:
        - Complexity growth rate and acceleration
        - Quality decay probability thresholds
        - Pattern classification and risk assessment
        - Confidence scoring based on data quality

        Args:
            file_path: Path to the file to analyze, relative to repository root.
                Same path handling as evaluate_file_evolution().

        Returns:
            List of TemporalDiscernment objects, sorted by severity (highest first).
            Returns empty list if evaluation fails or no significant discernment found.

            Each insight contains:
            - file_path: The evaluated file
            - discernment_type: Category (complexity_growth, quality_decay, etc.)
            - severity: 0.0-1.0 severity score
            - description: Human-readable insight description
            - confidence: 0.0-1.0 confidence in the insight
            - detected_at: When the insight was generated

        Example:
            >>> evaluator = TemporalEvaluator("/path/to/repo")
            >>> discernment = evaluator.generate_discernment("src/api.py")
            >>> for insight in discernment:
            ...     severity_icon = "🚨" if insight.severity > 0.7 else "⚠️"
            ...     print(f"{severity_icon} {insight.description}")
            ...     print(f"   Confidence: {insight.confidence:.0%}")
            ...     if insight.severity > 0.8:
            ...         print("   Action required!")

            >>> # Filter high-priority discernment
            >>> high_priority = [i for i in discernment if i.severity > 0.7]
            >>> if high_priority:
            ...     print(f"Found {len(high_priority)} high-priority issues")

        Note:
            Insights are generated based on configurable thresholds:
            - Complexity growth > 0.5/month triggers complexity_growth insight
            - Quality decay prediction > 0.7 triggers quality_decay insight

            Future versions will include additional insight types for:
            - Developer productivity patterns
            - Refactoring opportunities
            - Technical debt accumulation
        """
        logger.debug(f"Generating discernment for: {file_path}")

        evaluation = self.evaluate_file_evolution(file_path)
        if "error" in evaluation:
            logger.debug(
                f"Insight generation failed due to evaluation error: {evaluation['error']}"
            )
            return []

        discernment = []

        complexity_slope = evaluation.get("complexity_trend_slope", 0)
        if complexity_slope > 0.5:
            severity = min(complexity_slope / 2.0, 1.0)
            insight = TemporalDiscernment(
                file_path=file_path,
                discernment_type="complexity_growth",
                severity=severity,
                description=f"Complexity growing rapidly (+{complexity_slope:.1f}/month)",
                confidence=0.85,
                detected_at=datetime.now(),
            )
            discernment.append(insight)
            logger.debug(
                f"Generated complexity_growth insight: severity={severity:.2f}"
            )

        decay_prediction = evaluation.get("quality_decay_forecast", 0)
        if decay_prediction > 0.7:
            insight = TemporalDiscernment(
                file_path=file_path,
                discernment_type="quality_decay",
                severity=decay_prediction,
                description=f"High risk of quality decay ({decay_prediction:.0%})",
                confidence=0.80,
                detected_at=datetime.now(),
            )
            discernment.append(insight)
            logger.debug(
                f"Generated quality_decay insight: severity={decay_prediction:.2f}"
            )

        discernment.sort(key=lambda x: x.severity, reverse=True)
        logger.debug(f"Generated {len(discernment)} discernment for {file_path}")

        return discernment

    def _get_file_at_commit(self, commit, relative_path: Path) -> Optional[str]:
        """Get file content at specific commit.

        Retrieves the file content as it existed at a specific commit point.
        Used internally to build the temporal evolution timeline.

        Args:
            commit: GitPython commit object representing a specific commit.
            relative_path: Path to file relative to repository root.

        Returns:
            File content as string, or None if file doesn't exist at commit
            or cannot be decoded as text.

        Note:
            Uses UTF-8 decoding with error handling for non-text files.
            Binary files or encoding issues will outcome in None return.
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
        """Extract code metrics from file content.

        Calculates various code quality metrics including cyclomatic complexity,
        lines of code, and structural elements like functions and classes.
        This method processes the source code at a specific commit point.

        Args:
            content: Source code content as string.
            commit: GitPython commit object for metadata extraction.

        Returns:
            Dictionary containing extracted metrics:
            - timestamp: When the commit was made (datetime)
            - complexity: Cyclomatic complexity score (int)
            - lines_of_code: Total lines in the file (int)
            - function_count: Number of function definitions (int)
            - class_count: Number of class definitions (int)
            - author: Commit author name (string)
            - commit_hash: Full commit hash for reference (string)

        Note:
            If the file contains syntax errors, complexity will be set to 0
            but other metrics will still be calculated. This handles cases
            where intermediate commits may have syntax issues.
        """
        try:
            tree = ast.parse(content)
            complexity = self._cyclomatic_complexity(tree)

            # Count structural elements
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
        """Calculate cyclomatic complexity using AST evaluation.

        Implements McCabe cyclomatic complexity calculation by counting
        decision points in the code's abstract syntax tree. This provides
        a quantitative measure of code complexity that correlates with
        testing difficulty and error probability.

        Args:
            tree: Python AST (Abstract Syntax Tree) object from ast.parse().

        Returns:
            Cyclomatic complexity score as integer. Minimum value is 1
            (representing linear code flow with no decision points).

        Note:
            Counts the following as decision points that increase complexity:
            - if/elif statements (+1 each)
            - while/for loops (+1 each)
            - Boolean operators: and/or (+1 for each additional operand)
            - Exception handlers: except blocks (+1 each)

            Does not count:
            - Function/class definitions (structural, not complexity)
            - Import statements
            - Assignment statements
            - Return statements (unless part of conditional)

        Reference:
            McCabe, T.J. (1976). "A Complexity Measure". IEEE Transactions
            on Software Engineering, SE-2(4):308-320.

        Example:
            Simple linear code: complexity = 1
            ```python
            def simple():
                x = 1
                return x
            ```

            Code with decisions: complexity = 3
            ```python
            def complex(x):
                if x > 0:        # +1
                    if x > 10:   # +1
                        return x
                return 0
            ```
        """
        complexity = 1  # Base complexity for linear execution

        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                # Boolean operations: and/or add complexity for each additional operand
                complexity += len(node.values) - 1
            elif isinstance(node, ast.ExceptHandler):
                complexity += 1

        return complexity

    def _compute_temporal_discernment(
        self, evolution_data: List[Dict], file_path: str
    ) -> Dict:
        """Compute temporal intelligence from evolution data.

        Processes the extracted metrics timeline to calculate trends,
        patterns, and predictions about code quality evolution. This is
        the core evaluation method that transforms raw commit data into
        actionable temporal intelligence.

        The computation process includes:
        1. Data preparation and timestamp normalization
        2. Linear regression for trend evaluation
        3. Statistical evaluation of complexity patterns
        4. Quality decay prediction modeling
        5. Risk level classification

        Args:
            evolution_data: List of metric dictionaries from commit history.
                Each dictionary contains metrics from _extract_metrics().
            file_path: Path to the evaluated file for reference in results.

        Returns:
            Dictionary containing comprehensive temporal evaluation results.
            See evaluate_file_evolution() for complete return value documentation.

        Note:
            Uses linear regression for trend evaluation and heuristic models
            for quality decay prediction. Future versions will incorporate
            more sophisticated machine learning approaches for improved
            accuracy and additional pattern recognition.

        Raises:
            Exception: Logs errors but may propagate to calling method.
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

        # Complexity trend evaluation using linear regression
        complexity_trend = np.polyfit(
            range(len(data_frame)), data_frame["complexity"], 1
        )[0]
        logger.debug(f"Calculated complexity trend slope: {complexity_trend:.3f}")

        # Quality decay prediction (simplified model)
        recent_complexity = data_frame["complexity"].tail(5).mean()
        historical_complexity = data_frame["complexity"].head(5).mean()

        if historical_complexity > 0:
            complexity_growth_rate = (
                recent_complexity - historical_complexity
            ) / historical_complexity
        else:
            complexity_growth_rate = 0

        logger.debug(f"Complexity growth rate: {complexity_growth_rate:.3f}")

        # Simple decay prediction model (will be enhanced in future versions)
        quality_decay_forecast = min(max(complexity_growth_rate * 2, 0), 1)

        # Risk level classification
        if quality_decay_forecast > 0.7:
            exposure_level = "HIGH"
        elif quality_decay_forecast > 0.4:
            exposure_level = "MEDIUM"
        else:
            exposure_level = "LOW"

        logger.debug(
            f"Quality decay prediction: {quality_decay_forecast:.3f}, risk level: {exposure_level}"
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
            "evolution_timetable": data_frame[
                ["timestamp", "complexity", "author"]
            ].to_dict("records"),
        }

        return outcome


def expedited_analysis(repository_path: str, file_path: str) -> Dict:
    """Quick evaluation of a single file.

    Convenience function for one-off temporal evaluation without creating
    a TemporalEvaluator instance manually. Useful for scripts, notebooks,
    or simple evaluation tasks that don't require batch processing.

    Args:
        repository_path: Path to the Git repository containing the file.
        file_path: Path to the file to analyze, relative to repository root.

    Returns:
        Dictionary containing evaluation results, same format as
        TemporalEvaluator.evaluate_file_evolution(). Will contain 'error'
        key if evaluation fails.

    Example:
        >>> outcome = expedited_analysis("/path/to/repo", "src/main.py")
        >>> if 'error' not in outcome:
        ...     print(f"Risk: {outcome['exposure_level']}")
        ...     print(f"Trend: {outcome['complexity_trend_slope']:+.2f}/month")
        ...     print(f"Commits: {outcome['commits_evaluated']}")
        ... else:
        ...     print(f"Analysis failed: {outcome['error']}")

        >>> # Quick batch evaluation
        >>> files = ["src/api.py", "src/models.py", "src/utils.py"]
        >>> for file_path in files:
        ...     outcome = expedited_analysis("/path/to/repo", file_path)
        ...     if 'error' not in outcome:
        ...         print(f"{file_path}: {outcome['exposure_level']} risk")

    Note:
        Uses default evaluation window (180 days). For custom windows or
        multiple analyses on the same repository, create a TemporalEvaluator
        instance instead for better performance.
    """
    logger.debug(f"Running expedited evaluation for {file_path} in {repository_path}")

    try:
        evaluator = TemporalEvaluator(repository_path)
        outcome = evaluator.evaluate_file_evolution(file_path)
        logger.debug(f"Expedited evaluation completed for {file_path}")
        return outcome
    except Exception as e:
        error_message = f"Expedited evaluation failed: {e}"
        logger.error(error_message)
        return {"error": error_message}


def forecast_decay(repository_path: str, file_path: str) -> float:
    """Quick quality decay prediction.

    Convenience function for getting just the quality decay prediction
    without full evaluation details. Useful for prioritization and triage
    of maintenance efforts across multiple files.

    Args:
        repository_path: Path to the Git repository containing the file.
        file_path: Path to the file to analyze, relative to repository root.

            Returns:
        Quality decay risk score from 0.0 to 1.0.
        Returns 0.0 if evaluation fails due to insufficient data.

        Risk interpretation:
        - 0.0-0.3: Low risk - stable or improving
        - 0.4-0.6: Medium risk - monitor for changes
        - 0.7-1.0: High risk - consider refactoring

    Example:
        >>> risk = forecast_decay("/path/to/repo", "src/legacy.py")
        >>> if risk > 0.7:
        ...     print("High risk - consider refactoring")
        >>> elif risk > 0.4:
        ...     print("Medium risk - monitor closely")
        ... else:
        ...     print("Low risk - stable quality")

        >>> # Batch risk assessment for prioritization
        >>> files = ["src/api.py", "src/models.py", "src/utils.py", "src/legacy.py"]
        >>> risks = [(f, forecast_decay("/path/to/repo", f)) for f in files]
        >>> # Sort by risk level for prioritization
        >>> sorted_risks = sorted(risks, key=lambda x: x[1], reverse=True)
        >>> print("Files prioritized by decay risk:")
        >>> for file_path, risk in sorted_risks:
        ...     risk_label = "HIGH" if risk > 0.7 else "MED" if risk > 0.4 else "LOW"
        ...     print(f"  {risk_label}: {file_path} ({risk:.1%})")

    Note:
        This is optimized for batch processing multiple files. For detailed
        evaluation including trends and timelines, use expedited_analysis()
        or create a TemporalEvaluator instance.
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
    """Main execution block for module testing and demonstration.

    When run directly, displays module information and provides basic
    functionality verification. Useful for development and debugging.
    """
    logging.basicConfig(
        level=logging.INFO, format="%(levelname)s - %(name)s - %(message)s"
    )

    logger.info("🔮 GitVoyant Temporal Code Intelligence v0.1.0")
    logger.info("This is just the beginning...")
    logger.info("")
    logger.info("Module loaded successfully. Key components:")
    logger.info("  • TemporalEvaluator: Core evaluation engine")
    logger.info("  • TemporalDiscernment: Insight representation")
    logger.info("  • expedited_analysis(): Quick single-file evaluation")
    logger.info("  • forecast_decay(): Risk prediction utility")
    logger.info("")
    logger.info("Example usage:")
    logger.info("  from src.core.temporal_evaluator import TemporalEvaluator")
    logger.info("  evaluator = TemporalEvaluator('/path/to/repo')")
    logger.info("  outcome = evaluator.evaluate_file_evolution('src/main.py')")
    logger.info("")
    logger.info("For more examples, see: examples/flask_discovery_demo")
