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

Module: src/gitvoyant/cli/banner.py

GitVoyant CLI Banner Display Module

Provides branded banner display functionality for the GitVoyant CLI application,
creating visually appealing startup messages with version information and
branding elements.

This module handles terminal width detection, responsive layout, and consistent
branding across different CLI contexts.

Author: Jesse Moses (@Cre4T3Tiv3) <jesse@bytestacklabs.com>
Version: 0.2.0
License: Apache 2.0
"""

from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

__version__ = "0.2.0"
__author__ = "Jesse Moses (@Cre4T3Tiv3) - jesse@bytestacklabs.com"


def print_banner(executed_command: Optional[str] = None, width: Optional[int] = None):
    """Display the GitVoyant application banner with branding and version info.

    Creates a rich, formatted banner display using the Rich library for enhanced
    CLI presentation. The banner includes application name, version, description,
    and optional command context information.

    Args:
        executed_command (Optional[str]): The CLI command that was executed,
            displayed below the banner for context. If None, no command
            information is shown.
        width (Optional[int]): Override for banner width. If None, automatically
            calculated based on terminal dimensions with sensible defaults
            and maximum constraints.

    Note:
        The banner automatically adapts to terminal width while maintaining
        readability and visual appeal. Minimum and maximum width constraints
        ensure consistent appearance across different terminal environments.

    Example:
        >>> print_banner()  # Basic banner display
        >>> print_banner("gitvoyant analyze temporal")  # With command context
        >>> print_banner(width=80)  # With custom width
    """
    console = Console(width=width)
    terminal_width = console.size.width

    banner = Text(justify="center")
    banner.append("🔮 GitVoyant", style="bold cyan")
    banner.append("  v0.2.0\n", style="magenta")
    banner.append("AI Agent Platform for Temporal Code Intelligence\n", style="white")

    panel = Panel(
        banner,
        border_style="cyan",
        title="[bold blue]Welcome to GitVoyant",
        subtitle="[dim italic]by ByteStack Labs",
        padding=(1, 4),
        expand=True,
        width=terminal_width,
    )

    console.print("\n")
    console.print(panel, justify="left")
    if executed_command:
        console.print(f"\n[dim italic]$ {executed_command}[/dim italic]\n")
    else:
        console.print("")
