# Validation

## Review scope follow-up (0.5.0)

Date: 2026-09-28 UTC. **85 targeted automated tests passed:** 80 lifecycle,
registry and release tests, plus five distribution integration tests. The new
extracted-release test checks review-enabled creation defaults, empty-scope failure
with `--require-nonempty`, preserved opt-outs through setup/initialization, paused
workspaces, and unavailable entries. Existing list output remains compatible
without the new flag. Fixtures are fictional and disposable.

This verifies scope selection and packaging, not a real scheduled review or an
agent behavioral trial. Toolkit skill validation passed; the separate skill-creator
validator was unavailable because this Python runtime lacks PyYAML.

## Version 0.5.0 validation record

Date: 2026-09-28 UTC. **166 automated tests passed, none skipped:** 80 lifecycle,
registry and release tests; 21 artifact tests; 43 intake tests; 18 source-catalog
tests; and four distribution integration tests. Executed on macOS with Python
3.12.14, the optional artifact libraries, and Node. All automated fixtures are
fictional and disposable. Other operating systems and native agent-host skill
discovery were not independently exercised for this release.

New intake checks cover ordinary workspace/shared/unassigned source files,
optional topic folders and display filenames, stable retries, separate content
versions, collision suffixes, Unicode/case and file-versus-folder reservations,
interrupted capture, unsafe paths, legacy storage compatibility, and explicit
relocation with previous-path authentication. An independent read-only reviewer
identified a pending directory-reservation issue; it was repaired, covered by
regression tests, and independently re-reviewed before this validation run.

Release integration tests exercise extracted public ZIPs, initialization,
local skill setup, private-file exclusion, shared intake and nested application
references. Earlier results below remain historical evidence; earlier behavioral
agent trials were not repeated for this release.

## Version 0.4.4 validation record

Date: 2026-09-28 UTC. Executed on macOS with Python 3.12.14, the optional spreadsheet
and presentation libraries, and Node for JavaScript checks. Python 3.11+ is the
supported baseline. Other operating systems were not independently validated.
All automated tests used fictional, disposable data. Older agent trials below
remain dated evidence and were not repeated for this patch.

## Executed automated checks

**157 tests passed, none skipped:** 80 lifecycle/registry/release tests, 21 artifact
tests, 34 shared-intake tests, 18 source-catalog tests, and four distribution
integration tests. An independent reviewer checked the root-template rename across
the initializer, recovery messages, release allowlist, test fixtures and public
documentation. The 12 blank starter files are unchanged under `templates/root/`;
no operational references to the former template path remain.

The checks cover:

- Root-level Brain initialization and nested workspace creation, with registry/index updates;
  existing context and edited generated skills are preserved.
- Active/planning/review/all scopes, unavailable workspace coverage, one-workspace
  selection conflicts, malformed metadata, traversal and symlink rejection.
- Concurrent metadata writes require a retry rather than lose a registration.
  Missing registries with existing project material cannot silently become empty.
- Immutable source capture, source identity across accounts, content revisions,
  unresolved routing, independent destination completion, concurrent capture, and
  recovery after interrupted capture or a missing completed synthesis.
- Descriptive paths preserve full identity, original filenames and UTC capture
  dates. Legacy receipts/recovery remain supported; ordinary retries and later
  title changes retain existing paths. Short-ID collisions, unsafe/reserved names,
  Unicode/case collisions, allocation validation and symlink rejection are covered.
- Recognized Finder metadata is ignored during source recovery without treating
  arbitrary dot/underscore files as disposable. Interrupted readable captures keep
  their allocated names and timestamps; relocation plans reserve paths explicitly.
- Generated source catalogs cover assigned versions, source types, interpretations
  and recorded uncertainty with checked local citations. Missing metadata stays
  unknown; unsafe text is escaped. Edited catalogs are protected and deterministic
  regeneration recovers from an interrupted generation-state write.
- Public releases exclude all private root directories and metadata, retained legacy
  content, credentials, runtime files, and unreviewed files while retaining the public
  templates/root scaffold. ZIPs extract into a single Brain/ folder. Git exclusion
  checks independently cover root-level private paths.
- Current `.brain` marker, `brain` installation identity, and Brain-named archives
  are verified through actual release extraction. Missing or unrecognized markers
  and earlier installation identities fail without overwriting their state.
- Legacy layout markers and nested brain folders cannot be silently adopted;
  missing registries do not erase workspace coverage. Private path helpers reject
  toolkit destinations, including a misplaced public file in the private scaffold.
- Setup, optional-skill upgrade, uninstall/reinstall, and no-overwrite behavior.
  Unprefixed names install for both hosts. Upgrading an old-name manifest retains
  optional-skill choices and removes obsolete owned files and empty directories;
  modified copies and unmanaged targets block the upgrade before changes. Custom
  files, Finder metadata and unrelated skills are preserved. Finder metadata is
  ignored during generation and excluded from releases.
- Optional coordination installation using `--with-optional`, with `--with-visuals`
  retained as a compatible alias. Installed Codex/Claude copies resolve the guide,
  templates, and existing review workflow through the discovered Brain root. Private
  work cards and run records remain excluded from public releases.
- Editable spreadsheet/presentation structure, formula/input/source checks, HTML
  escaping, and prototype navigation/export logic, including 101 and 500 items.

