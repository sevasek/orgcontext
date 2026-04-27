# OrgContext

> **The LLM-native dictionary of mission, vision, roles, leadership frameworks, and organizational concepts.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Entries](https://img.shields.io/badge/entries-60%2B-blue)](./core/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](./CONTRIBUTING.md)

---

## Why OrgContext?

Agent failures are rarely about raw intelligence — they're about missing **organizational grounding**.

| Without OrgContext | With OrgContext |
|--------------------|-----------------|
| "Strategic alignment" means whatever the model guesses | Precise definition + decision heuristics + anti-patterns |
| Role ambiguity: "What does a Product Owner *actually* decide?" | Canonical scope, escalation rules, RACI mapping |
| Leadership model mismatch across agents | Shared, versioned, injectable leadership vocabulary |
| Custom `company-context.md` reinvented per project | One community-maintained corpus, pinnable by version |
| Multi-agent systems with conflicting interpretations | Single shared lexicon loaded the same way everywhere |

**OrgContext makes organizational context as reusable and reliable as code libraries.**

---

## Quick Start

### Python

```bash
pip install orgcontext
```

```python
from orgcontext import load, inject

# Load a single entry
entry = load("servant-leadership")
print(entry.definition)
print(entry.prompt_snippet)

# Inject multiple entries into a prompt
context = inject(["mission-alignment", "okrs", "raci"])
# → Ready-to-paste prompt block with definitions + heuristics
```

### Direct Markdown / RAG

Every entry is a self-contained Markdown file. Point your RAG pipeline at `./core/` or load files directly:

```python
import pathlib
entry = pathlib.Path("core/leadership-frameworks/servant-leadership.md").read_text()
```

### LangGraph State Injection

```python
from orgcontext.integrations.langgraph import OrgContextNode

graph.add_node("context", OrgContextNode(entries=["product-owner", "okrs"]))
```

### CrewAI Skill Loader

```python
from orgcontext.integrations.crewai import org_context_tool

researcher = Agent(
    role="Strategy Analyst",
    tools=[org_context_tool(entries=["mission-alignment", "cynefin"])]
)
```

### MCP Server

```bash
npx orgcontext-mcp --entries core/
# Exposes: orgcontext://lookup/{term}
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

integrations/
├── crewai/
├── langgraph/
├── autogen/
└── mcp/
```

---

## Entry Format

Every entry follows the same schema — designed to be pasted directly into prompts:

```markdown
---
id: servant-leadership
title: Servant Leadership
category: leadership-frameworks
tags: [leadership, management, culture]
related: [transformational-leadership, psychological-safety, trust]
version: 1.0.0
last_updated: 2025-01-01
---

## Definition
...

## When to Apply
...

## Decision Heuristics
...

## Counter-Examples / Anti-Patterns
...

## Prompt Snippet
> [Paste this block directly into an agent system prompt]
...

## See Also
...
```

[→ Full entry spec](./docs/entry-format.md)

---

## Versioning

OrgContext uses [Semantic Versioning](https://semver.org/):

- **PATCH** (1.0.x): Typo fixes, clarifications that don't change meaning
- **MINOR** (1.x.0): New entries, backward-compatible additions
- **MAJOR** (x.0.0): Breaking changes to entry schema or significant re-definitions

Pin to a version in your agent config:

```yaml
# agent.yaml
orgcontext_version: "1.2.3"
entries:
  - mission-alignment
  - servant-leadership
  - okrs
```

---

## Contributing

We welcome contributions from leadership coaches, PMs, engineers, and agent builders.

[→ Read the Contribution Guide](./CONTRIBUTING.md)  
[→ Browse open issues](https://github.com/your-org/orgcontext/issues)  
[→ Entry template](./docs/entry-template.md)

**Quick contribution path:**
1. Fork the repo
2. Copy `docs/entry-template.md` into the right `core/` subdirectory
3. Fill it out — especially the `## Prompt Snippet` section
4. Open a PR with the label `new-entry`

---

## Roadmap

| Milestone | Target |
|-----------|--------|
| MVP: 60+ core entries + Python loader | Q1 2025 |
| v1.0: Semantic versioning + MCP server | Q2 2025 |
| 200+ entries + industry forks | Q3 2025 |
| RAG embeddings + fine-tuning dataset | Q4 2025 |
| Enterprise sync (Notion, Confluence) | 2026 |

---

## License

MIT — free for personal, commercial, and agent use.  
[Full license](./LICENSE)

---

## Citation

```bibtex
@misc{orgcontext2025,
  title        = {OrgContext: The LLM-native organizational context dictionary},
  year         = {2025},
  url          = {https://github.com/your-org/orgcontext}
}
```
