---
name: redteam
description: "Challenge a proposal’s premise with evidence-backed objections, tracking consequential issues until resolved, accepted, or honestly blocked."
---

# Challenge the premise

## Resolve scope

Find the nearest enclosing `.brain` marker from this skill and read that toolkit's `docs/OPERATING_GUIDE.md` before private data. Follow its single-workspace routing with `brain.py resolve`; this workflow does not expand a selected workspace into the whole brain.

`TOOLKIT_ROOT` and `BRAIN` both mean the main `Brain/` folder; `PROJECT` is the resolved workspace under its `Projects/`. Shared resource paths below are toolkit-relative; unqualified knowledge and output paths are workspace-relative. Follow `docs/OPERATING_GUIDE.md` for shared evidence, central integrations, maintenance paths, and application access.

Examine whether a proposed decision is justified. Use `pre-mortem` when the user primarily wants execution failure modes for a direction already chosen.

## Establish the target

Read the supplied proposal, relevant evidence, goals, constraints, and prior decisions in the selected project.
State the claim being challenged and the quality bar: what would make this recommendation defensible?
Keep the review within the requested scope. Do not attack the author or assign motives.

## Build objections

Look for weak assumptions, missing user evidence, alternatives excluded too early, goal conflicts, feasibility gaps, viability constraints, and unsupported causal claims.
For each objection, record:

- A precise statement of what may be wrong.
- The supporting evidence or explicitly labeled reasoning.
- The consequence if it is true.
- Impact and uncertainty, kept distinct.
- What evidence or change would resolve it.

An objection must affect the decision; stylistic preferences are not high-impact issues.
Actively look for evidence against your own objection. Do not sustain an adversarial position after the evidence defeats it.

## Resolve without taking ownership

Give each objection an identifier and one of open, resolved, accepted by owner, or blocked on evidence.
Let the user or actual decision owner respond. Mark acceptance only when they explicitly accept the risk; silence or a model's judgment is not acceptance.
A wording change resolves a wording problem, not a missing evidence problem. Reopen an issue only with a clear explanation of why the response leaves its substance unresolved.
Do not rewrite the source artifact unless the user also requested edits; propose corrections in the review instead.

## Stop and report

Stop when no consequential objection remains open, the agreed budget or timebox ends, or two rounds repeat the same disagreement without new evidence.
Report a stalemate or blocked dependency honestly; do not label the proposal approved merely because the loop stopped.
Save `outputs/YYYY-MM-DD_redteam_<topic>.md` with the objection log, responses, disposition, and unresolved decisions.
Distinguish resolved evidence, explicitly accepted risk, and issues still requiring judgment. The decision remains with its owner.
