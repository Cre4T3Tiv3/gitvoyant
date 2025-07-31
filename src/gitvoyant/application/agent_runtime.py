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

Module: src/gitvoyant/application/agent_runtime.py

GitVoyant Agent Runtime Module

Provides the core agent runtime infrastructure for GitVoyant's AI-powered
repository analysis capabilities using LangGraph and Claude AI integration.

This module creates a conversational agent that can perform temporal analysis
and repository evaluation through natural language interactions, leveraging
specialized tools for Git repository inspection and code quality assessment.

Dependencies:
    - LangChain/LangGraph for agent orchestration
    - Anthropic Claude for natural language processing
    - Custom GitVoyant use cases and tools

Author: Jesse Moses (@Cre4T3Tiv3) <jesse@bytestacklabs.com>
Version: 0.2.0
License: Apache 2.0
"""

import contextlib
import io
import logging
import sys
from typing import Optional, TypedDict

from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph
from langgraph.prebuilt import create_react_agent

from gitvoyant.infrastructure.config import get_settings
from gitvoyant.presentation.agents.langchain_bindings import (
    make_repo_evaluation_tool,
    make_temporal_analysis_tool,
)

__version__ = "0.2.0"
__author__ = "Jesse Moses (@Cre4T3Tiv3) - jesse@bytestacklabs.com"

settings = get_settings()

for noisy_logger in ["httpx", "httpcore", "urllib3"]:
    logging.getLogger(noisy_logger).setLevel(logging.WARNING)


class GitVoyantAgentState(TypedDict):
    """State management for GitVoyant agent conversations.

    Defines the conversation state structure used by the LangGraph agent
    to maintain context between user inputs and AI responses.

    Attributes:
        input (str): The user's input message or query.
        output (Optional[str]): The agent's response output, if any.
    """

    input: str
    output: Optional[str]


@contextlib.contextmanager
def suppress_stdout():
    """Context manager to suppress stdout output during agent execution.

    Temporarily redirects stdout to prevent verbose logging and tool output
    from cluttering the user interface when verbose mode is disabled.

    Yields:
        None: Context manager yields control back to caller.

    Example:
        >>> with suppress_stdout():
        ...     noisy_function()  # Output will be suppressed
    """
    saved_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        yield
    finally:
        sys.stdout = saved_stdout


def create_gitvoyant_agent():
    """Create a LangGraph ReAct agent with Claude AI and GitVoyant tools.

    Initializes and configures a conversational AI agent capable of performing
    repository analysis, temporal evaluation, and code quality assessment through
    natural language interactions. The agent uses Claude AI for language processing
    and specialized GitVoyant tools for repository analysis.

    Returns:
        CompiledGraph: A compiled LangGraph agent ready for conversation execution.

    Note:
        The agent is configured with:
        - Claude AI model (version specified in settings)
        - Temporal analysis tools for file-level evaluation
        - Repository evaluation tools for holistic assessment
        - System prompt optimized for concise, insightful responses

    Example:
        >>> agent = create_gitvoyant_agent()
        >>> result = agent.invoke({"input": "Analyze the quality of main.py"})
        >>> print(result["output"])
    """

    claude = ChatAnthropic(
        model_name=settings.claude_model,
        temperature=settings.claude_temperature,
        timeout=60,
        stop=None,
    )

    tools = [
        make_temporal_analysis_tool(),
        make_repo_evaluation_tool(),
    ]

    raw_agent_node = create_react_agent(
        claude,
        tools,
    )

    def run_agent(state: GitVoyantAgentState) -> GitVoyantAgentState:
        """Execute agent processing for a single conversation turn.

        Processes user input through the Claude AI agent, managing tool execution
        and response formatting. Handles verbose output control and error recovery.

        Args:
            state (GitVoyantAgentState): Current conversation state containing
                user input and any previous context.

        Returns:
            GitVoyantAgentState: Updated state with agent's response output.

        Note:
            The function handles multiple response formats from Claude:
            - Simple string responses
            - Complex structured responses with tool calls
            - Multi-part responses combining text and tool usage
        """
        messages = [
            {
                "role": "system",
                "content": (
                    "You are GitVoyant, an expert agent for analyzing software repositories "
                    "using commit history and code complexity. Respond concisely and with insight."
                ),
            },
            {
                "role": "user",
                "content": state["input"],
            },
        ]

        if settings.verbose_mode:
            print(f"\n⚙️ Invoking Claude with: \033[96m{state['input']}\033[0m")

        if settings.verbose_mode:
            response = raw_agent_node.invoke({"messages": messages})
        else:
            with suppress_stdout():
                response = raw_agent_node.invoke({"messages": messages})

        if settings.verbose_mode:
            print("📬 Raw Claude response:")

        ai_response = "[No AI response]"

        for msg in response.get("messages", []):
            if getattr(msg, "type", "") == "ai":
                content = msg.content
                if isinstance(content, str):
                    ai_response = content
                    if settings.verbose_mode:
                        print(f"🧠 Claude says: \033[92m{content}\033[0m")
                elif isinstance(content, list):
                    parts = []
                    for part in content:
                        if isinstance(part, dict):
                            if part.get("type") == "text":
                                parts.append(part["text"])
                                if settings.verbose_mode:
                                    print(
                                        f"🧠 Claude says: \033[92m{part['text']}\033[0m"
                                    )
                            elif part.get("type") == "tool_use":
                                tool = part.get("name")
                                args = part.get("input")
                                if settings.verbose_mode:
                                    print(
                                        f"🛠️ Tool called: \033[93m{tool}\033[0m with args \033[93m{args}\033[0m"
                                    )
                    if parts:
                        ai_response = "\n".join(parts)

        return {
            "input": state["input"],
            "output": ai_response,
        }

    graph = StateGraph(GitVoyantAgentState)
    graph.add_node("agent", run_agent)
    graph.set_entry_point("agent")
    graph.set_finish_point("agent")

    return graph.compile()
