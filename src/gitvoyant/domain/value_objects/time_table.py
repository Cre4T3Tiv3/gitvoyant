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

Module: src/gitvoyant/domain/value_objects/time_table.py

Time Table Value Object for Temporal Evaluation Windows

Defines the TimeTable value object used in temporal evaluation to represent
time intervals and ranges. This immutable object encapsulates datetime ranges
with utilities to compute durations and construct time windows for analysis.

The TimeTable value object provides a domain-specific abstraction for temporal
scoping in GitVoyant's analysis pipeline, offering convenient factory methods
and duration calculations optimized for code quality assessment workflows.

Key Features:
    - Immutable value object for temporal ranges
    - Duration calculations in multiple units (days, months)
    - Factory methods for common time window patterns
    - Domain-optimized month calculations
    - Clean abstraction over datetime complexity

Author: Jesse Moses (@Cre4T3Tiv3) <jesse@bytestacklabs.com>
Version: 0.2.0
License: Apache 2.0
"""

from dataclasses import dataclass
from datetime import datetime, timedelta

__version__ = "0.2.0"
__author__ = "Jesse Moses (@Cre4T3Tiv3) - jesse@bytestacklabs.com"


@dataclass(frozen=True)
class TimeTable:
    """Represents a time interval used in temporal evaluation workflows.

    This value object encapsulates a specific time range defined by start and
    end datetime boundaries, providing domain-specific utilities for duration
    calculation and time window construction. The object is immutable to ensure
    temporal consistency throughout analysis pipelines.

    The TimeTable serves as the temporal foundation for GitVoyant's analysis,
    defining the scope of commit history examination and enabling consistent
    time-based comparisons across different files and repositories.

    Attributes:
        start_date (datetime): The beginning of the time range, inclusive.
            Represents the earliest point in time for analysis inclusion.
            Typically set based on analysis window requirements or specific
            historical points of interest.
        end_date (datetime): The end of the time range, inclusive. Represents
            the latest point in time for analysis inclusion. Often set to
            the current time for "recent history" analysis or to specific
            points for historical comparisons.

    Design Principles:
        - Immutability: Frozen dataclass prevents temporal inconsistencies
        - Domain Semantics: Methods provide analysis-specific calculations
        - Value Object: Identity based on temporal values, not reference
        - Convenience: Factory methods for common time window patterns

    Invariants:
        - start_date should be <= end_date for meaningful durations
        - Time zone handling should be consistent across datetime values
        - Duration calculations assume valid datetime ranges
    """

    start_date: datetime
    end_date: datetime

    @property
    def days(self) -> int:
        """Total duration of the time range in complete days.

        Calculates the number of full days between the start and end dates,
        providing a discrete measure of temporal scope. This property is
        fundamental for determining analysis window sizes and comparing
        evaluation periods across different assessments.

        Returns:
            int: Number of complete days between start and end dates.
                Fractional days are truncated to provide consistent discrete
                values. A range from Monday to Wednesday would return 2 days.

        Example:
            >>> from datetime import datetime
            >>> start = datetime(2024, 1, 1)
            >>> end = datetime(2024, 1, 8)
            >>> table = TimeTable(start, end)
            >>> print(table.days)  # 7
        """
        return (self.end_date - self.start_date).days

    @property
    def months(self) -> float:
        """Approximate duration of the time range in months.

        Converts the day-based duration to months using the average month
        length of 30.44 days. This approximation is optimized for temporal
        analysis where precise calendar months are less important than
        consistent duration scaling across different time periods.

        Returns:
            float: Approximate number of months in the time range, calculated
                using the statistical average month length. Provides fractional
                values for precise temporal scaling in trend analysis.

        Calculation Method:
            Uses 30.44 days per month, which accounts for:
            - Variation in month lengths (28-31 days)
            - Leap year effects over multiple years
            - Statistical accuracy for temporal trend analysis

        Example:
            >>> # 90-day analysis window
            >>> table = TimeTable.from_days(90)
            >>> print(f"{table.months:.2f}")  # approximately 2.96 months
            >>>
            >>> # 180-day analysis window
            >>> table = TimeTable.from_days(180)
            >>> print(f"{table.months:.2f}")  # approximately 5.92 months
        """
        return self.days / 30.44

    @classmethod
    def from_days(cls, days: int) -> "TimeTable":
        """Creates a TimeTable ending now and spanning a specified number of days.

        Factory method that constructs a time window ending at the current
        moment and extending backwards for the specified number of days.
        This is the most common pattern for temporal analysis, creating
        "recent history" windows for quality assessment.

        Args:
            days (int): Number of days to include in the time range, extending
                backwards from the current time. Must be positive to create
                a meaningful time window for analysis.

        Returns:
            TimeTable: A new TimeTable instance with end_date set to the
                current time and start_date calculated by subtracting the
                specified number of days.

        Usage Patterns:
            This factory method is ideal for:
            - Standard analysis windows (30, 90, 180 days)
            - Rolling time window analysis
            - Consistent temporal scoping across evaluations
            - Real-time quality monitoring

        Example:
            >>> # Create a 180-day analysis window ending now
            >>> recent_history = TimeTable.from_days(180)
            >>>
            >>> # Create a 30-day short-term analysis window
            >>> short_term = TimeTable.from_days(30)
            >>> print(short_term.days)  # 30
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        return cls(start_date, end_date)

    @classmethod
    def last_months(cls, months: int) -> "TimeTable":
        """Creates a TimeTable ending now and spanning a specified number of months.

        Factory method that constructs a time window ending at the current
        moment and extending backwards for the specified number of months.
        Uses the same 30.44-day month approximation as the months property
        for consistency in temporal calculations.

        Args:
            months (int): Number of months to include in the time range,
                extending backwards from the current time. Converted to days
                using the statistical average month length for consistent
                temporal scoping.

        Returns:
            TimeTable: A new TimeTable instance with end_date set to the
                current time and start_date calculated by subtracting the
                equivalent number of days (months * 30.44).

        Conversion Logic:
            Months are converted to days using the formula: days = months * 30.44
            This provides consistent temporal windows regardless of:
            - Calendar month variations (28-31 days)
            - Leap year effects
            - Seasonal timing differences

        Example:
            >>> # Create a 6-month analysis window
            >>> half_year = TimeTable.last_months(6)
            >>> print(f"Days: {half_year.days}")  # approximately 182 days
            >>>
            >>> # Create a 1-year analysis window
            >>> full_year = TimeTable.last_months(12)
            >>> print(f"Months: {full_year.months:.1f}")  # approximately 12.0
        """
        return cls.from_days(int(months * 30.44))
