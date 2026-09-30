# Sources, routing, and the workspace registry

The registry chooses eligible workspaces. Integrations identify approved accounts,
source collections, and routing mappings. Original evidence is captured once in
shared raw; each workspace owns its relevant interpretation.

## Registry

registry.json uses schema version 1:

```json
{
  "schema_version": 1,
  "workspaces": [
    {
      "slug": "studio-a",
      "name": "Studio A",
      "type": "business",
      "status": "active",
      "planning": true,
      "review": true,
      "application": null
    }
  ]
}
```

This is a fictional example. The installed template starts with an empty list.
new-project registers new workspaces; their type is business|career|personal|
research|general. Status is active|paused|archived. Planning/review scopes include
only active entries whose corresponding flag is true; all includes every entry.

Use list-projects to inspect registered metadata and validated workspace paths.
An entry with `available: false` carries an error and remains part of reported
coverage; skip its content and continue independent available workspaces. A true
value confirms only the directory and identity file, not a completed content review.
An explicit “across my brain” request, or a recurring activity whose scope was
approved once, authorizes that registry scope without asking about each workspace
on each run. Flags do not themselves create a schedule or authorize external sends.
State that scope when configuring the activity; new active entries participate
according to those saved flags. Single-workspace requests remain limited to that
workspace and its specifically relevant shared evidence.

Application references live in the workspace's registry entry, for example
`{"kind":"internal","path":"app"}` or
`{"kind":"external","path":"/explicit/approved/repository"}`.
See [application work](APPLICATIONS.md). Registry enumeration must not read the app.

## Source and routing configuration

integrations.json starts as:

```json
{"schema_version": 1, "connections": [], "sources": [], "routes": []}
```

The optional mapping below is an agent/connector configuration convention, not a
built-in provider API or routing engine. All values are fictional; it is disabled.

```json
{
  "schema_version": 1,
  "connections": [
    {"id": "demo-notion", "provider": "notion", "account_label": "demo-account"}
  ],
  "sources": [
    {
      "id": "meeting-notes",
      "connection_id": "demo-notion",
      "locator": "explicitly-approved-database-id",
      "enabled": false
    }
  ],
  "routes": [
    {
      "source_id": "meeting-notes",
      "match": {"property": "Workspace", "equals": "Studio A"},
      "projects": ["studio-a"]
    }
  ]
}
```

Here the configured source ID names an allowed collection; an intake source ID
identifies one actual item, such as `notion:demo-account:note-0001`.
Specify exact collections/pages or local paths and allowed destinations once.
A connector must map its trusted metadata to the configured property and report
unsupported rules; matching text inside a transcript is not trusted metadata.
Multiple destinations must be explicit. Conflicting/no matches go to inbox;
do not guess, widen account scope, or create a workspace automatically.

Keep credentials in the host credential manager or process environment. An account
label or source locator is not a secret token. Existing authentication does not
authorize reading every item from that account.

## Capture and completion

For readable storage paths, per-source type/gap metadata, generated workspace
catalogs and explicitly approved relocation, see [source browsing](SOURCE_BROWSING.md).
Legacy receipts remain supported; ordinary capture does not rename existing sources.

The local helper accepts a file the user supplied or an approved connector already
retrieved. It does not fetch Notion or choose a destination semantically:

```sh
python3 scripts/intake.py capture --file examples/first-note.md --source-id "demo:local:first-note" --revision "v1" --project harbor-demo
```

Use repeatable --project arguments for explicitly scoped multiple destinations;
omit them to retain an unresolved item in the inbox. Use a stable source ID that
includes provider/account/item identity, never a credential. Capture preserves an
immutable original under raw and returns its digest/path and intake state. A new
capture defaults to raw/<workspace>/ for one destination, raw/shared/ for multiple,
and raw/unassigned/ for none. Optional --folder (relative to raw/) and --filename
choose a meaningful folder and readable filename; they do not assign workspaces.
Reusing the same source/content reuses the original; a new revision label is added
to its receipt. Changed content gets a separate file, with a distinguishing suffix
only when needed. Retries and routing changes retain existing paths. Follow the
returned path, and use receipts rather than folder names to determine routing.

