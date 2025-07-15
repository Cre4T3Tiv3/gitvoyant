"""
Module: tests/unit/testdata/test_repo/nested/utils.py

Test Utility Module for Repository Testing

Simple utility module used in GitVoyant's test scenarios to provide
realistic Python code for temporal evaluation testing. Contains
basic mathematical operations with minimal complexity.

This module serves as test data for:
- Multi-file repository analysis
- Nested directory structure handling
- Basic complexity calculation validation

Author: Jesse Moses (@Cre4T3Tiv3) <jesse@bytestacklabs.com>

Version: 0.2.0

License: Apache 2.0
"""

__version__ = "0.2.0"
__author__ = "Jesse Moses (@Cre4T3Tiv3) - jesse@bytestacklabs.com"


def multiply(x, y):
    """Multiply two numbers and return the result.

    Simple multiplication function with minimal cyclomatic complexity,
    suitable for testing baseline complexity calculations and temporal
    trend analysis in controlled test scenarios.

    Args:
        x: First number to multiply.
        y: Second number to multiply.

    Returns:
        The product of x and y.
    """
    return x * y
