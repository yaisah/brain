# Coordinating delegated work

Use this workflow for longer assignments, multiple workers, or a handoff that must
survive a new chat. A small task can use the ordinary workspace workflow. This is
an optional operating convention, not a scheduler, tmux launcher, or file-lock service.

The workspace owns the outcome and its evidence. Agents supply temporary capacity.
Terminal panes, chat titles, and remembered worker status are execution context;
check actual files and available host state before treating a worker as active.

## Choose scope and the authoritative task

Follow `docs/OPERATING_GUIDE.md` to resolve the selected workspace or explicitly approved group.
Toolkit maintenance uses the requested public-file scope without requiring a
private workspace. Reuse the user's existing authorization, constraints, and completion criteria.
Delegating part of a request does not expand its source access or allowed actions.
For a read-only request, return the plan or handoff in chat without writing records.

Use the workspace's established task tracker when there is one. Link its task IDs
from the run plan and `STORY.md`; do not copy its current task status into another
tracker. When a durable task record is useful and no tracker exists, use
[the work-card template](../templates/coordination/work-card.md) at
`Projects/<slug>/coordination/tasks/<work-id>.md`. That card is then the task's
canonical home. Create these folders only when needed. Cross-workspace runs link
each selected task rather than creating a second global task database.
For toolkit maintenance without a tracker, the authorized request and run plan
define scope; do not create a private workspace or work card just for that work.

## Prepare one run

Use a new, noncolliding `maintenance/runs/<run-id>/` directory. The coordinator owns
`plan.md` and the final `handoff.md`; workers own separate
`workers/<worker-id>.md` reports and explicitly allocated draft paths. Keep final
deliverables in the owning workspace's normal outputs, ingestion, or wiki location.
Toolkit changes belong in their authorized public paths. All live coordination
records stay in private paths; generic templates remain public.

The plan records only what is needed to execute and resume:

- Run ID, selected workspaces, canonical task links, and coordinator identity as known.
- Goal, scope, relevant source IDs or input paths, and observable completion criteria.
- Assignments: role/worker, exact writable paths, expected output, and dependencies.
- Input versions: content digests or repository revisions, plus the files they cover.
- Shared-file writer, required validation, blockers, and the next permitted action.
- Completion behavior: return results, propose a next step, or continue within the
  approved scope. Reuse the user's instruction; clarify only if the distinction matters.

Use roles such as researcher, writer, and reviewer only when useful. Record actual
worker handles if the host supplies them; otherwise use a local role label and say
the runtime identity is unknown. A planned assignment is not a launched worker.
Use available delegation only within the authorized task. If unavailable, work
sequentially and report that fact. No particular agent host or terminal is required.

## Keep edits from colliding

Before dispatch, check that writable path sets do not overlap, including parent
directories and common indexes. Workers can research or draft in parallel in their
allocated files. Assign one integrator to each shared destination, such as
`STORY.md`, a wiki page/index, the root registry, or a canonical task record.
Workers propose changes to those files in their reports; the designated writer
validates and applies them. Separate workspaces may have separate integrators.

For each shared-file update, reread the current file and compare it with the input
version. If it changed, reconcile against the newer content and review the proposal
again. Preserve other writers' changes. A version check detects some stale work;
it does not make a later write atomic or reserve the file.

This convention assumes all competing writers are coordinated. If an independent
chat, collector, or maintenance job could write the same targets, arrange sequential
execution through the authorized host before shared writes. If exclusive ownership
cannot be established, preserve separate drafts and report the blocked integration.
An unattended system permitting overlapping writers needs an actual reservation or
transaction mechanism; this toolkit does not implement one for general note edits.
Never treat a Markdown assignment, timestamp, or expired-looking state as such a lock.

Existing helper locks cover registry-creation and individual intake transactions.
They do not cover the period between source capture and completed interpretation.
Atomic file replacement is also not protection against overwriting a newer version.
Inspect the owning operation before recovering a stale helper lock; age alone is
insufficient evidence that it is abandoned.

## Parallel intake and maintenance

Capture an authorized source once with the existing intake helper, then allocate
each `(source ID, content digest, destination workspace)` interpretation to one
worker in the run plan. A pending receipt is retryable work, not an exclusive claim.
Several sources may affect the same wiki page: keep their final integration under
the designated writer even when their interpretations are drafted independently.

The integrator checks source links and scope, writes the accepted destination
synthesis, and only then marks that destination complete. Failed or blocked work
remains pending. Maintain one run report with per-workspace coverage and unresolved
routing. If maintenance and intake touch the same files, serialize those writes.
Follow [source routing](SOURCES_AND_ROUTING.md) for provenance and checkpoints.

## Review, deliver, and hand off

Workers use [the handoff template](../templates/coordination/handoff.md) for compact
reports: inspected inputs, actual outputs, checks, blockers, and one next action.
Label proposed changes and unavailable validation. A report saying “ready” is
evidence to inspect, not acceptance or proof that the canonical task is complete.

Use independent review when the task's criteria or consequences warrant it. For
convergence, follow the existing canonical `skills/converge/SKILL.md`; it
requires real reviewers of the same artifact version and bounded review rounds.
An unavailable reviewer remains a gap. No fixed seven-stage process is required.

The coordinator verifies deliverables and evidence against the agreed criteria,
then updates the authoritative task when that update is authorized. Keep task
status there; worker/run status describes execution only. Link outcomes from the
workspace's story and preserve useful learning in its normal knowledge files.
Record unfinished or failed work explicitly in the final run handoff.

Follow the selected completion behavior. A proposed next step does not authorize
itself. Close or stop only sessions/monitors owned by this run and authorized for
cleanup; leave unrelated sessions alone. A terminal label is not proof of completion.

## Resume from evidence

Read the canonical task, run plan, and latest handoff first. Verify the relevant
files, artifact versions, and actual worker/session state when available. Record
when this check occurred. Treat an unavailable worker's liveness as unknown.
Reconcile missing outputs, changed inputs, and conflicting status before resuming.
Completed and accepted work should not be repeated merely because a chat is new.

For app work, verify the exact repository/worktree, revision, current changes,
and session access using [the application guide](APPLICATIONS.md). Brain coordination
does not move repositories or grant permissions. Resume only the remaining approved
work; surface scope changes or unresolved ownership before applying shared edits.
