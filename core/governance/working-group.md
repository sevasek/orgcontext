---
id: working-group
title: Working Group
category: governance
tags: [governance, coordination, temporary, cross-functional, decision-making]
related: [steering-committee, raci, decision-rights, escalation-path]
version: 1.0.0
last_updated: 2026-06-09
authors: ["Paul Seville"]
references:
  - IEEE Standards Association, Working Group Guidelines
  - IETF, The Tao of IETF and working group processes
---

## Definition

A Working Group is a time-bounded, cross-functional team assembled to investigate, design, or deliver a specific outcome or recommendation, after which it disbands. It owns the creation of a defined artifact (report, proposal, design, policy) rather than ongoing operations or execution.

Working groups are distinct from:
- Standing committees (permanent oversight bodies)
- Project teams (focused on delivery and implementation)
- Communities of practice (ongoing knowledge sharing)

They are typically chartered with a clear mandate, timeline, and expected deliverable. Once the work is complete and the output is handed off, the group dissolves.

---

## When to Apply

- **Complex cross-functional problems:** When an issue spans multiple departments and requires focused investigation or design work.
- **One-time policy or framework development:** When creating new standards, processes, or recommendations that will then be owned by existing teams.
- **Exploratory or advisory work:** When the organization needs input from diverse perspectives before making a strategic decision.
- **Temporary coordination needs:** When a specific initiative requires structured collaboration but does not justify creating a permanent role or team.
- **Knowledge synthesis:** When consolidating input from many stakeholders into a single coherent recommendation.

---

## Decision Heuristics

- Form a working group when the problem is important enough to warrant dedicated cross-functional attention but not permanent.
- The group should have a clear charter, defined end date or deliverable, and explicit decision rights for its output.
- Membership should be based on relevant expertise and stakeholder representation, not just availability or seniority.
- Working groups should not be used to avoid making hard decisions — they are for investigation and recommendation, not indefinite consensus-seeking.
- Once the deliverable is accepted, the working group should be formally disbanded to avoid scope creep into operations.

---

## Counter-Examples / Anti-Patterns

- **Permanent working groups:** Groups that never disband and become de facto standing committees without the accountability or authority of one.
- **Working group as decision avoidance:** Using a working group to delay a decision that a single leader or existing body should make.
- **No clear handoff:** Creating recommendations that no one owns after the group disbands, leading to the work being ignored.
- **Overly large or political groups:** Including too many people for the sake of representation, which slows progress and dilutes ownership.
- **Confusing working groups with project teams:** Treating a working group as an implementation body rather than a temporary investigation or design team.

---

## Prompt Snippet

```
[ORGANIZATIONAL CONTEXT: Working Group]
Definition: A time-bounded, cross-functional team formed to investigate or design a specific outcome and then disband. Owns a recommendation or artifact, not ongoing operations.
Key distinctions:
• Working Group = temporary, focused on a deliverable or recommendation
• Standing Committee = permanent oversight body
• Project Team = focused on execution and delivery
When relevant: Cross-functional problems requiring investigation, one-time policy design, or synthesis of stakeholder input.
Action guidance: Charter the group with a clear mandate, timeline, and expected output. Ensure decision rights for the group's recommendation are defined upfront. Disband the group once the deliverable is handed off. If a "working group" becomes permanent or lacks a clear end, treat it as a governance problem that needs restructuring.
```

---

## See Also

- [Steering Committee](../governance/steering-committee.md) — Provides ongoing oversight; working groups are often chartered or sponsored by steering committees.
- [RACI](../governance/raci.md) — Useful for clarifying roles within the temporary working group.
- [Decision Rights](../governance/decision-rights.md) — The working group's authority to recommend vs. decide should be explicit.
- [Escalation Path](../governance/escalation-path.md) — Defines how the group's recommendations or conflicts are resolved.

**External references:**
- IEEE Standards Association working group processes
- IETF working group model for open, time-bounded collaboration
