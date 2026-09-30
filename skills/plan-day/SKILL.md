---
name: plan-day
description: "Build a realistic daily plan from canonical actions and capacity in one workspace or across active planning-enabled workspaces."
---

# Plan the day

## Resolve planning scope

Find the nearest enclosing `.brain` marker from this skill and read that toolkit's `docs/OPERATING_GUIDE.md` before private data. `TOOLKIT_ROOT` and `BRAIN` both mean the main `Brain/` folder; `PROJECT` is a resolved workspace under its `Projects/`. Shared templates below are toolkit-relative. Follow the root manual for source permissions, evidence links, and application exclusions.

For an unqualified "what should I work on today" request, an explicit whole-brain daily plan, or approved recurring planning scope, use `brain.py resolve-brain` and `brain.py list-projects --scope planning`. A request narrowed to a named workspace stays within it. Follow the root manual when current context and the request conflict; clarify genuinely ambiguous scope. Include a paused, archived, or planning-disabled workspace only when explicitly requested.

## Gather the smallest useful planning packet

Read central goals/preferences, the target date and timezone, known fixed commitments, and each selected workspace's goals, `STORY.md`, and pointer to its canonical action records. Follow those pointers for current status, deadline, dependency, effort estimate, and evidence. Do not scan application trees or all raw sources to build a daily plan.

Use one canonical record per action and stable identifiers or direct links. A plan references those records; it does not create duplicate task status, copy an entire backlog, or infer completion from yesterday's omission. When no canonical tracker exists, propose a location and make newly suggested actions visibly provisional. Do not create an external tracker or edit task status merely because planning needs a list.

## Fit work to capacity

Determine available hours or effort capacity after supplied commitments, energy constraints, breaks, and interruption allowance. Ask for a missing capacity fact when it changes feasibility; otherwise provide a bounded provisional plan and label the assumption. Do not invent calendar events, priorities, deadlines, or precise effort estimates. An unavailable calendar is unknown capacity, not an empty day.

Choose a small set of concrete outcomes using deadline consequence, goal relevance, dependency readiness, and expected effort. Separate must-do commitments, discretionary focus, and blocked work. Across workspaces, make tradeoffs explicit rather than forcing equal time for each area. Route a disputed strategic ranking to `prioritize`; this skill sequences today's actions.

For each selected action give its canonical link, next observable step, effort range or unknown, relevant deadline/source, and a stop condition. Exclude work that cannot start until a dependency resolves, or include the concrete unblock action. If requested work exceeds capacity, show what must move or shrink; do not hide overload in an optimistic schedule. Label optional fallback tasks and leave room for recovery.

## Save a plan, preserve the source of truth

Use `BRAIN/outputs/YYYY-MM-DD_daily-plan.md` for a whole-brain plan or `PROJECT/outputs/YYYY-MM-DD_daily-plan.md` for one workspace, with a noncolliding revision when needed. State planning scope, evidence date, known commitments, capacity assumptions, chosen outcomes, deferred work, and unresolved facts. Links should resolve from the written file to canonical records.

Treat the plan as a dated recommendation. Update canonical action status only when the user asks or provides completion evidence for capture; link any resulting record instead of maintaining a second status table. Report coverage gaps or inaccessible workspaces. Do not send reminders, modify calendars, or enable a schedule unless the user separately requested those actions and the required tool is available.
