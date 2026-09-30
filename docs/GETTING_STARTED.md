# Guided setup

Open the top-level `Brain/` folder in your agent and send **“Help me get started.”**
Opening the folder alone does not run the agent. This guide works before skills,
private root files, or a first workspace exist. Setup uses this folder as the brain;
it does not create an inner live `brain/` directory.

## Your first useful loop

**Choose one area → add one useful source → ask one real question → keep what you learn.**

Start with a business, career focus, personal responsibility, or research topic.
A source can be a note, document, or transcript. Ask a question that matters now,
such as “What changed in this meeting, and what should I follow up on?” Your agent
preserves the source, creates a relevant interpretation, and can connect supported,
useful findings to the workspace's existing wiki. You guide what matters and review
important conclusions.

You can also start with a goal and no existing notes: make one useful plan and add
sources as they become relevant. There is no need to fill every template or import
your whole history before beginning. Agents should use the setup steps below to
enable this first useful action, reusing context the user already supplied.

For the distinction between a second brain, an LLM wiki, and scheduled automation,
see [How Brain works](../README.md#how-brain-works). Memory is stored in files that
future sessions must read. Background routines are configured separately.

## 1. Choose the next useful action

Reuse the request's facts and any unambiguous existing selection. Ask at most two
concise questions per turn, only for information needed now. For a fresh brain:
“What would you like to organize first, and what should we call that workspace?”
A supplied name, purpose, and first task need no repeat interview.

An existing selected workspace keeps its slug. Verify the runtime, resolve it, and
read its context before asking about purpose or focus. A clear whole-brain request
such as “What should I do today?” uses brain mode; it does not require a single
workspace selection. If intent is unclear, ask whether the work is brain-wide
or for a particular workspace.

A one-workspace request conflicting with the actual working directory requires
clarification. Preserve the original directory for conflict detection; after the
user confirms a switch, run from the root with the confirmed selection.

Completion: mode and immediate intent are clear; optional details can stay unknown.

## 2. Verify the runtime and local skills

Locate this toolkit by its `.brain` marker (`brain:2` for the root
layout), regardless of the folder name. Check Python:

```sh
python3 -c 'import sys; print(sys.executable); print(sys.version); raise SystemExit(0 if sys.version_info >= (3, 11) else 1)'
```

If missing or too old, check an already available interpreter from the host/PATH.
Use the same verified Python 3.11+ for every later command; substitute its quoted
absolute path for `python3` as needed. Report the exact blocker if none is available.
Do not install a runtime or optional packages without consent.

If already installed, `verify --installed` can confirm setup is unnecessary.
For fresh setup, or safely refreshing unchanged generated copies, run:

```sh
python3 scripts/brain.py setup
python3 scripts/brain.py verify --installed
```

Preserve edited or unowned generated files if preflight rejects them. Explain the
specific recovery needed rather than overwriting. Include `--with-optional` when the user wants the optional bundle, including
coordination, visual, and review helpers. `--with-visuals` remains a legacy alias
for that same bundle. A canonical optional SKILL.md can also be read directly
without installing the bundle.

Completion: runtime and local skills are verified, or a concrete limitation is
reported. Use the manual fallback below when commands cannot run.

## 3. Initialize or resume

```sh
python3 scripts/brain.py init-brain
python3 scripts/brain.py resolve-brain
```

Initialization is idempotent and preserves existing content. For a nested `brain/`
from version 0.2 or another older layout, follow [manual migration](MIGRATION.md);
never silently adopt existing notes or overwrite their metadata. In the current
layout, registered workspaces belong directly under `Projects/`.

For a selected existing workspace, resolve its slug and read its PROJECT.md,
profile, goals, preferences, and STORY before asking additional intake questions.
For a new workspace, derive a short lowercase slug with hyphens. Infer type when
clear, otherwise use `general`; omit purpose when unknown:

```sh
python3 scripts/brain.py new-project SLUG --name NAME --type TYPE --purpose PURPOSE
python3 scripts/brain.py resolve --project SLUG
```

Replace placeholders with safely quoted actual values. Types are `business`,
`career`, `personal`, `research`, and `general`. Missing-workspace errors during
creation requests lead to creation, not repeated selection questions. Existing
names are never overwritten; preserve their registered slug.

New workspaces are active and included in planning and review by default
(`planning: true`, `review: true`). Explain these defaults when creating one.
Existing exclusions survive setup and upgrades. These flags select eligible
workspaces; they do not activate an automation. Before scheduling a review, use
[the routine scope preflight](SOURCES_AND_ROUTING.md#routines-and-efficient-reading).

For whole-brain planning or review, resolve the brain and use `list-projects --scope
planning` or `--scope review`. Read shared context and only the included workspaces'
lightweight goals/current work. An empty registry means ask for a first area or
record a concrete next step; it does not justify importing an old vault.

Ordinary local setup and creation are included in a getting-started request. Honor
any explicit request to preview changes first. No source connection or recurring
routine is activated by these commands.

Completion: the brain and needed workspace(s) resolve, with the scope explicit.

## 4. Record minimum context and help

Fill only user-supplied facts or specifically authorized evidence. Record a source
and date; a dated reference to the setup conversation is valid. Leave optional
metrics, budgets, constraints, and branding unknown. Shared goals/capacity belong
in context; workspace-specific purpose/goals belong in that workspace.
Record actions in STORY or a linked canonical tracker. Do not turn every small
capture task into a strategic goal.

Do one useful thing: capture a supplied note, make a small plan, or draft the
requested artifact. Use the appropriate canonical local skill from
capabilities.json. If local skill discovery has not refreshed, read that skill's
canonical SKILL.md directly in this toolkit; a new session may refresh the picker.

Originals go to shared raw through scoped intake. Workspace Ingestion/wiki
contain only relevant interpretations with source IDs and resolving links.
Brain-wide outputs go to outputs; run records/checkpoints go to
maintenance. Source connections and routing are configured once under
[the source guide](SOURCES_AND_ROUTING.md), only when requested.

Completion: known context is sourced, unknowns are clear, and the useful action
is done or its concrete next step is ready. Check actual files and links. Report
paths, results, and gaps without claiming unexecuted verification.

## If file or command tools are unavailable

Say what is unavailable, provide the relevant commands with actual values and a
short context draft, and ask for output only when needed. Do not claim files were
created, skills installed, or checks passed without evidence. Existing account
sessions, sibling folders, and global memory are not automatic sources.
