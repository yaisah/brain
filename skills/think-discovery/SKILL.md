---
name: think-discovery
description: "Clarify a product problem through context retrieval and dependency-ordered questions, producing an evidence-backed discovery record and next decision."
---

# Discover the problem and next decision

## Resolve scope

Find the nearest enclosing `.brain` marker from this skill and read that toolkit's `docs/OPERATING_GUIDE.md` before private data. Follow its single-workspace routing with `brain.py resolve`; this workflow does not expand a selected workspace into the whole brain.

`TOOLKIT_ROOT` and `BRAIN` both mean the main `Brain/` folder; `PROJECT` is the resolved workspace under its `Projects/`. Shared resource paths below are toolkit-relative; unqualified knowledge and output paths are workspace-relative. Follow `docs/OPERATING_GUIDE.md` for shared evidence, central integrations, maintenance paths, and application access.

Resolve what matters before shaping delivery. Existing evidence should shorten the conversation; the user should not have to repeat context already present in the selected project.

## Read before interviewing

Read relevant goals, product context, recent research, hypotheses, decisions, and supplied artifacts. Inspect only sources relevant to this initiative.
Separate established facts, interpretations, decisions already made, accepted assumptions, and material unknowns.
Build a small dependency map showing which unknown facts or decisions block other decisions. The current frontier is the set that can usefully be resolved now.
Check ambiguous terms against the project's glossary and authoritative sources. Surface incompatible definitions before using them in a decision.

## Ask at the frontier

Use the following dimensions as coverage guidance, not a mandatory questionnaire:

- The concrete user problem, attempted task, current workaround, and affected beneficiary.
- Frequency, consequence, and differences between segments or contexts.
- Evidence, its limits, contradictory observations, and what would change the assessment.
- Urgency, the cost of waiting, and the connection to the project's goals.
- The value mechanism and raw inputs needed to estimate benefit and effort.
- The observable outcome that would demonstrate success.
- Constraints, alternatives, and assumptions that could overturn the direction.

Ask one coherent topic at a time in prerequisite order. Offer an evidence-backed recommendation when available instead of an empty question, while leaving the decision with its owner.
Label whether an answer provides a fact, chooses an option, or accepts an assumption.
If another stakeholder controls an essential answer, record the dependency and use `skills/stakeholder-questionnaire/SKILL.md`; do not ask the user to guess that person's judgment.
Stop when material unknowns are resolved, the agreed timebox expires, or the next decision depends on unavailable evidence. Do not continue to satisfy a generic question count.

## Synthesize

Use `templates/workflows/discovery-record.md` to summarize the problem, beneficiary, evidence, value mechanism, constraints, decisions, accepted assumptions, and remaining dependencies.
Ask for confirmation only where the synthesis introduces a meaningful interpretation or proposed decision; do not require ritual approval of facts the user already supplied.
If the initiative is a major or unusually uncertain bet, offer the optional checkpoint described in `skills/think-discovery/references/working-backwards.md` before commitment.
Preserve unresolved terminology in the record. Route a durable, authoritative resolution through `ingest` for the single project glossary.

## Save and route

Save `outputs/YYYY-MM-DD_discovery_<topic>.md`, or update the discovery section of a selected project-owned draft when requested.
Recommend the next action based on the actual gap: research, measurement, stakeholder input, prioritization, business case, or brief.
A completed interview does not establish validation or delivery readiness; state the evidence limits and the next decision explicitly.
