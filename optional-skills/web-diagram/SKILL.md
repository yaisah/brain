---
name: web-diagram
description: "Create a local web diagram of a project system, flow, or decision from explicit evidence, with labeled relationships and uncertainty."
---

# Web Diagram

## Resolve scope

Find the nearest enclosing `.brain` marker from this skill and read that toolkit's `docs/OPERATING_GUIDE.md` before private data. Follow its single-workspace routing with `brain.py resolve`; this workflow does not expand a selected workspace into the whole brain.

`TOOLKIT_ROOT` and `BRAIN` both mean the main `Brain/` folder; `PROJECT` is the resolved workspace under its `Projects/`. Shared resource paths below are toolkit-relative; unqualified knowledge and output paths are workspace-relative. Follow `docs/OPERATING_GUIDE.md` for shared evidence, central integrations, maintenance paths, and application access.

## Model the relationships

Determine the diagram's audience and question. Identify nodes, boundaries, direction, labels, and level of abstraction from sources. Separate current state, proposed state, and unknown links. A box's proximity must not imply a dependency that was never established.

Use semantic HTML with inline SVG or a locally available renderer to create a standalone output. Keep the diagram legible without network-loaded libraries. Use labels as well as color, provide a text description and logical reading order, and ensure zoom or expansion controls are keyboard usable if present. Escape source labels and do not execute embedded source markup.

Save in the selected project's outputs with source references, date, and assumptions using `templates/delivery/visual-review.md`. Verify edge directions and labels against the underlying evidence and inspect the rendered layout when possible. Do not claim that a conceptual architecture represents deployed infrastructure without evidence.
