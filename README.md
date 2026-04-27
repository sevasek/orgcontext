# OrgContext

> **A growing, LLM-native dictionary of mission, vision, roles, leadership frameworks, and organizational concepts.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](./CONTRIBUTING.md)

---

## Why OrgContext?

LLM agents often fail not because they lack intelligence, but because they lack **shared organizational grounding**. Terms like "strategic alignment," "Product Owner," or "servant leadership" get interpreted differently across prompts, agents, or sessions.

OrgContext aims to provide a reusable, community-curated corpus of clear definitions, decision heuristics, anti-patterns, and ready-to-inject prompt snippets for these concepts.

Think of it as a living reference library that you can load into your agents, RAG pipelines, or system prompts — the same way you import code libraries.

| Without OrgContext | With OrgContext |
|--------------------|-----------------|
| "Strategic alignment" means whatever the model guesses | Precise definition + decision heuristics + anti-patterns |
| Role ambiguity: "What does a Product Owner *actually* decide?" | Canonical scope, escalation rules, RACI mapping |
| Leadership model mismatch across agents | Shared, versioned, injectable leadership vocabulary |
| Custom `company-context.md` reinvented per project | One community-maintained corpus |
| Multi-agent systems with conflicting interpretations | Single shared lexicon loaded the same way everywhere |

---

## Current Status
- Core ideas and entry format are defined.
- A few starter Markdown entries in `core/`.
- Early Python utilities for loading and injecting context.
- Open to contributions for new entries and integrations.
This is an early-stage / MVP project. The vision is big, but we're starting small and iterating in public.

---

## Quick Start

### Install

```bash
git clone https://github.com/sevasek/orgcontext.git
cd orgcontext
```
Each entry is a self-contained Markdown file with a Prompt Snippet section ready for direct use.

#### Copy-paste
Prototype the integration of OrgContext by copy-pasting the Prompt Snippet section into your agent prompts.

#### Point
You can also point any RAG/vector store directly at the `core/` directory.

#### Load
Simple loader example:
```python
import pathlib

def load_entry(relative_path: str) -> str:
    path = pathlib.Path(f"core/{relative_path}.md")
    return path.read_text(encoding="utf-8")

context = load_entry("leadership-frameworks/servant-leadership")
print(context)
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
└── strategy-execution/      # OKRs, Cynefin, strategy maps, etc.

industry/
├── tech-startup/            # Velocity, runway, PMF, growth loops
├── enterprise/              # Steering committees, change management
└── nonprofit/               # Theory of change, impact measurement

```
See [Index](/docs/index.md) for current entries.

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
4. Open a PR with the label `new-entry`

---

## Roadmap

| Target | Milestone |
|--------|-----------|
| Now | Solid entry format + 10–20 high-quality starter entries + basic loaders. |
| Short-term | Python package on PyPI, more entries, initial integrations (LangGraph, CrewAI, etc.). |
| Medium-term | Versioning, RAG-friendly embeddings, MCP/server support. |
| Longer-term | Industry-specific packs, enterprise sync tools. |

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
