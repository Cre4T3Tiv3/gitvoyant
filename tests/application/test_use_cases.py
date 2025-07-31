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

Module: tests/application/test_use_cases.py

Application Layer Use Case Tests

Integration tests for GitVoyant application layer use cases, validating
the coordination between use cases and domain services. These tests ensure
that use cases properly orchestrate domain operations and handle various
repository states and configurations.

The tests use temporary Git repositories to provide realistic testing
scenarios while maintaining test isolation and repeatability.

Author: Jesse Moses (@Cre4T3Tiv3) <jesse@bytestacklabs.com>
Version: 0.2.0
License: Apache 2.0
"""

from pathlib import Path

import git
import pytest

from gitvoyant.application.use_cases.analyze_repo_use_case import AnalyzeRepoUseCase

__version__ = "0.2.0"
__author__ = "Jesse Moses (@Cre4T3Tiv3) - jesse@bytestacklabs.com"


@pytest.mark.asyncio
async def test_analyze_repo_use_case_executes(tmp_path):
    """Test that AnalyzeRepoUseCase successfully executes repository analysis.

    Creates a minimal Git repository with a single Python file and verifies
    that the use case can successfully orchestrate the analysis process,
    returning structured results without errors.

    Args:
        tmp_path: Pytest fixture providing a temporary directory path.

    Validates:
        - Use case executes without raising exceptions
        - Returns a dictionary containing analysis results
        - Results are truthy (non-empty and valid)

    Example Repository Structure:
        analyze_repo/
        └── main.py  # Simple Python function

    Note:
        This is an integration test that exercises the full use case flow
        including Git repository access, file analysis, and result formatting.
    """
    repo_path = tmp_path / "analyze_repo"
    repo_path.mkdir()
    file_path = repo_path / "main.py"
    file_path.write_text("def hello(): return 'world'")

    repo = git.Repo.init(repo_path)
    repo.index.add([str(file_path)])
    repo.index.commit("Initial commit")

    use_case = AnalyzeRepoUseCase()
    result = await use_case.execute(repo_path=str(repo_path), max_files=5)

    assert isinstance(result, dict)
    assert result
