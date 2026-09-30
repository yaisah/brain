---
name: strategic-narrative
description: "Turn sourced strategy or analysis into an audience-specific decision brief, strategy one-pager, or executive memo with a clear recommendation and ask."
---

# Write a strategic narrative

## Resolve scope

Find the nearest enclosing `.brain` marker from this skill and read that toolkit's `docs/OPERATING_GUIDE.md` before private data. Follow its single-workspace routing with `brain.py resolve`; this workflow does not expand a selected workspace into the whole brain.

`TOOLKIT_ROOT` and `BRAIN` both mean the main `Brain/` folder; `PROJECT` is the resolved workspace under its `Projects/`. Shared resource paths below are toolkit-relative; unqualified knowledge and output paths are workspace-relative. Follow `docs/OPERATING_GUIDE.md` for shared evidence, central integrations, maintenance paths, and application access.

Make the argument understandable to its audience without converting uncertainty into confidence. This is a strategic or decision artifact, not a weekly status update or promotional copy.

## Establish the communication task

Identify the audience, decision or understanding needed, format, and constraints. Infer these from the request when clear; ask only when the answer changes the substance.
Read the selected project's goals, relevant analysis, decisions, customer evidence, and supplied source artifacts.
Separate approved strategy from a proposal, facts from inferences, and evidence gaps from disagreements.
If the underlying case is missing, draft an explicitly provisional argument or route to discovery or a business case; never fabricate support to make the narrative complete.

## Build the argument

Write the conclusion and requested action first in plain language. State whether the reader is being asked to decide, fund, prioritize, align, or understand.
Explain the current situation, the consequential change or problem, the proposed response, and why that response follows from the evidence.
Use alternatives and tradeoffs to make the recommendation assessable. Include doing nothing when it is a realistic choice.
Show why this matters now without manufacturing a deadline. Connect to the project's actual goals, not generic claims about growth or efficiency.
For each material claim, provide a source or label it as inference, assumption, or unknown.

## Match the format

Use `templates/workflows/strategic-narrative.md` as a flexible structure.
For a one-pager, retain the recommendation, strongest evidence, principal tradeoff, and ask; link supporting detail.
For a decision brief, include options, criteria, recommendation, owner, and the condition that would change the choice.
For a board or executive memo, distinguish current performance from forward-looking scenarios and make risks visible at the same level as benefits.
For a longer narrative, make each section advance the argument rather than repeat the summary in different words.

## Review for decision quality

Read only the opening sentence of each section. Together they should communicate the argument and the required action.
Check numbers, dates, quotes, and claims of approval against their sources. Preserve inconvenient evidence and meaningful uncertainty.
Remove jargon the audience does not need, unsupported superlatives, and repeated framing. Do not edit away a caveat that changes the decision.
If no clear ask exists, say the artifact is explanatory rather than inventing an approval request.

## Deliver

Save `outputs/YYYY-MM-DD_strategic-narrative_<topic>.md` with status Draft, audience, evidence date, and source links.
For a high-consequence unresolved disagreement, offer `redteam` or `converge`; neither is a required ritual for ordinary drafting.
Do not publish, contact readers, or modify canonical strategy unless separately requested.
