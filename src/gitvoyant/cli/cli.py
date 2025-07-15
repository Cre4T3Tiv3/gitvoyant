"""
Module: src/gitvoyant/cli/cli.py

GitVoyant CLI Main Entry Point

Primary command-line interface module that orchestrates GitVoyant's CLI
functionality, including repository analysis commands and shell completion
setup.

This module serves as the entry point for the GitVoyant CLI application,
providing a hierarchical command structure with subcommands for different
analysis modes and utility functions.

Author: Jesse Moses (@Cre4T3Tiv3) <jesse@bytestacklabs.com>

Version: 0.2.0

License: Apache 2.0
"""

from pathlib import Path

import typer

from gitvoyant.cli.analyze import analyze_app
from gitvoyant.cli.banner import print_banner

__version__ = "0.2.0"
__author__ = "Jesse Moses (@Cre4T3Tiv3) - jesse@bytestacklabs.com"

app = typer.Typer(help="🧠 GitVoyant - Temporal Intelligence for Repositories")
app.add_typer(analyze_app, name="analyze", help="Perform repository analysis tasks")

analyze_app = typer.Typer()


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    GitVoyant CLI Entry Callback

    Automatically prints banner for top-level commands only.
    """
    if ctx.invoked_subcommand is None:
        print_banner()
        typer.echo(ctx.get_help())
        raise typer.Exit()


@app.command("install-completion")
def install_completion():
    """Print instructions to enable shell auto-completion.

    Provides shell-specific instructions for enabling auto-completion
    support across different shell environments including bash, zsh,
    fish, and PowerShell.

    The function detects the current shell environment and provides
    tailored instructions for both temporary and permanent auto-completion
    setup.

    Example:
        $ gitvoyant install-completion
        Detected shell: zsh
        Run the following command to enable auto-completion temporarily:

            eval "$(gitvoyant --show-completion zsh)"
    """
    import os
    import sys

    shell = os.environ.get("SHELL", "unknown").split("/")[-1]

    typer.echo(f"Detected shell: {shell}")
    typer.echo("Run the following command to enable auto-completion temporarily:\n")
    typer.echo(f'    eval "$({Path(sys.argv[0]).name} --show-completion {shell})"')
    typer.echo("\nTo make it permanent, add the above line to your shell config file:")
    typer.echo("    ~/.bashrc, ~/.zshrc, ~/.config/fish/config.fish, etc.\n")


@app.command("version")
def version():
    """Show GitVoyant version and banner."""
    print_banner()
    typer.echo(f"Version: {__version__}")


def get_app():
    return app


if __name__ == "__main__":
    app()
