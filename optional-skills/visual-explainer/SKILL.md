---
name: visual-explainer
description: "Explain a project concept or decision as a self-contained visual document when relationships or comparisons are easier to see than read."
---

# Visual Explainer

## Resolve scope

Find the nearest enclosing `.brain` marker from this skill and read that toolkit's `docs/OPERATING_GUIDE.md` before private data. Follow its single-workspace routing with `brain.py resolve`; this workflow does not expand a selected workspace into the whole brain.

`TOOLKIT_ROOT` and `BRAIN` both mean the main `Brain/` folder; `PROJECT` is the resolved workspace under its `Projects/`. Shared resource paths below are toolkit-relative; unqualified knowledge and output paths are workspace-relative. Follow `docs/OPERATING_GUIDE.md` for shared evidence, central integrations, maintenance paths, and application access.

## Explain with an appropriate visual

Choose the decision or mental model the reader needs. Read only the supplied or selected project evidence, then choose a diagram, comparison, timeline, or interactive control that clarifies it. Do not add motion or interaction without an explanatory purpose. Mark illustrative values and uncertain relationships.

Create a self-contained HTML artifact in the project's outputs using semantic HTML, inline CSS, and simple SVG or local JavaScript where useful. Use `templates/delivery/visual-review.md` for the accompanying evidence and limitation note. Charts need labels, units, sources, and a text alternative. Controls need keyboard access, visible focus, and a readable initial state. Escape imported text; avoid remote scripts, trackers, and company assets from other projects.

Check the artifact with an available browser at a narrow and wide viewport. Verify controls and links rather than claiming correctness from code inspection. If rendering is unavailable, deliver the source with an explicit unverified-rendering note. For publication-grade plots, prefer an available plotting tool and export a standalone figure rather than an interactive webpage. Keep the output local unless publication is explicitly requested.
