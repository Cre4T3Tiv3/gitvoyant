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

Module: src/gitvoyant/presentation/agents/langchain_bindings.py

GitVoyant LangChain Tool Integration

Provides LangChain-compatible tools for GitVoyant's temporal code intelligence
capabilities, enabling AI agents to perform repository analysis and file-level
quality assessment through natural language interactions.

This module bridges GitVoyant's core temporal evaluation infrastructure with
LangChain's agent framework, creating specialized tools that can be invoked
by AI agents to analyze code quality trends, complexity evolution, and decay
risk patterns in Git repositories.

The tools are designed for conversational AI agents, providing formatted
output suitable for natural language responses while maintaining access to
the full analytical power of GitVoyant's temporal evaluation algorithms.

Key Features:
    - Temporal analysis tool for individual file assessment
    - Repository evaluation tool for holistic quality overview
    - Output suppression for clean agent interactions
    - Error handling with user-friendly messages
    - Formatted results optimized for conversational display

Author: Jesse Moses (@Cre4T3Tiv3) <jesse@bytestacklabs.com>
Version: 0.2.0
License: Apache 2.0
"""

import contextlib
import os
import sys

from langchain_core.tools import Tool

from gitvoyant.infrastructure.temporal_evaluator import (
    TemporalEvaluator,
    expedited_analysis,
)

__version__ = "0.2.0"
__author__ = "Jesse Moses (@Cre4T3Tiv3) - jesse@bytestacklabs.com"


@contextlib.contextmanager
def suppress_stdout():
    """Context manager to suppress stdout output during tool execution.

    Prevents verbose logging and debug output from GitVoyant's infrastructure
    components from cluttering the agent's conversational interface. Ensures
    that only the formatted tool results are returned to the agent for
    presentation to users.

    This is particularly important for agent interactions where clean,
    formatted responses are essential for maintaining conversational flow
    and user experience quality.

    Yields:
        None: Context manager yields control back to caller while stdout
            is redirected to devnull, effectively suppressing all print
            statements and logging output.

    Example:
        >>> with suppress_stdout():
        ...     # Any print statements or logging here will be suppressed
        ...     result = some_noisy_function()
        >>> # Normal stdout behavior resumes here

    Note:
        The suppression only affects stdout, not stderr. Critical errors
        and exceptions will still be visible for debugging purposes.
        The original stdout is always restored, even if exceptions occur
        during the suppressed operation.
    """
    with open(os.devnull, "w") as fnull:
        old_stdout = sys.stdout
        try:
            sys.stdout = fnull
            yield
        finally:
            sys.stdout = old_stdout


def make_temporal_analysis_tool() -> Tool:
    """Create a LangChain tool for temporal analysis of individual files.

    Constructs a LangChain Tool that enables AI agents to perform detailed
    temporal analysis on specific Python files within Git repositories.
    The tool analyzes complexity trends, quality patterns, and decay risk
    to provide actionable insights about code evolution.

    Returns:
        Tool: LangChain Tool configured for temporal file analysis with:
            - Name: "temporal_analysis_tool"
            - Description optimized for agent understanding
            - Function wrapper providing formatted output
            - Error handling for graceful failure scenarios

    Tool Capabilities:
        - Analyzes complexity evolution over configurable time windows
        - Computes quality decay risk predictions
        - Identifies trend patterns (improving/declining/stable)
        - Provides commit-level analysis depth
        - Handles various error conditions gracefully

    Agent Integration:
        The tool is designed for natural language agent interactions,
        providing formatted output that can be directly presented to
        users or further processed by the agent for conversational
        responses.

    Example Agent Usage:
        Agent: "I'll analyze the temporal patterns in your main.py file"
        Tool Call: temporal_analysis_tool(file_path="src/main.py", repo_path=".")
        Result: "📊 File: src/main.py\nTrend: -0.15/month\nExposure: LOW | Risk: 0.23"

    Note:
        The tool suppresses verbose output from the underlying infrastructure
        to maintain clean agent interactions while preserving full analytical
        capabilities and error reporting.
    """

    def analyze(file_path: str, repo_path: str = ".", window_days: int = 180) -> str:
        """Perform temporal analysis on a specific file within a repository.

        Analyzes the temporal evolution of a Python file by examining its
        commit history, complexity trends, and quality patterns over the
        specified time window. Provides formatted results suitable for
        agent presentation and user consumption.

        Args:
            file_path (str): Path to the target Python file for analysis.
                Can be absolute or relative to the repository root. The file
                must exist in the current repository state and have sufficient
                commit history for meaningful temporal analysis.
            repo_path (str, optional): Path to the Git repository root directory.
                Defaults to "." (current directory). Must be a valid Git
                repository with accessible commit history.
            window_days (int, optional): Number of days of commit history to
                analyze for temporal patterns. Defaults to 180 days. Larger
                windows provide more stable trends but may include less
                relevant historical data.

        Returns:
            str: Formatted analysis results containing:
                - File path and identification
                - Complexity trend slope (units per month)
                - Risk exposure level (LOW/MEDIUM/HIGH)
                - Quality decay forecast (0.0-1.0 probability)
                - Number of commits analyzed
                - Error message if analysis fails

        Output Format:
            Success: "📊 File: {path}\nTrend: {slope}/month\nExposure: {level} | Risk: {forecast}\nCommits evaluated: {count}"
            Error: "❌ {error_description}"

        Example:
            >>> tool_func = make_temporal_analysis_tool().func
            >>> result = tool_func("src/main.py", "./my-repo", 90)
            >>> print(result)
            📊 File: src/main.py
            Trend: -0.15/month
            Exposure: LOW | Risk: 0.23
            Commits evaluated: 12
        """
        with suppress_stdout():
            result = expedited_analysis(repo_path, file_path, window_days)
        if "error" in result:
            return f"❌ {result['error']}"
        return (
            f"📊 File: {result['file_path']}\n"
            f"Trend: {result['complexity_trend_slope']:+.2f}/month\n"
            f"Exposure: {result['exposure_level']} | Risk: {result['quality_decay_forecast']:.2f}\n"
            f"Commits evaluated: {result['commits_evaluated']}"
        )

    return Tool.from_function(
        name="temporal_analysis_tool",
        description="Analyze decay risk and complexity trends in a Python file using Git history.",
        func=analyze,
    )


def make_repo_evaluation_tool() -> Tool:
    """Create a LangChain tool for comprehensive repository evaluation.

    Constructs a LangChain Tool that enables AI agents to perform holistic
    quality assessment across all Python files in a Git repository. The tool
    analyzes multiple files simultaneously and ranks them by decay risk to
    identify the most concerning areas requiring attention.

    Returns:
        Tool: LangChain Tool configured for repository-wide analysis with:
            - Name: "repo_temporal_intelligence"
            - Description optimized for agent understanding
            - Function wrapper providing risk-ranked file listing
            - Automatic file discovery and filtering
            - Error handling for various repository conditions

    Tool Capabilities:
        - Discovers all Python files in repository automatically
        - Filters out non-source directories (.venv, __pycache__, etc.)
        - Analyzes temporal patterns for each discoverable file
        - Ranks files by quality decay risk (highest first)
        - Provides configurable analysis limits for performance

    Agent Integration:
        The tool provides a comprehensive repository overview that agents
        can use to identify priority areas for development attention,
        answer questions about overall repository health, and guide
        refactoring or quality improvement efforts.

    Example Agent Usage:
        Agent: "Let me evaluate the overall quality trends in this repository"
        Tool Call: repo_temporal_intelligence(repo_path=".", max_files=15)
        Result: "📦 Repository decay risks:\nsrc/api.py: 0.85\nutils/helper.py: 0.72\n..."

    Note:
        The tool automatically handles file discovery, path resolution,
        and error recovery to provide robust repository analysis even
        in complex project structures or repositories with mixed file types.
    """

    def evaluate_repo(repo_path: str, max_files: int = 20) -> str:
        """Perform comprehensive temporal evaluation across repository files.

        Analyzes all discoverable Python files within a Git repository to
        identify quality trends, complexity patterns, and decay risks across
        the entire codebase. Results are ranked by risk level to prioritize
        attention on the most concerning files.

        Args:
            repo_path (str): Path to the Git repository root directory.
                Must be a valid Git repository with accessible commit history
                and contain Python source files for analysis.
            max_files (int, optional): Maximum number of files to analyze
                to prevent excessive processing time on large repositories.
                Defaults to 20. Files are processed in discovery order
                until the limit is reached.

        Returns:
            str: Formatted repository analysis results containing:
                - Repository identification header
                - Risk-ranked list of files with decay probabilities
                - File paths relative to repository root
                - Decay risk scores (0.0-1.0 probability scale)
                - Message if no analyzable files found

        File Discovery:
            - Recursively searches repository for .py files
            - Excludes common non-source directories:
              * .venv (virtual environments)
              * site-packages (installed packages)
              * __pycache__ (Python bytecode cache)
            - Validates file existence and accessibility
            - Handles permission and access errors gracefully

        Risk Ranking:
            Files are sorted by quality decay forecast in descending order,
            placing the highest-risk files at the top of the results for
            immediate attention and prioritization.

        Output Format:
            Success: "📦 Repository decay risks:\n{file1}: {risk1}\n{file2}: {risk2}\n..."
            No Files: "No analyzable Python files found."

        Example:
            >>> tool_func = make_repo_evaluation_tool().func
            >>> result = tool_func("./my-project", 10)
            >>> print(result)
            📦 Repository decay risks:
            src/api/handlers.py: 0.85
            utils/data_processing.py: 0.72
            core/business_logic.py: 0.68
            tests/integration_tests.py: 0.45

        Performance Considerations:
            - File analysis is performed sequentially for stability
            - Max files limit prevents excessive processing time
            - Error recovery allows partial results on problematic files
            - Output suppression maintains agent interaction performance
        """
        with suppress_stdout():
            evaluator = TemporalEvaluator(repo_path)
            results = []

            for root, _, files in os.walk(repo_path):
                if any(
                    ignored in root
                    for ignored in [".venv", "site-packages", "__pycache__"]
                ):
                    continue

                for file in files:
                    if file.endswith(".py") and len(results) < max_files:
                        full_path = os.path.join(root, file)
                        rel_path = os.path.relpath(full_path, repo_path)
                        if not os.path.exists(os.path.join(repo_path, rel_path)):
                            continue
                        try:
                            outcome = evaluator.evaluate_file_evolution(rel_path)
                            if "error" not in outcome:
                                results.append(
                                    (rel_path, outcome["quality_decay_forecast"])
                                )
                        except Exception:
                            continue

        if not results:
            return "No analyzable Python files found."

        results.sort(key=lambda x: x[1], reverse=True)
        report = "\n".join([f"{path}: {risk:.2f}" for path, risk in results])
        return f"📦 Repository decay risks:\n{report}"

    return Tool.from_function(
        name="repo_temporal_intelligence",
        description="Analyzes all Python files in a Git repo and ranks by decay risk.",
        func=evaluate_repo,
    )
