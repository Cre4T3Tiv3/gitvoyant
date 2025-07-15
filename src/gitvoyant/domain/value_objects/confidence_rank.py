"""
Module: src/gitvoyant/domain/value_objects/confidence_rank.py

Confidence Rank Value Object for Evaluation Certainty

Defines the ConfidenceRank value object for interpreting evaluation certainty
in temporal quality analysis. This immutable object represents a normalized
confidence level (0.0 to 1.0) and provides derived representations useful
for thresholding, display, and classification in quality assessment workflows.

The ConfidenceRank value object encapsulates business rules for interpreting
statistical confidence in temporal evaluations, providing semantic meaning
to numerical confidence scores through threshold-based classification and
human-readable descriptions.

Key Features:
    - Immutable value object with built-in validation
    - Normalized confidence scale (0.0 to 1.0)
    - Business logic for confidence classification
    - Multiple representation formats (percentage, description)
    - Threshold-based decision support

Author: Jesse Moses (@Cre4T3Tiv3) <jesse@bytestacklabs.com>

Version: 0.2.0

License: Apache 2.0
"""

from dataclasses import dataclass

__version__ = "0.2.0"
__author__ = "Jesse Moses (@Cre4T3Tiv3) - jesse@bytestacklabs.com"


@dataclass(frozen=True)
class ConfidenceRank:
    """Represents the statistical confidence level of an evaluation result.

    This value object encapsulates confidence measurements from temporal
    analysis and provides domain-specific interpretation through properties
    that encode business rules for confidence assessment. The object enforces
    data integrity through validation and immutability.

    The ConfidenceRank serves as a bridge between statistical analysis and
    business decision-making, transforming numerical confidence scores into
    actionable guidance for quality assessment and risk management.

    Attributes:
        value (float): A normalized confidence level between 0.0 and 1.0,
            where 0.0 represents no confidence and 1.0 represents complete
            confidence in the evaluation results. Values are typically
            derived from statistical analysis of data quality and quantity.

    Design Principles:
        - Immutability: Frozen dataclass prevents accidental modification
        - Validation: Post-init validation ensures data integrity
        - Domain Semantics: Properties provide business-meaningful interpretations
        - Value Object: Identity based on value, not reference

    Raises:
        ValueError: If the confidence value is outside the valid range [0.0, 1.0]
            during object construction.
    """

    value: float

    def __post_init__(self):
        """Validates the confidence rank is within the accepted range.

        Enforces the business rule that confidence must be a valid probability
        value between 0.0 and 1.0 inclusive. This validation ensures data
        integrity and prevents invalid confidence values from propagating
        through the domain model.

        Raises:
            ValueError: If the confidence value is negative (< 0.0) or exceeds
                the maximum probability (> 1.0). The error message provides
                clear guidance on the expected range.

        Design Rationale:
            Confidence represents a probability, which by mathematical definition
            must be bounded between 0.0 and 1.0. Values outside this range are
            meaningless in statistical context and could lead to incorrect
            business decisions if allowed to propagate.

        Example:
            >>> valid_confidence = ConfidenceRank(0.85)  # Valid
            >>> invalid_confidence = ConfidenceRank(1.2)  # Raises ValueError
        """
        if not 0.0 <= self.value <= 1.0:
            raise ValueError("Confidence rank must be between 0.0 and 1.0")

    @property
    def percentage(self) -> int:
        """Returns the confidence rank as a whole number percentage.

        Converts the normalized confidence value to a percentage representation
        suitable for display in user interfaces, reports, and dashboards.
        Uses integer truncation to provide clean percentage values.

        Returns:
            int: The confidence as an integer from 0 to 100, representing
                the percentage confidence level. Values are truncated rather
                than rounded to avoid overstating confidence levels.

        Example:
            >>> confidence = ConfidenceRank(0.857)
            >>> print(confidence.percentage)  # 85 (truncated, not rounded)
            >>>
            >>> confidence = ConfidenceRank(0.99)
            >>> print(confidence.percentage)  # 99
        """
        return int(self.value * 100)

    @property
    def is_high_confidence(self) -> bool:
        """Determines if the confidence rank qualifies as high confidence.

        Applies business logic to classify confidence levels for decision-making
        purposes. High confidence evaluations can be trusted for automated
        decisions and strategic planning, while lower confidence results may
        require additional validation or human review.

        Returns:
            bool: True if the confidence rank is 0.75 or above (75%+),
                indicating sufficient statistical confidence for reliable
                quality assessment and decision-making. False otherwise.

        Business Logic:
            The threshold of 0.75 (75%) represents the minimum confidence
            level considered reliable for automated quality decisions in
            GitVoyant's domain. This threshold is based on statistical
            best practices and empirical validation of temporal analysis
            accuracy across diverse codebases.

        Example:
            >>> high_conf = ConfidenceRank(0.85)
            >>> print(high_conf.is_high_confidence)  # True
            >>>
            >>> low_conf = ConfidenceRank(0.65)
            >>> print(low_conf.is_high_confidence)  # False
        """
        return self.value >= 0.75

    @property
    def description(self) -> str:
        """Provides a qualitative label for the confidence rank.

        Converts numerical confidence scores into categorical descriptions
        that are more intuitive for human interpretation and communication.
        The descriptions follow standard confidence classification patterns
        used in statistical analysis and decision support systems.

        Returns:
            str: A descriptive confidence level classification:
                - "Very High Confidence" for values >= 0.9 (90%+)
                - "High Confidence" for values >= 0.75 (75-89%)
                - "Medium Confidence" for values >= 0.5 (50-74%)
                - "Low Confidence" for values < 0.5 (below 50%)

        Business Application:
            These classifications align with common decision-making frameworks:
            - Very High/High: Suitable for automated decisions and strategic planning
            - Medium: May require additional validation or human review
            - Low: Indicates insufficient data for reliable assessment

        Example:
            >>> very_high = ConfidenceRank(0.95)
            >>> print(very_high.description)  # "Very High Confidence"
            >>>
            >>> medium = ConfidenceRank(0.65)
            >>> print(medium.description)  # "Medium Confidence"
            >>>
            >>> low = ConfidenceRank(0.35)
            >>> print(low.description)  # "Low Confidence"
        """
        if self.value >= 0.9:
            return "Very High Confidence"
        elif self.value >= 0.75:
            return "High Confidence"
        elif self.value >= 0.5:
            return "Medium Confidence"
        else:
            return "Low Confidence"
