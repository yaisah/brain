---
name: north-star
description: "Define or test a North Star Metric and its controllable inputs against a project’s stated customer value and business goals."
---

# Define a useful North Star Metric

## Resolve scope

Find the nearest enclosing `.brain` marker from this skill and read that toolkit's `docs/OPERATING_GUIDE.md` before private data. Follow its single-workspace routing with `brain.py resolve`; this workflow does not expand a selected workspace into the whole brain.

`TOOLKIT_ROOT` and `BRAIN` both mean the main `Brain/` folder; `PROJECT` is the resolved workspace under its `Projects/`. Shared resource paths below are toolkit-relative; unqualified knowledge and output paths are workspace-relative. Follow `docs/OPERATING_GUIDE.md` for shared evidence, central integrations, maintenance paths, and application access.

Choose a measure of value delivered, not merely activity that is easy to count. A project may need a small metric system rather than one universal number.

## Read the strategy

Read `context/goals.md`, product and customer context, existing measurement definitions, and evidence about how users obtain value.
Identify the product scope, primary beneficiary, recurring value event, and business mechanism. Do not import another project's goals or economic assumptions.
If the goals are absent, ask for the intended outcome or draft alternatives explicitly for decision; never treat invented goals as approved strategy.

## Form candidates

Propose a small set of candidate metrics that connect repeated user value with a meaningful business outcome.
For each candidate, define the event or state counted, population, window, unit, exclusions, and source needed to measure it.
Explain why the metric represents value and when that relationship could fail. Acquisition, engagement, and revenue may be useful indicators without being the best North Star.
Reject candidates that reward harmful volume, obscure quality, or exclude a major beneficiary without justification.

## Choose inputs and guardrails

Recommend a candidate with its tradeoffs, then define a few inputs the team can influence.
Show the causal hypothesis connecting each input to delivered value. Do not claim causality solely from correlation.
Include quality, reliability, cost, or harm guardrails where they are material to the project's goals.
Separate leading inputs from the lagging outcome and from diagnostic metrics used only to explain changes.

## Make it operational

State available baseline, target if justified, accountable owner, review cadence, data source, and known data gaps.
A missing baseline is an instrumentation or research task, not permission to invent a target.
Test the proposal against two scenarios: the number rises while users receive less value; and real value improves without the number moving. Refine the definition if either is plausible.
Describe gaming risks, segment effects, delayed benefits, and what would trigger replacing the metric.

## Deliver

Write `outputs/YYYY-MM-DD_north-star_<topic>.md` with the recommendation, definition, input map, guardrails, evidence, and open decisions.
Keep the choice advisory until the user approves it. Do not silently modify `context/goals.md`, dashboards, instrumentation, or experiment settings.
Route detailed event planning to the toolkit's metric-design workflow when available, while preserving these definitions as the source.
