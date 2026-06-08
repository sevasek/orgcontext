"""Example usage of the OrgContext Python API.

Run with:
    python examples/usage.py
"""
from orgcontext import load, inject, list_entries, search_entries, get_frontmatter

print("=== OrgContext Quick Demo ===\n")

# 1. Load a single entry and access rich metadata + sections
entry = load("okrs")
print(f"Loaded: {entry.title}")
print(f"Authors: {entry.authors}")
print(f"Last updated: {entry.last_updated}")
print(f"Version: {entry.version}")
print(f"Deprecated: {entry.deprecated}")
print(f"\nDefinition snippet: {entry.definition[:120]}...\n")

# 2. Use to_dict for serialization (RAG, JSON export, etc.)
data = entry.to_dict(include_sections=False)
print("to_dict keys:", list(data.keys()))

# 3. Inject multiple entries into a prompt block
context = inject(["okrs", "raci", "servant-leadership"])
print(f"\nInjected context length: {len(context)} chars\n")

# 4. List and filter
strategy = list_entries(category="strategy-execution")
print(f"Strategy entries: {[e['id'] for e in strategy]}\n")

# 5. Search
leadership_entries = search_entries("leadership")
print(f"Leadership-related: {[e['id'] for e in leadership_entries]}\n")

# 6. Raw frontmatter access
fm = get_frontmatter("psychological-safety")
print("Raw frontmatter keys:", list(fm.keys()))

print("\n=== Demo complete ===")
