---
name: stakeholder-questionnaire
description: "Draft decision-focused questions for a stakeholder who holds missing facts or judgment, distinguishing feasibility, value, and viability."
---

# Draft a stakeholder questionnaire

## Resolve scope

Find the nearest enclosing `.brain` marker from this skill and read that toolkit's `docs/OPERATING_GUIDE.md` before private data. Follow its single-workspace routing with `brain.py resolve`; this workflow does not expand a selected workspace into the whole brain.

`TOOLKIT_ROOT` and `BRAIN` both mean the main `Brain/` folder; `PROJECT` is the resolved workspace under its `Projects/`. Shared resource paths below are toolkit-relative; unqualified knowledge and output paths are workspace-relative. Follow `docs/OPERATING_GUIDE.md` for shared evidence, central integrations, maintenance paths, and application access.

Create a draft the user can review and send. Use `prep` for meeting context and relationship planning; use this workflow for obtaining missing evidence or decisions.

## Identify the dependency

Read the relevant initiative, prior decisions, stakeholder record, and existing evidence.
Establish the recipient's role, what knowledge or authority they hold, and which decision depends on their response.
Classify the gap without treating roles as interchangeable:

- **Feasibility:** whether the approach can be delivered under technical, operational, or resource constraints.
- **Value:** whether the intended user needs the outcome and receives meaningful benefit; an internal sponsor cannot substitute for user evidence without justification.
- **Viability:** whether the approach fits commercial, legal, financial, security, or organizational requirements.
- **Usability or other constraints:** how the intended user can accomplish the task, or a clearly named additional risk.

One questionnaire may span dimensions, but identify which recipient can answer which part. Do not ask a person to approve beyond their authority.

## Build useful questions

Read the available context first and remove questions already answered by reliable sources.
Map dependencies so prerequisite facts and blocking decisions appear before questions that depend on them.
Separate required answers from optional background. Keep each question to one topic and include the known context needed to answer it.
Distinguish a factual request, an estimate with confidence, and a decision or acceptance request. Make uncertainty an acceptable response.
For estimates, ask for assumptions and a range when exact precision is unavailable. For decisions, show relevant alternatives and consequences neutrally.
Avoid leading wording, duplicated questions, and disguised commitments. Close by inviting the recipient to identify a missing constraint or mistaken assumption.

## Check the draft

Use `templates/workflows/stakeholder-questionnaire.md`. Every question must change a decision, requirement, risk assessment, or next action.
Estimate the response effort honestly. Include a requested date only if supplied or clearly marked proposed; do not manufacture urgency.
If the remaining unknowns belong elsewhere, recommend the right source or owner instead of generating an unnecessary questionnaire.
Do not append unrelated stakeholder history or private notes to an external-facing draft.

## Save and hand off

Save `outputs/YYYY-MM-DD_questionnaire_<topic>.md` with status Draft and the decision it informs.
Never send, publish, contact the recipient, record consent, or invent their answers.
When responses arrive, use `ingest` to preserve the source and distinguish evidence, interpretation, and decisions before updating memory.
