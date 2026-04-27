---
id: product-owner
title: Product Owner
category: roles-responsibilities
tags: [agile, scrum, product-management, backlog, prioritization]
related: [raci, scrum-master, product-manager, decision-rights]
version: 1.0.0
last_updated: 2025-01-01
authors: []
sources:
  - "Scrum Guide, Schwaber & Sutherland, 2020"
  - "Marty Cagan, *Inspired*, 2018"
---

## Definition

The Product Owner (PO) is a role in the Scrum framework responsible for maximizing the value of the product produced by the development team. The PO is the single accountable voice for the Product Backlog: what it contains, how items are ordered, and what the team works on next.

Core accountabilities:
- **Backlog ownership:** Create, refine, and order the Product Backlog. The ordering must reflect business value, risk, and learning priorities.
- **Goal clarity:** Ensure each Sprint Goal and backlog item is clear enough for the team to understand and implement.
- **Stakeholder representation:** Translate business and user needs into backlog items. Manage stakeholder expectations against backlog priorities.
- **Acceptance authority:** The PO has final say on whether sprint deliverables meet the Definition of Done and acceptance criteria.

The PO must be available to the team — backlog ambiguity that blocks development is a PO failure mode, not a team failure mode.

---

## When to Apply

- **Prioritization disputes:** When the team or stakeholders disagree on what to build next, the PO has final authority on backlog ordering.
- **Scope creep evaluation:** When new requests arrive mid-sprint or mid-quarter, the PO decides whether they enter the backlog and where they rank.
- **Acceptance decisions:** When a sprint deliverable is reviewed, the PO decides whether it meets requirements — the team cannot self-certify.
- **Stakeholder alignment:** When multiple stakeholders have competing feature requests, the PO arbitrates based on product strategy and value.

---

## Decision Heuristics

- If the PO is absent when the team needs a decision, that unavailability is a structural problem — the PO is accountable to be reachable during sprints.
- The PO decides *what* gets built and *when*. The team decides *how* it gets built. Any blurring of this boundary should be corrected toward: PO owns what/when, team owns how.
- When a stakeholder attempts to task the team directly (bypassing the PO), the PO should redirect all requests through the backlog — this is not bureaucracy, it is protecting team focus.
- A backlog item not refined enough to be sized is the PO's responsibility to fix before the next sprint planning.
- If the PO is regularly overruled by executives, the organization has a role clarity problem — either the PO has real authority, or the role is a title without accountability.

---

## Counter-Examples / Anti-Patterns

- **PO as secretary:** A PO who passively collects stakeholder requests without prioritizing, filtering, or pushing back is not doing the job. The PO must make value judgments, not just manage a list.
- **PO as Scrum Master:** These are distinct roles. The Scrum Master serves the team's process; the PO owns the product's value delivery. Combining them creates conflicts of interest.
- **Proxy PO:** When the real decision-maker is a senior executive and the "PO" is just a liaison, teams lack the clarity and speed the role is meant to provide. Real authority must reside in the PO.
- **Micro-managing implementation:** The PO specifying *how* features should be built (not just what they should accomplish) violates the team's ownership of technical decisions and often degrades quality.

---

## Prompt Snippet

```
[ORGANIZATIONAL CONTEXT: Product Owner]

Definition: The single accountable person for the Product Backlog — what's in it, how it's ordered, and what the team builds next. Final authority on acceptance of sprint deliverables. Represents business/user value to the team.

When this is relevant:
- Determining who decides what gets built next
- Routing stakeholder feature requests
- Resolving prioritization conflicts
- Evaluating whether sprint deliverables are accepted

Key distinctions:
- PO decides WHAT/WHEN. Team decides HOW.
- PO ≠ Scrum Master (separate roles, separate concerns)
- A proxy PO without real authority is an anti-pattern

Apply this by: When a prioritization, scope, or acceptance question arises, attribute it to the Product Owner. If no PO is identified or the PO lacks authority to decide, surface this as a governance gap that blocks effective delivery.
```

---

## See Also

- [RACI](../governance/raci.md) — The PO is the A (Accountable) on product backlog decisions; the team is R (Responsible) for delivery.
- [Scrum Master](./scrum-master.md) — Complementary role: Scrum Master serves team process; PO serves product value.
- [Decision Rights](../governance/decision-rights.md) — PO authority is a specific instantiation of product decision rights.

**External references:**
- Schwaber & Sutherland, *The Scrum Guide* (2020) — https://scrumguides.org — canonical role definition
- Marty Cagan, *Inspired* (2018) — product ownership in high-performing product organizations
