---
name: discovery-rigor
description: "Create an opportunity tree, assumption map, or research interview guide grounded in a selected project’s outcomes and evidence."
---

# Add discovery rigor

## Resolve scope

Find the nearest enclosing `.brain` marker from this skill and read that toolkit's `docs/OPERATING_GUIDE.md` before private data. Follow its single-workspace routing with `brain.py resolve`; this workflow does not expand a selected workspace into the whole brain.

`TOOLKIT_ROOT` and `BRAIN` both mean the main `Brain/` folder; `PROJECT` is the resolved workspace under its `Projects/`. Shared resource paths below are toolkit-relative; unqualified knowledge and output paths are workspace-relative. Follow `docs/OPERATING_GUIDE.md` for shared evidence, central integrations, maintenance paths, and application access.

Use the method that answers the user's discovery question. Do not produce every framework merely because it is available.

## Establish the question

Read relevant `context/goals.md`, discovery outputs, hypotheses, and supplied research. Identify the decision being informed and the desired user or business outcome.
Separate evidence from plausible explanations. Label unsupported nodes and assumptions so a polished diagram cannot imply validation.
Ask for the intended decision only when it is missing and would change the method.

## Opportunity tree

Start with a measurable desired outcome, then map user opportunities, candidate responses, and tests.
Ground opportunities in observed unmet needs or workflow friction. Do not rename a preferred solution as an opportunity.
Connect each candidate response to the specific opportunity it addresses; allow multiple responses and the option to do nothing.
For each test, state the assumption it probes, evidence to collect, and the decision that would follow.
If using a diagram, include a readable textual equivalent and sources; no external diagram tool is required.

## Assumption map

List assumptions across value, usability, feasibility, viability, and relevant external constraints.
Rank by the consequence of being wrong and the uncertainty of current evidence. Do not multiply arbitrary scores into false precision.
For the most consequential unknowns, propose the cheapest credible test, the owner, the observation window, and a decision threshold.
Link related `Hypotheses/` entries. An assumption becomes validated only through evidence, not agreement in the workshop.

## Interview guide or transcript analysis

For a guide, define the participant's relevant experience and what the interview must learn. Ask about a recent concrete episode: trigger, attempted progress, alternatives, barriers, and consequences.
Avoid leading questions, hypothetical purchase promises, and teaching the respondent the desired answer. Distinguish a user interview from an internal approval request.
For supplied transcripts, separate direct quotations, factual observations, interpretation, and unresolved questions. Preserve participant context without generalizing one person's experience to a population.
Offer a follow-up test where the interview cannot establish prevalence or causality.

## Deliver

Save the requested artifact under `outputs/YYYY-MM-DD_discovery-rigor_<topic>.md`, with method, evidence, assumptions, and next decision.
Update a hypothesis only when requested or when the current capture request includes that update. Otherwise link the proposed change.
Feed useful results into `think-discovery`; do not overwrite an approved product brief simply because a new framework suggests a different direction.
