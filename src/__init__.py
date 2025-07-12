"""
GitVoyant - Temporal Code Intelligence

See your code's future with AI-powered temporal analysis.
"""

__version__ = "0.1.0"
__author__ = "Jesse Moses (@Cre4T3Tiv3) - jesse@bytestacklabs.com"

from .core.temporal_evaluator import TemporalEvaluator, forecast_decay, expedited_analysis

__all__ = ["TemporalEvaluator", "expedited_analysis", "forecast_decay"]
