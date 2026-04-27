---
id: raci
title: RACI (Responsible, Accountable, Consulted, Informed)
category: governance
tags: [governance, decision-rights, roles, accountability, coordination]
related: [decision-rights, product-owner, okrs, escalation-path]
version: 1.0.0
last_updated: 2026-04-27
authors: ["Paul Seville"]
references:
  - "Project Management Institute, *PMBOK Guide*"
  - "Smith & Erwin, *Role & Responsibility Charting (RACI)*, 2005"
---

## Definition

RACI is a responsibility assignment matrix that clarifies who does what on any given decision, task, or deliverable. Each letter represents a role:

- **R – Responsible:** The person (or people) who does the work. There can be multiple R's on a task.
- **A – Accountable:** The single person who owns the outcome and must answer for results. There must be exactly one A per item. The A approves what the R produces.
- **C – Consulted:** People whose input is sought before a decision or deliverable is finalized. Two-way communication. Their feedback should influence the outcome.
- **I – Informed:** People who are notified of decisions or outcomes after the fact. One-way communication. They don't influence the work but need visibility.

RACI removes ambiguity at handoff points, prevents duplication of effort and gaps in ownership, and clarifies escalation paths.

---

## When to Apply

- **New project kickoff:** Before work starts, a RACI matrix maps all major deliverables to the four roles.
- **Cross-functional initiatives:** When multiple teams or functions touch a deliverable, RACI prevents "everyone owns it, so no one owns it."
- **Decision audit:** When a team is slow or conflict-ridden, a RACI audit often reveals either multiple A's (competing accountability) or missing A's (no one owns it).
- **Onboarding:** A RACI chart for recurring decisions helps new team members understand where to go for what.

---

## Decision Heuristics

- Every item in a RACI matrix must have exactly one A. If you find two A's, escalate or arbitrate until one person is designated.
- If you're unsure whether someone is C or I, ask: "Would the outcome change based on their input?" Yes → C. No → I.
- Too many C's signal either a culture of over-consensus or a lack of clear decision authority. Audit and trim to genuine stakeholders.
- The A should have the authority to say yes or no to the R's output. If they don't, the accountability is misassigned.
- When a task stalls, ask: "Who is the A on this?" If no one can answer immediately, that's the root cause.

---

## Counter-Examples / Anti-Patterns

- **Diffuse accountability:** Phrases like "We're all accountable" violate RACI. True collective accountability usually means no one is accountable.
- **The A who delegates accountability:** The A can delegate work (to R's) but not accountability. If things go wrong, the A answers for it, even if someone else did the work.
- **Consulting everyone to avoid conflict:** When everyone is C, the consulted list loses meaning. Stakeholders who are always consulted but never change the outcome should be moved to I.
- **RACI as bureaucracy:** RACI on tiny tasks creates overhead without value. Apply it to decisions and deliverables with real ambiguity or cross-functional impact, not to every to-do.

---

## Prompt Snippet

```
[ORGANIZATIONAL CONTEXT: RACI]
Definition: A responsibility assignment matrix that clarifies ownership.
• R = Responsible (does the work, multiple allowed)
• A = Accountable (owns the outcome, exactly ONE per item)
• C = Consulted (two-way input, can influence the result)
• I = Informed (one-way notification, no influence)
Key rules:
• Exactly one A per task/decision — never zero, never multiple
• Accountability cannot be delegated (only the work can)
• C’s input matters; I’s does not
When relevant: Project kickoffs, cross-functional work, stalled tasks, role confusion, or governance audits.
Action guidance: When ownership is unclear, build or reference a RACI. Always ask “Who is the A?” If there is no clear single A or multiple A's exist, resolve it immediately. This prevents duplication, gaps, and finger-pointing.
```

---

## See Also

- [Decision Rights](../governance/decision-rights.md) — RACI operationalizes decision rights into specific assignments.
- [Escalation Path](../governance/escalation-path.md) — When no clear A exists or A's conflict, escalation paths determine who breaks the tie.
- [Product Owner](../roles-responsibilities/product-owner.md) — In agile contexts, the Product Owner is typically the A on product backlog decisions.

**External references:**
- Smith & Erwin, "Role & Responsibility Charting (RACI)" (2005) — foundational academic treatment
- PMI, *PMBOK Guide*, 7th edition — Chapter on resource management
