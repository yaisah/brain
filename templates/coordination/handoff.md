# Handoff: [work or worker outcome]

Use for one worker report or the run's final handoff. Save worker reports at
`maintenance/runs/<run-id>/workers/<worker-id>.md` and the run handoff at
`maintenance/runs/<run-id>/handoff.md`. Give each worker a unique report path;
the run coordinator owns the final handoff. This is an evidence snapshot,
not another canonical task-status store. For a read-only request, return it in chat.

Report kind: [worker | run]  
Run ID: [actual local run ID or unknown]  
Worker/session identity: [actual observed ID, known descriptive identity, or unknown; not applicable for a run summary]  
Checked at: [timestamp and time zone, or not checked]  
Canonical task: [resolving record link; for toolkit maintenance without a tracker, identify the authorized request and link its run plan]  
Plan: [resolving run-plan link or none]  
Result: [complete | partial | blocked; applies to this report's work only]

## Assigned scope and inputs

- Outcome and limits: [assignment being reported]
- Inputs actually used: [paths/source IDs and hashes or revisions; mark unknown]
- Writable paths: [exact assigned paths or none]
- Shared destinations: [designated integrator and actual reservation/serialization evidence, or unresolved]

## Evidence and checks

| Output or changed path | Expected result | Observed evidence | Check result |
|---|---|---|---|
| [resolving link or none] | [assignment criterion] | [actual artifact/version, command result, or observation] | [passed | failed | not run, with reason] |

[Distinguish your observations from another worker's claims. Identify input drift,
unintegrated drafts, missing outputs, and incomplete checks. Do not report a skipped
check, absent worker response, or unavailable reviewer as success.]

## Remaining work and handoff

- Gaps or blockers: [specific items or none]
- Next action: [one concrete action, with destination/owner if known]
- Completion behavior: [return results | propose next step | continue within approved scope]
- Resume checks: [files/versions and relevant host task state to verify before continuing]
- Canonical record update: [verified change and its evidence, or none]

[Saved state may be stale. If another writer may own a shared destination, retain
separate drafts and coordinate actual ownership before integrating. No follow-on
work or external action is authorized merely by appearing in this handoff.]
