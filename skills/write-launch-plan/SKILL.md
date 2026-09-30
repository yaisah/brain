---
name: write-launch-plan
description: "Prepare a project launch plan with readiness evidence, audience communications, owners, support, measurement, and rollback criteria."
---

# Write Launch Plan

## Resolve scope

Find the nearest enclosing `.brain` marker from this skill and read that toolkit's `docs/OPERATING_GUIDE.md` before private data. Follow its single-workspace routing with `brain.py resolve`; this workflow does not expand a selected workspace into the whole brain.

`TOOLKIT_ROOT` and `BRAIN` both mean the main `Brain/` folder; `PROJECT` is the resolved workspace under its `Projects/`. Shared resource paths below are toolkit-relative; unqualified knowledge and output paths are workspace-relative. Follow `docs/OPERATING_GUIDE.md` for shared evidence, central integrations, maintenance paths, and application access.

## Prepare a bounded launch

Read the project brief, delivery state, measurement plan, audience context, and prior launch decisions. Identify the release type and proposed audience; do not assume a public launch, paid campaign, or fixed date. Distinguish planned scope from verified available behavior.

Use `templates/delivery/launch-plan.md` to cover customer impact, rollout cohorts, eligibility, readiness checks, documentation and communications, support ownership, observation windows, and rollback or pause conditions. Each readiness claim needs an evidence reference, owner, and status. Include access, migration, failure recovery, and operational capacity when relevant. An unresolved critical dependency must remain a launch blocker even if a date has been announced.

Prepare audience-specific drafts using project brand and tone only when supplied. Keep internal enablement, customer messages, and external announcements distinct. Avoid unsupported promises, testimonials, availability claims, or dates. Describe what will be measured, when the readout happens, and who decides to expand or stop.

Save `outputs/YYYY-MM-DD_launch-plan_<topic>.md` and any communication drafts in the same selected project. This workflow does not publish, send, change rollout flags, or deploy. If the user later authorizes such an action, review the exact destination and current readiness at that point.
