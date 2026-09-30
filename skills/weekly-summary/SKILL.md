---
name: weekly-summary
description: "Draft an evidence-backed weekly update for one workspace or an explicitly selected whole-brain scope."
---

# Draft a weekly update

## Resolve scope

Find the nearest enclosing `.brain` marker from this skill and read that toolkit's `docs/OPERATING_GUIDE.md` before private data. For one workspace, use `brain.py resolve`. For an explicit whole-brain update or approved recurring brain-wide scope, use `brain.py resolve-brain` and `brain.py list-projects --scope active`, or a narrower user-selected set. Resolve the intended mode when ambiguous; a workspace update does not expand automatically into a brain-wide report.

`TOOLKIT_ROOT` and `BRAIN` both mean the main `Brain/` folder; `PROJECT` is the resolved workspace under its `Projects/`. Shared resource paths below are toolkit-relative; unqualified knowledge and output paths are workspace-relative. Follow `docs/OPERATING_GUIDE.md` for shared evidence, central integrations, maintenance paths, and application access.

Produce a reviewable update for the intended audience. Drafting does not send an email, publish a page, or make a commitment.

## Gather the week

Use the requested period; otherwise use the last seven days in the selected scope's timezone. If a missing date boundary would change the account materially, ask one targeted question.
For a whole-brain update, use central goals, preferences, and timezone plus lightweight `STORY.md`, goals, and canonical task pointers from the selected workspaces. Drill into evidence for material claims only. Keep per-workspace source attribution and coverage visible, and skip application code, dependencies, builds, and secrets.
For each selected workspace, read `context/preferences.md` for audience and format. Use its latest `Ingestion/YYYY-MM-DD_weekly-accomplishments.md` within the period as the primary account when one exists.
Supplement it from dated ingestion entries, `wiki/log.md`, decisions, the current `STORY.md`, relevant outputs, and verified metric summaries inside that workspace.
If an accomplishments file is absent, draft from the available activity and say which sources supplied the account. Do not ask the user to recreate a week already documented.
Distinguish work performed this week from an old artifact edited this week. Link evidence for completed or shipped claims.
Use the canonical action record for status. A weekly update is a dated view, not a second tracker; unfinished work stays linked to its source rather than silently disappearing.

## Compose

Use `templates/workflows/weekly-summary.md` as the default structure, adapting section labels to the audience when helpful.
Lead with the material result or decision. Separate discovery and learning, delivery and outcomes, blockers and dependencies, and next-period focus.
For each included item, explain what changed and why it matters. A meeting is usually context for progress, not an outcome by itself.
Quantify only with sourced numbers and explicit periods. Do not equate instrumentation, a draft, an approval, and a launch.
Show unresolved blockers with an owner and required action when known. Report no known blockers only when the inspected evidence supports that statement.
Build next-period focus from documented plans and open work. Label inferred suggestions as proposed; do not invent deadlines or promises.

## Ask only what is necessary

Proceed with the draft when context is sufficient. Ask targeted questions only for a consequential gap, such as an ambiguous audience or contradictory completion status.
A missing optional detail can remain marked unknown. Do not stop the whole draft for a cosmetic preference.
In the accompanying chat, name additions beyond the accomplishments file and their sources so the user can trim them.

## Format and deliver

Default to a concise Markdown draft in `PROJECT/outputs/YYYY-MM-DD_weekly-summary.md` for one workspace or `BRAIN/outputs/YYYY-MM-DD_weekly-summary.md` for a whole-brain update. Use a noncolliding revision when an output already exists.
When the user requests HTML or email-ready output, produce a complete local HTML document with inline styles and escaped source text. Use a supplied brand only for its authorized audience and scope; keep a whole-brain update neutral unless a brand was requested.
Link audience-appropriate artifacts and verified dashboards once per destination. Exclude private notes, raw transcripts, and local-only links from an external-facing draft unless the user explicitly includes them.
For a single workspace, append a short draft-created entry to its `wiki/log.md`; a whole-brain run can link the consolidated draft from `BRAIN/maintenance/runs/<run-id>/`. Record skipped or inaccessible workspaces without treating missing evidence as no activity.
State that the update is a draft, identify unresolved claims and coverage gaps, and provide the file path. Never send it automatically.
