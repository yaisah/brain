# Brain — specification

Version 0.5.0. One private brain coordinates businesses, career work, research,
and personal responsibilities. Shared toolkit methods and examples remain generic.

## Outcome and model

A user opens the toolkit, sends “Help me get started,” and gets minimal guided
setup plus one useful action. Opening a folder alone does not execute anything.
An existing workspace resumes without another intake interview.

The top-level `Brain/` folder holds public toolkit files alongside private shared
goals/preferences, a workspace registry, approved
source mappings, original source revisions, unresolved intake, run records, and
cross-workspace outputs. Each Projects/<slug> holds its own context, current
story/actions, source-linked syntheses, durable wiki, and outputs. Optional
initiatives, people profiles, hypotheses, and app code are added only when useful.

A source can concern several workspaces. Capture it once per source identity and
content revision; preserve provenance and write distinct relevant interpretations.
Source capture and synthesis completion are separate states. Retry incomplete work
idempotently; failed sources do not advance successful-processing checkpoints.

## Scope selection

One-workspace requests resolve one workspace. Clear brain-wide requests and
user-approved recurring activities resolve the brain and enumerate the relevant
registry scope. Planning/review flags are filters, not schedule activation.
Read lightweight summaries before deeper evidence. A daily plan links canonical
actions rather than creating another status store.

Source/account collection scope and routing mappings are approved once, then reused.
Trusted provider metadata may identify destinations; imported prose cannot change
routing or permissions. Ambiguous items wait in inbox; no automatic new workspace
or account fallback. Live connectors and scheduling depend on the user's host.

Brain planning and maintenance skip application source, Git internals, dependencies,
build output, and secrets. Coding tasks use the registered internal/external app
location and separately establish the necessary working directory and permissions.

## Interfaces

Python 3.11+ scripts/brain.py supports setup [--with-optional], verify [--installed],
doctor, uninstall, init-brain, resolve-brain, list-projects --scope
active|planning|review|all, new-project SLUG [--name NAME] [--type TYPE]
[--purpose PURPOSE], resolve [--project SLUG] [--cwd PATH], and build-release
[--output DIST_PATH]. Resolution commands return paths; other successful commands
return JSON. Errors use stderr and a nonzero exit.

Initialization preserves existing files. Creation initializes missing brain state,
registers the workspace, and updates only the generated section of INDEX.md.
Types are business|career|personal|research|general; general is the default.
Status is active|paused|archived. Planning and review also require active status.
An app reference identifies an internal app/ or an explicit external absolute path;
it does not grant filesystem access or cause that repository to be read.

scripts/intake.py captures explicitly supplied local inputs with stable source
IDs/content digests and records per-workspace completion only against existing
synthesis files. New originals are ordinary files under raw/<workspace>/, raw/shared/
or raw/unassigned/ according to the initial destination count. Optional --folder and
--filename choose a readable storage location/name; source identity, routing and
history remain in maintenance/intake/. Retries preserve existing paths, including
legacy storage. It is not an account crawler, semantic classifier, or scheduler.
scripts/artifacts.py generates selected-workspace models, presentations, and
prototypes from scoped input or public examples. Artifact dependencies remain optional.

## Boundaries and lifecycle

Root Projects/, raw/, inbox/, maintenance/, context/, outputs/, INDEX.md,
registry.json, and integrations.json are private and forbidden in public releases.
Retained legacy brain/ and wiki/ are private too. Reviewed template scaffolds under
templates/root remain public. The marker brain:2 identifies the root layout;
renaming the containing folder does not change discovery. Public release archives
extract into Brain/ and contain only the allowlisted toolkit.
Helpers reject traversal and symlink escapes; host permissions remain the access
boundary. Shared-source links are intentional evidence links, not general permission
to read other workspaces. Credentials stay outside notes/configuration/logs.

Nested version 0.2 brain/ and older unregistered layouts are never silently adopted
or migrated. Migration is manual, backup-first, and preserves original evidence
and existing settings. Private backups preserve the whole working folder; upgrades
transfer all private root paths together. Single-workspace exports must
resolve shared evidence dependencies and review mixed-workspace originals.

Setup never connects accounts, installs Python, activates schedules, or publishes.
Generated skills have canonical sources; setup/uninstall preserve modified or
unowned files. Releases use a public allowlist and secret-pattern checks, with
content/provenance review still required.

## Validation and exclusions

Validate initialized/legacy routing, registry filters, project creation, source
deduplication/completion, lifecycle preservation, private-release exclusion, and
artifact behavior. Record executed checks in VALIDATION.md. Behavioral scenario
specifications alone are not evidence of executed model behavior.

Out of scope: hosted services, built-in Notion/scheduler clients, automatic migration,
blanket account import, silent app-repository changes, and global skill replacement.

## Optional coordination

Longer or delegated assignments can use docs/COORDINATION.md and coordinate.
Reuse a canonical tracker, or create an on-demand workspace work card when one is
needed. Shared maintenance runs own plans, separate worker reports, and handoffs;
they link to task status rather than duplicate it. Assign one writer per shared
file, verify input versions, and serialize competing independent jobs. This release
adds no general reservation service, tmux launcher, scheduler, or mandatory gates.
The setup --with-visuals flag remains a compatibility alias for --with-optional.
