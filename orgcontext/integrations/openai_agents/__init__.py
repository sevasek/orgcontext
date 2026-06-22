"""OpenAI Agents SDK integration for OrgContext.

Requires ``openai-agents`` to be installed:
    pip install openai-agents

Re-exports the public surface from tool.py so the documented import path
works:

    from orgcontext.integrations.openai_agents import org_context_tool, inject_system_prompt
"""

from orgcontext.integrations.openai_agents.tool import (  # noqa: F401
    inject_system_prompt,
    org_context_tool,
)

__all__ = ["org_context_tool", "inject_system_prompt"]