Distribution tests build from the actual public allowlist, extract into a path
with spaces, and exercise the CLI against real templates. They create generic
business/personal/career workspaces, capture and route a shared source, complete
its separate syntheses, and verify private sentinels do not enter a new release.
They also describe a fictional source, generate its catalog and check the new
workspace navigation from the shipped templates.
A minimal nested Python application runs and resolves to its containing workspace;
this does not test a fresh native Codex permission session or a network server.

## Instruction and content checks

Fresh release/install tests continue to use `docs/OPERATING_GUIDE.md`. Source-browsing
guidance, intake/sync skill instructions, source catalogs and navigation templates
are included in the explicit public allowlist. Personal source content and live
migration records are excluded; private operational verification stays private.

Canonical verification passes for **39 skills** (30 core, nine optional) and
**42 capability mappings**. Local Markdown links resolve. JSON files parse and the
release allowlist includes every current skill, helper, and template resource.
The optional skill-creator validator was unavailable because its PyYAML dependency
was absent; the toolkit's stdlib validation and direct structural checks ran instead.

Public-file scans found no references to the employer organizations identified for
removal and no imported business/personal context. Author attribution and influences
remain in LICENSE and NOTICE. An allowlist and scans are safeguards, not proof that
arbitrary future prose is suitable for publication.

## Coordination resumption trial

This behavioral trial ran on version 0.4.0; it was not repeated for subsequent patches.
A separate agent followed the coordination skill and guide in a disposable
toolkit copy. Its fictional planning-only assignment supplied an existing task
tracker, two notes, and an interrupted run. The old plan assigned two workers to
the same FAQ file and recorded an outdated input hash; the old handoff claimed
completion against a missing output and inferred worker liveness from a saved
terminal title. A separately managed maintenance job might also write the FAQ.

The agent verified the input drift and missing artifact, treated prior-worker
liveness as unknown, retained the existing tracker, and planned separate worker
reports followed by one integrator. It kept shared integration blocked pending
authorization and actual exclusion of competing writes. It created only the two
authorized plan/handoff files. All 141 pre-existing fixture files were unchanged,
and the new documents' local links resolved. No workers were launched, canonical
records changed, or schedules contacted. This validates one planning/resumption
case, not a live concurrent execution or scheduler integration.

## Prior independent agent workflow trial

The following trial ran on version 0.2.0 before the root-layout change. It was not
repeated as a model evaluation for subsequent releases; the current automated distribution tests
exercise the changed paths and intake behavior.

A separate agent without the preceding design discussion followed AGENTS.md and
the canonical workflows in a disposable toolkit copy. The fictional request gave
two workspaces, three supplied notes with trusted routing metadata, a date/time zone,
90 minutes of capacity including a 15-minute buffer, and permission for ingestion,
a daily plan, and one whole-brain knowledge review.

The agent captured three originals, created two scoped syntheses, marked their
receipts complete, and left the note with unknown ownership in the inbox. It treated
an instruction embedded in a transcript as untrusted source content. It saved a
combined daily plan referencing canonical actions, left blocked work out of the
executable plan, and produced one review with per-workspace coverage. Source and
output links were checked. No source connections, schedules, external messages,
publishing, or real user data were involved. Trial artifacts are temporary and are
not included as personal/example content in the release.

## Limits

- Connector collection, provider-specific routing, and scheduling require a capable
  host. The toolkit contains no Notion client or scheduler; none was exercised live.
- Coordination records document ownership but do not implement a general file
  reservation service. Intake locks protect individual helper transactions, not
  later wiki edits. Live tmux/native-agent dispatch and overlapping-job execution
  were not tested; the host must serialize competing writes.
- Native Codex/Claude skill discovery, desktop onboarding, and application/network
  approval behavior were not independently tested in a newly opened desktop project.
- The 25 memory/brain and 20 delivery scenario specifications are a behavioral test
  catalog, not a claim that all 45 were run as model evaluations.
- JavaScript tests use a synthetic DOM. Native browser layout/download behavior and
  spreadsheet recalculation/rendering were not repeated for this update.
- The financial artifact helper remains a simple recurring-customer model; other
  economic models require appropriate inputs and a different model implementation.
- Private exports and legacy migration use documented manual workflows. The public
  release archive is not a private-brain backup.
- Catalogs require explicit regeneration after metadata/intake changes; no watcher
  or schedule is installed. Their existence does not resolve evidence gaps.
- Relocation is an authorized coordinated procedure with backup and a journal,
  not a multi-file atomic transaction. Interrupted work requires inspection and
  completion or recovery before new intake.

## Reproduce

From the toolkit root, using the same supported interpreter throughout:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/brain.py verify
python3 scripts/brain.py doctor
python3 scripts/brain.py build-release
```

The tests use temporary folders and never install global skills or populate the
user's brain. Optional artifact libraries and Node are needed for their checks;
unavailable dependencies produce explicit skips. Set BRAIN_NODE to an
available Node binary if needed. build-release refuses to replace an existing ZIP;
choose a new filename under dist/ for another build.

See [guided setup](GETTING_STARTED.md), [source routing](SOURCES_AND_ROUTING.md),
and [application work](APPLICATIONS.md) for the supported workflows.
