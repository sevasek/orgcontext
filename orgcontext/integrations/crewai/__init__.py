"""CrewAI integration for OrgContext.

Requires `crewai-tools` to be installed:
    pip install crewai-tools

Re-exports the public surface from loader.py so the documented import path
works:

    from orgcontext.integrations.crewai import org_context_tool, inject_agent_context
"""

from orgcontext.integrations.crewai.loader import (  # noqa: F401
    inject_agent_context,
    org_context_tool,
)

__all__ = ["org_context_tool", "inject_agent_context"]
