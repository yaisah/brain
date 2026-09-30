---
name: plan-review
description: "Compare a proposed implementation plan with the current selected code or system evidence and identify concrete missing work or incorrect assumptions."
---

# Plan Review

## Resolve scope

Find the nearest enclosing `.brain` marker from this skill and read that toolkit's `docs/OPERATING_GUIDE.md` before private data. Follow its single-workspace routing with `brain.py resolve`; this workflow does not expand a selected workspace into the whole brain.

`TOOLKIT_ROOT` and `BRAIN` both mean the main `Brain/` folder; `PROJECT` is the resolved workspace under its `Projects/`. Shared resource paths below are toolkit-relative; unqualified knowledge and output paths are workspace-relative. Follow `docs/OPERATING_GUIDE.md` for shared evidence, central integrations, maintenance paths, and application access.

## Check feasibility against the current state

Fix the plan version, relevant source checkout or documentation revision, and intended outcome. Read the actual interfaces, dependencies, configuration, and tests that the plan relies on. Do not use file names or comments as a substitute for checking the implementation. Keep the inspected sources read-only.
Application code is in scope only when explicitly selected for this implementation review and permitted by the host; ordinary brain maintenance does not inspect a registered application tree.

Map each material plan step to supporting evidence, a gap, or a contradiction. Look for missing migrations, incompatible interfaces, configuration, rollback, observability, access constraints, and work that is already complete. Prioritize gaps that prevent the stated outcome. Distinguish required corrections from optional improvements and unresolved product choices.

Save an evidence-linked review in project outputs using `templates/delivery/visual-review.md`, with a proposed revised dependency order only where supported. Do not silently expand the objective or implement the plan. State inspection and test limits; a static review is not an end-to-end feasibility demonstration.
