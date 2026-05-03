# Agent Operating Guide — OrgContext

You are working on **OrgContext** — a curated corpus of organizational and leadership concepts designed to ground LLM agents. This document tells you how to find work, implement it, validate it, and submit it.

---

## Scope of Work

Agents are authorized to work on:

| Task Type | Description | Where It Lives |
|-----------|-------------|----------------|
| **New Entry** | Write a new OrgContext entry | `core/<category>/<slug>.md` |
| **Entry Fix** | Edit, correct, or improve an existing entry | `core/<category>/<slug>.md` |
| **Tooling** | Python package, loaders, scripts | `orgcontext/`, `scripts/`, `tests/` |
| **Docs** | README, contributing guides, templates | `docs/`, `README.md`, `CONTRIBUTING.md` |
| **Infra** | CI workflows, repo config, project setup | `.github/`, `pyproject.toml` |

Do NOT work on entries outside organizational/leadership scope (e.g. general business jargon, industry-specific technical terms). If unsure, read `docs/entry-format.md` and `CONTRIBUTING.md`.

---

## Finding Work

GitHub Issues are the **single source of truth** for agent work. Use the GitHub CLI:

```bash
# Find ready, unassigned issues — your primary work queue
gh issue list --label "status:ready" --search "no:assignee" --json number,title,labels

# Filter by category
gh issue list --label "entry:new" --search "no:assignee" --state open
gh issue list --label "tooling" --search "no:assignee" --state open

# View a specific issue (full body, comments, acceptance criteria)
gh issue view <N> --comments
```

Rules:
- Only pick up issues with the `status:ready` label. Open issues without it are still in backlog and not yet scoped for an agent.
- Never pick up an issue that already has an assignee — that means another agent or contributor has claimed it.
- The "OrgContext Roadmap" project board, if present, is a human-only kanban view. Agents do not need to read it or update it.

---

## Claiming Work

Before you start:

1. **Assign yourself and clear the ready label** in one command — this is the atomic claim:
   ```bash
   gh issue edit <N> --add-assignee "@me" --remove-label "status:ready"
   ```
   Removing `status:ready` prevents another agent from racing to claim the same issue. The assignee field is now the signal that work is in progress — no separate label needed.

2. **Comment** on the issue:
   ```
   Claiming this issue. Starting work now.
   ```

Never work on an issue that already has an assignee. If you need a task that is assigned, ask the coordinator — do not steal it.

---

## Codebase Map

```
orgcontext/
├── core/                           # OrgContext entries (Markdown)
│   ├── mission-vision/
│   ├── roles-responsibilities/
│   ├── leadership-frameworks/
│   ├── governance/
│   ├── culture-values/
│   └── strategy-execution/
├── docs/                           # Documentation
│   ├── entry-format.md             # Entry schema specification
│   ├── entry-template.md           # Template for new entries
│   ├── index.md                    # Auto-generated corpus index
│   └── PROJECT-GUIDE.md            # Coordinator reference
├── integrations/                   # Framework integrations
│   ├── langgraph/
│   └── crewai/
├── orgcontext/                     # Python package
│   └── __init__.py                 # load(), inject(), list_entries()
├── scripts/
│   ├── validate_entry.py           # Entry validation
│   └── build_index.py              # Index generator
├── tests/                          # Test suite
│   └── test_core.py
├── AGENT.md                        # This file
├── CONTRIBUTING.md                 # Human contribution guide
├── README.md                       # Project overview
└── pyproject.toml                  # Build config, dev deps
```

### Where New Files Go

- **New entry**: `core/<category>/<slug>.md` (copy `docs/entry-template.md`)
- **New test**: `tests/test_<module>.py`
- **New script**: `scripts/<name>.py`
- **New integration**: `integrations/<framework>/<file>.py`

---

## Validation Checklist

Run these **before** opening any PR. All must be green.

### If you touched entries (`core/`):

```bash
python scripts/validate_entry.py --all
```

Expected output: `All X entries valid.` with no errors.

