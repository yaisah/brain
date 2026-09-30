---
name: think-roi
description: "Estimate project-specific value, cost, payback, and uncertainty without treating assumptions as measured returns."
---

# Think Roi

## Resolve scope

Find the nearest enclosing `.brain` marker from this skill and read that toolkit's `docs/OPERATING_GUIDE.md` before private data. Follow its single-workspace routing with `brain.py resolve`; this workflow does not expand a selected workspace into the whole brain.

`TOOLKIT_ROOT` and `BRAIN` both mean the main `Brain/` folder; `PROJECT` is the resolved workspace under its `Projects/`. Shared resource paths below are toolkit-relative; unqualified knowledge and output paths are workspace-relative. Follow `docs/OPERATING_GUIDE.md` for shared evidence, central integrations, maintenance paths, and application access.

## Decision economics

Identify the decision, time horizon, currency, budget constraint, and alternatives, including doing less or deferring. Read project goals and available evidence before asking for inputs. Separate observed amounts, stakeholder estimates, and untested assumptions; record a source and date for each material number.

Use a transparent driver model. For a time-saving proposal, distinguish affected users, adoption, frequency, minutes saved, utilization, and whether saved time actually creates capacity or cash savings. Do not count both recovered payroll and the same capacity's revenue without a distinct mechanism. Include implementation, rollout, maintenance, support, and opportunity costs as relevant.

Show conservative, central, and upside cases only when their drivers differ explicitly. Report gross benefit, net benefit, ROI definition, and break-even condition; calculate payback only when cumulative net cash flow actually crosses zero. Keep one-time and recurring costs separate. Do not hide missing inputs inside precise totals or call hypothetical benefits realized.

Save the reasoning and sensitivity table with `templates/delivery/decision-economics.md`. Identify the assumption most likely to reverse the recommendation and the cheapest useful evidence to collect. Use a financial-model artifact when the user needs editable formulas or a longer forecast. This workflow supplies decision analysis, not approval to spend or transact.
