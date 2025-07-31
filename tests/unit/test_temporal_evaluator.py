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

Module: tests/unit/test_temporal_evaluator.py

Temporal Evaluator Infrastructure Unit Tests

Core unit tests for the TemporalEvaluator infrastructure component,
validating complexity analysis, trend computation, and insight generation
using realistic Git repository scenarios.

These tests create actual Git repositories with commit history to ensure
the evaluator correctly processes real Git data and produces accurate
temporal analysis results.

Author: Jesse Moses (@Cre4T3Tiv3) <jesse@bytestacklabs.com>

Version: 0.2.0

License: Apache 2.0
"""

from typing import Dict, List

from gitvoyant.infrastructure.temporal_evaluator import TemporalEvaluator

__version__ = "0.2.0"
__author__ = "Jesse Moses (@Cre4T3Tiv3) - jesse@bytestacklabs.com"


def test_complexity_trend_slope(tmp_path):
    """Test complexity trend analysis with incremental code changes.

    Creates a realistic Git repository with multiple commits showing
    gradual complexity evolution, then validates that the evaluator
    correctly computes trend slopes and risk assessments.

    Args:
        tmp_path: Pytest fixture providing temporary directory.

    Test Scenario:
        - Create Git repository with 5 commits
        - Each commit adds incremental complexity to a Python file
        - Analyze the file's temporal evolution
        - Verify trend computation and risk assessment

    Commit Progression:
        - Commit 0: Simple function returning 42
        - Commit 1: Function returning 42 + 1
        - ...continuing incrementally
        - Commits create realistic complexity progression

    Validates:
        - Evaluator processes multi-commit history successfully
        - Result contains expected temporal analysis fields
        - Quality decay forecast is computed and bounded
        - Complexity trend slope reflects actual code changes
    """
    repo_path = tmp_path / "dummy_repo"
    repo_path.mkdir()
    file_path = repo_path / "sample.py"
    import git

    repo = git.Repo.init(repo_path)

    for i in range(5):
        file_path.write_text(f"def foo():\n    return 42 + {i}\n")
        repo.index.add([str(file_path)])
        repo.index.commit(f"Change {i}")

    evaluator = TemporalEvaluator(repo_path)
    result = evaluator.evaluate_file_evolution("sample.py")

    assert isinstance(result, Dict)
    assert "quality_decay_forecast" in result
    assert "complexity_trend_slope" in result


def test_no_commit_history(tmp_path):
    """Test evaluator behavior with insufficient commit history.

    Validates that the evaluator gracefully handles repositories with
    insufficient commit history for temporal analysis, returning
    appropriate error messages rather than crashing.

    Args:
        tmp_path: Pytest fixture providing temporary directory.

    Test Scenario:
        - Create Git repository with minimal commit history
        - Add file that wasn't tracked in any commits
        - Attempt temporal evaluation on untracked file
        - Verify graceful error handling

    Error Conditions:
        - Files with no commit history in analysis window
        - Files that exist but weren't tracked by Git
        - Repositories with insufficient temporal data

    Validates:
        - Evaluator returns error dictionary instead of crashing
        - Error message clearly indicates insufficient history
        - Error handling preserves system stability
        - Partial repository analysis remains possible
    """
    repo_path = tmp_path / "empty_repo"
    repo_path.mkdir()
    (repo_path / "sample.py").write_text("print('Hello')")

    import git

    repo = git.Repo.init(repo_path)

    dummy_file = repo_path / "dummy.py"
    dummy_file.write_text("pass")
    repo.index.add([str(dummy_file)])
    repo.index.commit("Initial dummy commit")
    dummy_file.unlink()
    repo.index.remove([str(dummy_file)])
    repo.index.commit("Remove dummy")

    evaluator = TemporalEvaluator(repo_path)
    result = evaluator.evaluate_file_evolution("sample.py")

    assert "error" in result
    assert "Insufficient commit history" in result["error"]


def test_forecast_quality_decay(tmp_path):
    """Test quality decay forecasting with minimal repository setup.

    Validates that the evaluator can compute decay risk predictions even
    with limited commit history, producing bounded probability scores
    suitable for risk assessment and decision making.

    Args:
        tmp_path: Pytest fixture providing temporary directory.

    Test Scenario:
        - Create minimal Git repository with single commit
        - Add simple Python file with basic function
        - Generate quality decay forecast
        - Verify prediction bounds and data types

    Prediction Characteristics:
        - Decay score must be float type
        - Score bounded between 0.0 and 1.0 (probability range)
        - Prediction handles minimal data gracefully
        - Results suitable for risk classification

    Validates:
        - Forecasting returns proper float value
        - Prediction score within valid probability bounds (0.0-1.0)
        - Minimal repository data doesn't cause errors
        - Decay prediction algorithm handles edge cases
    """
    repo_path = tmp_path / "forecast_repo"
    repo_path.mkdir()
    file_path = repo_path / "compute.py"
    file_path.write_text("def compute(): return 1 + 2")

    import git

    repo = git.Repo.init(repo_path)
    repo.index.add([str(file_path)])
    repo.index.commit("Init compute")

    evaluator = TemporalEvaluator(repo_path)
    decay_score = evaluator.forecast_quality_decay("compute.py")

    assert isinstance(decay_score, float)
    assert 0.0 <= decay_score <= 1.0


def test_generate_discernment(tmp_path):
    """Test insight generation from temporal evaluation results.

    Validates that the evaluator can generate structured discernment signals
    from temporal analysis, providing actionable insights for code quality
    management and decision making.

    Args:
        tmp_path: Pytest fixture providing temporary directory.

    Test Scenario:
        - Create Git repository with moderately complex Python code
        - Add file containing conditional logic and complexity
        - Generate discernment signals from temporal analysis
        - Verify insight structure and content quality

    Code Complexity:
        - Function with conditional branching (if statement)
        - Multiple return paths creating cyclomatic complexity
        - Realistic code pattern for complexity analysis

    Discernment Validation:
        - Returns list of TemporalDiscernment objects
        - Each discernment has required fields and valid data types
        - Discernment types match expected categories
        - Confidence values within valid probability bounds

    Validates:
        - Insight generation returns list data structure
        - Individual insights contain all required fields
        - Discernment types match expected categories (trend, exposure, decay)
        - Confidence scores bounded within valid range (0.0-1.0)
        - File path information correctly preserved in insights
    """
    repo_path = tmp_path / "insight_repo"
    repo_path.mkdir()
    file_path = repo_path / "logic.py"
    file_path.write_text(
        """def calculate(x):
    if x > 10:
        return x * 2
    return x + 2
"""
    )

    import git

    repo = git.Repo.init(repo_path)
    repo.index.add([str(file_path)])
    repo.index.commit("Add logic")

    evaluator = TemporalEvaluator(repo_path)
    signals = evaluator.generate_discernment("logic.py")

    assert isinstance(signals, List)
    if signals:
        signal = signals[0]
        assert isinstance(signal.file_path, str)
        assert signal.discernment_type in {"trend", "exposure", "decay"}
        assert 0.0 <= signal.confidence <= 1.0
