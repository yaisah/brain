---
name: fact-check
description: "Check a project document’s factual claims against specified code, source records, and version history, separating contradictions from missing evidence."
---

# Fact Check

## Resolve scope

Find the nearest enclosing `.brain` marker from this skill and read that toolkit's `docs/OPERATING_GUIDE.md` before private data. Follow its single-workspace routing with `brain.py resolve`; this workflow does not expand a selected workspace into the whole brain.

`TOOLKIT_ROOT` and `BRAIN` both mean the main `Brain/` folder; `PROJECT` is the resolved workspace under its `Projects/`. Shared resource paths below are toolkit-relative; unqualified knowledge and output paths are workspace-relative. Follow `docs/OPERATING_GUIDE.md` for shared evidence, central integrations, maintenance paths, and application access.

## Audit claims against evidence

Identify the document version and the authoritative source scope. Extract load-bearing claims about behavior, dates, quantities, implementation, and completion. Read the named code or records and relevant history; do not treat an earlier assistant answer, file name, or comment as proof of runtime behavior.

For each claim record supported, contradicted, partially supported, or unverified, with a source location and rationale. Compare the claimed time period to the source revision. An API definition alone does not prove deployment, use, authorization, or successful behavior. A search with no match is an evidence gap, not automatic disproof.

Save a claim table and a short list of material corrections in project outputs using `templates/delivery/visual-review.md`. Offer exact corrected wording only where evidence supports it; preserve uncertainty otherwise. Keep the source document unchanged unless the user explicitly requested editing. Do not access private histories or other project sources outside the selected scope.
