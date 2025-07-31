"""GitVoyant CLI Initialization

Copyright 2025 ByteStack Labs

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Module: src/gitvoyant/__init__.py
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
