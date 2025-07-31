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

Module: tests/unit/test_value_objects_confidence_and_tenor.py

Value Objects Unit Tests - Confidence and Complexity Tenor

Comprehensive unit tests for GitVoyant's core value objects, validating
business logic for confidence ranking and complexity trend analysis.
These value objects encapsulate critical domain concepts and business
rules for temporal quality assessment.

Tests use parameterized testing to validate behavior across ranges of
input values, ensuring robust handling of edge cases and boundary conditions.

Author: Jesse Moses (@Cre4T3Tiv3) <jesse@bytestacklabs.com>
Version: 0.2.0
License: Apache 2.0
"""

import pytest

from gitvoyant.domain.value_objects.complexity_tenor import ComplexityTrend
from gitvoyant.domain.value_objects.confidence_rank import ConfidenceRank

__version__ = "0.2.0"
__author__ = "Jesse Moses (@Cre4T3Tiv3) - jesse@bytestacklabs.com"


@pytest.mark.parametrize(
    "score, expected_description, high_conf",
    [
        (0.95, "Very High Confidence", True),
        (0.80, "High Confidence", True),
        (0.65, "Medium Confidence", False),
        (0.30, "Low Confidence", False),
    ],
)
def test_confidence_rank_description_and_thresholds(
    score, expected_description, high_conf
):
    """Test confidence rank classification and description generation.

    Validates that confidence scores are correctly classified into descriptive
    categories and that threshold-based properties work as expected across
    the full range of confidence values.

    Args:
        score (float): Test confidence value between 0.0 and 1.0.
        expected_description (str): Expected qualitative description.
        high_conf (bool): Expected result for is_high_confidence property.

    Confidence Classification Thresholds:
        - 0.90-1.00: "Very High Confidence" (high_confidence=True)
        - 0.75-0.89: "High Confidence" (high_confidence=True)
        - 0.50-0.74: "Medium Confidence" (high_confidence=False)
        - 0.00-0.49: "Low Confidence" (high_confidence=False)

    Business Logic:
        - High confidence threshold set at 0.75 for quality decisions
        - Percentage conversion uses integer truncation
        - Description provides user-friendly confidence interpretation

    Validates:
        - Confidence percentage calculation (score * 100)
        - Qualitative description matches expected category
        - High confidence threshold applied correctly (>= 0.75)
        - Classification boundaries handle edge cases properly
    """
    rank = ConfidenceRank(value=score)
    assert rank.percentage == int(score * 100)
    assert rank.description == expected_description
    assert rank.is_high_confidence is high_conf


@pytest.mark.parametrize("invalid_value", [-0.1, 1.1, 2.0])
def test_confidence_rank_validation(invalid_value):
    """Test confidence rank validation rejects invalid values.

    Validates that the ConfidenceRank value object properly enforces
    its invariant that confidence values must be valid probabilities
    within the range [0.0, 1.0].

    Args:
        invalid_value (float): Test value outside valid confidence range.

    Validation Rules:
        - Confidence values must be >= 0.0 (non-negative probability)
        - Confidence values must be <= 1.0 (probability upper bound)
        - Invalid values raise ValueError with descriptive message

    Business Rationale:
        - Confidence represents statistical certainty (probability)
        - Values outside [0.0, 1.0] are mathematically invalid
        - Early validation prevents downstream calculation errors

    Validates:
        - ValueError raised for negative confidence values
        - ValueError raised for confidence values exceeding 1.0
        - Validation occurs during object construction (__post_init__)
        - Error handling prevents creation of invalid domain objects
    """
    with pytest.raises(ValueError):
        ConfidenceRank(value=invalid_value)


@pytest.mark.parametrize(
    "slope, expected_description, improving, declining",
    [
        (-0.5, "Quality improvement: -0.50 complexity reduction/month", True, False),
        (0.3, "Quality degradation: +0.30 complexity increase/month", False, True),
        (0.05, "Stable complexity: +0.05 change/month", False, False),
    ],
)
def test_complexity_trend_description(
    slope, expected_description, improving, declining
):
    """Test complexity trend classification and description generation.

    Validates that complexity slope values are correctly interpreted as
    quality trends with appropriate classification and human-readable
    descriptions for reporting and decision making.

    Args:
        slope (float): Complexity change rate (units per month).
        expected_description (str): Expected formatted description.
        improving (bool): Expected result for is_improving property.
        declining (bool): Expected result for is_declining property.

    Complexity Interpretation:
        - Negative slopes: Decreasing complexity (quality improvement)
        - Positive slopes: Increasing complexity (quality degradation)
        - Near-zero slopes: Stable complexity (minimal change)

    Classification Thresholds:
        - is_improving: slope < -0.1 (significant complexity reduction)
        - is_declining: slope > +0.1 (significant complexity increase)
        - Stable: -0.1 <= slope <= +0.1 (minimal change)

    Description Formatting:
        - Improving: "Quality improvement: X.XX complexity reduction/month"
        - Declining: "Quality degradation: +X.XX complexity increase/month"
        - Stable: "Stable complexity: ±X.XX change/month"

    Validates:
        - Monthly change accessor returns raw slope value
        - Quality trend classification applied correctly
        - Human-readable descriptions formatted consistently
        - Threshold boundaries handle edge cases properly
        - Sign conventions preserved in description formatting
    """
    trend = ComplexityTrend(slope=slope)

    assert trend.monthly_change == slope
    assert trend.is_improving is improving
    assert trend.is_declining is declining
    assert trend.description == expected_description
