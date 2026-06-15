"""Optional integrations for OrgContext (LangGraph, CrewAI, ...).

Submodules are intentionally optional dependencies — importing the parent
package must not require LangGraph or CrewAI to be installed. Import the
specific submodule you need:

    from orgcontext.integrations.langgraph import OrgContextNode
    from orgcontext.integrations.crewai import org_context_tool
"""
