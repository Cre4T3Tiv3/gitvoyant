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

Module: src/gitvoyant/application/dto/evaluation_response.py
DTO: EvaluationResponse for API layer

This module defines the EvaluationResponse data transfer object used to
translate domain-level TemporalEvaluation entities into structured responses
for API consumers.

Preserves all key discernment from GitVoyant's temporal evaluation logic,
including quality pattern classification, complexity tenors, confidence levels,
and actionable recommendations.

Author: Jesse Moses (@Cre4T3Tiv3) <jesse@bytestacklabs.com>
Version: 0.2.0
License: Apache 2.0
"""

from dataclasses import dataclass
from typing import List

from ...domain.entities.temporal_evaluation import TemporalEvaluation

__version__ = "0.2.0"
__author__ = "Jesse Moses (@Cre4T3Tiv3) - jesse@bytestacklabs.com"


@dataclass
class EvaluationResponse:
    """Represents a structured evaluation result for a single file.

    This data transfer object encapsulates all temporal evaluation metrics
    and recommendations for a specific file, providing a clean API interface
    for consumers of GitVoyant's evaluation services.

    Attributes:
        file_path (str): Relative or absolute path to the evaluated file within
            the repository.
        complexity_tenor_slope (float): Rate of complexity change over time,
            measured in complexity units per month. Positive values indicate
            increasing complexity (declining quality), negative values indicate
            decreasing complexity (improving quality).
        quality_pattern (str): Classification of the overall quality trend.
            Valid values are "IMPROVING", "STABLE", or "DECLINING".
        confidence_rank (float): Statistical confidence level in the tenor
            evaluation, ranging from 0.0 to 1.0.
        commits_evaluated (int): Total number of commits analyzed in the
            evaluation window for this file.
        risk_level (str): Categorical risk assessment based on complexity trends.
            Valid values are "LOW", "MEDIUM", or "HIGH".
        description (str): Human-readable summary describing the complexity
            tenor and trend analysis.
        recommendations (List[str]): List of actionable engineering recommendations
            based on the detected quality patterns and risk levels.
    """

    file_path: str
    complexity_tenor_slope: float
    quality_pattern: str
    confidence_rank: float
    commits_evaluated: int
    risk_level: str
    description: str
    recommendations: List[str]

    @classmethod
    def from_domain(cls, evaluation: TemporalEvaluation) -> "EvaluationResponse":
        """Constructs an EvaluationResponse from a domain TemporalEvaluation.

        Transforms a domain model instance into a structured response suitable
        for API consumption, including automatic recommendation generation based
        on the evaluation results.

        Args:
            evaluation (TemporalEvaluation): The domain model instance containing
                raw evaluation data and metrics.

        Returns:
            EvaluationResponse: A fully populated response object with all
                necessary fields extracted from the domain model and generated
                recommendations.

        Example:
            >>> domain_eval = TemporalEvaluation(...)
            >>> response = EvaluationResponse.from_domain(domain_eval)
            >>> print(response.quality_pattern)
            "IMPROVING"
        """
        return cls(
            file_path=evaluation.file_path,
            complexity_tenor_slope=evaluation.complexity_tenor.slope,
            quality_pattern=evaluation.quality_pattern,
            confidence_rank=evaluation.confidence_rank.value,
            commits_evaluated=evaluation.commits_evaluated,
            risk_level=evaluation.risk_level,
            description=evaluation.complexity_tenor.description,
            recommendations=cls._generate_recommendations(evaluation),
        )

    @staticmethod
    def _generate_recommendations(evaluation: TemporalEvaluation) -> List[str]:
        """Generates actionable recommendations based on detected quality patterns.

        Analyzes the temporal evaluation results to produce specific, actionable
        engineering recommendations tailored to the observed complexity trends
        and quality patterns.

        Args:
            evaluation (TemporalEvaluation): The evaluation result containing
                quality patterns, complexity trends, and confidence metrics.

        Returns:
            List[str]: A list of specific engineering actions or observations,
                such as refactoring suggestions, pattern adoption recommendations,
                or monitoring advice.

        Note:
            Recommendations are generated based on three primary quality patterns:
            - IMPROVING: Suggests pattern replication and continued monitoring
            - DECLINING: Recommends refactoring and architectural review
            - STABLE: Advises ongoing monitoring with no immediate action
        """
        recommendations = []

        if evaluation.quality_pattern == "IMPROVING":
            recommendations.append("Quality improvement pattern detected.")
            recommendations.append(
                f"Complexity is reducing at {abs(evaluation.complexity_tenor.slope):.2f} units/month."
            )
            recommendations.append(
                "Consider applying this pattern across other modules."
            )
        elif evaluation.quality_pattern == "DECLINING":
            recommendations.append("Quality degradation pattern detected.")
            recommendations.append(
                f"Complexity is increasing at {evaluation.complexity_tenor.slope:.2f} units/month."
            )
            recommendations.append(
                "Refactoring or architectural review may be warranted."
            )
        else:
            recommendations.append("Complexity tenor is stable.")
            recommendations.append(
                "No immediate action required; monitor for future changes."
            )

        return recommendations
