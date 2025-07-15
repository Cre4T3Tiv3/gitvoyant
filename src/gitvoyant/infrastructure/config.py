"""
Module: src/gitvoyant/infrastructure/config.py

Configuration module for GitVoyant platform.

Provides environment-based configuration management for the GitVoyant temporal
code intelligence platform. Supports AI model integration (Claude),
API server settings, temporal evaluation parameters, and agent configuration.

This module implements a simple, dependency-free configuration system that
loads settings from environment variables with sensible defaults, enabling
flexible deployment across different environments.

Author: Jesse Moses (@Cre4T3Tiv3) <jesse@bytestacklabs.com>

Version: 0.2.0

License: Apache 2.0
"""

import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

__version__ = "0.2.0"
__author__ = "Jesse Moses (@Cre4T3Tiv3) - jesse@bytestacklabs.com"

logger = logging.getLogger(__name__)

project_root = Path(__file__).parent.parent.parent.parent
env_file = project_root / ".env"

if env_file.exists():
    load_dotenv(env_file)
    logger.debug(f"Loaded configuration from {env_file}")
else:
    logger.debug(f"No .env file found at {env_file}")
    logger.warning("Tip: Copy .env.example to .env and configure your settings.")


class GitVoyantSettings:
    """Configuration class for GitVoyant runtime environment.

    Centralizes all configuration management for the GitVoyant platform,
    loading settings from environment variables with appropriate type
    conversion and default values. Provides validation and utility methods
    for configuration verification.

    The settings class organizes configuration into logical groups:
    - AI model configuration (Claude)
    - API server settings
    - Temporal evaluation parameters
    - Agent behavior configuration
    - Development and debugging options

    All settings can be overridden via environment variables, making the
    system deployable across different environments without code changes.
    """

    def __init__(self):
        """Initialize GitVoyant settings from environment variables.

        Loads all configuration values from environment variables with
        appropriate type conversion and fallback defaults. Missing optional
        settings use sensible defaults while required settings (like API keys)
        are loaded as None and validated separately.
        """
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

        self.claude_model = os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20241022")
        self.claude_temperature = float(os.getenv("CLAUDE_TEMPERATURE", "0.1"))
        self.claude_max_tokens = int(os.getenv("CLAUDE_MAX_TOKENS", "4000"))
        self.verbose_mode: bool = False
        self.default_window_days = int(
            os.getenv("GITVOYANT_DEFAULT_WINDOW_DAYS", "180")
        )
        self.log_level = os.getenv("GITVOYANT_LOG_LEVEL", "INFO")

        self.api_host = os.getenv("API_HOST", "0.0.0.0")
        self.api_port = int(os.getenv("API_PORT", "8000"))
        self.api_reload = os.getenv("API_RELOAD", "true").lower() == "true"

        self.min_commits_required = int(os.getenv("MIN_COMMITS_REQUIRED", "5"))
        self.max_files_per_analysis = int(os.getenv("MAX_FILES_PER_ANALYSIS", "50"))

        self.agent_verbose = os.getenv("AGENT_VERBOSE", "true").lower() == "true"
        self.agent_max_iterations = int(os.getenv("AGENT_MAX_ITERATIONS", "3"))

    def validate_api_keys(self) -> dict:
        """Check whether required AI API keys are present and configured.

        Validates the availability of API keys for supported AI services,
        providing feedback on which services are properly configured for use.

        Returns:
            dict: Dictionary containing validation results with keys:
                - claude (bool): True if Anthropic Claude API key is configured
                - any_configured (bool): True if at least one API key is available

        Example:
            >>> settings = GitVoyantSettings()
            >>> status = settings.validate_api_keys()
            >>> if not status['any_configured']:
            ...     print("No AI API keys configured!")
            >>> elif status['claude']:
            ...     print("Claude API is ready")
        """
        return {
            "claude": bool(self.anthropic_api_key),
            "any_configured": bool(self.anthropic_api_key),
        }

    def get_claude_config(self) -> dict:
        """Get Claude-related API configuration for model initialization.

        Assembles all Claude-specific configuration parameters into a
        dictionary suitable for passing to Claude API initialization.

        Returns:
            dict: Claude configuration containing:
                - api_key (str): Anthropic API key for authentication
                - model (str): Claude model identifier
                - temperature (float): Sampling temperature for responses
                - max_tokens (int): Maximum token limit for responses

        Example:
            >>> settings = GitVoyantSettings()
            >>> config = settings.get_claude_config()
            >>> claude_client = ChatAnthropic(**config)
        """
        return {
            "api_key": self.anthropic_api_key,
            "model": self.claude_model,
            "temperature": self.claude_temperature,
            "max_tokens": self.claude_max_tokens,
        }

    def get_temporal_config(self) -> dict:
        """Get temporal evaluation configuration parameters.

        Assembles configuration parameters specific to temporal evaluation
        including analysis windows, commit requirements, and processing limits.

        Returns:
            dict: Temporal evaluation configuration containing:
                - window_days (int): Default analysis window in days
                - min_commits (int): Minimum commits required for evaluation
                - max_files (int): Maximum files to process per analysis

        Example:
            >>> settings = GitVoyantSettings()
            >>> config = settings.get_temporal_config()
            >>> evaluator = TemporalEvaluator(window_days=config['window_days'])
        """
        return {
            "window_days": self.default_window_days,
            "min_commits": self.min_commits_required,
            "max_files": self.max_files_per_analysis,
        }


