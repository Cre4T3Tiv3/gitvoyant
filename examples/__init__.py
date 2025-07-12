"""
GitVoyant Examples Package

This package contains example scripts and demonstrations of GitVoyant's
temporal code intelligence capabilities.

Available Examples:
    flask_discovery_demo: Recreates the Flask quality engineering discovery
    fundamental_analysis: Basic temporal analysis example

Usage:
    # Run Flask discovery demo
    python examples/flask_discovery_demo.py
    
    # Or use make commands
    make demo

Author: Jesse Moses (@Cre4T3Tiv3) - ByteStack Labs
"""

__version__ = "0.1.0"
__author__ = "Jesse Moses (@Cre4T3Tiv3) - jesse@bytestacklabs.com"

from pathlib import Path

EXAMPLES_DIR = Path(__file__).parent