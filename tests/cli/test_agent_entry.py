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

Module: tests/cli/test_agent_entry.py

CLI Agent Entry Point Tests

End-to-end tests for the GitVoyant CLI agent functionality, validating
the complete user interaction flow from command invocation through
agent initialization and graceful termination.

These tests use subprocess execution to simulate real user interactions
with the CLI interface, ensuring the agent behaves correctly in production
environments.

Author: Jesse Moses (@Cre4T3Tiv3) <jesse@bytestacklabs.com>

Version: 0.2.0

License: Apache 2.0
"""

import subprocess

__version__ = "0.2.0"
__author__ = "Jesse Moses (@Cre4T3Tiv3) - jesse@bytestacklabs.com"


def test_gitvoyant_agent_entry():
    """Test the complete CLI agent lifecycle from startup to shutdown.

    Simulates a user running the 'gitvoyant analyze agent' command,
    interacting with the agent, and then exiting gracefully. Validates
    that the agent initializes properly and responds to user commands.

    Test Flow:
        1. Launch the CLI agent via subprocess
        2. Send 'exit' command to terminate gracefully
        3. Verify successful initialization and clean shutdown
        4. Validate expected output messages appear

    Validates:
        - CLI command executes successfully (exit code 0)
        - Claude agent initializes without errors
        - Agent displays expected startup messages
        - Graceful shutdown occurs when 'exit' is sent
        - No timeout or hanging processes

    Raises:
        RuntimeError: If the agent process doesn't terminate within timeout
        AssertionError: If expected output messages are missing

    Note:
        This test requires a valid Anthropic API key in the environment
        for the Claude agent to initialize successfully. The test uses
        a 10-second timeout to prevent hanging in CI environments.
    """
    process = subprocess.Popen(
        ["gitvoyant", "analyze", "agent"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    try:
        stdout, stderr = process.communicate(input="exit\n", timeout=10)
    except subprocess.TimeoutExpired:
        process.kill()
        raise RuntimeError("Agent CLI did not exit in time.")

    assert process.returncode == 0
    assert "Claude agent initialized" in stdout
    assert "Goodbye" in stdout