### If you touched Python code (`orgcontext/`, `scripts/`, `tests/`):

```bash
pytest tests/ -v
ruff check orgcontext/ scripts/ tests/
```

Expected output: `X passed in ...` and `All checks passed!`

### If you touched the index (`docs/index.md`):

```bash
python scripts/build_index.py
```

Verify the generated index looks correct.

---

## PR Protocol

### Branch Naming

```
entry/<slug>              — new entry (e.g., entry/psychological-safety)
fix/<slug>                — entry fix (e.g., fix/cynefin-word-count)
tooling/<description>     — code changes (e.g., tooling/test-suite)
docs/<description>        — documentation (e.g., docs/agent-guide)
infra/<description>       — infrastructure (e.g., infra/ci-workflow)
```

### Commit Messages

Use conventional commits:

```
fix: trim cynefin prompt snippet to meet word limit
feat: add crewai integration with org_context_tool
docs: add AGENT.md for multi-agent workflow
chore: update index with new entries
test: add test suite for core package
```

### PR Body

```markdown
## Summary
<1-2 sentences describing what this PR does>

## Type
- [ ] New entry
- [ ] Entry fix
- [ ] Tooling
- [ ] Documentation
- [ ] Infrastructure

## Validation
- [ ] `python scripts/validate_entry.py --all` passes (if entry changes)
- [ ] `pytest tests/ -v` passes (if code changes)
- [ ] `ruff check .` passes (if code changes)

## Checklist
- [ ] Follows entry format spec (if new/edited entry)
- [ ] All required sections present (if new/edited entry)
- [ ] Prompt snippet is agent-ready (if new/edited entry)

Fixes #<issue-number>
```

---

## Review Rule

**You MUST NOT approve your own pull request.** All changes require review from a third party or the repository maintainer. This is non-negotiable.

After opening your PR:

1. Make sure the PR body contains `Fixes #<issue-number>` so GitHub links the PR to the issue and auto-closes it on merge.
2. Leave a comment on the issue: `PR opened: #<pr-number>. Ready for review.`
3. Wait for approval before merging. Do not merge your own code.

---

## Escalation

If you are blocked:

1. **Comment** on the issue with a clear description of what is blocking you and what you have already tried
2. **Add the `status:blocked` label and unassign yourself** so the coordinator can see the issue is parked, not actively progressing:
   ```bash
   gh issue edit <N> --add-label "status:blocked" --remove-assignee "@me"
   ```
3. If the blocker requires a decision (ambiguous spec, conflicting guidance), also add the `needs-decision` label and wait for the coordinator

Common blockers:
- Entry scope is unclear or overlaps with existing entry
- Validation rules conflict with content requirements
- Missing acceptance criteria in the issue
- Dependencies on other issues that are not yet resolved

---

## Entry Writing Guidelines

When creating or editing an entry:

1. **Read** `docs/entry-template.md` for the exact structure
2. **Read** `docs/entry-format.md` for the full specification
3. **Check** `docs/index.md` to avoid duplicates
4. **Follow** the quality bar from `CONTRIBUTING.md`:
   - Accurate: matches mainstream practitioner usage
   - Balanced: includes anti-patterns and counter-examples
   - Agent-ready: prompt snippet is written for an LLM
   - Narrow scope: one concept per entry

---

## Quick Reference

| Need | Command |
|------|---------|
| List ready, unassigned tasks | `gh issue list --label "status:ready" --search "no:assignee"` |
| View issue details | `gh issue view <N> --comments` |
| Claim an issue (atomic) | `gh issue edit <N> --add-assignee "@me" --remove-label "status:ready"` |
| Mark blocked | `gh issue edit <N> --add-label "status:blocked" --remove-assignee "@me"` |
| Validate entries | `python scripts/validate_entry.py --all` |
| Run tests | `pytest tests/ -v` |
| Run linter | `ruff check orgcontext/ scripts/ tests/` |
| Rebuild index | `python scripts/build_index.py` |
| List available entries | `python -c "from orgcontext import list_entries; print(list_entries())"` |
