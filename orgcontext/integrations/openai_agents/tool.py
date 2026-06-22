"""
OrgContext × OpenAI Agents SDK Integration
==========================================
Load organizational context as a function tool for OpenAI agents.

Usage:
    from orgcontext.integrations.openai_agents import org_context_tool, inject_system_prompt

    agent = Agent(
        name="Strategy Analyst",
        instructions=inject_system_prompt(["okrs", "mission-alignment"]),
        tools=[org_context_tool(entries=["okrs", "raci", "cynefin"])],
    )
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

try:
    from agents import FunctionTool
    import inspect

    HAS_OPENAI_AGENTS = True
except ImportError:
    HAS_OPENAI_AGENTS = False

from orgcontext import inject, load, search_entries


def org_context_tool(
    entries: list[str],
    corpus_root: Optional[Path] = None,
):
    """
    Build an OpenAI Agents SDK FunctionTool that queries OrgContext entries.

    The tool pre-loads all requested entries at construction time and answers
    keyword queries at runtime. If no keyword matches, it returns the full
    combined context block — ensuring the agent always gets useful context.

    Args:
        entries: List of entry ID slugs to pre-load (e.g. ["okrs", "raci"]).
        corpus_root: Optional corpus root override.

    Returns:
        A FunctionTool compatible with the OpenAI Agents SDK.

    Raises:
        ImportError: If the ``openai-agents`` package is not installed.
    """
    if not HAS_OPENAI_AGENTS:
        raise ImportError(
            "openai-agents is required. Install with: pip install openai-agents"
        )

    context_block = inject(entries, corpus_root=corpus_root)

    def _query_org_context(query: str) -> str:
        """Query the OrgContext organizational knowledge base.

        Use when you need definitions, decision heuristics, or leadership
        frameworks to interpret a task correctly. Pass a keyword or concept
        name (e.g. "okrs", "servant leadership", "raci").
        """
        query_lower = (query or "").strip().lower()
        if not query_lower:
            return context_block

        results = []
        for entry_id in entries:
            entry = load(entry_id, corpus_root=corpus_root)
            if (
                query_lower in entry.title.lower()
                or query_lower in entry.id
                or any(query_lower in t for t in entry.tags)
            ):
                results.append(entry.prompt_snippet)

        return "\n\n---\n\n".join(results) if results else context_block

    params_schema = {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": (
                    "Keyword or concept to look up in the organizational knowledge base "
                    "(e.g. 'okrs', 'servant leadership', 'raci')."
                ),
            }
        },
        "required": ["query"],
        "additionalProperties": False,
    }

    async def _on_invoke(ctx, input_json: str) -> str:
        import json

        data = json.loads(input_json) if input_json else {}
        return _query_org_context(data.get("query", ""))

    return FunctionTool(
        name="query_org_context",
        description=(
            "Query the OrgContext organizational knowledge base for definitions, "
            "decision heuristics, and leadership frameworks. Use this tool when you "
            "need organizational context to interpret or complete a task correctly."
        ),
        params_json_schema=params_schema,
        on_invoke_tool=_on_invoke,
    )


def inject_system_prompt(
    entries: list[str],
    corpus_root: Optional[Path] = None,
) -> str:
    """
    Return a formatted context block to inject into an agent's ``instructions``.

    Example:
        agent = Agent(
            name="Analyst",
            instructions=inject_system_prompt(["okrs", "mission-alignment"]),
        )

    Args:
        entries: List of entry ID slugs to include.
        corpus_root: Optional corpus root override.

    Returns:
        A string containing all prompt snippets, suitable for use as or
        appended to an agent's ``instructions`` field.
    """
    block = inject(entries, corpus_root=corpus_root)
    return f"\n\n[ORGANIZATIONAL CONTEXT]\n\n{block}\n\n[END ORGANIZATIONAL CONTEXT]"


if __name__ == "__main__":
    entries = ["okrs", "raci", "mission-alignment"]
    prompt = inject_system_prompt(entries)
    print(prompt[:1000])
    print("...")
    print(f"\n[Loaded {len(entries)} entries]")
