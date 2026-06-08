"""OrgContext MCP Server — exposes the corpus as Model Context Protocol tools."""
from __future__ import annotations

from mcp.server.fastmcp import FastMCP

import orgcontext as _oc

mcp = FastMCP("orgcontext")


@mcp.tool()
def get_entry(id: str) -> str:
    """Get a single OrgContext entry by ID, returning its prompt-ready content with metadata."""
    entry = _oc.load(id)
    tags_val = entry.tags
    if isinstance(tags_val, list):
        tags = ", ".join(tags_val) if tags_val else "none"
    else:
        tags = str(tags_val) if tags_val else "none"

    authors = ", ".join(entry.authors) if entry.authors else "unknown"
    meta = f"Version: {entry.version} | Last updated: {entry.last_updated} | Authors: {authors}"
    if entry.deprecated:
        meta += " | DEPRECATED"

    return f"# {entry.title}\n\nCategory: {entry.category}\nTags: {tags}\n{meta}\n\n{entry.prompt_snippet}"


@mcp.tool()
def inject_entries(ids: list[str]) -> str:
    """Combine multiple OrgContext entries into one prompt-ready block for system prompt injection."""
    return _oc.inject(ids)


@mcp.tool()
def list_entries(category: str | None = None) -> str:
    """List all available OrgContext entries, optionally filtered by category.
    Includes authors and last_updated from the enhanced list_entries API."""
    entries = _oc.list_entries(category=category)
    if not entries:
        if category:
            return f"No entries found for category '{category}'."
        return "No entries found."
    lines = []
    for e in entries:
        author_str = ", ".join(e.get("authors", [])) if e.get("authors") else "unknown"
        last = e.get("last_updated", "")
        lines.append(f"- {e['id']}: {e['title']} ({e['category']}) [by {author_str}, updated {last}]")
    if category:
        header = f"OrgContext entries in '{category}' ({len(entries)} total):\n"
    else:
        header = f"OrgContext entries ({len(entries)} total):\n"
    return header + "\n".join(lines)


@mcp.tool()
def search_entries(query: str) -> str:
    """Search OrgContext entries by keyword across entry IDs, titles, and tags.
    Results now include authors and update date thanks to enhanced metadata."""
    all_entries = _oc.list_entries()
    q = query.lower()
    matches = [
        e for e in all_entries
        if q in e["id"].lower()
        or q in e["title"].lower()
        or any(q in tag.lower() for tag in (e.get("tags") or []))
    ]
    if not matches:
        return f"No entries found matching '{query}'. Try list_entries() to see all available entries."
    lines = []
    for e in matches:
        author_str = ", ".join(e.get("authors", [])) if e.get("authors") else "unknown"
        last = e.get("last_updated", "")
        lines.append(f"- {e['id']}: {e['title']} ({e['category']}) [by {author_str}, updated {last}]")
    return f"Found {len(matches)} entries matching '{query}':\n" + "\n".join(lines)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
