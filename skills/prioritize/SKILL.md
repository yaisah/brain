---
name: prioritize
description: "Rank initiatives within a workspace or across an explicitly selected planning portfolio using evidence, capacity, strategic fit, and dependencies."
---

# Compare competing initiatives

## Resolve scope

Find the nearest enclosing `.brain` marker from this skill and read that toolkit's `docs/OPERATING_GUIDE.md` before private data. Use `brain.py resolve` for one workspace. For an explicit whole-brain portfolio request or approved recurring planning scope, use `brain.py resolve-brain` and `brain.py list-projects --scope planning`; narrow further when the user names a subset. Clarify ambiguous scope instead of expanding a single-workspace request. Additional inactive or disabled workspaces require explicit selection.

`TOOLKIT_ROOT` and `BRAIN` both mean the main `Brain/` folder; `PROJECT` is the resolved workspace under its `Projects/`. Shared resource paths below are toolkit-relative; unqualified knowledge and output paths are workspace-relative. Follow `docs/OPERATING_GUIDE.md` for shared evidence, central integrations, maintenance paths, and application access.

Produce a defensible comparison rather than a score that conceals judgment. This skill combines portfolio ranking with explicit delivery sequencing. For a concrete plan for today, use `skills/plan-day/SKILL.md`; strategic ranking alone does not establish a feasible day.

## Establish the decision

Read the selected project's goals, capacity constraints, relevant initiative artifacts, and available cost or value evidence.
For whole-brain planning, read central goals/preferences and lightweight goals, `STORY.md`, and canonical action pointers from selected workspaces. Resolve conflicting goals and shared capacity explicitly; do not compare business revenue, career learning, and personal commitments as if their units were identical. Keep action identity and current status in the source tracker, with links from this recommendation. Skip application trees and raw-source sweeps.
Identify the decision window, candidate set, resource limit, and whether the user needs a ranked list, a cut line, or a delivery sequence.
Ask only for missing inputs that materially change the recommendation. Record unknowns instead of assigning favorable defaults.
State capacity in the user's available units and distinguish known commitments from estimates. If capacity is unknown, offer conditional rankings and identify the fact needed for a defensible cut line rather than pretending all high-scoring work fits.

## Choose a method

Use the method requested by the user. Otherwise select one that matches the available evidence:

- Confidence-adjusted value versus cost when benefit and implementation estimates are credible.
- RICE or ICE for comparable opportunities, with clearly defined scales and time periods.
- Weighted shortest job first for delay-sensitive work, with transparent cost-of-delay assumptions.
- Kano for customer response patterns, preserving the distinction between research findings and guesses.
- MoSCoW for a bounded release scope, not as a substitute for economic ranking.
- Opportunity scoring when satisfaction and importance research supports it.

Explain the choice briefly. Do not combine incompatible scores from different frameworks into a single unexplained number.

## Build the comparison

For every initiative show the source, units, estimate range or confidence, effort, dependencies, and the goal it serves.
Distinguish direct business value, customer value, risk reduction, and required maintenance; avoid counting the same benefit twice.
Where quantitative inputs are missing, show the gap and how the ranking changes under plausible assumptions. A blank is not a zero.
Flag an initiative that scores well but conflicts with stated goals. Do not rewrite the goals to justify it.
Run a simple sensitivity check on the leading uncertain inputs. Identify fragile rankings and ties rather than forcing precision.

## Turn rank into sequence

Separate hard prerequisites from preferred ordering. A high-ranked initiative may need a lower-ranked enabler first.
Show capacity tradeoffs and what falls below the cut line. Include mandatory obligations explicitly instead of hiding them in a score adjustment.
Recommend what to start, defer, investigate, or stop considering, with the condition that would change each recommendation.

## Deliver

Save the recommendation under `PROJECT/outputs/` for one workspace or `BRAIN/outputs/` for a whole-brain portfolio, using `YYYY-MM-DD_prioritization_<topic>.md` and a noncolliding revision if needed. Include scope and per-workspace coverage, source-linked inputs, method, comparison, sensitivity, capacity, sequence, and unresolved decisions.
This recommendation does not change a roadmap, create tickets, or commit a team. Make strategy or capacity changes explicit proposals for their owner.
