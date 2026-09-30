---
name: think-data-analyst
description: "Design outcome metrics and an instrumentation plan before implementation; distinguish measured baselines from assumptions."
---

# Think Data Analyst

## Resolve scope

Find the nearest enclosing `.brain` marker from this skill and read that toolkit's `docs/OPERATING_GUIDE.md` before private data. Follow its single-workspace routing with `brain.py resolve`; this workflow does not expand a selected workspace into the whole brain.

`TOOLKIT_ROOT` and `BRAIN` both mean the main `Brain/` folder; `PROJECT` is the resolved workspace under its `Projects/`. Shared resource paths below are toolkit-relative; unqualified knowledge and output paths are workspace-relative. Follow `docs/OPERATING_GUIDE.md` for shared evidence, central integrations, maintenance paths, and application access.

## Measurement design

Read the project goals and proposed customer outcome. Translate the intended decision into one primary outcome, a small set of diagnostic inputs, and guardrails. Distinguish adoption, successful task completion, reliability, economics, and unintended effects; select what fits the product rather than assuming one is always primary.

For every metric define its entity and denominator, event or source, calculation, window, exclusions, segmentation, owner, and freshness requirement. Label unknown baselines as unknown. Targets need an explicit rationale and review date. Include a qualitative signal when numbers cannot explain why behavior changes.

Specify the event contract: when it fires, identifier and deduplication rule, required fields, allowed values, consent or retention constraints, and how retries or offline activity affect counts. Avoid collecting personal data merely because it may be useful later. Describe verification against a known user journey and the expected counts.

Save `outputs/YYYY-MM-DD_measurement-plan_<topic>.md` using `templates/delivery/measurement-plan.md`. Separate instrumentation tasks from the readout plan. Do not create analytics events, dashboards, or production configuration automatically. Route analysis of existing measurements to the project-scoped metrics-analysis workflow.
