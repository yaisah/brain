---
name: diff-review
description: "Review an explicitly selected code or document diff and produce an evidence-linked visual explanation of behavior changes and actionable risks."
---

# Diff Review

## Resolve scope

Find the nearest enclosing `.brain` marker from this skill and read that toolkit's `docs/OPERATING_GUIDE.md` before private data. Follow its single-workspace routing with `brain.py resolve`; this workflow does not expand a selected workspace into the whole brain.

`TOOLKIT_ROOT` and `BRAIN` both mean the main `Brain/` folder; `PROJECT` is the resolved workspace under its `Projects/`. Shared resource paths below are toolkit-relative; unqualified knowledge and output paths are workspace-relative. Follow `docs/OPERATING_GUIDE.md` for shared evidence, central integrations, maintenance paths, and application access.

## Review the actual change

Confirm the exact base and target versions or two supplied files. Read repository instructions if an explicitly selected code checkout is the source. Do not fetch, reset, stage, commit, or modify it as part of this review. A source in another workspace requires the root manual's explicit cross-workspace scope.
Resolve a registered internal application or external repository only when this code-review request includes it. A brain-maintenance run does not inherit this code access; a registry pointer alone does not grant host permission.

Inspect the diff and surrounding callers, configuration, and tests needed to understand observable behavior. Identify the concrete triggering condition and user impact for each finding; avoid speculative style complaints. Cite the actual file and verified lines or revisions. Separate bugs, intentional tradeoffs, unknowns, and questions. A passing test command means only the checks that actually ran.

Save a concise review and optional self-contained HTML change map in the project's outputs using `templates/delivery/visual-review.md`. Show before/after behavior and the relevant dependency or flow, not a decorative screenshot of a diff. If no actionable issue is found, say so with the reviewed scope and limits. Do not implement fixes or post review comments externally unless separately requested.
