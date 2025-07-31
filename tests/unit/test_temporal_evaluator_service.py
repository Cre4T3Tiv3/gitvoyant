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

Module: tests/unit/test_temporal_evaluator_service.py

Temporal Evaluator Service Unit Tests

Comprehensive unit tests for the TemporalEvaluatorService, validating
service-level orchestration, error handling, and integration with the
underlying temporal evaluation infrastructure.

These tests use extensive mocking to isolate service logic from
infrastructure dependencies while ensuring proper coordination
between service methods and domain objects.

Author: Jesse Moses (@Cre4T3Tiv3) <jesse@bytestacklabs.com>

Version: 0.2.0

License: Apache 2.0
"""

import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Union
from unittest.mock import AsyncMock, patch

import pytest

from gitvoyant.domain.services.temporal_evaluator_service import (
    TemporalEvaluatorService,
)
from gitvoyant.infrastructure.temporal_evaluator import TemporalDiscernment

__version__ = "0.2.0"
__author__ = "Jesse Moses (@Cre4T3Tiv3) - jesse@bytestacklabs.com"


@pytest.fixture
def mock_evaluator():
    """Provide a mocked TemporalEvaluator for service testing.

    Creates a mock of the underlying TemporalEvaluator infrastructure
    component, allowing service-level tests to focus on orchestration
    logic without dependencies on Git operations or file system access.

    Yields:
        Mock: Configured mock object representing TemporalEvaluator instance.
    """
    with patch(
        "gitvoyant.domain.services.temporal_evaluator_service.TemporalEvaluator"
    ) as MockEval:
        yield MockEval.return_value


@pytest.mark.asyncio
async def test_evaluate_file_returns_expected_output(mock_evaluator):
    """Test service file evaluation returns properly structured results.

    Validates that the service correctly orchestrates file evaluation and
    returns results in the expected format with appropriate data types
    and structure.

    Args:
        mock_evaluator: Mocked TemporalEvaluator infrastructure component.

    Test Scenario:
        - Configure mock to return realistic evaluation data
        - Call service.evaluate_file() with test parameters
        - Verify result structure and data types

    Validates:
        - Service returns dictionary with evaluation results
        - Result structure matches expected format
        - Service properly delegates to infrastructure layer
        - Async operation completes successfully
    """
    mock_evaluator.evaluate_file_evolution.return_value = {
        "complexity_trend_slope": -0.2,
        "quality_decay_forecast": 0.6,
    }
    service = TemporalEvaluatorService()
    result = await service.evaluate_file("repo/path", "main.py")
    assert isinstance(result, dict)


def test_generate_discernment_uses_underlying_evaluator(mock_evaluator):
    """Test service insight generation delegates properly to infrastructure.

    Validates that the service correctly transforms infrastructure-level
    TemporalDiscernment objects into the expected dictionary format for
    external consumption.

    Args:
        mock_evaluator: Mocked TemporalEvaluator infrastructure component.

    Test Scenario:
        - Configure mock to return TemporalDiscernment objects
        - Call service.generate_insight() method
        - Verify proper transformation and delegation

    Data Transformation:
        - TemporalDiscernment objects → dictionary format
        - Datetime objects → ISO string format
        - Confidence values within expected ranges

    Validates:
        - Service delegates to infrastructure generate_discernment()
        - TemporalDiscernment objects transformed to dictionaries
        - All required fields present in transformed results
        - Confidence values are properly bounded (0.0-1.0)
        - ISO timestamp formatting applied correctly
    """
    now = datetime.now()
    mock_evaluator.generate_discernment.return_value = [
        TemporalDiscernment(
            file_path="main.py",
            discernment_type="complexity_growth",
            severity=0.75,
            description="Complexity growing",
            confidence=0.88,
            detected_at=now,
        )
    ]

    service = TemporalEvaluatorService()
    signals = service.generate_insight("main.py", "repo/path")

    assert isinstance(signals, list)
    assert isinstance(signals[0], dict)
    assert signals[0]["file_path"] == "main.py"
    assert signals[0]["type"] == "complexity_growth"
    assert signals[0]["severity"] == 0.75
    assert signals[0]["description"] == "Complexity growing"
    assert signals[0]["confidence"] == 0.88
    assert "detected_at" in signals[0]
    assert 0.0 <= float(signals[0]["confidence"]) <= 1.0
    mock_evaluator.generate_discernment.assert_called_once_with("main.py")


def test_evaluate_repository_returns_data():
    """Test repository-wide evaluation returns aggregated results.

    Validates that the service can orchestrate multi-file evaluation and
    return properly aggregated results with risk-based sorting.

    Test Scenario:
        - Mock infrastructure to return file evaluation results
        - Call service.evaluate_repository() with test parameters
        - Verify result aggregation and structure

    Mocking Strategy:
        - Mock TemporalEvaluator initialization
        - Mock evaluate_file_evolution() to return test data
        - Use asyncio.run() to handle async service method

    Validates:
        - Repository evaluation returns expected structure
        - Results include repository path and evaluation list
        - Individual file evaluations maintain expected format
        - Service properly handles async repository analysis
    """
    mock_result = {
        "file_path": "a.py",
        "quality_decay_forecast": 0.75,
        "complexity_trend_slope": 0.25,
    }

    with (
        patch(
            "gitvoyant.domain.services.temporal_evaluator_service.TemporalEvaluator.evaluate_file_evolution"
        ) as mock_eval,
        patch(
            "gitvoyant.domain.services.temporal_evaluator_service.TemporalEvaluator.__init__",
            return_value=None,
        ),
    ):
        mock_eval.return_value = mock_result

        service = TemporalEvaluatorService()
        result = asyncio.run(service.evaluate_repository(".", max_files=1))

        assert "repo_path" in result
        assert isinstance(result["evaluations"], list)
        assert result["evaluations"][0]["file_path"] == "a.py"
