---
name: write-business-case
description: "Draft an evidence-backed business case comparing investment options, uncertainty, economics, and a specific decision."
---

# Write Business Case

## Resolve scope

Find the nearest enclosing `.brain` marker from this skill and read that toolkit's `docs/OPERATING_GUIDE.md` before private data. Follow its single-workspace routing with `brain.py resolve`; this workflow does not expand a selected workspace into the whole brain.

`TOOLKIT_ROOT` and `BRAIN` both mean the main `Brain/` folder; `PROJECT` is the resolved workspace under its `Projects/`. Shared resource paths below are toolkit-relative; unqualified knowledge and output paths are workspace-relative. Follow `docs/OPERATING_GUIDE.md` for shared evidence, central integrations, maintenance paths, and application access.

## Frame the decision

Retrieve the project goals, problem evidence, prior decisions, relevant hypotheses, and available research before interviewing the user. Separate established facts, interpretation, options already ruled out, and missing decisions. Ask only questions that change the recommendation; assign stakeholder-controlled unknowns instead of guessing.

For a material or difficult-to-reverse bet with uncertain customer value, offer the Working Backwards checkpoint in `skills/think-discovery/references/working-backwards.md`. Use it only when warranted and accepted. Its companion draft stays in this project's outputs. Carry unresolved customer-value gaps into the case rather than dressing them as delivery readiness.

Use `templates/delivery/business-case.md`. Compare realistic alternatives including a smaller step or no immediate investment. Explain alignment to this project's goals, who benefits, why now, constraints, costs, benefits, risks, and the evidence that could change the recommendation. Show adoption and uncertainty in economic estimates; link an existing model rather than copying contradictory numbers. Unknown effort or commercial assumptions must remain visible with an owner and validation path.

Lead with the requested decision and bounded recommendation. Include success and stop criteria, proposed owner, and next action. Draft dates and ownership are proposals unless confirmed. Link sources and companion artifacts. Save a new `outputs/YYYY-MM-DD_business-case_<topic>.md`; a draft request does not authorize publishing or creating tickets.
