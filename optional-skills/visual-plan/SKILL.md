---
name: visual-plan
description: "Turn a project implementation plan into a visual sequence of dependencies, decisions, milestones, and acceptance evidence."
---

# Visual Plan

## Resolve scope

Find the nearest enclosing `.brain` marker from this skill and read that toolkit's `docs/OPERATING_GUIDE.md` before private data. Follow its single-workspace routing with `brain.py resolve`; this workflow does not expand a selected workspace into the whole brain.

`TOOLKIT_ROOT` and `BRAIN` both mean the main `Brain/` folder; `PROJECT` is the resolved workspace under its `Projects/`. Shared resource paths below are toolkit-relative; unqualified knowledge and output paths are workspace-relative. Follow `docs/OPERATING_GUIDE.md` for shared evidence, central integrations, maintenance paths, and application access.

## Show what must happen and why

Read the proposed plan and current constraints. Separate outcomes, work packages, decisions, and genuine dependencies. Do not invent estimates, owners, or dates to make a timeline look complete. Mark critical unknowns and distinguish a hard blocker from preferred sequencing.

Create a self-contained HTML plan in project outputs with a dependency map and a compact milestone table. For every milestone state its observable acceptance evidence and unresolved decision. Include a text reading order, legend, source references, and an update date. Interactivity may reveal details but must not be necessary to discover a blocker.

Use `templates/delivery/visual-review.md` for evidence and limits. Check references and the dependency graph for cycles; verify any dates against stated constraints. If the plan cannot meet its own dependencies, surface that before polishing the visual. Rendering checks and any inferred sequence must be labeled; this workflow does not change tickets, dates, or code.
