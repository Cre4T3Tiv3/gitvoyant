"""
Module: src/gitvoyant/cli/cli_output_service.py

GitVoyant CLI Output Rendering Service

Provides rich, formatted output rendering for GitVoyant CLI analysis results,
including styled tables, color-coded metrics, and responsive layout management
for various terminal environments.

This module handles the presentation layer for analysis results, ensuring
consistent and visually appealing output across different CLI contexts.

Author: Jesse Moses (@Cre4T3Tiv3) <jesse@bytestacklabs.com>

Version: 0.2.0

License: Apache 2.0
"""

import shutil
from typing import List

from rich import box
from rich.console import Console
from rich.style import Style
from rich.table import Table

from gitvoyant.application.dto.evaluation_response import EvaluationResponse

__version__ = "0.2.0"
__author__ = "Jesse Moses (@Cre4T3Tiv3) - jesse@bytestacklabs.com"

console = Console()


def color_for_score(score: float) -> tuple[str, Style]:
    """Determine appropriate color coding and emoji for complexity scores.

    Maps numerical complexity scores to visual indicators, providing intuitive
    color coding and emoji representations for quick assessment of code quality
    trends.

    Args:
        score (float): Complexity tenor slope value. Positive values indicate
            decreasing complexity (improving quality), negative values indicate
            increasing complexity (declining quality), values near zero indicate
            stable complexity.

    Returns:
        tuple[str, Style]: A tuple containing:
            - str: Emoji indicator (🟢 for decreasing complexity, 🟡 for stable, 🔴 for increasing)
            - Style: Rich style object with appropriate color and formatting

    Note:
        Score interpretation:
        - score > 0.25: Positive complexity decrease (green 🟢)
        - score < -0.25: Concerning complexity increase (red 🔴)
        - -0.25 <= score <= 0.25: Stable complexity (yellow 🟡)
    """
    if score > 0.25:
        return "🟢", Style(color="green", bold=True)
    elif score < -0.25:
        return "🔴", Style(color="red", bold=True)
    else:
        return "🟡", Style(color="yellow", bold=True)


def render_repo_evaluation(
    repo_url: str,
    score: float,
    responses: List[EvaluationResponse],
    executed_command: str,
    cached_path: str = None,
):
    """Render comprehensive repository evaluation results with rich formatting.

    Creates a complete, formatted display of repository analysis results including
    header banner, summary metrics, and detailed file-level evaluations in a
    structured table format.

    Args:
        repo_url (str): URL or path of the analyzed repository for display
            in the header section.
        score (float): Overall repository health score, typically representing
            aggregate complexity trends across evaluated files.
        responses (List[EvaluationResponse]): List of individual file evaluation
            results, displayed in order of risk priority (highest risk first).
        executed_command (str): The CLI command that generated these results,
            shown in the banner for context and reproducibility.
        cached_path (str, optional): Local path to cached repository if applicable.
            When provided, displays cache usage information to the user.

    Note:
        The output automatically adapts to terminal width and displays up to
        the top 5 highest-risk files for focused attention. The layout includes:
        - Application banner with command context
        - Repository summary information
        - Color-coded risk table with temporal scores
        - Responsive formatting for various terminal sizes

    Example:
        >>> responses = [EvaluationResponse(...), ...]
        >>> render_repo_evaluation(
        ...     repo_url="https://github.com/user/repo.git",
        ...     score=-0.15,
        ...     responses=responses,
        ...     executed_command="gitvoyant analyze temporal"
        ... )
    """
    from gitvoyant.cli.banner import print_banner

    term_width = shutil.get_terminal_size((100, 20)).columns
    content_width = min(term_width - 4, 100)

    print_banner(executed_command=executed_command, width=content_width)

    if cached_path:
        console.print(f"[dim]✓ Using cached repo at {cached_path}[/dim]\n")

    info_table = Table.grid(padding=(0, 2))
    info_table.add_row("🔍", f"[bold]Repository:[/bold] {repo_url}")
    info_table.add_row("📊", f"[bold]Health Score:[/bold] {score:.2f}")
    info_table.add_row("📂", f"[bold]Evaluated Files:[/bold] {len(responses)}")
    console.print(info_table)
    console.print()

    table = Table(show_lines=True, box=box.SIMPLE_HEAVY, row_styles=["none", "dim"])
    table.add_column("File", style="cyan", no_wrap=True)
    table.add_column("[bold]Temporal Score[/bold]", justify="center", style="magenta")

    for r in responses[:5]:
        score = r.complexity_tenor_slope
        emoji, style = color_for_score(score)
        formatted_score = f"{score:+.2f}"
        color_name = style.color.name if style.color else "white"
        table.add_row(
            r.file_path,
            f"[bold {color_name}]{emoji} {formatted_score}[/bold {color_name}]",
        )

    console.print(table)
