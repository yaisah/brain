---
name: think-launch-report
description: "Evaluate a launched project outcome against its original goals using observed data, qualitative evidence, limitations, and follow-up decisions."
---

# Think Launch Report

## Resolve scope

Find the nearest enclosing `.brain` marker from this skill and read that toolkit's `docs/OPERATING_GUIDE.md` before private data. Follow its single-workspace routing with `brain.py resolve`; this workflow does not expand a selected workspace into the whole brain.

`TOOLKIT_ROOT` and `BRAIN` both mean the main `Brain/` folder; `PROJECT` is the resolved workspace under its `Projects/`. Shared resource paths below are toolkit-relative; unqualified knowledge and output paths are workspace-relative. Follow `docs/OPERATING_GUIDE.md` for shared evidence, central integrations, maintenance paths, and application access.

## Evaluate what happened

Read the original launch plan, success criteria, measurement definitions, rollout exposure, and actual observations. Fix the reporting window and eligible population. Compare to the intended baseline or experiment; distinguish an absent instrument, an immature cohort, and a measured zero.

Use `templates/delivery/launch-report.md`. Report each target alongside result, source, window, and confidence limits. Segment only when there is enough data to support the comparison and protect sensitive groups. Separate usage from successful outcomes, reliability, economics, and customer impact. Include contrary evidence and support incidents. Do not infer causation from a before/after movement without a suitable design.

Reconcile quantitative results with interviews or feedback rather than selecting only favorable quotes. State whether evidence supports expansion, adjustment, more observation, or stopping, and why. Name unresolved hypotheses, proposed owner and next evidence, and any decision requiring approval. Record what the team learned without rewriting original success criteria after seeing the result.

Save `outputs/YYYY-MM-DD_launch-report_<topic>.md`. Link any proposed durable learning for review under the root manual's promotion rule. Never change production rollout, archive an initiative, or mark a strategic decision approved from this report alone.
