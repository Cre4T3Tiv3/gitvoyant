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
