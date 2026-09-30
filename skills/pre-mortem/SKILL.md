---
name: pre-mortem
description: "Explore how a plan could fail, rank the consequential failure modes, and propose practical mitigations before commitment."
---

# Test a plan by imagining failure

## Resolve scope

Find the nearest enclosing `.brain` marker from this skill and read that toolkit's `docs/OPERATING_GUIDE.md` before private data. Follow its single-workspace routing with `brain.py resolve`; this workflow does not expand a selected workspace into the whole brain.

`TOOLKIT_ROOT` and `BRAIN` both mean the main `Brain/` folder; `PROJECT` is the resolved workspace under its `Projects/`. Shared resource paths below are toolkit-relative; unqualified knowledge and output paths are workspace-relative. Follow `docs/OPERATING_GUIDE.md` for shared evidence, central integrations, maintenance paths, and application access.

Examine execution and outcome risk. Use `redteam` when the central question is whether the premise or proposed decision is wrong.

## Set the frame

Identify the plan, intended outcome, time horizon, and current commitment level. Read its source artifact, active hypotheses, known constraints, and relevant prior decisions.
Define a concrete failure state before brainstorming. A missed date, weak adoption, harmful side effect, and negative return may have different causes.
Choose the horizon from the plan; use a provisional horizon only when a missing one does not prevent useful analysis, and label it.

## Generate failure modes

Consider delivery, technical dependencies, user behavior, operations, commercial fit, stakeholder alignment, measurement, and external conditions where relevant.
For each plausible failure, state the causal path: triggering condition, mechanism, affected outcome, and evidence that makes it worth considering.
Include failure from doing too much, doing too little, or solving the wrong part of the problem. Avoid generic risks with no relation to the plan.
Treat weak evidence as uncertainty, not proof that a failure is likely. Separate risks already accepted from newly discovered ones.

## Rank and respond

Rank by expected consequence and plausibility, explaining the basis. Use qualitative bands unless defensible numerical estimates exist.
For the leading risks, propose:

- The smallest useful prevention or scope change.
- An early signal that the failure path is emerging.
- A response or rollback when prevention fails.
- An owner and decision date when known.
- Residual risk after mitigation.

A mitigation must address the causal path, not merely say to communicate more or test thoroughly.
Distinguish a risk the team can control from an external dependency it can only monitor.
If an acceptance decision is needed, leave it open for the actual decision owner. Do not interpret silence as acceptance.

## Deliver and stop

Write `outputs/YYYY-MM-DD_pre-mortem_<topic>.md` with the failure definition, ranked risks, evidence, proposed mitigations, and open decisions.
Stop when the major failure modes have a plausible response or a clearly identified acceptance decision. Further brainstorming is useful only when it changes a material decision.
Do not rewrite the plan, change its status, or block execution automatically. Report the most consequential action for the user to consider.
