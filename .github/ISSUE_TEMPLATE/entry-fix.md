---
name: "Entry Fix"
description: "Edit, correct, or improve an existing OrgContext entry"
title: "[Fix] <entry-slug>"
labels: ["entry:fix", "status:ready"]
---

## Entry
<!-- Which entry needs fixing? Include the slug (e.g., servant-leadership) -->

## Problem
<!-- What is wrong or could be improved? -->

## Proposed Change
<!-- Describe the specific changes you want made -->

## Acceptance Criteria
- [ ] Updated entry still passes `python scripts/validate_entry.py --all`
- [ ] Changes improve accuracy, clarity, or agent-readiness
- [ ] Version number bumped appropriately in frontmatter (PATCH for typos, MINOR for content additions, MAJOR for definition changes)
- [ ] `last_updated` date refreshed
