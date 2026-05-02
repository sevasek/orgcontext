# Project Guide — OrgContext Roadmap

This document is for the **coordinator** (human or agent) managing the OrgContext project via GitHub Projects.

---

## Project Board Setup

Create a GitHub Project board named **OrgContext Roadmap** with the following configuration:

### Columns (Kanban Layout)

| Column | Purpose |
|--------|---------|
| **Backlog** | Ideas, future entries, unscoped work. Not yet ready for agents. |
| **Ready** | Scoped issues with clear acceptance criteria. Agents should pull from here. |
| **In Progress** | An agent has claimed the issue and is actively working on it. |
| **In Review** | A PR is open. Waiting for third-party or maintainer review. |
| **Done** | PR has been merged. Work is complete. |

### Label Taxonomy

Create these labels in the repository. They serve as the primary routing mechanism for agents.

#### Category Labels

| Label | Color | Use |
|-------|-------|-----|
| `entry:new` | `#0e8a16` | Create a new OrgContext entry |
| `entry:fix` | `#fbca04` | Edit or improve an existing entry |
| `tooling` | `#1d76db` | Python code, scripts, integrations |
| `docs` | `#5319e7` | README, guides, templates |
| `infra` | `#e99695` | CI, repo config, project setup |

#### Status Labels

| Label | Color | Use |
|-------|-------|-----|
| `status:ready` | `#0e8a16` | Issue is scoped and ready to be claimed |
| `status:blocked` | `#d73a4a` | Agent cannot proceed; needs human input |
| `needs-decision` | `#fbca04` | Ambiguity requires coordinator decision |

#### Priority Labels

| Label | Color | Use |
|-------|-------|-----|
| `priority:0` | `#b60205` | Critical — blocks other work or breaks validation |
| `priority:1` | `#d93f0b` | Important — should be done soon |
| `priority:2` | `#fbca04` | Nice to have — do when capacity allows |
| `priority:3` | `#fef2c0` | Someday — no urgency |

#### Special Labels

| Label | Color | Use |
|-------|-------|-----|
| `good-first-task` | `#7057ff` | Simple task for new agents to learn the workflow |
| `duplicate` | `#ffffff` | Issue duplicates another |
| `wontfix` | `#ffffff` | Deliberately not doing this |

### Setting Up Labels Quickly

Run this script from the repo root to create all labels at once:

```bash
python scripts/setup_labels.py
```

Or manually via `gh`:

```bash
# Category labels
gh label create "entry:new" --color 0e8a16
gh label create "entry:fix" --color fbca04
gh label create "tooling" --color 1d76db
gh label create "docs" --color 5319e7
gh label create "infra" --color e99695

# Status labels
gh label create "status:ready" --color 0e8a16
gh label create "status:blocked" --color d73a4a
gh label create "needs-decision" --color fbca04

# Priority labels
gh label create "priority:0" --color b60205
gh label create "priority:1" --color d93f0b
gh label create "priority:2" --color fbca04
gh label create "priority:3" --color fef2c0

# Special labels
gh label create "good-first-task" --color 7057ff
```

---

## Coordinator Workflow

### 1. Seed the Board

Create initial issues for known gaps using the issue templates. See `docs/index.md` → "Planned Entries" section for entry requests.

### 2. Prioritize

Assign priority labels to each issue. Use `priority:0` sparingly — only for things that block other work or break the build.

### 3. Move to Ready

Once an issue has clear acceptance criteria (all templates include these by default), move it from **Backlog** to **Ready**. Add the `status:ready` label.

Agents will pull from the **Ready** column. If something is in **Backlog**, agents will ignore it.

### 4. Monitor In Progress

Track what agents are working on. If an issue sits in **In Progress** for too long, check the issue comments for blocker reports.

### 5. Review

When a PR is opened, the card should be in **In Review**. Review the PR or delegate to a third party. Enforce the rule: **the author never approves their own code**.

### 6. Done

Once merged, the card moves to **Done**. If you use GitHub's `Fixes #N` convention in PR bodies, the issue auto-closes.

---

## Roadmap Synchronization

The README.md contains a high-level roadmap summary. Keep it in sync with the project board:

### When to Update

- After completing a milestone (column reaches a certain count or specific issues are done)
- When adding a new phase to the roadmap
- When priorities shift significantly

### How to Update

1. Review the **Done** column in the project board
2. Check the current roadmap table in `README.md`
3. Update the milestones to reflect reality
4. Commit with `docs: update roadmap to reflect completed work`

### Current Roadmap Milestones

| Phase | Focus | Indicators |
|-------|-------|------------|
| **Now** | Entry format, 10-20 quality entries, basic loaders, test suite | Core entries ≥ 15, tests passing |
| **Short-term** | PyPI package, more entries, framework integrations | `pip install orgcontext` works, 3+ integrations |
| **Medium-term** | Versioning, RAG embeddings, MCP/server support | Embedding pipeline, versioned entries |
| **Longer-term** | Industry-specific packs, enterprise sync tools | `industry/` directory populated |

---

## Agent Delegation Patterns

### Pattern 1: Batch Entry Creation

When you want multiple entries written in parallel:

1. Create issues for each entry using the `entry-new` template
2. Assign all to **Backlog**, then move to **Ready**
3. Agents will self-assign from **Ready** and work in parallel

### Pattern 2: Coordinated Refactoring

When a change spans multiple files (e.g., updating entry format):

1. Create a single issue with a checklist of all files to touch
2. Assign to a single agent (to avoid merge conflicts)
3. Mark as `priority:1` to ensure it gets picked up before parallel work

### Pattern 3: Fix Cascade

When a validation change might break existing entries:

1. Create the tooling issue first with `priority:0`
2. Create entry-fix issues for each broken entry, but keep them in **Backlog**
3. Once the tooling PR merges, move entry-fix issues to **Ready**

---

## Useful gh Commands for Coordinators

```bash
# List all open issues by category
gh issue list --label "entry:new"
gh issue list --label "tooling"

# List blocked issues
gh issue list --label "status:blocked"

# View issues needing decisions
gh issue list --label "needs-decision"

# List ready-to-work issues (what agents should see)
gh issue list --label "status:ready" --json number,title,assignees

# Check PRs awaiting review
gh pr list --state open --json number,title,reviewDecision

# Approve a PR (third-party review)
gh pr review <N> --approve

# Merge an approved PR
gh pr merge <N> --squash
```
