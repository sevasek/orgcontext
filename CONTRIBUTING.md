# Contributing to OrgContext

Thank you for helping build the standard organizational context library for LLM agents. This guide explains how to add entries, fix errors, and improve the project.

---

## Table of Contents
1. [Development Setup](#development-setup)
2. [Before You Contribute](#before-you-contribute)
3. [Types of Contributions](#types-of-contributions)
4. [Adding a New Entry](#adding-a-new-entry)
5. [Editing an Existing Entry](#editing-an-existing-entry)
6. [Quality Bar](#quality-bar)
7. [Review Process](#review-process)
8. [Style Guide](#style-guide)
9. [Code of Conduct](#code-of-conduct)

---

## Development Setup

```bash
git clone https://github.com/sevasek/orgcontext.git
cd orgcontext
pip install -e ".[dev]"
```

---

## Before You Contribute

**Check what we're NOT:** OrgContext is strictly about *organizational and leadership concepts*. We reject entries that are:

- General business jargon ("synergy", "bandwidth")
- Generic project management terms already covered by PMI/PMBOK docs
- Industry-specific technical terms (code architecture, financial instruments, etc.) — these belong in industry forks
- Academic or purely theoretical frameworks with no practitioner application

If in doubt, open an issue and ask before writing the entry.

**Check for duplicates:** Search existing entries and open issues before starting.

---

## Types of Contributions

| Type | Branch prefix | Label |
|------|--------------|-------|
| New core entry | `entry/` | `new-entry` |
| Edit / fix existing | `fix/` | `entry-fix` |
| Core tooling / Python package | `tooling/` | `tooling` |
| Documentation | `docs/` | `docs` |

---

## Adding a New Entry

### Step 1: Pick a category

```
core/mission-vision/          → mission, vision, purpose, BHAG, north star
core/roles-responsibilities/  → named roles (Product Owner, CTO, Scrum Master…)
core/leadership-frameworks/   → servant leadership, transformational, situational…
core/governance/              → RACI, decision rights, escalation, OKRs
core/culture-values/          → psychological safety, trust, DEI, belonging
core/strategy-execution/      → strategy maps, Cynefin, portfolio management
```

### Step 2: Copy the template

```bash
cp docs/entry-template.md core/<category>/<your-term-slug>.md
```

Use lowercase-hyphenated slugs: `servant-leadership`, `product-owner`, `okr`.

### Step 3: Fill out every section

The **Prompt Snippet** section is the most important — it's what agents actually use. Write it as if you're pasting it into a system prompt. Be concrete, imperative, and brief.

### Step 4: Validate

Carefully review your entry against the [entry template](./docs/entry-template.md) and the [Quality Bar](#quality-bar) below.

### Step 5: Open a PR

- Title: `[New Entry] Your Term Name`
- Label: `new-entry`
- Fill out the PR template

---

## Editing an Existing Entry

- **Typo / clarity fix** → open a PR directly, label `entry-fix`
- **Meaning change or significant rewrite** → open an issue first to discuss
- **Deprecating a term** → never delete; add `deprecated: true` to frontmatter and a `## Superseded By` section

---

## Quality Bar

Before a PR is merged, maintainers check:

- [ ] **Accurate** — Definition matches mainstream practitioner usage, not just one school of thought
- [ ] **Balanced** — Counter-examples and anti-patterns are included
- [ ] **Agent-ready** — Prompt snippet is written for an LLM, not a human reader
- [ ] **Narrow scope** — Not trying to cover more than one concept

---

## Review Process

1. Automated validation runs on PR open
2. One maintainer reviews within 7 days
3. Merged on approval

If a PR gets no review in 7 days, ping the repository owner in a comment.

---

## Style Guide

- **Voice:** Second-person, imperative for prompt snippets ("When the agent encounters X, it should…"). Third-person neutral for definitions.
- **Length:** Definitions: 50–300 words. Prompt snippets: 30–150 words. Heuristics: 3–7 bullet points.
- **Examples:** Prefer concrete, company-agnostic scenarios. Use placeholder names: "Acme Corp," "Team Alpha."
- **No editorializing:** Don't say a framework is "better" than another. Present tradeoffs.
- **Markdown only:** No HTML. No images. Tables are fine.
- **Oxford comma:** Always.

---

## Code of Conduct

Be kind. Disagreements about definitions are common in org/leadership theory — that's expected and healthy. What's not acceptable: dismissiveness, gatekeeping, or treating any one methodology as the only valid approach.

This project follows the [Contributor Covenant](https://www.contributor-covenant.org/version/2/1/code_of_conduct/).
