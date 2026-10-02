---
name: review
description: "Review knowledge health in one workspace or the enabled whole brain, reporting coverage, stale evidence, contradictions, and safe housekeeping."
---

# Review the brain's knowledge

## Resolve the review scope

Find the nearest enclosing `.brain` marker from this skill and read that toolkit's `docs/OPERATING_GUIDE.md` before private data. `TOOLKIT_ROOT` and `BRAIN` both mean the main `Brain/` folder; `PROJECT` is a resolved workspace under its `Projects/`. Shared templates below are toolkit-relative. Follow the root manual for source permissions, evidence links, and application exclusions.

When work is delegated or could overlap another writer, follow `BRAIN/docs/COORDINATION.md` for assignments, separate drafts, and designated shared-file writers. Existing intake locks protect helper transactions, not an entire synthesis or wiki edit.

For a named or current workspace, use `brain.py resolve` and review only it. For an explicit whole-brain review or approved recurring brain-wide scope, use `brain.py resolve-brain` and `brain.py list-projects --scope review --require-nonempty`; this already selects active, review-enabled workspaces. A whole-brain request does not require asking again for every workspace. If a generic request does not establish either mode, clarify the mode before opening unrelated private content. Additional paused, archived, or disabled workspaces require explicit scope.

If the listing fails, report the cause before treating the sweep as ready or successful. For an empty selection, inspect registry metadata with `list-projects --scope all` and distinguish no registered workspaces from inactive or review-disabled entries. Report "No eligible workspaces; no workspace review performed" and the relevant exclusions. Preserve the flags unless changing them is already authorized; use existing authorization without asking again. In an unattended run, record the scope issue for attention rather than silently enabling workspaces. If shared intake checks still run, report them separately from workspace coverage. Nonempty results can still contain unavailable workspaces; report those failures and continue available ones.

Before configuring a recurring sweep, follow the scope preflight in `docs/SOURCES_AND_ROUTING.md#routines-and-efficient-reading`.

Create one run under `BRAIN/maintenance/runs/<run-id>/`. Read central preferences and goals, the last relevant run, and lightweight workspace `PROJECT.md`, goals, `STORY.md`, wiki index, decision index, and canonical task pointer. Drill into evidence only for the checks that need it; record any sampling or time limit.

## Check knowledge and actions

- **Currency:** find claims, market research, metrics, and assumptions whose dated evidence may no longer support a live decision. Use configured freshness preferences; modification time alone does not establish evidence age.
- **Evidence and disagreement:** inspect material claims for source IDs, revision/digest, and resolving links to shared raw. Flag contradictory claims, missing support, or ambiguous terminology without manufacturing citations or erasing minority evidence.
- **Hypotheses and commitments:** surface important tests or commitments missing next evidence, an owner, a decision trigger, or a source-supported status. A blocked test is not disproved; silence is not completion.
- **Goals and capacity:** compare active commitments with applicable workspace and brain goals. Identify tensions and missing capacity facts; leave strategy and priority changes as proposals.
- **Structure and lifecycle:** check index coverage, decision pointers, local links, duplicate or orphaned records, and apparently superseded threads. Preserve one canonical action status; daily/weekly plans should link to it rather than become competing task trackers.
- **Shared intake:** in brain-wide mode, review relevant pending/failed source receipts, routing queue, and checkpoints. Distinguish source capture from completed destination synthesis; never advance a failed-source checkpoint to make a run look clean.

## Keep maintenance out of code and secrets

Visit knowledge and permitted shared evidence only. Do not descend into registered `app/`, external repositories, `.git`, dependency directories, builds, secret stores, or private credentials during maintenance. An application entry in the registry is a pointer, not permission to inspect its tree. Report an unexpected cross-workspace or external path before opening it. A requested code review is a separate explicitly scoped workflow.

## Apply only clear housekeeping

Fix an unambiguous index omission, a local link with one established destination, or an obvious formatting/path error when the review request allows fixes. Honor a read-only request. Preserve before/after meaning and record each fix. Propose merges, archival, changes to canonical claims, or revised goals for the owner; do not delete sources or silently resolve uncertainty. Source refresh needs its own authorized source scope and available tool, not merely a stale date.

## Deliver one honest report

Write `BRAIN/maintenance/runs/<run-id>/review.md`, even for a single-workspace review. Include scope, per-workspace coverage and skips, checks performed, fixes, unresolved findings, evidence pointers, failed sources, and the next material decision. Link it from each inspected workspace's `wiki/log.md` only when writing is allowed. A read-only request returns the report in chat unless saving was authorized.

Make the chat result useful on its own. Surface each material item needing the user's action or judgment with the workspace, what needs attention, the concrete next action or decision, whether it is new/changed or still open, and a link to its evidence or report section. Group related details instead of copying the full report. State coverage failures in chat. When no user action is supported by the review, say that plainly and link the report. Do not bury actionable findings behind the report link or turn uncertain source status into a task.

One unavailable workspace or source need not block independent checks, but makes the affected coverage partial. Distinguish complete, sampled, skipped, and failed workspaces; a folder's existence is not proof it was reviewed. A recurring review requires a separately configured supported scheduler; this skill creates no schedule.
