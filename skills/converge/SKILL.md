---
name: converge
description: "Coordinate independent reviews of the same artifact version, revising within scope and reporting genuine agreement or unavailable review honestly."
---

# Seek independent review agreement

## Resolve scope

Find the nearest enclosing `.brain` marker from this skill and read that toolkit's `docs/OPERATING_GUIDE.md` before private data. Follow its single-workspace routing with `brain.py resolve`; this workflow does not expand a selected workspace into the whole brain.

`TOOLKIT_ROOT` and `BRAIN` both mean the main `Brain/` folder; `PROJECT` is the resolved workspace under its `Projects/`. Shared resource paths below are toolkit-relative; unqualified knowledge and output paths are workspace-relative. Follow `docs/OPERATING_GUIDE.md` for shared evidence, central integrations, maintenance paths, and application access.

Use independent reviewers to test an artifact against a shared quality bar. Agreement is meaningful only when both reviewers inspected the same unchanged version.

## Define the review

Identify the target artifact, scope, acceptance criteria, maximum rounds, and allowed changes. Default to three rounds when no limit is supplied.
Read the source and relevant project evidence. Preserve an original draft snapshot under `BRAIN/maintenance/evaluations/<slug>/<run>/` before revising a project-owned draft.
Record a content hash or an equally unambiguous version identifier for every reviewed version.

## Establish actual reviewers

Use real independent agent or model calls when supported. Prefer different model families when available and suitable, but do not claim that capability without observing it.
Give each reviewer the same quality bar, artifact version, and necessary evidence. Do not feed one reviewer's findings to the other before its initial review.
Log reviewer identity as actually known, including whether the family is known or the reviewers share a model. Separate independent reviews from role-played personas in one response.
If independent reviewer execution is unavailable, perform or offer a single review and mark the result **single review only**. Never simulate two approvals or report convergence.

## Review and revise

Ask reviewers for actionable findings with evidence, severity, and a clear pass or revise judgment against the bar.
Reconcile findings by substance, not by majority vote. When reviewers disagree, identify the disputed fact or criterion and seek the evidence that can resolve it.
Apply only authorized revisions and keep the source meaning and user's scope intact. A new requirement needs an explicit decision, not automatic inclusion.
After any change, create a new version identifier and obtain both reviewers' judgments on that new version. Prior approval does not carry across a changed artifact.
Do not let a reviewer invent citations, change strategy, or contact external people to clear a finding.

## Stop conditions

Stop on both reviewers approving the same unchanged version, the round limit, repeating disagreement, missing reviewer capability, or a decision requiring user input.
A partial review, timeout, tool error, or absent response is not an approval.
If the quality bar cannot be met within scope, report the remaining gap rather than expanding the task silently.

## Deliver

Save the reviewed draft in the selected workspace's `outputs/` and the versioned review log under `BRAIN/maintenance/evaluations/<slug>/<run>/`.
Report reviewer identities, versions, findings resolved, open issues, and one precise verdict: agreed, revise, blocked, or single review only.
Review agreement does not publish the artifact or transfer decision authority from the user.
