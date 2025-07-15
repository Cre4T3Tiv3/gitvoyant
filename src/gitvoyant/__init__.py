"""
GitVoyant v0.2.0 - Temporal Code Intelligence Platform
Real-World Ready evolution of proven temporal evaluation research
"""

__version__ = "0.2.0"
__author__ = "Jesse Moses (@Cre4T3Tiv3)"
__email__ = "jesse@bytestacklabs.com"

from .domain.entities.repository import Repository
from .domain.entities.temporal_evaluation import TemporalEvaluation
from .domain.services.temporal_evaluator_service import TemporalEvaluatorService

__all__ = [
    "TemporalEvaluatorService",
    "TemporalEvaluation",
    "Repository",
    "__version__",
    "__author__",
]
