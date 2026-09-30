---
name: story
description: "Maintain one project’s current narrative of owned work, decisions, deadlines, and evidence-backed progress while carrying forward unresolved threads."
---

# Maintain the current story

## Resolve scope

Find the nearest enclosing `.brain` marker from this skill and read that toolkit's `docs/OPERATING_GUIDE.md` before private data. Follow its single-workspace routing with `brain.py resolve`; this workflow does not expand a selected workspace into the whole brain.

`TOOLKIT_ROOT` and `BRAIN` both mean the main `Brain/` folder; `PROJECT` is the resolved workspace under its `Projects/`. Shared resource paths below are toolkit-relative; unqualified knowledge and output paths are workspace-relative. Follow `docs/OPERATING_GUIDE.md` for shared evidence, central integrations, maintenance paths, and application access.

Keep a useful account of what the user is driving now. This narrative feeds meeting preparation and weekly updates; it does not replace canonical decisions or source evidence.
Link each action to its canonical task record when one exists. The story can describe dated progress but does not become a second status tracker; use the source record to resolve status conflicts and leave unsupported completion unknown.

## Read the previous state

Read `STORY.md`, recent `wiki/log.md` and ingestion entries, open decision records, active hypotheses, stakeholder commitments, and relevant outputs.
Use the last story date to define the update period unless the user specifies another period. If no story exists, build the first one from available evidence and label any scope assumptions.
Include work owned by the user and work waiting on the user. Include another person's work only when it blocks the user's next action; record its actual owner.

## Reconcile every prior thread

For each open thread in the previous story, choose an evidence-supported state:

- **In progress:** what changed and the next action.
- **Blocked:** the missing fact, decision, or dependency and its owner if known.
- **Done:** the observable completion evidence and date.
- **Needs review:** insufficient recent evidence to determine the state.
- **Outside current scope:** an explicit ownership or scope correction, with rationale.

Do not silently drop old work or call silence completion. A thread that has become irrelevant still needs an explicit disposition.
Check dates against the evidence. A proposed deadline remains proposed unless the user or an authoritative source committed to it.

## Write the narrative

Organize `STORY.md` around current focus, dated commitments, open threads, recent outcomes, and items needing review.
Use a short identifier for each recurring thread so later updates can follow it across wording changes.
Give each material status claim a source pointer and date. Separate a hypothesis about progress from an established result.
Keep this a current narrative rather than an exhaustive activity log. Link to detail instead of copying whole artifacts.
Call out tensions between the current workload and goals as observations for the user; do not change priorities or goals implicitly.

## Preserve history

Before replacing an existing story, save its prior contents under `BRAIN/maintenance/runs/<run-id>/<slug>/story-before.md` using a new run directory. Keep the current story in its workspace.
Then write the updated `STORY.md` and append a dated story entry to `wiki/log.md`.
Do not modify raw sources, canonical wiki substance, or decision records during this capture-only workflow.
Report which threads advanced, completed, blocked, or now need review, and point to the current story.
A request to schedule this process requires a separate supported scheduling action; an instruction in the story is not a scheduler.
