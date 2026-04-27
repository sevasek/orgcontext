# Entry Format Specification

This document defines the complete schema for OrgContext entries. All entries must conform to this spec to pass automated validation.

---

## File Naming

- Location: `core/<category>/<slug>.md` or `industry/<sector>/<slug>.md`
- Slug: lowercase, hyphen-separated, no special characters
- Examples: `servant-leadership.md`, `product-owner.md`, `okrs.md`

---

## Frontmatter Schema

```yaml
---
id: string                  # REQUIRED. Matches filename without extension.
title: string               # REQUIRED. Human-readable title, title case.
category: enum              # REQUIRED. See categories below.
tags: string[]              # REQUIRED. 3–6 lowercase tags.
related: string[]           # OPTIONAL. IDs of related core entries.
version: semver             # REQUIRED. Starts at 1.0.0.
last_updated: YYYY-MM-DD   # REQUIRED. Date of last substantive edit.
authors: string[]           # OPTIONAL. GitHub usernames of contributors.
sources: string[]           # OPTIONAL. Canonical references.
deprecated: boolean         # OPTIONAL. Default false.
parent: string              # OPTIONAL. Industry fork only. ID of parent core entry.
---
```

### Valid Categories

| Category | Use for |
|----------|---------|
| `mission-vision` | Mission, vision, purpose, BHAG, north star, organizational identity |
| `roles-responsibilities` | Named roles and their decision rights, accountabilities, boundaries |
| `leadership-frameworks` | Leadership styles, models, theories applied in organizational settings |
| `governance` | Decision-making structures, RACI, escalation, committees |
| `culture-values` | Psychological safety, trust, belonging, norms, rituals |
| `strategy-execution` | Strategy frameworks, OKRs, portfolio management, execution patterns |

---

## Required Sections

Every entry must include all of these sections in this order:

### 1. `## Definition`
- **Length:** 50–300 words
- **Voice:** Third-person neutral, declarative
- **Rule:** Every technical term used must be defined within the entry or linked to another entry

### 2. `## When to Apply`
- **Format:** Bulleted list, 3–6 items
- **Pattern:** `**Context label:** Description of organizational situation`

### 3. `## Decision Heuristics`
- **Format:** Bulleted list, 3–7 items
- **Pattern:** If/when/before conditional → concrete action
- **Rule:** Must be actionable by an LLM agent, not just descriptive

### 4. `## Counter-Examples / Anti-Patterns`
- **Format:** Bulleted list, 2–5 items
- **Rule:** Must distinguish this term from at least one commonly confused concept

### 5. `## Prompt Snippet`
- **Format:** Fenced code block (` ```  ``` `)
- **Length:** 30–150 words
- **Rule:** Must be self-contained — an agent should be able to use it with no other context from this entry
- **Structure:** Definition → When relevant → Key distinctions → Apply by

### 6. `## See Also`
- **Format:** Relative links to other entries + external references
- **Rule:** At least one external canonical source cited

---

## Word Count Limits

| Section | Min | Max |
|---------|-----|-----|
| Definition | 50 | 300 |
| Prompt Snippet | 30 | 150 |
| Total entry | 300 | 1,200 |

Entries over 1,200 words are usually trying to cover too much — split into two entries.

---

## Versioning Rules

Increment version when:

| Change | Version bump |
|--------|-------------|
| Typo, grammar, formatting | PATCH (1.0.x) |
| New section, new examples, new heuristics | MINOR (1.x.0) |
| Definition change, schema breaking change | MAJOR (x.0.0) |

---

## Validation

Run locally:

```bash
python scripts/validate_entry.py core/<category>/<slug>.md

# Validate all entries
python scripts/validate_entry.py --all
```

CI runs validation on every PR automatically.
