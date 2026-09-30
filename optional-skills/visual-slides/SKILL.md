---
name: visual-slides
description: "Make a self-contained HTML slide narrative for a selected project with visual pacing, source notes, and keyboard navigation."
---

# Visual Slides

## Resolve scope

Find the nearest enclosing `.brain` marker from this skill and read that toolkit's `docs/OPERATING_GUIDE.md` before private data. Follow its single-workspace routing with `brain.py resolve`; this workflow does not expand a selected workspace into the whole brain.

`TOOLKIT_ROOT` and `BRAIN` both mean the main `Brain/` folder; `PROJECT` is the resolved workspace under its `Projects/`. Shared resource paths below are toolkit-relative; unqualified knowledge and output paths are workspace-relative. Follow `docs/OPERATING_GUIDE.md` for shared evidence, central integrations, maintenance paths, and application access.

## Present one argument across slides

Read the audience, purpose, timing, and project sources. Draft the slide assertions before layout. Use a sequence that establishes the problem, alternatives, evidence, recommendation, and next step when the task is a decision; adjust for education or a status update. Each slide should do one job. Do not disguise uncertain assumptions as visual facts.

Use `templates/delivery/presentation-outline.md` and the local presentation helper documented by `skills/write-presentation/SKILL.md` when its format fits. For a custom HTML deck, keep all necessary assets local, offer keyboard and visible navigation, use readable text sizes, and provide a print-friendly fallback. Hide neither source notes nor qualifications behind inaccessible hover-only interactions.

Save the outline and deck in project outputs. Inspect every rendered slide for overflow, chart labels, contrast, navigation, and print layout when rendering is available. Report structural-only validation honestly when it is not. This optional workflow adds visual storytelling; it does not publish or import a different project's brand.