settings = GitVoyantSettings()


def get_settings() -> GitVoyantSettings:
    """Retrieve the global GitVoyant settings instance.

    Provides access to the singleton settings object configured at module
    import time. This function is the primary interface for accessing
    configuration throughout the application.

    Returns:
        GitVoyantSettings: The configured settings object containing all
            environment-based configuration values.

    Example:
        >>> from gitvoyant.core.config import get_settings
        >>> settings = get_settings()
        >>> print(f"Analysis window: {settings.default_window_days} days")
    """
    return settings


def check_configuration() -> None:
    """Display comprehensive configuration status for verification and debugging.

    Outputs a detailed report of the current GitVoyant configuration including
    API key status, core settings, model configuration, and server parameters.
    Useful for troubleshooting configuration issues and verifying deployment
    settings.

    This function provides clear feedback about missing API keys and suggests
    corrective actions for common configuration problems.

    Example:
        >>> from gitvoyant.core.config import check_configuration
        >>> check_configuration()
        GitVoyant Configuration Status
        ========================================
        API Keys:
          Claude (Anthropic): Configured
        ...
    """
    logger.info("GitVoyant Configuration Status")
    logger.info("=" * 40)

    api_status = settings.validate_api_keys()
    logger.info("API Keys:")
    logger.info(
        f"  Claude (Anthropic): {'Configured' if api_status['claude'] else 'Missing'}"
    )

    if not api_status["any_configured"]:
        logger.warning("No AI API keys configured.")
        logger.warning(
            "To proceed, add keys to the .env file or environment variables."
        )
        logger.warning("Get a Claude API key at: https://console.anthropic.com/")

    logger.info("\nCore Settings:")
    logger.info(f"  Evaluation Window: {settings.default_window_days} days")
    logger.info(f"  Log Level: {settings.log_level}")
    logger.info(f"  Minimum Commits Required: {settings.min_commits_required}")

    logger.info("\nClaude Configuration:")
    logger.info(f"  Model: {settings.claude_model}")
    logger.info(f"  Temperature: {settings.claude_temperature}")
    logger.info(f"  Max Tokens: {settings.claude_max_tokens}")

    logger.info("\nAPI Server:")
    logger.info(f"  Host: {settings.api_host}:{settings.api_port}")
    logger.info(f"  Reload Enabled: {settings.api_reload}")

    logger.info("\n" + "=" * 40)


if __name__ == "__main__":
    check_configuration()
