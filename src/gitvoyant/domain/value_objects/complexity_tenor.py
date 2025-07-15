"""
Module: src/gitvoyant/domain/value_objects/complexity_tenor.py

Complexity Trend Value Object for Temporal Quality Analysis

Defines the ComplexityTrend value object for tracking complexity changes over time.
This immutable object encapsulates the monthly slope of cyclomatic complexity
trends and provides semantic interpretation of whether a file's quality is
improving, declining, or stable based on mathematical trend analysis.

The ComplexityTrend value object is central to GitVoyant's temporal intelligence,
encoding business rules for quality assessment and providing a domain-specific
abstraction over raw statistical measurements. It transforms numerical slope
values into meaningful quality indicators that development teams can act upon.

Key Features:
    - Immutable value object ensuring data integrity
    - Business logic for quality trend interpretation
    - Human-readable descriptions for reporting
    - Threshold-based classification for decision making
    - Mathematical foundation with domain semantics

Author: Jesse Moses (@Cre4T3Tiv3) <jesse@bytestacklabs.com>

Version: 0.2.0

License: Apache 2.0
"""

from dataclasses import dataclass

__version__ = "0.2.0"
__author__ = "Jesse Moses (@Cre4T3Tiv3) - jesse@bytestacklabs.com"


@dataclass(frozen=True)
class ComplexityTrend:
    """Represents the temporal trend of complexity change in a source file.

    This value object encapsulates the mathematical slope of complexity evolution
    over time and provides domain-specific interpretation through properties that
    encode business rules for quality assessment. The object is immutable to
    ensure data integrity and consistent behavior across the domain model.

    The ComplexityTrend serves as a bridge between raw statistical analysis and
    business intelligence, transforming numerical slope measurements into
    actionable quality insights that development teams can understand and respond
    to effectively.

    Attributes:
        slope (float): The monthly rate of complexity change measured in
            complexity units per month. Negative values indicate complexity
            reduction (quality improvement), while positive values indicate
            complexity increase (quality degradation). The magnitude represents
            the speed of change.

    Design Principles:
        - Immutability: Frozen dataclass prevents accidental modification
        - Domain Semantics: Properties provide business-meaningful interpretations
        - Value Object: Identity based on value, not reference
        - Encapsulation: Business logic contained within the object
    """

    slope: float

    @property
    def monthly_change(self) -> float:
        """Returns the raw monthly change in complexity.

        Provides direct access to the underlying mathematical slope value
        without interpretation or transformation. This property serves as
        the foundation for all derived interpretations and calculations.

        Returns:
            float: The raw slope of complexity change over time, measured in
                complexity units per month. Negative values indicate decreasing
                complexity, positive values indicate increasing complexity.

        Example:
            >>> trend = ComplexityTrend(slope=-0.5)
            >>> print(trend.monthly_change)  # -0.5
            >>> # Complexity decreasing by 0.5 units per month
        """
        return self.slope

    @property
    def is_improving(self) -> bool:
        """Indicates whether the complexity trend represents quality improvement.

        Applies business logic to determine if the complexity change rate
        represents meaningful quality improvement. Uses a threshold-based
        approach to distinguish significant improvement from normal variation.

        Returns:
            bool: True if the complexity slope is significantly negative
                (< -0.1), indicating meaningful quality improvement through
                complexity reduction. False otherwise.

        Business Logic:
            The threshold of -0.1 complexity units per month represents the
            minimum rate of change considered statistically and practically
            significant for quality improvement classification. This threshold
            filters out noise in complexity measurements while identifying
            genuine improvement trends.

        Example:
            >>> improving_trend = ComplexityTrend(slope=-0.2)
            >>> print(improving_trend.is_improving)  # True
            >>>
            >>> stable_trend = ComplexityTrend(slope=-0.05)
            >>> print(stable_trend.is_improving)  # False (below threshold)
        """
        return self.slope < -0.1

    @property
    def is_declining(self) -> bool:
        """Indicates whether the complexity trend represents quality degradation.

        Applies business logic to determine if the complexity change rate
        represents concerning quality degradation. Uses a threshold-based
        approach to distinguish significant degradation from normal variation.

        Returns:
            bool: True if the complexity slope is significantly positive
                (> 0.1), indicating concerning quality degradation through
                complexity increase. False otherwise.

        Business Logic:
            The threshold of +0.1 complexity units per month represents the
            minimum rate of change considered problematic for quality assessment.
            This threshold helps identify files that may require refactoring
            or architectural attention before quality issues become severe.

        Example:
            >>> declining_trend = ComplexityTrend(slope=0.3)
            >>> print(declining_trend.is_declining)  # True
            >>>
            >>> stable_trend = ComplexityTrend(slope=0.05)
            >>> print(stable_trend.is_declining)  # False (below threshold)
        """
        return self.slope > 0.1

    @property
    def description(self) -> str:
        """Provides a human-readable summary of the complexity trend.

        Generates descriptive text that translates the mathematical slope
        into natural language suitable for reports, dashboards, and
        communication with stakeholders. The description includes both
        qualitative assessment and quantitative details.

        Returns:
            str: A formatted description of the trend's impact on code quality:
                - Improving: "Quality improvement: X.XX complexity reduction/month"
                - Declining: "Quality degradation: +X.XX complexity increase/month"
                - Stable: "Stable complexity: ±X.XX change/month"

        Formatting Rules:
            - Improving trends show negative slope as positive reduction
            - Declining trends show positive slope with explicit + sign
            - Stable trends show signed value for complete information
            - All values formatted to 2 decimal places for readability

        Example:
            >>> improving = ComplexityTrend(slope=-0.25)
            >>> print(improving.description)
            # "Quality improvement: -0.25 complexity reduction/month"

            >>> declining = ComplexityTrend(slope=0.18)
            >>> print(declining.description)
            # "Quality degradation: +0.18 complexity increase/month"

            >>> stable = ComplexityTrend(slope=0.03)
            >>> print(stable.description)
            # "Stable complexity: +0.03 change/month"
        """
        if self.is_improving:
            return f"Quality improvement: {self.slope:.2f} complexity reduction/month"
        elif self.is_declining:
            return f"Quality degradation: +{self.slope:.2f} complexity increase/month"
        else:
            return f"Stable complexity: {self.slope:+.2f} change/month"
