# Browse shared sources

Sources remain shared at the Brain root. Each workspace's generated `SOURCES.md`
answers which sources and versions are assigned, where their interpretations are,
and what evidence gaps are recorded. `PROJECT.md` links knowledge, sources and
current work. Imported wiki summaries are labeled separately from primary evidence;
even primary records can be historical, incomplete or wrong.

## Ordinary source files

New captures use readable files under a small number of folders:

```text
raw/
  harbor-demo/
    Research notes.md
    supplier-review/
      Installation quote.pdf
  shared/
    Joint planning notes.md
  unassigned/
    Incoming notes.md
```

The default folder comes from the initial approved destinations: one workspace uses
`raw/<workspace>/`, multiple workspaces use `raw/shared/`, and none uses
`raw/unassigned/`. The folder is a browsing aid. Receipt metadata determines routing;
a source can remain in its original folder when destinations are added or clarified.
Meaningful topic folders are optional. Historical imports can use
`raw/<workspace>/archive/`; their contents, provenance and assignments remain intact.

Use `--folder` to choose a relative folder **below raw/**, and `--filename` for a
readable filename, for example:

```sh
python3 scripts/intake.py capture --file examples/first-note.md --source-id "demo:local:first-note" --project harbor-demo --folder harbor-demo/research --filename "Research notes.md"
```

The Python interface also accepts `capture(..., folder="harbor-demo/research",
filename="Research notes.md")`. These options affect a new allocation; retrying an
existing capture preserves its path. Supply only a filename to `--filename`, using
`--folder` for subfolders. The helper rejects unsafe folder paths and normalizes
unsafe/reserved filename characters and excessive length for portable storage.
The exact supplied original filename remains in `original_name`; a display name
does not replace that metadata.

Source IDs, full SHA-256 digests, capture timestamps, revision history and routing
live under `maintenance/intake/`, not in a mandatory directory hierarchy. Storage
allocation records bind readable paths to full identities, including incomplete
captures awaiting retry. Names that collide receive distinguishing suffixes rather
than overwriting another file. Changed content is preserved as a separate immutable
file; a suffix is added only when needed to distinguish its name. Matching content
for the same source reuses the capture and preserves per-workspace completion.

`captured_at` is retrieval time, not an authored date, event date, modification time
or relocation date. A suffix containing a date uses the UTC capture date. Existing
source IDs, `original_name` values and capture times are unchanged by retries or
relocation. Use the helper's returned path rather than reconstructing a filename.

Version-1 storage records, legacy receipts and earlier hash-based or descriptive
source/version directories remain supported. Normal setup and retry leave those
paths unchanged; see explicit relocation below to reorganize them. Recognized
harmless Finder metadata is excluded from source-content recovery; unexpected real
files cause an error rather than being adopted or discarded.

## Describe and generate

Receipts are authoritative for source/version identity, routing and processing.
Their optional `description` holds a supplied title, source type, known gaps and
evidence links. Add only supported metadata; unknown type or gaps remain explicit.
An absent gap record is not evidence that a source is complete or current.

Use a private JSON descriptor, for example:

```json
{
  "title": "Research notes",
  "source_type": "primary_evidence",
  "known_gaps": ["Interview date is not recorded."],
  "evidence_links": [{"label": "Interpretation", "path": "Projects/example/Ingestion/research.md"}]
}
```

`source_type` is `primary_evidence`, `imported_summary`, or `unknown`. Evidence paths
are resolving private Brain-relative paths; describing a source does not grant
new source access or change its destination. Supply the full intended descriptor
when replacing it. From the Brain root with a verified Python 3.11+ interpreter:

```sh
python3 scripts/source_catalog.py describe --source-id "local:example:research-01" --digest FULL_SHA256 --metadata-json maintenance/example-description.json
python3 scripts/source_catalog.py generate --project example
```

Generate after capture, completed interpretation, description changes or approved
relocation. It includes all assigned versions and links the actual stored original,
receipt and available interpretation. It does not scan sources to invent facts.
Generation state protects manually edited or unmanaged catalogs from silent loss;
preserve and reconcile edits if regeneration reports a conflict. Catalog freshness
depends on explicitly regenerating it; no watcher or schedule is installed.

## Explicit relocation of existing captures

Relocation needs authorization beyond ordinary ingestion. Back up the affected
originals, receipts and active citations first. Preserve the old dated verification
reports; record a new old-to-new path manifest rather than rewriting history.

Coordinate all writers. Use the intake relocation planning and allocation APIs to
reserve destinations against full source IDs/checksums under the appropriate locks.
`intake.plan_relocation(root, receipt, title=None, folder=None, filename=None)` is
read-only; `folder` is relative to `raw/`. `intake.register_relocation(root, plan)`
reserves the reviewed path while the caller holds that source's `source_lock`.
Neither function moves files or rewrites receipts. There is no relocation CLI;
ordinary capture with new naming options is not a substitute for this workflow.
Stage byte-identical destination files and storage/receipt/citation updates; compare
current input hashes with the backed-up versions before committing. Preserve source
IDs, original names, capture times, revision history, routing and completion state.
Commit all affected active references as one coordinated operation, with a durable
journal and recovery paths; regenerate affected source catalogs as part of the cutover.
Multiple files cannot be swapped atomically by this toolkit: on interruption,
inspect the journal and complete or restore the pending operation before ingestion.

Keep old originals until destination hashes, updated receipts and active links are
verified; only then remove the superseded raw copies within the approved scope.
Keep all backups. Harmless Finder metadata can remain in legacy directories; leave
unrecognized files in place. Regenerate affected workspace catalogs and verify all
source IDs, digests, histories, destinations and paused/planning/review flags.

This workflow neither regenerates source identity from a path nor changes remote
sources, schedulers or external systems. Full private transfers still include raw,
receipts/allocation metadata and referenced evidence together.
