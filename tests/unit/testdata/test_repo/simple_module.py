"""
Module: tests/unit/testdata/test_repo/simple_module.py

Simple Test Module for Temporal Evaluation

Basic Python module containing minimal functionality for testing
GitVoyant's temporal evaluation capabilities. Provides a simple
function with linear execution flow and minimal complexity.

This module serves as test data for:
- Single-file temporal analysis
- Baseline complexity measurements
- Repository evaluation test scenarios

Author: Jesse Moses (@Cre4T3Tiv3) <jesse@bytestacklabs.com>

Version: 0.2.0

License: Apache 2.0
"""

__version__ = "0.2.0"
__author__ = "Jesse Moses (@Cre4T3Tiv3) - jesse@bytestacklabs.com"


def add(a, b):
    """Add two numbers and return the result.

    Simple addition function with minimal cyclomatic complexity (value of 1),
    representing the simplest possible code structure for temporal analysis
    baseline testing.

    Args:
        a: First number to add.
        b: Second number to add.

    Returns:
        The sum of a and b.
    """
    return a + b
