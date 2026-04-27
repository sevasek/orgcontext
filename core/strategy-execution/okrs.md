---
id: okrs
title: OKRs (Objectives and Key Results)
category: strategy-execution
tags: [goals, strategy, measurement, alignment, performance]
related: [mission-alignment, raci, north-star-metric, strategy-map]
version: 1.0.0
last_updated: 2025-01-01
authors: []
sources:
  - "John Doerr, *Measure What Matters*, 2018"
  - "Andy Grove, *High Output Management*, 1983"
---

## Definition

OKRs (Objectives and Key Results) are a goal-setting framework that pairs an ambitious, qualitative **Objective** (where we want to go) with 2–5 measurable **Key Results** (how we'll know we got there). Objectives are inspirational and directional; Key Results are specific, time-bound, and measurable — they function as leading or lagging indicators that, if all achieved, would confirm the Objective was met.

OKRs operate at multiple levels: company, team, and individual. Upper-level OKRs inform lower-level ones, creating vertical alignment. Shared Key Results across teams create horizontal alignment. OKRs are typically set quarterly at the team level and annually at the company level.

A critical feature of healthy OKR culture: Key Results should be ambitious enough that achieving 70%–80% is considered strong performance (the "stretch goal" principle). Consistently hitting 100% signals the targets were too conservative.

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

- **Activity OKRs:** "Complete the market research report" is an activity, not a Key Result. Add the *impact* of that report: "Identify 3 market segments with >$50M TAM."
- **Vanity metrics:** Key Results like "increase social followers by 10%" may not predict real business outcomes. Ask: "If we hit this, does it confirm the Objective was achieved?"
- **OKR theater:** Organizations that write OKRs but never review them mid-cycle or adjust when reality shifts. OKRs should be living, reviewed artifacts — not annual documents filed away.
- **Too many OKRs:** More than 3–5 Objectives per team or 3–5 Key Results per Objective creates diffusion, not focus. If everything is a priority, nothing is.

---

## Prompt Snippet

```
[ORGANIZATIONAL CONTEXT: OKRs]

Definition: A goal framework pairing an Objective (qualitative direction) with 2–5 Key Results (measurable indicators). Achieving all Key Results should confirm the Objective was met. Healthy targets are ambitious: 70–80% attainment is strong.

When this is relevant:
- Evaluating whether work is strategically aligned
- Assessing whether a goal or metric is well-formed
- Planning prioritization across competing initiatives

Key distinctions:
- Key Results measure outcomes, not activities or outputs
- OKRs are NOT performance scorecards — decouple from comp/review
- Hitting 100% consistently = targets are too conservative

Apply this by: When given a task, goal, or initiative, check whether it maps to a Key Result. If it doesn't, surface that gap. If asked to evaluate a proposed Key Result, check: Is it measurable? Is it an outcome (not activity)? Is it ambitious enough to require effort?
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
