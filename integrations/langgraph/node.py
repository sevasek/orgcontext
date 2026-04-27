"""
OrgContext × LangGraph Integration
=====================================
Inject organizational context as a LangGraph node or state field.

Usage:
    from orgcontext.integrations.langgraph import OrgContextNode, inject_state

    # As a node
    graph.add_node("org_context", OrgContextNode(entries=["okrs", "raci"]))
    graph.add_edge(START, "org_context")
    graph.add_edge("org_context", "your_next_node")

    # Or inject directly into initial state
    initial_state = inject_state(["servant-leadership", "psychological-safety"])
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional, TypedDict

from orgcontext import inject


class OrgContextState(TypedDict, total=False):
    """Extend this TypedDict in your graph state to include OrgContext fields."""
    org_context: str  # Injected prompt block from OrgContext


class OrgContextNode:
    """
    A LangGraph-compatible node that loads OrgContext entries into graph state.

    The node adds an `org_context` key to the state dict containing
    all specified entries as a combined prompt-ready block.

    Usage:
        graph.add_node("context", OrgContextNode(entries=["okrs", "raci"]))
    """

    def __init__(
        self,
        entries: list[str],
        state_key: str = "org_context",
        corpus_root: Optional[Path] = None,
    ) -> None:
        self.entries = entries
        self.state_key = state_key
        self.corpus_root = corpus_root
        # Pre-load at node init time, not on every invocation
        self._context_block = inject(entries, corpus_root=corpus_root)

    def __call__(self, state: dict[str, Any]) -> dict[str, Any]:
        """LangGraph node: adds org_context to state."""
        return {**state, self.state_key: self._context_block}


def inject_state(
    entries: list[str],
    state_key: str = "org_context",
    corpus_root: Optional[Path] = None,
) -> dict[str, str]:
    """
    Return a partial state dict with the org_context block pre-loaded.
    Use to initialize graph state before invoking.

    Example:
        initial = inject_state(["okrs", "mission-alignment"])
        result = graph.invoke({**initial, "user_input": "..."})
    """
    return {state_key: inject(entries, corpus_root=corpus_root)}


# ── Example: minimal working LangGraph graph ──────────────────────────────────
if __name__ == "__main__":
    try:
        from langgraph.graph import StateGraph, START, END
        from typing import TypedDict

        class MyState(TypedDict):
            org_context: str
            result: str

        def strategy_node(state: MyState) -> MyState:
            # The org_context is available here from the previous node
            ctx = state.get("org_context", "")
            print(f"[strategy_node] Context loaded ({len(ctx)} chars)")
            return {**state, "result": "done"}

        builder = StateGraph(MyState)
        builder.add_node(
            "context", OrgContextNode(entries=["okrs", "mission-alignment", "cynefin"])
        )
        builder.add_node("strategy", strategy_node)
        builder.add_edge(START, "context")
        builder.add_edge("context", "strategy")
        builder.add_edge("strategy", END)

        graph = builder.compile()
        output = graph.invoke({"org_context": "", "result": ""})
        print(f"Result: {output['result']}")

    except ImportError:
        print("LangGraph not installed. Install with: pip install langgraph")
