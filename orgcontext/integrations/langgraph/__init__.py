"""LangGraph integration for OrgContext.

Requires `langgraph` to be installed:
    pip install langgraph

Re-exports the public surface from node.py so the documented import path
works:

    from orgcontext.integrations.langgraph import OrgContextNode, inject_state
"""

from orgcontext.integrations.langgraph.node import (  # noqa: F401
    OrgContextNode,
    OrgContextState,
    inject_state,
)

__all__ = ["OrgContextNode", "OrgContextState", "inject_state"]
