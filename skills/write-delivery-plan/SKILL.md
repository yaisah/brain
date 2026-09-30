---
name: write-delivery-plan
description: "Turn a product brief into demonstrable delivery slices, dependencies, and acceptance criteria; optionally map approved work to an issue tracker."
---

# Write Delivery Plan

## Resolve scope

Find the nearest enclosing `.brain` marker from this skill and read that toolkit's `docs/OPERATING_GUIDE.md` before private data. Follow its single-workspace routing with `brain.py resolve`; this workflow does not expand a selected workspace into the whole brain.

`TOOLKIT_ROOT` and `BRAIN` both mean the main `Brain/` folder; `PROJECT` is the resolved workspace under its `Projects/`. Shared resource paths below are toolkit-relative; unqualified knowledge and output paths are workspace-relative. Follow `docs/OPERATING_GUIDE.md` for shared evidence, central integrations, maintenance paths, and application access.

## Plan independently reviewable outcomes

Read the selected project's brief and design or technical constraints. If no usable brief exists, produce a missing-context list or a clearly labeled preliminary outline; do not invent finalized scope. Read project preferences and only this workspace's mappings in `BRAIN/integrations.json` after project resolution. Never borrow owners, teams, fields, labels, or credentials from another workspace or a global skill.

Use `templates/delivery/delivery-plan.md`. Start with the smallest demonstrable path through the user journey, then add vertical increments. Split by user or operational outcome rather than reflexively creating separate frontend, backend, and database stories. A technical enabling task is appropriate when its dependency and verification are explicit. Distinguish hard blockers from a preferred order; flag circular dependencies and decisions masquerading as implementation work.

Give each slice a single outcome, numbered acceptance criteria covering relevant normal, error, and permission states, and clear exclusions. Identify owners only when configured or supplied; otherwise leave them unassigned. Estimates are unknown until supplied or explicitly requested as provisional. Preserve traceability to the brief and its open questions.

Save `outputs/YYYY-MM-DD_delivery-plan_<topic>.md`. A request to draft is not authorization to create or edit issues. If the user explicitly requests an external write, use the selected project's configured tracker and field mappings, including Jira only when configured. Verify required fields and the reviewable payload first. Keep acceptance criteria separate from description when the configured tracker supports that field. Stop on absent mappings rather than guessing account, team, labels, or project. Report created identifiers only after tool confirmation.
