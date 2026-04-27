# Contributing to OrgContext

Thank you for helping build the standard organizational context library for LLM agents. This guide explains how to add entries, fix errors, and contribute industry forks.

---

## Table of Contents

1. [Before You Contribute](#before-you-contribute)
2. [Types of Contributions](#types-of-contributions)
3. [Adding a New Entry](#adding-a-new-entry)
4. [Editing an Existing Entry](#editing-an-existing-entry)
5. [Adding an Industry Fork](#adding-an-industry-fork)
6. [Quality Bar](#quality-bar)
7. [Review Process](#review-process)
8. [Style Guide](#style-guide)

---

## Before You Contribute

**Check what we're NOT:** OrgContext is strictly about *organizational and leadership concepts*. We reject entries that are:

- General business jargon ("synergy, "bandwidth")
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
| New industry fork entry | `industry/` | `industry-fork` |
| Schema / tooling | `tooling/` | `tooling` |
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

```bash
pip install orgcontext[dev]
python scripts/validate_entry.py core/<category>/<your-term>.md
```

The validator checks:
- All required frontmatter fields are present
- `related` entries exist in the corpus
- `version` follows semver
- Word count is within limits (definition: 50–300 words; prompt snippet: 30–150 words)

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

## Adding an Industry Fork

Industry forks extend core entries with domain-specific context. They live in `industry/<sector>/`.

Fork entries must:
1. Reference a parent core entry in frontmatter: `parent: servant-leadership`
2. Only *extend* (not contradict) the parent definition
3. Be maintained by at least one domain expert (list yourself in `CODEOWNERS`)

Example sectors: `tech-startup`, `enterprise`, `healthcare`, `nonprofit`, `financial-services`, `government`.

---

## Quality Bar

Before a PR is merged, maintainers check:

- [ ] **Accurate** — Definition matches mainstream practitioner usage, not just one school of thought
- [ ] **Balanced** — Counter-examples and anti-patterns are included
- [ ] **Agent-ready** — Prompt snippet is written for an LLM, not a human reader
- [ ] **Cited** — At least one real-world source or canonical framework cited in `## See Also`
- [ ] **Narrow scope** — Not trying to cover more than one concept
- [ ] **No jargon in definitions** — Define every technical term used in the entry

---

## Review Process

1. Automated validation runs on PR open
2. One maintainer reviews within 7 days
3. One community review (any contributor with ≥2 merged entries)
4. Merged on approval; version bump in next release

If a PR gets no review in 7 days, tag `@orgcontext/maintainers` in a comment.

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
