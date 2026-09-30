---
name: project-recap
description: "Create an evidence-linked project recap for resuming work, showing current state, recent changes, unresolved decisions, and the next action."
---

# Project Recap

## Resolve scope

Find the nearest enclosing `.brain` marker from this skill and read that toolkit's `docs/OPERATING_GUIDE.md` before private data. Follow its single-workspace routing with `brain.py resolve`; this workflow does not expand a selected workspace into the whole brain.

`TOOLKIT_ROOT` and `BRAIN` both mean the main `Brain/` folder; `PROJECT` is the resolved workspace under its `Projects/`. Shared resource paths below are toolkit-relative; unqualified knowledge and output paths are workspace-relative. Follow `docs/OPERATING_GUIDE.md` for shared evidence, central integrations, maintenance paths, and application access.

## Reconstruct the project state

Read the selected project's profile, recent story, decisions, outputs, and activity log. Use explicitly authorized source history when needed. Distinguish planned work, attempted actions, observed results, and accepted decisions. Do not infer completion from an artifact's existence or a confident previous summary.

Produce a concise recap with objective, current state, recent material changes, evidence, open decisions, blockers, and next actions. Name dates and owners only when supplied; surface stale or contradictory records. A timeline or flow can help when several workstreams interact, but do not fill empty sections with guesses.

Save a Markdown recap and, when useful, self-contained HTML in project outputs using `templates/delivery/visual-review.md`. Link to canonical project records rather than duplicating a private archive. Make the next action and what would unblock it visible. Reading this recap does not authorize executing its action list or combining other businesses' context.
