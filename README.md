# OrgContext

> **A growing, LLM-native dictionary of mission, vision, roles, leadership frameworks, and organizational concepts.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](./CONTRIBUTING.md)
[![Entries](https://img.shields.io/badge/corpus-34%20entries-blue)](#corpus-structure)

---

## Why OrgContext?

LLM agents often fail not because they lack intelligence, but because they lack **shared organizational grounding**. Terms like "strategic alignment," "Product Owner," or "servant leadership" get interpreted differently across prompts, agents, or sessions.

OrgContext provides a reusable, community-curated corpus of clear definitions, decision heuristics, anti-patterns, and ready-to-inject prompt snippets for these concepts.

Think of it as a living reference library that you can load into your agents, RAG pipelines, or system prompts — the same way you import code libraries.

| Without OrgContext | With OrgContext |
|--------------------|-----------------|
| "Strategic alignment" means whatever the model guesses | Precise definition + decision heuristics + anti-patterns |
| Role ambiguity: "What does a Product Owner *actually* decide?" | Canonical scope, escalation rules, RACI mapping |
| Leadership model mismatch across agents | Shared, versioned, injectable leadership vocabulary |
| Custom `company-context.md` reinvented per project | One community-maintained corpus |
| Multi-agent systems with conflicting interpretations | Single shared lexicon loaded the same way everywhere |

---

## Quick Start

### Install

```bash
git clone https://github.com/sevasek/orgcontext.git
cd orgcontext
pip install -e .
```

### Use the Python API

```python
from orgcontext import load, inject, list_entries, search_entries, get_frontmatter

# Load a single entry and access structured sections
entry = load("servant-leadership")
print(entry.definition)
print(entry.decision_heuristics)
print(entry.prompt_snippet)   # ready to paste into a system prompt

# Combine multiple entries into one prompt-ready block
context_block = inject(["okrs", "raci", "mission-alignment"])

# Browse available entries
all_entries = list_entries()
strategy_entries = list_entries(category="strategy-execution")

# New: Rich metadata is now available on every entry
entry = load("okrs")
print(entry.authors)          # ['Paul Seville']
print(entry.version)          # '1.0.0'
print(entry.last_updated)     # '2026-06-08'
print(entry.deprecated)       # False
print(entry.references)       # list of source materials

# list_entries() now returns the full metadata too
entries = list_entries()
print(entries[0]["authors"])     # list of authors
print(entries[0]["last_updated"])

# Convenience method for serialization / RAG pipelines
entry_dict = entry.to_dict()           # includes sections by default
minimal = entry.to_dict(include_sections=False)

# Search the corpus programmatically
results = search_entries("leadership")
for e in results:
    print(e["id"], e["title"])

# Or search for specific authors
results = search_entries("Paul Seville")
```

### Copy-paste

Each entry has a `## Prompt Snippet` section. Copy it directly into your agent's system prompt — no code required.

### Point a RAG store at the corpus

```python
corpus_dir = "core/"  # 34 validated Markdown entries, ready for embedding
```

### Command Line Interface

After installing, you can use the `orgcontext` CLI:

```bash
# List all entries
orgcontext list

# Filter by category
orgcontext list --category governance

# Get full details for one entry
orgcontext get okrs

# Search across the corpus
orgcontext search leadership
```

---

## Integrations

### LangGraph

```python
from integrations.langgraph.node import OrgContextNode, inject_state

# Add as a graph node
graph.add_node("context", OrgContextNode(entries=["okrs", "raci"]))
graph.add_edge(START, "context")

# Or inject into initial state directly
initial_state = inject_state(["servant-leadership", "psychological-safety"])
result = graph.invoke({**initial_state, "user_input": "..."})
```

### CrewAI

```python
from integrations.crewai.loader import org_context_tool, inject_agent_context

# Give an agent a tool to query the corpus
analyst = Agent(
    role="Strategy Analyst",
    tools=[org_context_tool(entries=["okrs", "cynefin", "mission-alignment"])],
)

# Or inject directly into an agent's backstory
analyst = Agent(
    backstory=inject_agent_context(["okrs", "mission-alignment"]),
)
```

---

## Corpus Structure

```
core/
├── mission-vision/          # Mission, vision, purpose, north star
├── roles-responsibilities/  # Product Owner, Scrum Master, CTO, etc.
├── leadership-frameworks/   # Servant, transformational, situational, etc.
├── governance/              # RACI, decision rights, escalation paths
├── culture-values/          # Psychological safety, trust, belonging
├── strategy-execution/      # OKRs, Cynefin, strategy maps, etc.
└── industry/                # Sector-specific entries
    ├── tech-startup/        # Product–Market Fit, and more
    ├── enterprise/          # Digital Transformation, and more
    └── nonprofit/           # Theory of Change, and more
```

See [Corpus Index](docs/index.md) for all 34 current entries.

---

## Current Status

- **34 validated entries** — 31 core entries across 6 categories + 3 industry entries (tech-startup, enterprise, nonprofit), all passing automated validation + test suite
- Python package with `load()`, `inject()`, `list_entries()`, and full metadata (`authors`, `references`, `deprecated`, `to_dict()`)
- LangGraph and CrewAI integrations
- Multi-agent workflow with AGENT.md, issue templates, and CI validation
- PyPI release in progress

---

## Contributing

We welcome contributions from leadership coaches, PMs, engineers, and agent builders.

[→ Read the Contribution Guide](./CONTRIBUTING.md)  
[→ Browse open issues](https://github.com/sevasek/orgcontext/issues)  
[→ Entry Format Specification](./docs/entry-format.md)  
[→ Entry template](./docs/entry-template.md)

**Quick contribution path:**
1. Fork the repo
2. Copy `docs/entry-template.md` into the right `core/` subdirectory
3. Fill it out — especially the `## Prompt Snippet` section
4. Run `python scripts/validate_entry.py --all` to verify
5. Open a PR with the label `new-entry`

---

## Roadmap

> [Open issues](https://github.com/sevasek/orgcontext/issues) are the source of truth for all planned work.

| Phase | Focus | Status |
|-------|-------|--------|
| **Now** | Entry format, 31 quality core entries, Python package, test suite, multi-agent workflow | ✅ Complete |
| **Short-term** | Industry packs (3 initial entries ✅), PyPI release, additional integrations | In progress |
| **Medium-term** | Versioning, RAG-friendly embeddings, MCP server support | Planned |
| **Longer-term** | Enterprise sync tools, hosted corpus API | Planned |

**Next contributions welcome:**  
Industry packs: more entries under `tech-startup/`, `enterprise/`, `nonprofit/`  
New sectors: `healthcare/`, `education/`, `government/`  
Integrations: LlamaIndex, AutoGen, OpenAI Agents SDK

---

## License

MIT — free for personal, commercial, and agent use.  
[Full license](./LICENSE)

---

## Citation

```bibtex
@misc{orgcontext2026,
  title        = {OrgContext: The LLM-native organizational context dictionary},
  year         = {2026},
  url          = {https://github.com/sevasek/orgcontext}
}
```
