---
name: write-financial-model
description: "Build an editable project financial workbook with explicit assumptions, formulas, sources, and independently checked results."
---

# Write Financial Model

## Resolve scope

Find the nearest enclosing `.brain` marker from this skill and read that toolkit's `docs/OPERATING_GUIDE.md` before private data. Follow its single-workspace routing with `brain.py resolve`; this workflow does not expand a selected workspace into the whole brain.

`TOOLKIT_ROOT` and `BRAIN` both mean the main `Brain/` folder; `PROJECT` is the resolved workspace under its `Projects/`. Shared resource paths below are toolkit-relative; unqualified knowledge and output paths are workspace-relative. Follow `docs/OPERATING_GUIDE.md` for shared evidence, central integrations, maintenance paths, and application access.

## Model the decision

Agree the model's purpose, horizon, periods, currency, and accounting meanings. Read existing project assumptions and sources. Distinguish cash from revenue and profit; specify opening cash, timing, costs, and any financing explicitly. Do not force an investment, valuation, or complex forecast into a simple operating model it does not fit.

The bundled operating-model helper covers customers, unit price, variable costs, fixed costs, profit, and cash by period. Read `examples/artifacts/model.json` for its accepted input. Build the actual input JSON inside the selected project's `outputs/`; the shipped example is synthetic, never evidence for the business. Generate with:

`python3 TOOLKIT_ROOT/scripts/artifacts.py model --project <slug> --input <project-input.json> --name <artifact-slug>`

The helper requires `openpyxl`. If unavailable, report that concrete dependency and provide the calculation specification; do not claim a workbook was created or install packages silently. If the requested model exceeds the helper's structure, define the additional schedules and build them only with available spreadsheet tooling; preserve source assumptions and editable formulas.

Inspect generated formulas, units, signs, periods, totals, and source notes. Compare key results with the helper's independent expected-results file or another calculation. Generated formula cells may lack cached values until a spreadsheet application recalculates them; do not describe those cells as recalculated unless that happened. Deliver the workbook plus assumptions, sensitivity limits, and the actual verification performed. Stop rather than overwrite an existing artifact directory.
