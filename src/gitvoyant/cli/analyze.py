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

Module: src/gitvoyant/cli/analyze.py

GitVoyant Analysis Commands Module

Provides CLI commands for performing various types of repository analysis,
including temporal evaluation of individual files and interactive agent
sessions for comprehensive repository assessment.

This module implements the 'analyze' subcommand group, offering specialized
analysis modes for different GitVoyant use cases.

Author: Jesse Moses (@Cre4T3Tiv3) <jesse@bytestacklabs.com>
Version: 0.3.0
License: Apache 2.0
"""

import asyncio
from pathlib import Path
from typing import Optional

import typer

from gitvoyant.cli.banner import print_banner
from gitvoyant.cli.cli_output_service import render_repo_evaluation
from gitvoyant.cli.utils import error, info, success
from gitvoyant.domain.services.temporal_evaluator_service import (
    TemporalEvaluatorService,
)

__version__ = "0.3.0"
__author__ = "Jesse Moses (@Cre4T3Tiv3) - jesse@bytestacklabs.com"

analyze_app = typer.Typer()
app = analyze_app


@analyze_app.command("temporal")
def analyze_temporal(
    repo_input: str = typer.Argument(..., help="Path or URL to the Git repo"),
    file_path: Optional[str] = typer.Argument(
        None, help="(Optional) Target file path inside repo"
    ),
    window_days: int = typer.Option(
        180,
        help="Days of commit history to analyze",
        rich_help_panel="Advanced Options",
    ),
    language: Optional[str] = typer.Option(
        None,
        help="Restrict analysis to a specific language (python, javascript, java, go). Default: auto-detect all.",
        rich_help_panel="Advanced Options",
    ),
):
    """Run temporal evaluation on a single file or entire repository.

    Performs deep temporal analysis on a specific file, examining its
    complexity evolution over time through commit history analysis.
    If no file path is provided, evaluates all Python files in the repository.

    Args:
        repo_input (str): Local filesystem path to a Git repository or
            remote Git URL (https/http). Remote repositories will be
            cloned to a temporary directory automatically.
        file_path (Optional[str]): Relative path to the target file within the
            repository for analysis. If omitted, evaluates the entire repo.
        window_days (int, optional): Number of days of commit history
            to include in the temporal analysis. Defaults to 180 days.
            Larger windows provide more stable trends but may include
            irrelevant historical data.

    Raises:
        typer.Exit: Exits with code 1 if analysis fails due to invalid
            repository, missing file, or processing errors.

    Example:
        $ gitvoyant analyze temporal ./my-repo src/main.py --window-days 90
        $ gitvoyant analyze temporal https://github.com/user/repo.git lib/utils.py
        $ gitvoyant analyze temporal ./my-repo
    """
    info("Initializing temporal analysis...")

    repo_path = Path(repo_input).resolve()

    if not repo_path.exists():
        error(f"Repository path does not exist: {repo_path}")
        raise typer.Exit(code=1)

    if not (repo_path / ".git").exists():
        error(f"Path is not a Git repository: {repo_path}")
        raise typer.Exit(code=1)

    try:
        if file_path:
            target_file = repo_path / file_path
            if not target_file.exists():
                error(f"Target file does not exist: {target_file}")
                raise typer.Exit(code=1)

        languages = [language] if language else None
        asyncio.run(
            _analyze_temporal_async(repo_input, file_path, window_days, languages)
        )
        success("Temporal evaluation complete.")

    except typer.Exit:
        raise
    except Exception as e:
        error(f"Analysis failed: {e}")
        raise typer.Exit(code=1)


async def _analyze_temporal_async(
    repo_input: str,
    file_path: Optional[str],
    window_days: int,
    languages: Optional[list[str]] = None,
):
    """Asynchronous implementation of temporal evaluation logic.

    Separated async logic to allow proper event loop handling from the
    synchronous CLI command entry point.

    Args:
        repo_input (str): Path or URL to the Git repository.
        file_path (Optional[str]): Target file path for analysis, or None.
        window_days (int): Analysis window in days.
        languages (Optional[list[str]]): Restrict to these languages.

    Raises:
        typer.Exit: Exits with code 1 if analysis encounters errors.
    """
    service = TemporalEvaluatorService(languages=languages)

    if file_path:
        result = await service.evaluate_file(file_path, repo_input)
    else:
        result = await service.evaluate_repository(repo_input)

    if "error" in result:
        error(str(result["error"]))
        raise typer.Exit(code=1)

    from gitvoyant.application.dto.evaluation_response import EvaluationResponse

    from gitvoyant.infrastructure.analyzers import get_analyzer

    def _detect_language(fpath: str) -> str:
        a = get_analyzer(fpath)
        return a.language_name if a else "unknown"

    if file_path:
        responses = [
            EvaluationResponse(
                file_path=str(result.get("file_path", file_path)),
                complexity_tenor_slope=float(result.get("complexity_trend_slope", 0.0)),
                quality_pattern="",
                confidence_rank=round(
                    float(result.get("quality_decay_forecast", 0.0)), 2
                ),
                commits_evaluated=int(result.get("commits_evaluated", 0)),
                risk_level=str(result.get("exposure_level", "UNKNOWN")),
                language=_detect_language(str(result.get("file_path", file_path))),
                description="Automated temporal complexity analysis result.",
                recommendations=[],
            )
        ]
        score = float(result.get("complexity_trend_slope", 0.0))
    else:
        responses = [
            EvaluationResponse(
                file_path=item.get("file_path", "unknown"),
                complexity_tenor_slope=float(item.get("complexity_trend_slope", 0.0)),
                quality_pattern="",
                confidence_rank=round(
                    float(item.get("quality_decay_forecast", 0.0)), 2
                ),
                commits_evaluated=int(item.get("commits_evaluated", 0)),
                risk_level=str(item.get("exposure_level", "UNKNOWN")),
                language=_detect_language(item.get("file_path", "")),
                description="Automated temporal complexity analysis result.",
                recommendations=[],
            )
            for item in result.get("evaluations", [])
        ]
        score = responses[0].complexity_tenor_slope if responses else 0.0

    render_repo_evaluation(
        repo_url=repo_input,
        score=score,
        responses=responses,
        executed_command="gitvoyant analyze temporal",
    )


@app.command("agent")
def launch_agent():
    """Launch the GitVoyant AI agent for interactive repository analysis.

    Starts an interactive session with the GitVoyant AI agent, powered by
    an AI model and equipped with specialized tools for repository analysis.
    The agent can perform temporal evaluations, assess code quality patterns,
    and provide insights through natural language conversation.

    The agent session runs in a continuous loop, allowing users to ask
    questions about repository quality, request specific analyses, and
    receive detailed recommendations based on GitVoyant's temporal
    evaluation algorithms.

    Commands within the agent session:
        - Ask about specific files: "How is the quality of src/main.py?"
        - Request repository overview: "Give me a health check of this repo"
        - Get recommendations: "What files need the most attention?"
        - Exit: Type 'exit' or 'q' to quit the session

    Example:
        $ gitvoyant analyze agent
        AI agent initialized. Ask anything about repo quality or code decay.
        Type 'exit' or 'q' to quit.

        > You: How is the quality trending in my main application file?
        > GitVoyant: I'll analyze that for you...
    """
    print_banner(executed_command="gitvoyant analyze agent")

    from gitvoyant.application.agent_runtime import create_gitvoyant_agent

    agent = create_gitvoyant_agent()

    typer.echo("\nAI agent initialized. Ask anything about repo quality or code decay.")
    typer.echo("Type 'exit' or 'q' to quit.\n")

    while True:
        user_input = typer.prompt("> You")
        if user_input.lower() in {"exit", "q"}:
            typer.echo("Goodbye.")
            break

        try:
            result = agent.invoke({"input": user_input})
            response = result.get("output", "[No response]")
            typer.echo(f"\n> GitVoyant: {response}\n")
        except Exception as e:
            typer.echo(f"Error: {e}")
