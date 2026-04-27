---
id: okrs
title: OKRs (Objectives and Key Results)
category: strategy-execution
tags: [goals, strategy, measurement, alignment, performance]
related: [mission-alignment, raci, north-star-metric, strategy-map]
version: 1.0.0
last_updated: 2026-04-27
authors: ["Paul Seville"]
references:
  - "John Doerr, *Measure What Matters*, 2018"
  - "Andy Grove, *High Output Management*, 1983"
---

## Definition

OKRs (Objectives and Key Results) are a goal-setting framework that pairs an ambitious, qualitative **Objective** (where we want to go) with 2–5 measurable **Key Results** (how we'll know we got there). Objectives are inspirational and directional; Key Results are specific, time-bound, and measurable — they function as leading or lagging indicators that, if all achieved, would confirm the Objective was met.

OKRs operate at multiple levels: company, team, and individual. Upper-level OKRs inform lower-level ones, creating vertical alignment. Shared Key Results across teams create horizontal alignment. OKRs are typically set quarterly at the team level and annually at the company level.

A critical feature of healthy OKR culture: Key Results should be ambitious enough that achieving 70%–80% is considered strong performance (the "stretch goal" principle). Consistently hitting 100% signals the targets were set too conservatively.

---

## When to Apply

- **Strategic planning cycles:** OKRs provide the translation layer between annual strategy and quarterly execution.
- **Cross-team alignment:** When multiple teams must coordinate toward a shared outcome, shared Key Results make dependencies explicit.
- **Focus decisions:** Use OKRs to evaluate whether a proposed initiative is in-scope ("does this move any of our Key Results?").
- **Evaluating progress:** Mid-cycle check-ins compare current actuals against Key Result targets to surface whether the team is on track or needs to course-correct.

---

## Decision Heuristics

- If a proposed initiative doesn't map to any current Key Result, it either belongs in a backlog or signals a gap in the OKRs themselves — not automatic approval.
- A well-formed Key Result is falsifiable: there must be a clear way to measure whether it was achieved. If you can't measure it, it's an activity, not a Key Result.
- Objectives describe outcomes, not outputs. "Launch feature X" is an output. "Users can accomplish Y without support tickets" is an outcome-oriented Objective.
- If a team is consistently hitting 100% of Key Results, the OKRs are too conservative. Revise upward.
- OKRs should not be used as a performance review scoring mechanism — this causes sandbagging. Decouple OKR attainment from compensation decisions.

---

## Counter-Examples / Anti-Patterns

- **Activity OKRs:** "Run the market research" is an activity, not a Key Result. Add the **impact** of that report: "Identify 3 market segments with >$50M TAM."
- **Vanity metrics:** Key Results like "increase social followers by 10%" may not predict real business outcomes. Ask: "If we hit this, does it confirm the Objective was achieved?"
- **OKR theater:** Organizations that write OKRs but never review them mid-cycle or adjust when reality shifts. OKRs should be living, reviewed artifacts — not annual documents filed away.
- **Too many OKRs:** More than 3–5 Objectives per team or 3–5 Key Results per Objective creates diffusion, not focus. If everything is a priority, nothing is.

---

## Prompt Snippet

```
[ORGANIZATIONAL CONTEXT: OKRs]
Definition: A goal-setting framework that pairs an ambitious, qualitative Objective with 2–5 measurable Key Results. Achieving most Key Results (70–80%) should mean the Objective was met. OKRs create alignment between strategy and execution.
Key principles:
• Objectives are inspirational outcomes ("where we want to go")
• Key Results are measurable indicators of progress (not activities or outputs)
• Targets should be stretch goals — consistently hitting 100% means they were too easy
• OKRs are NOT performance scorecards — decouple from compensation/reviews
When relevant: Strategic planning, prioritization, evaluating initiatives, or diagnosing lack of focus/alignment.
Action guidance: When reviewing any proposed goal, project, or task, ask: "Which Key Result does this support?" If none, surface the misalignment. Ensure Key Results are measurable outcomes, not tasks. Use OKRs as a living tool for quarterly focus and learning, not as static documents.
```

---

## See Also

- [Mission Alignment](../mission-vision/mission-alignment.md) — OKRs operationalize mission into measurable quarterly commitments.
- [RACI](../governance/raci.md) — RACI clarifies who drives each Key Result; combining both prevents ownership ambiguity.
- [North Star Metric](../strategy-execution/north-star-metric.md) — The North Star sits above OKRs and provides the single long-term signal OKRs should contribute to.

**External references:**
- John Doerr, *Measure What Matters* (2018) — definitive modern reference
- Andy Grove, *High Output Management* (1983) — original iMBO (Intel's precursor to OKRs)
- Google re:Work OKR guide — https://rework.withgoogle.com/guides/set-goals-with-okrs/
