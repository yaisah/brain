# Brain

**An AI-assisted second brain for work and life, built around an agent-maintained wiki.**

Keep original sources, turn them into connected knowledge, and use that knowledge
to support your projects, goals, and decisions. Your agent handles organization and
maintenance within the scope you request; you guide the priorities and review
important conclusions. Separate workspaces keep businesses, careers, research,
and personal life organized in one brain.

Brain uses ordinary files. Ingestion, planning, and maintenance run when requested;
recurring routines require separate configuration. The top-level `Brain/` folder
contains your private knowledge alongside the generic toolkit. The release builder
includes only the public toolkit files.

[Start here](#start-here) · [How Brain works](#how-brain-works) · [Structure](#structure) · [Everyday use](#everyday-use) ·
[Manual setup](#manual-setup) · [Privacy and sharing](#privacy-and-sharing)

## Start here

1. Extract the toolkit; the release contains a folder named `Brain`.
2. Open that `Brain` folder as a local project in Codex, or start
   Claude Code there. Opening the folder alone does not run anything.
3. Send:

   > Help me get started. Initialize my brain here, help me choose my first workspace,
   > and do one useful thing. Reuse what I tell you and leave other details unknown.

The agent follows [guided setup](docs/GETTING_STARTED.md), checks Python, installs
local core skills, initializes the brain, and creates or resumes a workspace. It
asks at most two concise questions at a time. Accounts, metrics, branding, and
scheduled routines can wait. You can supply the essentials immediately:

> Create a career workspace called Career Lab for exploring product management.
> First, help me plan one portfolio case study. I have no sources yet.

Prerequisites: an agent with local file/command access and Python 3.11 or newer.
Agent accounts and usage are separate from this MIT-licensed toolkit. macOS is the
initial validated environment; check [validation limits](docs/VALIDATION.md).
If the guide is not discovered, ask the agent to read it. Newly installed skills
can be read directly in the first session; restart the agent if its picker needs
to refresh. See the official [Codex instructions guide](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
and [skills guide](https://learn.chatgpt.com/docs/build-skills).

## How Brain works

**Second brain** describes the purpose: help you remember, understand, decide,
and act. **LLM wiki** describes how knowledge is maintained: your agent builds
and updates connected, source-linked pages as useful information arrives.
**Automation** describes when those workflows run. These ideas work together;
you can use Brain on request and add scheduled routines later.

A typical workflow is **capture → interpret → connect → use**. For example, a
meeting transcript is preserved in `raw/`; its workspace interpretation records
what was discussed, decided, and left uncertain. Supported, useful findings can
then update existing wiki pages and inform a plan or deliverable. Keeping the
wiki current means connecting new evidence to what is already known, including
contradictions, rather than only accumulating separate meeting summaries.

![Source lifecycle diagram showing one original captured in shared raw storage, separate workspace interpretations, and evidence flowing into each wiki and output](docs/images/architecture/03-source-lifecycle.svg)

*Source lifecycle, using fictional workspaces. The [source guide](docs/SOURCES_AND_ROUTING.md)
explains how receipts track each destination.*

Your durable memory lives in the files. In later sessions, the agent must read
the relevant context; saving a note does not train the underlying model or make
it automatically available in every chat. Preserved sources remain evidence,
with their original limitations; generated interpretations can need correction.

Obsidian is an optional way to browse and edit the files. The broader second-brain
approach is described in [Tiago Forte's guide](https://fortelabs.com/blog/basboverview/);
the maintained-wiki pattern is described in
[Andrej Karpathy's LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

## Structure

![Brain system overview showing the public toolkit, optional agent host connections, and private shared and workspace files](docs/images/architecture/01-system-overview.svg)

*The toolkit is public; your sources, workspace notes, and plans stay in ignored
private paths. Workspace names in the diagram are fictional.*

```text
Brain/
  AGENTS.md / CLAUDE.md          Agent entrypoints
  docs/OPERATING_GUIDE.md        Shared operating rules
  skills/ / optional-skills/    Generic methods
  templates/ / examples/        Empty scaffolds and fictional practice inputs
  scripts/ / docs/              Local helpers and guides
  INDEX.md                      Private workspace directory and shared notes
  registry.json                 Private workspace scope, status, flags, app paths
  integrations.json             Private approved accounts, sources, and routing rules
  context/                      Private shared goals, capacity, and preferences
  inbox/                        Private unassigned or ambiguous intake
  raw/                          Private original files, captured once per content version
    my-workspace/               Sources initially assigned to one workspace
    shared/                     Sources initially assigned to multiple workspaces
    unassigned/                 Sources awaiting a routing decision
  maintenance/                  Private run records, intake receipts, evaluations, cache
  outputs/                      Private daily plans and cross-workspace artifacts
  Projects/                     Private workspaces
    my-workspace/
      PROJECT.md / context/     Purpose, goals, scope, and relevant facts
      STORY.md                  Current focus and links to canonical actions
      SOURCES.md                Generated source catalog, versions and evidence gaps
      Ingestion/                This workspace's interpretation of shared sources
      wiki/                     Durable knowledge and its index
      outputs/                  Workspace-specific drafts and artifacts
      app/                      Optional application code
```

Setup creates the private root files and folders when first needed. There is no
inner live `brain/` directory. The public `templates/root/` folder holds the empty
scaffold used by setup. You can rename `Brain`; discovery uses the `.brain`
marker, not the folder's name.

A **workspace** is an ongoing area of work or life. An **initiative** is a finite
effort inside it. A **goal** is a desired outcome; a **task** is an action; a
**source** is evidence. Types are `business`, `career`, `personal`, `research`,
and `general`; they guide questions rather than restrict methods.

Add topic pages, initiatives, people profiles, hypotheses, or a task tracker only
when needed. Keep each action's status in one canonical place and link to it from
daily plans. A pet-care topic can link to original vet records in shared raw; it
does not require a separate workspace or make the full history relevant to every task.

Originals and intake records are shared. Interpretation stays with the workspace.
A transcript concerning two workspaces is captured once and can support two scoped
syntheses. Its presence does not justify copying its entire contents into both wikis.
See [sources, routing, and registry](docs/SOURCES_AND_ROUTING.md).

Browse ordinary files under `raw/<workspace>/`, `raw/shared/`, or `raw/unassigned/`,
or use each workspace's generated `SOURCES.md`. Add a meaningful topic subfolder
only when useful. Source IDs, checksums and processing history stay in
`maintenance/intake/`; receipt routing determines workspace access, not the folder
name. Existing captures keep their paths on retry or routing changes. See
[source browsing](docs/SOURCE_BROWSING.md) for naming, catalogs and approved relocation.
Capture dates are retrieval dates, not authorship dates.

## Everyday use

For work in one workspace, name it:

> For career-lab, use this supplied note to update what we know and suggest the next step.

For a brain-wide request, say so naturally:

> What should I focus on today across my active workspaces?

> Review my brain this week: find stale context, broken source links, and unresolved items.

The agent uses the registry's planning or review scope and shared preferences.
It starts with goals, current stories, and task indexes, then reads deeper only
when needed. It saves a daily plan under `outputs/` and review coverage
under `maintenance/`. It does not ask you to select each included workspace.
Paused/archived workspaces and disabled participation flags are excluded.

A connected intake routine can process an approved collection once each day and
route its items to multiple workspaces. For example, a 9 a.m. meeting tagged
Studio A and a 10 a.m. meeting tagged Studio B can reach different destinations
in the same run. Trusted provider metadata and approved mappings drive routing;
ambiguous items wait in the inbox. Imported prose cannot grant access or redirect work.

Configure source/account scope and destinations once. The host can then run one
user-approved schedule for intake, one for daily planning, and one for weekly review.
Each routine reuses that scope; it does not need one schedule per workspace.
This toolkit supplies workflows and local helpers, **not a Notion client or scheduler**.
An actual connector/host must be available. Setup activates no connections or schedules.

Use local skill names such as `$ingest` in Codex or `/ingest` in Claude Code.
If a name overlaps another installed skill, ask the agent to read this toolkit's
explicit `skills/<name>/SKILL.md` or `optional-skills/<name>/SKILL.md` path.
The [capability map](capabilities.json) lists methods for capture,
planning, evidence review, discovery, writing, delivery, and visual artifacts.
Use product-management frameworks only when they fit the task.

## Longer tasks and multiple agents

For a longer assignment or a handoff between chats, use the optional
`coordinate` workflow. It records bounded work, exact editing ownership,
separate worker reports, validation evidence, and what happens after completion.
It works with available agent tools or sequential work; tmux is optional.

> Coordinate research and drafting for my selected workspace. Use my existing task
> tracker, give workers separate outputs, and return findings before implementation.

Read [coordination](docs/COORDINATION.md). Generic work-card and handoff templates
live in `templates/coordination/`. Actual cards, when there is no existing task
tracker, live in `Projects/<slug>/coordination/tasks/`; run plans and reports use
`maintenance/runs/<run-id>/`. These private folders are created only when useful.
STORY.md links to authoritative tasks rather than maintaining a second status list.

Workers prepare separate outputs and a designated writer integrates shared notes.
This is a coordination convention, not an automatic reservation system. Independent
jobs that could edit the same targets must be serialized before those writes.

Install optional skills with `python3 scripts/brain.py setup --with-optional`, or
have the agent read `optional-skills/coordinate/SKILL.md` directly. Local
installation enables discovery; it does not launch agents or schedule anything.

## Manual setup

Run commands from the toolkit root. Verify Python first:

```sh
python3 --version
```

Use Python 3.11+. If necessary, substitute an already available supported interpreter
in every command. An agent must not silently install a runtime or optional packages.

```sh
python3 scripts/brain.py setup
python3 scripts/brain.py verify --installed
python3 scripts/brain.py init-brain
python3 scripts/brain.py new-project career-lab --name "Career Lab" --type career --purpose "Explore a career change"
python3 scripts/brain.py resolve --project career-lab
python3 scripts/brain.py list-projects --scope planning
```

Core setup installs 30 local skills; `setup --with-optional` includes all 39
(30 core and nine optional) and preserves that choice on later setup runs. The
older `--with-visuals` flag remains an alias for the same optional bundle. Generated copies live under `.agents/`
and `.claude/`; edit canonical skills rather than those copies. Edited/unowned
generated files stop setup instead of being overwritten.

`init-brain` preserves existing files. `new-project` also initializes a missing brain,
registers the workspace, and updates the generated list in `INDEX.md`.
Existing workspaces are never overwritten. Type defaults to `general`; omitted
purpose remains unknown. `resolve-brain` returns this initialized root's path.
`list-projects` reads registered metadata, not every workspace's private content.

### Practice and optional artifacts

Create a demonstration workspace and follow the [fictional walkthrough](examples/walkthrough.md):

```sh
python3 scripts/brain.py new-project harbor-demo --name "Harbor Demo" --type business
```

> For harbor-demo, capture examples/first-note.md and preserve its source.

HTML slides and the prototype use the Python standard library. XLSX/PPTX need
the optional libraries. Install them only when wanted:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-artifacts.txt
python scripts/artifacts.py model --project harbor-demo --input examples/artifacts/model.json --name sample-model
python scripts/artifacts.py presentation --project harbor-demo --input examples/artifacts/presentation.json --name sample-deck --pptx
python scripts/artifacts.py prototype --project harbor-demo --input examples/artifacts/prototype.json --name sample-prototype
```

Without those libraries, omit the model command and `--pptx` and use your supported
Python command. Outputs stay in the selected workspace. For custom generator inputs,
copy the sample JSON into workspace outputs; preserve captured sources unchanged.

The financial helper is a simple recurring-customer model. Define another model
when the economics differ. Spreadsheet formulas need recalculation in Excel or
LibreOffice; the expected-results JSON is a separate check, not cached formula results.
The prototype supports 1–500 ideas; export changes before closing it.
Inspect rendering and interactions before relying on an artifact.

## Applications, upgrades, and migration

An application can live in a workspace's `app/` or an explicitly referenced external
repository. A stored path does not change filesystem permissions. Brain planning and
maintenance skip application source trees. See [application work](docs/APPLICATIONS.md)
for coding-session roots, dependencies, and permission boundaries.

For software delivery, the application guide also explains document ownership and
provides a coding-agent handoff checklist. Optional templates cover
[technical designs](templates/delivery/technical-design.md) and
[architecture decision records](templates/delivery/architecture-decision.md),
alongside product briefs and delivery plans. Keep each document in one authoritative
location and link it from Brain. Use these when needed; workspace setup creates no
application scaffold or mandatory engineering documents.

For an upgrade, preserve a complete backup and extract a fresh release into a new
location. Transfer the private root paths together: `Projects/`, `raw/`, `inbox/`,
`maintenance/`, `context/`, `outputs/`, `INDEX.md`, `registry.json`, and
`integrations.json`. Review canonical skill changes, then run setup and verification.
Do not copy generated `.agents/`, `.claude/`, or `.local/` state over the new install.
Version 0.2 nested `brain/`, older project layouts, and existing personal vaults use
the [manual migration guide](docs/MIGRATION.md). The CLI does not migrate them silently.

Uninstall removes unchanged generated skills and their installation manifest.
It preserves the brain, canonical methods, and unrelated files.

## Privacy and sharing

The private root paths listed above are excluded from Git and public releases by
default, as are retained legacy `brain/` and `wiki/` folders. Keep personal content
in those paths; public instructions, skills, templates, and examples stay generic.
This is a workflow boundary, not encryption or separate OS permissions. AI services
and connectors have their own processing/settings.

**Share an allowlisted release, not the working folder.**

```sh
python3 scripts/brain.py verify
python3 scripts/brain.py doctor
python3 scripts/brain.py build-release
```

The archive appears in `dist/` and extracts into `Brain/`. Packaging rejects private paths, symlinks, Finder
metadata, and common secret patterns. Review content and [provenance](NOTICE.md);
scanning does not establish that arbitrary prose is safe to publish. For GitHub,
review a clean extracted release and publish that copy when ready. Nothing is uploaded
by setup or packaging. Private/third-party material does not acquire redistribution
rights merely by being stored in this toolkit.

A private backup should preserve the whole working `Brain/` folder, including hidden
files, plus any external app repositories separately. Keep that backup private;
the public release archive is not a backup of your knowledge.
A single-workspace export must carry its required evidence and working source links.
Mixed-workspace sources require explicit review before inclusion; see the source guide.

## Troubleshooting and validation

| What you see | Next step |
|---|---|
| Nothing happens after opening the folder | Send “Help me get started,” or explicitly request the guide. |
| Unsupported/missing Python | Use a verified supported interpreter consistently; report the exact blocked step. |
| No brain or workspace | Initialize the brain or create/select the intended workspace. |
| Nested brain or older layout detected | Back up and follow the migration guide. |
| Project conflict | Confirm the workspace, then resolve from the toolkit root. |
| Missing/stale local skills | Run doctor and verify; refresh unchanged generated copies with setup. |
| Edited or unmanaged generated file | Preserve it and reconcile intended edits before rerunning setup. |
| Unassigned intake or connector failure | Keep the item/checkpoint pending and report its specific gap. |
| Artifact or archive already exists | Choose a new name; inspect the existing version before replacing it. |

Run `python3 -m unittest discover -s tests -v` with fictional fixtures, then verify
and inspect a clean extracted release. Optional libraries and Node are needed for
their corresponding checks; missing capabilities must be reported honestly.
[Specification](docs/PRD.md) · [Executed validation and limits](docs/VALIDATION.md).
