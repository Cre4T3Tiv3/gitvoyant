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

Module: src/gitvoyant/cli/utils.py

GitVoyant CLI Utilities Module

Provides common utility functions for CLI output formatting and user messaging
using Rich library for enhanced terminal presentation. Offers consistent
styling and color coding across the GitVoyant CLI application.

This module centralizes CLI output formatting to ensure consistent user
experience and visual hierarchy throughout the application.

Author: Jesse Moses (@Cre4T3Tiv3) <jesse@bytestacklabs.com>
Version: 0.2.0
License: Apache 2.0
"""

from rich.console import Console

__version__ = "0.2.0"
__author__ = "Jesse Moses (@Cre4T3Tiv3) - jesse@bytestacklabs.com"

_console = Console()


def info(msg: str):
    """Display an informational message with cyan styling.

    Used for general information, status updates, and non-critical
    notifications during CLI operations.

    Args:
        msg (str): The informational message to display to the user.

    Example:
        >>> info("Initializing temporal analysis...")
        # Displays in cyan with bold formatting
    """
    _console.print(f"[bold cyan]{msg}[/]")


def success(msg: str):
    """Display a success message with green styling.

    Used for confirming successful completion of operations, positive
    outcomes, and achievement notifications.

    Args:
        msg (str): The success message to display to the user.

    Example:
        >>> success("Temporal evaluation complete ✅")
        # Displays in green with bold formatting
    """
    _console.print(f"[bold green]{msg}[/]")


def warn(msg: str):
    """Display a warning message with yellow styling.

    Used for non-fatal issues, cautionary information, and situations
    that require user attention but don't prevent operation completion.

    Args:
        msg (str): The warning message to display to the user.

    Example:
        >>> warn("Repository cache is outdated")
        # Displays in yellow with bold formatting
    """
    _console.print(f"[bold yellow]{msg}[/]")


def error(msg: str):
    """Display an error message with red styling.

    Used for error conditions, failures, and critical issues that
    prevent successful operation completion.

    Args:
        msg (str): The error message to display to the user.

    Example:
        >>> error("Failed to access repository")
        # Displays in red with bold formatting
    """
    _console.print(f"[bold red]{msg}[/]")
