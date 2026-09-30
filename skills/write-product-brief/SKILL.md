---
name: write-product-brief
description: "Define a project product outcome, user journey, scope, evidence gaps, and readiness in a reviewable brief."
---

# Write Product Brief

## Resolve scope

Find the nearest enclosing `.brain` marker from this skill and read that toolkit's `docs/OPERATING_GUIDE.md` before private data. Follow its single-workspace routing with `brain.py resolve`; this workflow does not expand a selected workspace into the whole brain.

`TOOLKIT_ROOT` and `BRAIN` both mean the main `Brain/` folder; `PROJECT` is the resolved workspace under its `Projects/`. Shared resource paths below are toolkit-relative; unqualified knowledge and output paths are workspace-relative. Follow `docs/OPERATING_GUIDE.md` for shared evidence, central integrations, maintenance paths, and application access.

## Define the outcome before the solution

Read the current project brief, research, business case, hypotheses, and decisions where available. For an existing brief, distinguish an approved decision from an outdated assumption; preserve the source and write a dated revision in outputs. Ask for unresolved choices only after checking sources. Do not invent user needs or quietly reverse a prior decision.

Use `templates/delivery/product-brief.md` to specify the target user and job, current problem, desired outcome, proposed behavior, scope boundaries, key states and exception paths, success measures, dependencies, and open questions. Include permissions, accessibility, failure recovery, and operational constraints when they affect the user's experience. Requirements should describe observable behavior; mark an implementation suggestion as such.

For a major uncertain customer bet, offer the Working Backwards reference at `skills/think-discovery/references/working-backwards.md` if no suitable checkpoint already exists. Link its result. A verdict calling for revision or more discovery leaves the brief not ready; carry the gaps into scope, research, and the readiness table.

Record assumptions with evidence needed, owner, and decision deadline. Separate design readiness, feasibility, commercial viability, and unresolved approval. Never mark readiness merely because every heading has text. Save `outputs/YYYY-MM-DD_product-brief_<topic>.md`, cite inputs, and identify exactly what reviewers must decide.
