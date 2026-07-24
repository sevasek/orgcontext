"""Optional integrations for OrgContext (LangGraph, CrewAI, OpenAI Agents SDK, ...).

Submodules are intentionally optional dependencies — importing the parent
package must not require LangGraph, CrewAI, or openai-agents to be installed.
Import the specific submodule you need:

    from orgcontext.integrations.langgraph import OrgContextNode
    from orgcontext.integrations.crewai import org_context_tool
    from orgcontext.integrations.openai_agents import org_context_tool, inject_system_prompt
"""
