# Project Guide — OrgContext Roadmap

This document is for the **coordinator** — the human (or agent) that scopes work, sets priorities, and keeps the project moving. It explains how the task system works, who interacts with what, and how to set up an optional kanban board for human visibility.

> **TL;DR for coordinators:** GitHub Issues + Labels are the source of truth. Agents read and write issues only. A GitHub Project board is **optional and human-only** — if you use one, automate it from labels and PR state so nobody has to maintain it manually.

---

## How the System Works

| Layer | Audience | Tool | Purpose |
|-------|----------|------|---------|
| **Issues** | Agents and humans | `gh issue` | Atomic, claimable units of work with acceptance criteria |
| **Labels** | Agents and humans | `gh label`, `gh issue edit` | Routing, status, priority, and category |
| **Pull Requests** | Agents and humans | `gh pr`, `Fixes #N` | Review and merge; auto-closes the linked issue |
| **Project Board** *(optional)* | Humans only | GitHub web UI | Visual kanban; never read or written by agents |

Agents follow [AGENT.md](../AGENT.md), which defines the issues-and-labels contract. They never inspect, mutate, or rely on the project board.

### Why Not Use the Project Board for Agents?

GitHub Projects (v2) is a GraphQL-only API. Moving a card between columns requires resolving a project ID, item node ID, status field ID, and option ID, then issuing an `updateProjectV2ItemFieldValue` mutation via `gh api graphql`. Compare that to `gh issue edit N --add-label foo` — same outcome, vastly more reliable for an agent. Agents stick to issues; the board, if it exists, is a derived view for humans.

---

## Label Taxonomy

Labels carry **all** state that GitHub doesn't natively track. Issue state (open/closed), assignee, and linked PRs cover the rest.

### Category Labels — what kind of work?

| Label | Color | Use |
|-------|-------|-----|
| `entry:new` | `#0e8a16` | Create a new OrgContext entry |
| `entry:fix` | `#fbca04` | Edit or improve an existing entry |
| `tooling` | `#1d76db` | Python code, scripts, integrations |
| `docs` | `#5319e7` | README, guides, templates |
| `infra` | `#e99695` | CI, repo config, project setup |

### Status Labels — agent-readable signals

| Label | Color | Use |
|-------|-------|-----|
| `status:ready` | `#0e8a16` | Issue is scoped and claimable. Coordinator adds this when an issue is ready for an agent. Agent removes it on claim. |
| `status:blocked` | `#d73a4a` | Agent could not proceed. Coordinator must unblock. |
| `needs-decision` | `#fbca04` | Ambiguity that the coordinator must resolve before work continues. |

There is **deliberately no** `status:in-progress`, `status:in-review`, or `status:done` label. Those states are encoded in the natural GitHub model:

- **In progress** → open issue with an assignee
- **In review** → open issue with a linked open PR (via `Fixes #N` in the PR body)
- **Done** → issue is closed (auto-closes when the linked PR merges)

This keeps the label set minimal and avoids drift between labels and reality.

### Priority Labels

| Label | Color | Use |
|-------|-------|-----|
| `priority:0` | `#b60205` | Critical — blocks other work or breaks validation |
| `priority:1` | `#d93f0b` | Important — should be done soon |
| `priority:2` | `#fbca04` | Nice to have — do when capacity allows |
| `priority:3` | `#fef2c0` | Someday — no urgency |

### Special Labels

| Label | Color | Use |
|-------|-------|-----|
| `good-first-task` | `#7057ff` | Simple task for new agents to learn the workflow |
| `duplicate` | `#ffffff` | Issue duplicates another |
| `wontfix` | `#ffffff` | Deliberately not doing this |

### Setting Up Labels

```bash
python scripts/setup_labels.py
```

This is idempotent — re-running skips labels that already exist.

---

## Coordinator Workflow

### 1. Seed Issues

Use the issue templates in `.github/ISSUE_TEMPLATE/`:

- **New entries**: `New Entry` template (auto-applies `entry:new` and `status:ready`)
- **Entry fixes**: `Entry Fix` template (auto-applies `entry:fix` and `status:ready`)
- **Tooling, Docs, Infra**: respective templates

For unscoped ideas, open issues *without* `status:ready` so agents skip them until you've fleshed out the acceptance criteria.

### 2. Prioritize

Add a `priority:N` label to every actionable issue. Use `priority:0` sparingly — only for genuinely blocking work.

### 3. Promote to Ready

When an issue has clear acceptance criteria, ensure `status:ready` is on it. Agents poll:

