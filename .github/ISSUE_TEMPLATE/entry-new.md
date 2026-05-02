---
name: "New Entry"
description: "Request or propose a new OrgContext entry"
title: "[Entry] <term name>"
labels: ["entry:new", "status:ready"]
---

## Term
<!-- What is the term or concept? -->

## Category
<!-- Choose one: mission-vision, roles-responsibilities, leadership-frameworks, governance, culture-values, strategy-execution -->

## Brief Description
<!-- 2-3 sentences explaining what this concept is and why it belongs in OrgContext -->

## Why This Matters for Agents
<!-- Why would an LLM agent need this concept to function correctly? What goes wrong without it? -->

## Key Sources
<!-- Books, papers, canonical references -->
- 

## Acceptance Criteria
- [ ] File created at `core/<category>/<slug>.md`
- [ ] All 6 required sections present (Definition, When to Apply, Decision Heuristics, Counter-Examples / Anti-Patterns, Prompt Snippet, See Also)
- [ ] `python scripts/validate_entry.py --all` passes with no errors
- [ ] Prompt snippet is agent-ready (self-contained, 30-150 words)
- [ ] Entry added to project board with priority label
