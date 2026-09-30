---
name: write-presentation
description: "Create a concise project presentation with a decision-focused narrative, evidence-linked slides, accessible layout, and local HTML or PPTX output."
---

# Write Presentation

## Resolve scope

Find the nearest enclosing `.brain` marker from this skill and read that toolkit's `docs/OPERATING_GUIDE.md` before private data. Follow its single-workspace routing with `brain.py resolve`; this workflow does not expand a selected workspace into the whole brain.

`TOOLKIT_ROOT` and `BRAIN` both mean the main `Brain/` folder; `PROJECT` is the resolved workspace under its `Projects/`. Shared resource paths below are toolkit-relative; unqualified knowledge and output paths are workspace-relative. Follow `docs/OPERATING_GUIDE.md` for shared evidence, central integrations, maintenance paths, and application access.

## Build the argument and the deck

Identify the audience, their decision or intended next action, time available, and deliverable format. Read the selected project's evidence and optional brand guidance. Use neutral typography and colors when no brand is configured; never search another workspace for assets. Build a short narrative from situation, tension, options, evidence, recommendation, and ask, adjusting the order to the meeting's purpose.

Use `templates/delivery/presentation-outline.md` as the starting structure and save the populated outline to `outputs/YYYY-MM-DD_presentation-outline_<topic>.md` inside the selected project. Keep the shared template unchanged. Give each slide one assertion supported by an appropriate chart, comparison, example, or source. Preserve uncertainty and alternatives; do not convert a conjecture into a headline fact. Put detailed calculations and citations in notes or an appendix without making the visual argument misleading. A board update, investment case, product review, and launch readout need different emphasis, not just different titles.

Read `examples/artifacts/presentation.json` for the helper input, then save the actual project input under its outputs. Generate a standalone local deck with:

`python3 TOOLKIT_ROOT/scripts/artifacts.py presentation --project <slug> --input <project-input.json> --name <artifact-slug>`

Add `--pptx` only when a PPTX is wanted and `python-pptx` is available. HTML remains available without that optional library. Be precise about which formats were actually generated. The bundled layout is a starting format; use other available presentation tools when the requested fidelity requires them, scoped to this project.

Inspect the rendered result when browser or slide rendering is available: text fit, hierarchy, contrast, charts, citations, and speaker notes. If only structural checks were possible, state that limit. Deliver the deck plus its source outline; do not send it to the audience or publish it.
