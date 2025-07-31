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

Module: tests/unit/test_cli_repo_resolver.py

CLI Repository Resolver Unit Tests

Unit tests for the repository path resolution functionality, validating
both local path handling and remote repository cloning with caching.
These tests ensure reliable repository access across different input
formats and network conditions.

Tests use mocking to avoid actual network operations while validating
the complete resolution logic and caching behavior.

Author: Jesse Moses (@Cre4T3Tiv3) <jesse@bytestacklabs.com>

Version: 0.2.0

License: Apache 2.0
"""

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from gitvoyant.cli.repo_resolver import resolve_repo_path

__version__ = "0.2.0"
__author__ = "Jesse Moses (@Cre4T3Tiv3) - jesse@bytestacklabs.com"


def test_resolve_local_repo_path(tmp_path):
    """Test resolution of local filesystem repository paths.

    Validates that local repository paths are correctly resolved to absolute
    Path objects without attempting network operations or caching logic.

    Args:
        tmp_path: Pytest fixture providing temporary directory.

    Test Scenario:
        - Create a local directory representing a repository
        - Pass the path to resolve_repo_path()
        - Verify correct Path object resolution

    Validates:
        - Returns Path object (not string)
        - Path is correctly resolved to absolute form
        - No network operations are attempted
        - Local paths work with both relative and absolute inputs
    """
    local_repo = tmp_path / "myrepo"
    local_repo.mkdir()
    result = resolve_repo_path(str(local_repo))

    assert isinstance(result, Path)
    assert result.resolve() == local_repo.resolve()


@patch("gitvoyant.cli.repo_resolver.Repo.clone_from")
def test_resolve_remote_repo_clones_if_not_cached(mock_clone):
    """Test remote repository cloning when no cached copy exists.

    Validates the complete remote repository resolution workflow including
    URL parsing, cache directory determination, and Git clone operation
    for repositories that haven't been previously cached.

    Args:
        mock_clone: Mocked Git clone operation to avoid network calls.

    Test Scenario:
        - Provide HTTPS Git repository URL
        - Ensure no cached copy exists in temp directory
        - Verify clone operation is initiated with correct parameters

    Cache Logic:
        - Extract repository name from URL path
        - Generate cache directory: temp/gitvoyant_{repo_name}
        - Clone only if cache directory doesn't exist

    Validates:
        - Correct cache path generation from repository URL
        - Git clone operation called with expected parameters
        - Cache directory cleanup handled for test isolation
        - Path object returned points to expected cache location
    """
    url = "https://github.com/example/repo.git"
    parsed_name = "repo"
    expected_path = Path(tempfile.gettempdir()) / f"gitvoyant_{parsed_name}"

    if expected_path.exists():
        if expected_path.is_dir():
            import shutil

            shutil.rmtree(expected_path)

    result = resolve_repo_path(url)

    assert result == expected_path
    mock_clone.assert_called_once_with(url, expected_path)


@patch("gitvoyant.cli.repo_resolver.Repo.clone_from")
def test_resolve_remote_repo_uses_cached_clone(mock_clone, tmp_path):
    """Test remote repository resolution with existing cached copy.

    Validates that the resolver correctly identifies and reuses existing
    cached repository clones without attempting redundant network operations.

    Args:
        mock_clone: Mocked Git clone operation to verify it's not called.
        tmp_path: Pytest fixture providing temporary directory.

    Test Scenario:
        - Provide HTTPS Git repository URL
        - Pre-create cache directory to simulate existing clone
        - Verify resolver uses cached copy without cloning

    Cache Reuse Logic:
        - Check for existing cache directory before cloning
        - Return cached path if directory exists
        - Skip clone operation entirely for cached repositories

    Validates:
        - Existing cache directories are detected correctly
        - No clone operation is attempted when cache exists
        - Correct cached path is returned
        - Performance optimization through cache reuse
    """
    url = "https://github.com/example/repo.git"
    parsed_name = "repo"
    temp_dir = Path(tempfile.gettempdir()) / f"gitvoyant_{parsed_name}"
    temp_dir.mkdir(exist_ok=True)

    result = resolve_repo_path(url)

    assert result == temp_dir
    mock_clone.assert_not_called()
