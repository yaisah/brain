# Technical design: [initiative]

Status: Draft | Owner: [supplied owner or unassigned] | Updated: [date]
Canonical location: [one authoritative path or URL]
Product brief / PRD: [link] | UX design: [link if relevant] | Delivery plan: [link if available]
Review: [needed decision, reviewer if known, and actual review date or not reviewed]

Use for a consequential technical proposal. Keep only relevant sections; a small
change can use a technical-design section in its product brief. Link to existing
requirements, contracts, and architecture rather than copying them here. Mark
unknowns explicitly. Document completion does not establish design approval.

## Scope and requirements
[Requirement/acceptance-criterion references, technical boundaries, and exclusions.]

## Proposed approach
[Components, responsibilities, dependency direction, and request/data flow.
Link the current architecture and explain what this proposal changes.]

## Data and interfaces
[Data model, authoritative schemas/contracts, compatibility, and migration needs.
Identify the contract source and generated derivatives when applicable.]

## Constraints and failure handling
[Relevant invariants, permissions/data boundaries, failure modes, and recovery.
Link the existing rules and the tests or checks that enforce them; identify gaps.]

## Alternatives and decisions
[Meaningful alternatives and tradeoffs. Link an ADR for a consequential choice;
keep proposed choices distinct from accepted decisions and identify who decides.]

## Verification
| Requirement / invariant reference | Test or check | Evidence / not run |
|---|---|---|

[Reference actual repository commands and their working directory. Record observed
results separately from proposed checks; do not invent passing tests.]

## Rollout and recovery
[Relevant deployment order, observability, success/failure signals, data migration,
and rollback or forward-recovery approach. Mark destructive/irreversible steps.]

## Open questions and readiness
[Unresolved choices, owner if known, evidence needed, and which block implementation.
Link the accepted review or leave the design as draft.]