```bash
gh issue list --label "status:ready" --search "no:assignee"
```

Anything not in that result set is invisible to agents.

### 4. Monitor Active Work

```bash
# Issues currently being worked on (have an assignee, still open)
gh issue list --assignee "*" --state open

# Open PRs (proxy for "in review")
gh pr list --state open
```

If an issue has been assigned for too long with no PR, comment to check status.

### 5. Review

When a PR opens with `Fixes #N`, GitHub automatically links it to the issue. Review the PR (or delegate to a third party).

> **Never approve a PR opened by yourself or by the same agent that wrote it.** This is enforced by [AGENT.md](../AGENT.md) and is non-negotiable.

### 6. Done

The merged PR auto-closes the issue. No manual cleanup needed.

### Handling Blocked Issues

When an agent adds `status:blocked`, they will also unassign themselves and leave a comment explaining what they tried. Your job:

1. Read the comment
2. Resolve the blocker (clarify spec, fix dependency, decide on ambiguity)
3. Remove `status:blocked`
4. Re-add `status:ready` so an agent can pick it up again

If the issue also has `needs-decision`, you're the decider — don't expect agents to choose for you.

---

## Optional: GitHub Project Board

You can keep a project board purely as a **human kanban view**. Agents never touch it, so it has to be either auto-driven or manually maintained.

### Recommended: Automated Board

Create a GitHub Project (v2) with a Status field whose options match the natural GitHub state model:

| Column | Driven by |
|--------|-----------|
| **Backlog** | Open issues without `status:ready` |
| **Ready** | Open issues with `status:ready` and no assignee |
| **In Progress** | Open issues with an assignee |
| **In Review** | Open issues with a linked open PR |
| **Done** | Closed issues |

Use GitHub's built-in [project workflows](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project) to move cards automatically:

- "Item added to project" → set status based on labels (e.g., `status:ready` → **Ready**, otherwise → **Backlog**)
- "Pull request opened that closes an issue" → set status to **In Review**
- "Pull request merged" → set status to **Done**

This keeps the board accurate without anyone (human or agent) updating it manually.

### If the Board Falls Out of Sync

**Trust the issues, not the board.** The board is a derived view; issues are the truth. The board is allowed to be slightly stale; never the other way around.

---

## Roadmap Synchronization

The README contains a high-level roadmap summary. Keep it in sync with reality.

### When to Update

- After completing a milestone
- When adding a new phase to the roadmap
- When priorities shift significantly

### How to Update

1. Review closed issues by category and milestone
2. Update the milestones in `README.md`
3. Commit with `docs: update roadmap to reflect completed work`

### Current Roadmap Milestones

| Phase | Focus | Indicators |
|-------|-------|------------|
| **Now** | Entry format, 10–20 quality entries, basic loaders, test suite | Core entries ≥ 15, tests passing |
| **Short-term** | PyPI package, more entries, framework integrations | `pip install orgcontext` works, 3+ integrations |
| **Medium-term** | Versioning, RAG embeddings, MCP/server support | Embedding pipeline, versioned entries |
| **Longer-term** | Industry-specific packs, enterprise sync tools | `industry/` directory populated |

---

## Coordination Patterns

### Pattern 1: Batch Entry Creation

When you want multiple entries written in parallel:

1. Create one issue per entry using the `New Entry` template
2. Add `priority:N` labels
3. Ensure each has `status:ready`
4. Agents will self-assign and work in parallel

### Pattern 2: Coordinated Refactoring

When a change spans multiple files (e.g., updating entry format):

1. Create a single issue with a checklist of all files to touch
2. Mark `priority:1`
3. Optionally pre-assign to a single agent to avoid merge conflicts

### Pattern 3: Fix Cascade

When a tooling change might break existing entries:

1. Create the tooling issue first with `priority:0`
2. Create entry-fix issues for each broken entry, but **do not** add `status:ready` yet
3. Once the tooling PR merges, add `status:ready` to the entry-fix issues so agents pick them up

---

## Useful gh Commands for Coordinators

```bash
# What's ready and waiting for an agent
gh issue list --label "status:ready" --search "no:assignee"

# What's currently being worked on
gh issue list --assignee "*" --state open

# What's blocked
gh issue list --label "status:blocked"

# What needs my decision
gh issue list --label "needs-decision"

# Open PRs awaiting review
gh pr list --state open --json number,title,reviewDecision

# Approve a PR (third-party review only — never on your own work)
gh pr review <N> --approve

# Merge an approved PR
gh pr merge <N> --squash
```
