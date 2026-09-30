# Manual migration to a root-level Brain

Version 0.5.0 uses the top-level `Brain/` folder itself as the brain. Shared private
paths live beside the generic toolkit files; workspaces live in `Projects/<slug>/`.
The `.brain` marker contains `brain:2`. The steps below cover earlier toolkit
versions, including the 0.3.0 flat layout, version 0.2 nested `brain/`, earlier
project layouts and existing personal vaults. For a multi-version upgrade, review
all applicable branches.
There is no automatic migration command. Keep the source intact while preparing a
reviewed destination; changing a marker alone does not migrate its content.

## Preserve a recoverable copy

Inventory the source folder, its layout/version, and any collectors, schedules,
mirrors, app references, or other consumers of its current path. Record their
scope. Arrange a coordinated writer cutover through the host only when authorized;
migrating files does not itself authorize changing schedules.

Back up the complete old working folder, including hidden files. Verify the backup
can be read and record original-source checksums. A compressed public template
preserves the toolkit, not an existing user's knowledge.

Extract the new public release into a **new location**. It supplies a `Brain/`
folder; keep the original alongside or elsewhere until verification is complete.
Check the supported Python interpreter and run setup there. Select the matching
migration branch below before initializing or copying private state.

## From version 0.4.4: simpler raw files

Version 0.5.0 stores new originals as ordinary files under `raw/<workspace>/`,
`raw/shared/` or `raw/unassigned/`, with optional meaningful topic folders. Source
identity, checksums, routing and history stay in `maintenance/intake/`. Refresh the
public toolkit and owned local skill copies together. Existing captures, including
version-1 storage, retain their paths during setup, retry and routing changes.

Relocating existing originals is a separate, explicitly scoped operation:

1. Coordinate affected writers, preserve a recoverable backup, and record an
   old-path → new-path map with each source ID and full checksum. Choose readable
   filenames and resolve collisions before moving anything. Historical imports can
   use a meaningful folder such as `raw/<workspace>/archive/`; this retains their
   content and does not mark them current or remove them from routing.
