"""
OrgContext × CrewAI Integration
================================
Load organizational context into CrewAI agents via a tool.

Usage:
    from orgcontext.integrations.crewai import org_context_tool, inject_agent_context

    researcher = Agent(
        role="Strategy Analyst",
        goal="...",
        backstory="...",
        tools=[org_context_tool(entries=["mission-alignment", "okrs", "cynefin"])]
    )
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

try:
    from crewai_tools import tool as crewai_tool
    HAS_CREWAI = True
except ImportError:
    HAS_CREWAI = False

from orgcontext import load, inject, list_entries


def org_context_tool(
    entries: list[str],
    corpus_root: Optional[Path] = None,
):
    """
    Build a CrewAI tool that provides OrgContext entries to an agent.

    Args:
        entries: List of entry IDs to pre-load (e.g. ["okrs", "raci"]).
        corpus_root: Optional corpus root override.

    Returns:
        A CrewAI-compatible tool function.
    """
    if not HAS_CREWAI:
        raise ImportError(
            "crewai-tools is required. Install with: pip install crewai-tools"
        )

    # Pre-load the context block once
    context_block = inject(entries, corpus_root=corpus_root)

    @crewai_tool("OrgContext Knowledge Base")
    def _org_context(query: str) -> str:
        """
        Query the OrgContext organizational knowledge base.
        Use this tool when you need definitions, decision heuristics,
        or role/leadership context to interpret your task correctly.
        """
        # Simple keyword match — swap for vector search in production
        query_lower = query.lower()
        results = []
        for entry_id in entries:
            entry = load(entry_id, corpus_root=corpus_root)
            if (
                query_lower in entry.title.lower()
                or query_lower in entry.id
                or any(query_lower in t for t in entry.tags)
            ):
                results.append(entry.prompt_snippet)

        if results:
            return "\n\n---\n\n".join(results)
        # Fall back to full context block if no keyword match
        return context_block

    return _org_context


def inject_agent_context(
    entries: list[str],
    corpus_root: Optional[Path] = None,
) -> str:
    """
    Return a formatted context block to inject into an agent's backstory or system prompt.

    Example:
        researcher = Agent(
            backstory=f"You are a senior strategy analyst. {inject_agent_context(['okrs', 'mission-alignment'])}",
            ...
        )
    """
    block = inject(entries, corpus_root=corpus_root)
    return f"\n\n[ORGANIZATIONAL CONTEXT LOADED]\n\n{block}\n\n[END ORGANIZATIONAL CONTEXT]"


# ── Example usage ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Show what a context injection looks like
    entries = ["okrs", "raci", "mission-alignment"]
    context = inject_agent_context(entries)
    print(context[:1000])
    print("...")
    print(f"\n[Loaded {len(entries)} entries]")
