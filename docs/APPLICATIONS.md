# Application work

A workspace can contain application code at Projects/<slug>/app/, or point
to an existing external repository. Record that choice in the workspace entry
of registry.json:

```json
{"kind": "internal", "path": "app"}
```

```json
{"kind": "external", "path": "/explicit/approved/repository"}
```

These values replace the entry's application: null. The external example is a
placeholder, not permission to search for a repository. Avoid symlinks as a way to
make an external checkout appear internal.

## Start a coding task

Use the user's named workspace and registered app location. Inspect that app's
own project instructions and Git status when relevant to the requested coding
work. An ordinary brain review or daily plan reads no application tree.

Choose a working directory and host workspace roots that include the files the
coding task must read/write, including normal test/build outputs. For an internal
app, the toolkit-root session may already cover them. For an external repository,
open a coding session there or explicitly add/authorize its root using the host's
supported controls. Refer back to named brain context as needed; do not copy the
entire brain into the app.

A nested Git repository or separately opened app session may have its own instruction
boundary. Verify which instructions the coding session actually loads. When app-local
AGENTS.md instructions are needed, retain the app's own coding rules and add a short
pointer to the toolkit rules and selected workspace's relevant context, using verified
relative or explicit paths. A pointer does not grant access or require reading the
whole brain. Avoid copying brain contents or overwriting existing app instructions.

A registry path, Markdown instruction, or tool working directory does not expand
filesystem, network, or approval permissions. Permissions depend on the host.
Dependencies, remote access, deployment, destructive operations, or out-of-scope
paths may require additional authorization; the toolkit cannot promise zero
approval prompts. Request only the access necessary for a concrete operation.
Script-level path checks do not establish native desktop permission behavior;
verify that behavior in the actual coding session.

## Choose documentation that fits the work

Reuse the application's existing conventions and create documents only when they
help the selected task. A small change can use one brief with separate sections;
separate documents help when they need different reviewers or evolve independently.

| Artifact | Purpose | Starting point |
|---|---|---|
| Product brief / PRD | User problem, intended behavior, scope, outcomes and success measures | [Product brief](../templates/delivery/product-brief.md) |
| UX design | User flows, interaction states, accessibility and mockups | Brief's proposed-experience section, or a linked design document/tool |
| Technical design | Implementation approach, interfaces, tradeoffs, verification and rollout | [Technical design](../templates/delivery/technical-design.md) |
| Architecture decision record (ADR) | Rationale and consequences of one significant technical choice | [Architecture decision](../templates/delivery/architecture-decision.md) |
| Delivery plan | Demonstrable increments, dependencies and acceptance criteria | [Delivery plan](../templates/delivery/delivery-plan.md) |

A design proposal and an ADR serve different purposes. Keep current system structure
in the app's existing architecture document, such as `docs/ARCHITECTURE.md`.
Record constraints that must remain true there; use a separate `INVARIANTS.md` only
when useful. Link constraints to enforcing tests or checks where available.
A written rule alone does not enforce behavior. Keep contracts in their authoritative
schema/code location, and label generated documentation with its source/generator.

### One authoritative location

Choose one canonical location for each document, following the team's existing
practice. Product discovery and draft briefs can start in workspace `outputs/`.
Implementation-specific architecture, technical designs, ADRs and contracts should
normally live with the application code. For example, a repository might use
`docs/specs/<feature>/prd.md` and `technical-design.md`, plus `docs/adr/`; these are
optional examples, not a required scaffold or a command to move existing documents.

Link from the workspace's PROJECT, story, or wiki to the authoritative document.
A Brain summary records useful context with a source link; it is not another editable
copy of the specification. If an approved document changes home, repair its pointers
and clearly mark retained drafts as historical. Keep one canonical task tracker.

Record status, owner when known, update date, related artifacts and review evidence.
A populated template is still a draft until its relevant decisions are established.
When work changes behavior or architecture, update the affected canonical documents
with the implementation. Preserve an ADR's decision history by superseding it.

The Brain toolkit's own root `docs/` documents the toolkit. Project-specific records
belong in the selected private workspace or application repo. Generic templates are
optional starting points; normal workspace setup does not populate them.

## Application handoff checklist

Before handing approved work to a coding agent, record the following in the existing
issue, delivery plan or coordination handoff. Link to authoritative records rather
than creating another tracker. For a planning-only request, collect this information
without running implementation, deployment or unrelated application changes.

- **Repository and scope:** exact checkout, relevant revision/current changes,
  applicable agent instructions, allowed edits and the selected feature or issue.
- **Requirements and design:** canonical brief/PRD, relevant UX/technical design,
  document status, unresolved decisions and what blocks implementation.
- **Architecture and constraints:** relevant component/dependency rules, contracts,
  accepted ADRs and invariants; read the referenced context before editing.
- **Execution commands:** working directory, supported runtime/setup, and exact
  build, test, lint or type-check commands verified from the repo's scripts/docs.
  Reuse its existing command entrypoints; an unavailable command remains a gap.
- **Verification:** map acceptance criteria and important invariants to checks;
  distinguish planned checks, observed results and checks that were not run.
- **Delivery and ownership:** canonical action tracker, editing ownership when work
  is shared, review needs, and relevant rollout/recovery requirements. Follow
  [coordination](COORDINATION.md) if multiple writers may overlap.

Completion: the receiver can locate the approved scope and required context, run
the relevant checks within its authorized environment, and identify unresolved
blockers. On return, record actual results and changed canonical documents in the
same handoff. A completed checklist does not authorize publishing or deployment.

For background on concise decision records, see
[Michael Nygard's ADR description](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions).

## Keep knowledge and code maintainable

Code follows the app's own structure, tests, dependency files, and version control.
Record useful decisions and outcomes in the workspace, with pointers to the
appropriate code or review. The canonical action tracker remains in one place.

Brain maintenance skips app source, .git, installed dependencies, build output,
and secrets. An app code review or cleanup is a separately scoped task.
Public toolkit releases exclude private Projects/, including internal apps.
Publishing an app requires its own reviewed release process.