2. Follow [source relocation](SOURCE_BROWSING.md#explicit-relocation-of-existing-captures)
   to reserve destinations and stage byte-identical originals. Preserve source IDs,
   exact `original_name` values, capture timestamps, revision history, destination
   assignments and completion records. A new storage path is not a new capture.
3. Update storage/allocation records, receipts and active citations together under
   the coordinated cutover, then regenerate affected `SOURCES.md` catalogs. Keep
   prior run reports intact as dated history; add the path map and new verification
   report instead of rewriting old reports to make them look newly executed.
4. Verify destination bytes, identity/history preservation and resolving links
   before retiring superseded raw copies within the approved scope. Keep backups
   and leave unexplained files in place. Resume writers only after the new records
   and files agree, or restore the previous consistent state.

Ordinary ingestion does not perform this relocation. Source and capture dates are
unchanged; the move changes navigation only. It does not reset mirrors or create
or alter automations.

## From version 0.4.3

The blank root scaffold now lives at `templates/root/`. Update the template
directory, initializer and release allowlist together; remove the superseded
root-template directory after preserving any custom template edits. The live
Brain layout and private data do not move.

## From version 0.4.2

Version 0.4.3 gives the local skills shorter names, such as `ingest`, `review`, and
`coordinate`, without changing their workflows or private data layout. Preserve
custom edits first. Use a clean current release, or replace the canonical `skills/`
and `optional-skills/` bundles with those from the new release; overlaying renamed
directories would leave duplicate old canonical skills behind. Verify that only
the current canonical skill names remain before running `setup`.

Setup replaces owned, unchanged generated files and removes obsolete owned files.
Modified or unmanaged copies are protected: preserve and reconcile them when setup
reports a conflict. Directories containing unrelated user-added files can remain;
setup does not delete those files. Global skills are untouched. If a shorter name
overlaps another installed skill, ask the agent to read this toolkit's explicit
local `skills/<name>/SKILL.md` or `optional-skills/<name>/SKILL.md` path. Refresh
the agent's skill discovery as needed.

## From version 0.4.1

Readable source storage and generated workspace source catalogs are additive.
Existing receipts and hash-based raw paths remain valid and are not automatically
relocated by setup or retry. Refresh the generic toolkit and owned local skill copies;
follow [source browsing](SOURCE_BROWSING.md) for metadata/catalogs or an explicitly
authorized, backed-up relocation. Preserve all source identities and historical
verification reports. The root marker and private workspace layout are unchanged.

## From version 0.4.0

The shared operating manual now lives at `docs/OPERATING_GUIDE.md`. The private
layout and operating rules are unchanged. Update the public toolkit files together
and regenerate any installed local skill copies through setup so their pointers
follow the new path. Preserve customized copies if setup reports a conflict.

## From version 0.3.1

The root layout, `.brain` marker, and installation identity are unchanged. Preserve
private state and custom changes before upgrading toolkit files. Coordination adds
public templates and an optional skill; no new private workspaces or task records
are populated during setup. Use `setup --with-optional` to include the optional
bundle; an existing enabled optional bundle remains enabled on later setup runs.
The previous `--with-visuals` spelling is still accepted. Regenerate owned local
skill copies through setup, preserving edited copies when its preflight reports a
conflict. Use [coordination](COORDINATION.md) only for work that benefits from it.

## From version 0.3.0 with the same root layout

Version 0.3.1 renames the toolkit and its marker/installation metadata while keeping
the private layout unchanged. Use a clean current release rather than changing the
marker or editing generated installation manifests in place. Transfer the private
root paths together: `Projects/`, `raw/`, `inbox/`, `maintenance/`, `context/`,
`outputs/`, `INDEX.md`, `registry.json`, and `integrations.json`. Preserve original
bytes, identities, receipts, and registry flags; review additional user-created files
for a private destination.

Regenerate local skills with the current `setup` command and verify the installation.
Keep old `.local/`, `.agents/`, and `.claude/` state in the backup, with any custom
edits retained for deliberate reconciliation. Relative links within the private
layout keep the same depths. Check absolute paths, app instruction pointers, and
approved host routines against the new location before cutover. Finish with the
verification steps below; copying files does not activate or change any schedule.

## From version 0.2 with an inner brain/

When the destination has no private state, copy all of the following from the old
`brain/` into the new root together:

- `Projects/`, `raw/`, `inbox/`, `maintenance/`, `context/`, and `outputs/`.
- `INDEX.md`, `registry.json`, and `integrations.json`.

Preserve registry identities, lifecycle flags, source IDs/digests, intake receipts,
checkpoints, histories, and unknown fields. Keep raw bytes unchanged. Check the
complete old private inventory for additional user-created files; assign them an
explicit private destination instead of silently leaving them behind. Preserve
modified generic instructions separately for review rather than replacing the new
public instructions with an old personalized copy.

Moving this complete group up one level preserves most relative links *within*
it: `Projects/<slug>/wiki` still has the same relation to shared `raw/`. References
to toolkit files outside the former `brain/`, absolute old paths, and links with a
literal `brain/` prefix may need adjustment. Verify links from their actual new
locations. Review internal application references and their local instructions;
external app repositories stay in place unless their move was separately requested.

Run `init-brain`, `resolve-brain`, and the registry checks only after the reviewed
copy is in place. Initialization preserves existing files and fills missing scaffold
files; it does not merge registries or repair source history. If the destination
already contains private state, prepare an explicit collision/merge map in another
fresh copy instead of overlaying two brains.

## From older project folders or a personal raw/wiki/outputs vault

1. Inventory the selected notes and source filenames, workspace identities if any,
   current actions, and app repositories. Start with indexes and lightweight context;
   read source contents only as needed. Identify stale notes, duplicates, material
   requiring confidentiality review, and unresolved ownership. Do not assume every
   folder or connected account should be imported.
2. Propose a workspace and old-path → new-path mapping for review. A personal vault's
   shared wiki may become several workspace wikis; mixed notes require deliberate
   scoped interpretation. Put shared goals/preferences in root `context/` and each
   area's facts/goals in `Projects/<slug>/context/`. Keep the generic root instructions
   and public toolkit files free of personal or employer context.
3. After approval, initialize the new root and run `new-project` for each selected
   slug. Start with one representative workspace. Copy selected PROJECT/context/
   STORY/Ingestion/wiki/outputs and useful optional material, preserving richer
   existing facts. Reconcile the new identity fields rather than replacing old
   context with blanks. Register status, planning/review flags, and app references
   deliberately. An old folder named `Projects/` alone is not a valid registry.
4. For each selected original, use the intake capture helper with a stable migration
   source ID, for example `legacy:<scope>:<relative-source-path>`. Record the old path,
   source ID, content digest, and new path in `maintenance/`. Use the ordinary raw
   folders described above; an optional `archive/` topic folder can hold historical
   imports without discarding content. Preserve source bytes and compare checksums. Collapse duplicates only when their identity is established,
   not merely because filenames match. Keep unselected originals in the old backup.
5. Repair citations, Markdown links, Obsidian backlinks, and attachment references in
   the copied interpretations. Record source IDs/revisions and verify each target from
   its new file location. Keep mixed-source claims scoped to the relevant workspace.
   Preserve historical originals; never rewrite raw documents to repair links.
6. Reconcile approved integrations into root `integrations.json` with distinct account
   labels and explicit source-to-workspace mappings. Preserve original scope and
   disabled states. Credentials move only through an approved secure-storage process,
   without printing them. Copying configuration activates no connection or schedule.
7. Preserve useful old per-workspace maintenance under `maintenance/legacy/<slug>/`
   and retain its migration map. Future experiments use `maintenance/evaluations/<slug>/`;
   new run records use `maintenance/runs/`. Preserve each action's canonical status
   and link to it from summaries, rather than creating duplicate task stores.

Repeat approved batches only after the pilot's content and links are checked. Keep
unresolved items explicit; a successful file copy is not proof that a note is current
or that its interpretation belongs in a destination.

## Verify before cutover or retirement

Resolve each workspace, inspect registry scope, and compare the source/destination
inventory. Verify original-source checksums, local links, representative artifacts,
and agreement between current stories and canonical task trackers. Test routing
with fictional or explicitly selected inputs.

If a pilot temporarily disables planning/review or pauses a workspace, record why
and the condition for restoring participation in its existing migration report.
At acceptance, reconcile those temporary holds with the user's approved scope;
leave intentional exclusions intact. Make unresolved holds explicit in the handoff.
An active status alone does not enable review. Use the
[routine scope preflight](SOURCES_AND_ROUTING.md#routines-and-efficient-reading)
before a maintenance cutover. Check a daily plan and a maintenance
run for intended workspace coverage. Report remaining gaps instead of treating a
successful CLI run as full proof.

Review old absolute path references in active configuration, app instructions,
Obsidian links, mirrors, and approved host routines. Verify coding-session access
separately; a folder move does not grant host permissions. Regenerate local skills
from the new canonical toolkit rather than copying `.agents/`, `.claude/`, or old
installation state. Retain custom modifications for deliberate reconciliation.

Back up the verified destination. When authorized, switch consumers and writers to
the new root and check for missed or duplicate work, including changes made since
the initial copy. Keep one active intake destination during the cutover. Retire the
old working copy only after recovery and normal-use checks are satisfactory; its
permanent deletion is a separate explicit action. Neither setup nor these migration
steps delete original files.

Keep the personal backup private. For GitHub, use `build-release` and review its
allowlisted public archive; do not publish a ZIP of the whole working `Brain/`.
