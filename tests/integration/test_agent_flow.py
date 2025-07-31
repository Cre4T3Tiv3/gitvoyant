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

Module: tests/integration/test_agent_flow.py

Agent Integration Flow Tests

Integration tests for the GitVoyant AI agent, validating the complete
agent workflow from initialization through prompt processing and response
generation. These tests ensure the agent correctly integrates with
Claude AI and GitVoyant's specialized tools.

Tests include error handling for API overload situations and validate
type safety across the agent interaction boundaries.

Author: Jesse Moses (@Cre4T3Tiv3) <jesse@bytestacklabs.com>

Version: 0.2.0

License: Apache 2.0
"""

import os

import pytest
from anthropic._exceptions import OverloadedError

from gitvoyant.application.agent_runtime import (
    GitVoyantAgentState,
    create_gitvoyant_agent,
)

__version__ = "0.2.0"
__author__ = "Jesse Moses (@Cre4T3Tiv3) - jesse@bytestacklabs.com"


def test_agent_flow_simple_prompt():
    """Test agent processing of a simple repository analysis prompt.

    Validates the complete agent workflow including state management,
    prompt processing, tool integration, and response generation.
    Ensures type safety and proper error handling for API limitations.

    Test Workflow:
        1. Check for required API key availability
        2. Create and initialize the GitVoyant agent
        3. Construct properly typed agent state with test prompt
        4. Invoke agent with repository analysis question
        5. Validate response structure and content

    Type Safety:
        - Input state conforms to GitVoyantAgentState TypedDict
        - Agent.invoke() accepts correct state type
        - Response output is validated as string type

    Error Handling:
        - Skips test when ANTHROPIC_API_KEY is not available
        - Gracefully handles Anthropic API overload conditions
        - Prevents test failures due to external service limits

    Validates:
        - Agent initializes without errors
        - State management follows expected patterns
        - Response is generated as a non-empty string
        - Type annotations are respected throughout

    Note:
        This test will be skipped if:
        - ANTHROPIC_API_KEY environment variable is not set
        - The Anthropic API is overloaded
        This prevents false negatives due to missing configuration
        or external service availability issues.
    """
    if not os.getenv("ANTHROPIC_API_KEY"):
        pytest.skip(
            "ANTHROPIC_API_KEY not available — skipping agent integration test."
        )

    try:
        agent = create_gitvoyant_agent()
        state: GitVoyantAgentState = {
            "input": "What is the decay risk of this repo?",
            "output": None,
        }

        result = agent.invoke(state)
        assert isinstance(result.get("output"), str)
        assert len(result.get("output", "")) > 0  # Ensure non-empty response

    except OverloadedError:
        pytest.skip("Anthropic API overloaded — skipping test.")
    except Exception as e:
        # If it's an authentication error, skip rather than fail
        if "authentication" in str(e).lower() or "api_key" in str(e).lower():
            pytest.skip(f"API authentication issue — skipping test: {e}")
        else:
            # Re-raise other unexpected errors
            raise