Write a relevant synthesis in each destination's Ingestion/ with the source ID,
revision/digest, and a relative link that resolves to the shared original. Identify
the relevant section of a mixed source and retain uncertainty. Once the actual
synthesis file exists, record that destination's completion:

```sh
python3 scripts/intake.py mark-complete --source-id "demo:local:first-note" --digest CONTENT_DIGEST --project harbor-demo --synthesis Ingestion/first-note.md
```

CONTENT_DIGEST is the capture result, not a literal value. Marking complete records
an existing artifact; it does not assess the quality or factual accuracy of prose.
Capture success is separate from synthesis success. On partial failure, retain
successful originals and outputs, leave failed destinations pending, and retry
only incomplete work. A provider checkpoint must never skip failed/unprocessed
items. The collector/host, not this local helper, manages provider fetch checkpoints.

Retries rely on the same stable source identity and original content. Changing an
ID can create a distinct capture even when the bytes match. The helper serializes
individual capture and receipt-update transactions per source; if an interrupted process leaves a lock, verify that no run is
active before considering removal. Preserve unexpected or changed originals and
receipts for investigation. A missing/empty recorded synthesis returns to pending
when the helper next checks it; that check still cannot establish semantic quality.

The lock is released before an agent interprets the source or updates a wiki.
A pending destination is not an exclusive worker assignment. For delegated intake
or overlap with maintenance, follow [coordination](COORDINATION.md): allocate each
source revision/destination once, use separate worker drafts, and designate the
shared-file writer. Serialize independent jobs that could edit the same targets;
these transaction locks do not provide that reservation.

## Routines and efficient reading

One approved routine can collect incremental changes and route multiple meetings
in one run. Daily planning can use every planning-enabled workspace; weekly
maintenance can use every review-enabled workspace. Configure each activity's
scope, time zone, cadence, and notification intent once through a supported host.
Keep routine prompts specific about sources, outputs, partial failures, and what
merits notification. None is activated by a config file or setup command.

Before enabling a recurring whole-brain review, inspect its actual selection:

```sh
python3 scripts/brain.py list-projects --scope all
python3 scripts/brain.py list-projects --scope review --require-nonempty
```

The first command shows registry metadata, including exclusions. The second returns
an error when no workspaces are eligible; it changes no flags. Resolve an empty
selection against the user's intended scope before calling the routine ready.
New workspaces default to active with planning/review enabled. Migrated workspaces
may retain deliberate opt-outs or temporary pilot holds; resolve those at handoff,
using existing authorization when available. Setup never resets exclusions.

Record included workspaces, exclusions, unavailable entries, and whether the saved
scope follows all eligible workspaces or a fixed list. Specify report-only or
permitted reversible housekeeping, and coordinate with active migrations/other
writers before edits. A fixed-list routine must intersect the eligible selection
with that list and detect an empty intersection too. Recheck the selection on each
run; empty or unavailable coverage is not a clean bill of health. The review skill
reports scope failures instead of changing registry flags automatically.

Eligibility does not validate note accuracy, refresh external sources, grant app
repository access, or prove a host schedule ran. Verify the first actual report's
coverage before relying on the routine.

Planning reads shared goals/capacity and lightweight workspace goals/STORY/task
indexes first. Maintenance records per-workspace coverage and failures and skips
app code, Git internals, dependencies, builds, and secrets. Source review drills
into only relevant originals; a shared raw directory is not an instruction to
scan every source on every run.

## Backups and exports

Make a private backup of the whole working Brain/ folder, including hidden files:
workspace folders alone omit shared evidence, connections, and run history. When
transferring private data to a fresh toolkit, include Projects/, raw/, inbox/,
maintenance/, context/, outputs/, INDEX.md, registry.json, and integrations.json
together. Back up external app repositories separately.
A single-workspace export must bundle necessary sources and rewrite/verify local
links. Review mixed-workspace sources before including them whole; use an explicitly
identified excerpt/redacted derivative when appropriate, preserving its provenance.
Removing one workspace must not remove originals still used elsewhere.

There is no automatic private-export or migration command. The public build-release
command includes only allowlisted public toolkit files; it excludes all private
root paths and is not a private-data backup.
