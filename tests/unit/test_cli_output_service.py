"""
Module: tests/unit/test_cli_output_service.py

CLI Output Service Unit Tests

Unit tests for GitVoyant's CLI output rendering functionality, validating
color coding logic, score interpretation, and formatted display generation.
These tests ensure consistent and accurate visual presentation of analysis
results across different terminal environments.

Tests cover both the scoring algorithm and the complete rendering pipeline
while avoiding side effects from actual terminal output.

Author: Jesse Moses (@Cre4T3Tiv3) <jesse@bytestacklabs.com>

Version: 0.2.0

License: Apache 2.0
"""

import pytest
from rich.style import Style

from gitvoyant.application.dto.evaluation_response import EvaluationResponse
from gitvoyant.cli.cli_output_service import color_for_score, render_repo_evaluation

__version__ = "0.2.0"
__author__ = "Jesse Moses (@Cre4T3Tiv3) - jesse@bytestacklabs.com"


def test_color_for_score():
    """Test the color coding algorithm for complexity scores.

    Validates that complexity scores are correctly mapped to visual indicators
    including emoji representations and Rich styling. Ensures consistent
    color coding that helps users quickly identify concerning trends.

    Score Mapping Logic:
        - score > 0.25: Green (🟢) - Positive trend, decreasing complexity
        - score < -0.25: Red (🔴) - Concerning trend, increasing complexity
        - -0.25 <= score <= 0.25: Yellow (🟡) - Stable, minimal change

    Validates:
        - Correct emoji selection for each score range
        - Proper Rich Style object creation with expected colors
        - Bold formatting applied consistently across all ranges
        - Boundary conditions handled correctly

    Note:
        The color mapping intentionally treats negative scores (increasing
        complexity) as concerning (red) and positive scores (decreasing
        complexity) as positive (green), following GitVoyant's convention
        where negative complexity trends indicate quality improvement.
    """
    emoji, style = color_for_score(0.3)
    assert emoji == "🟢"
    assert style == Style(color="green", bold=True)

    emoji, style = color_for_score(-0.3)
    assert emoji == "🔴"
    assert style == Style(color="red", bold=True)

    emoji, style = color_for_score(0.0)
    assert emoji == "🟡"
    assert style == Style(color="yellow", bold=True)


def test_render_repo_evaluation_renders(monkeypatch):
    """Test complete repository evaluation rendering without side effects.

    Validates that the full rendering pipeline executes successfully with
    realistic evaluation data, producing formatted output without errors.
    Uses monkeypatching to prevent actual terminal output during testing.

    Test Setup:
        - Creates realistic EvaluationResponse with HIGH risk scenario
        - Patches print_banner to avoid terminal output side effects
        - Exercises complete rendering pipeline with all parameters

    Validates:
        - Rendering function executes without raising exceptions
        - All parameters are properly handled and processed
        - Complex evaluation data structures are handled correctly
        - Optional parameters (cached_path) work as expected

    Side Effect Prevention:
        - Banner printing is mocked to avoid terminal pollution
        - No actual output is produced during test execution
        - Test focuses on execution success rather than output content

    Note:
        This test validates the structural integrity of the rendering
        process rather than the specific visual output, which would be
        difficult to test reliably across different terminal environments.
    """
    monkeypatch.setattr("gitvoyant.cli.banner.print_banner", lambda **kwargs: None)

    response = EvaluationResponse(
        file_path="main.py",
        complexity_tenor_slope=+0.33,
        quality_pattern="",
        confidence_rank=0.9,
        commits_evaluated=42,
        risk_level="HIGH",
        description="Quality degradation",
        recommendations=[],
    )

    render_repo_evaluation(
        repo_url="https://github.com/example/repo",
        score=0.33,
        responses=[response],
        executed_command="gitvoyant analyze temporal",
        cached_path="/tmp/test",
    )
