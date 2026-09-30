---
name: coordinate
description: "Coordinate longer or delegated tasks, resume interrupted work from evidence, or prepare a requested work plan and handoff. Simple tasks need no coordination files."
---

# Coordinate work and handoffs

## Establish the scope

Find the nearest enclosing `.brain` marker and read that toolkit's `docs/OPERATING_GUIDE.md` before
private content. For workspace work, resolve through `brain.py resolve`; a
cross-workspace request retains its explicitly selected scope and an owning
workspace for each task. Toolkit maintenance uses the requested public-file scope
without requiring a private workspace. `BRAIN` is the main folder.

Read `BRAIN/docs/COORDINATION.md` before creating or resuming coordination records.
Resolve every `BRAIN/` resource from the discovered marker root, including when
reading an installed copy of this skill.
Honor a read-only request by returning the plan or handoff in chat without saving
files. A request for a plan alone does not start execution. Reuse authorization
already given for the local task.

## Make the next step executable

Locate the canonical task record and current evidence first. Reuse an existing
tracker through its link. For workspace work without a tracker, use
`BRAIN/templates/coordination/work-card.md` at
`Projects/<slug>/coordination/tasks/<work-id>.md`, with a link from `STORY.md`.
Toolkit maintenance without a tracker uses the authorized request and run plan as
its scope record; do not create a private workspace, work card, or STORY link for it.
Run reports do not duplicate a canonical task's live status.

For work needing a durable run, keep the plan at `maintenance/runs/<run-id>/plan.md`,
unique worker reports at `workers/<worker-id>.md` within that run, and its final
handoff at `handoff.md`. Create only useful records. Each assignment identifies its
outcome, exact writable paths, input versions, expected outputs, evidence checks,
next action, and the boundary for returning results, proposing follow-on work, or
continuing within the approved scope. Public toolkit changes require that task scope.

Use actual available delegation tools when useful; otherwise execute sequentially
and describe the limitation. Agent identities are temporary execution references.
Each worker owns its report; one designated integrator owns each shared destination.
Markdown assignments and existing intake locks do not reserve files against other
chats or processes. If competing writers cannot be excluded, serialize through the
host or stop shared writes, preserving separate drafts until a real reservation
exists. Recheck input versions before integration and reconcile drift deliberately.

## Resume, verify, and return

On resumption, inspect actual files, versions, and relevant host task state before
trusting a saved status. Old notes are not proof that a worker is running or a task
is complete. Verify outputs against the stated criteria; distinguish evidence from
reported claims and unperformed checks. When independent review is warranted, use
the existing workflow at `BRAIN/skills/converge/SKILL.md`, reading that
canonical file if it is not installed; do not invent independent reviewers.

Use `BRAIN/templates/coordination/handoff.md` for a worker or
run report. Record actual identities when known, remaining gaps, and one next action.
Link evidence and the canonical task record; update that record only for verified
changes within scope. End according to the agreed completion behavior. A handoff
does not schedule future work, publish an artifact, or grant new permissions.
