---
name: champion
description: "Evaluate proposed prompt changes against frozen cases and must-pass checks, preserving the baseline and requiring evidence before promotion."
---

# Evaluate a prompt challenger

## Resolve scope

Find the nearest enclosing `.brain` marker from this skill and read that toolkit's `docs/OPERATING_GUIDE.md` before private data. Follow its single-workspace routing with `brain.py resolve`; this workflow does not expand a selected workspace into the whole brain.

`TOOLKIT_ROOT` and `BRAIN` both mean the main `Brain/` folder; `PROJECT` is the resolved workspace under its `Projects/`. Shared resource paths below are toolkit-relative; unqualified knowledge and output paths are workspace-relative. Follow `docs/OPERATING_GUIDE.md` for shared evidence, central integrations, maintenance paths, and application access.

Improve a skill or prompt only when observed results support the change. This workflow proposes changes in the selected workspace's central evaluation directory; it does not modify installed skills or global settings.

## Establish an evaluable target

Identify the target prompt, desired behavior, failure evidence, evaluation budget, scoring method, and must-pass requirements.
Create `BRAIN/maintenance/evaluations/<slug>/<run>/` containing the baseline, candidate, cases, results, and decision log for this workspace.
Use a supplied or explicitly selected prompt as input. Do not search other projects or installed global skills for candidates.
If no representative cases exist, help design a small set before claiming any improvement. Use synthetic cases unless the user explicitly includes this workspace's private data; keep it within the private brain and the agreed evaluation scope.

## Separate learning from evaluation

Keep development cases for diagnosing failures and a frozen holdout for the final comparison. Define scoring and must-pass checks before seeing candidate results.
Freeze the holdout content and record its hash. Do not edit expected answers to favor a challenger or choose a scoring rule after seeing which prompt wins.
Use fresh cases or a new holdout for subsequent optimization after its results have guided changes. Repeatedly tuning to the same revealed holdout invalidates it as independent evidence.
Preserve negative and inconclusive results, not just the winning examples.

## Compare honestly

Change one coherent aspect of the candidate in response to a recorded development failure.
Run baseline and challenger with the same inputs, tool availability, model settings when controllable, and scoring protocol. Record actual runtime and model identities when known.
If a required execution tool or independent scorer is unavailable, report **evaluation unavailable** or a limited manual review. Never fabricate runs, scores, or statistical confidence.
For nondeterministic outcomes, use enough repeated trials to assess the relevant failure mode within the agreed budget; state the limits rather than promising certainty.
Compare overall quality, critical regressions, and cost or latency when they matter to the stated goal.

## Decide and stop

Recommend a challenger only if it beats the baseline by the agreed margin and passes every must-pass check. A small score gain cannot compensate for a critical regression.
Stop on the budget, target, no useful progress, or missing capability. An inconclusive result leaves the baseline in place.
Save the candidate and proposed patch in this workspace's central evaluation directory; promotion to toolkit source or an installed skill requires a separate explicit request and is outside this evaluation workflow.

## Deliver

Report the baseline and challenger versions, frozen case hash, actual results, failures, limitations, and recommendation.
Link the workspace-specific evaluation log and proposed prompt. Do not call an unexecuted proposal an improvement.
