---
name: analyze-metrics
description: "Analyze supplied product or business data with cohorts, experiment estimates, and reviewable queries for one project."
---

# Analyze Metrics

## Resolve scope

Find the nearest enclosing `.brain` marker from this skill and read that toolkit's `docs/OPERATING_GUIDE.md` before private data. Follow its single-workspace routing with `brain.py resolve`; this workflow does not expand a selected workspace into the whole brain.

`TOOLKIT_ROOT` and `BRAIN` both mean the main `Brain/` folder; `PROJECT` is the resolved workspace under its `Projects/`. Shared resource paths below are toolkit-relative; unqualified knowledge and output paths are workspace-relative. Follow `docs/OPERATING_GUIDE.md` for shared evidence, central integrations, maintenance paths, and application access.

## Analysis contract

Establish the decision, population, observation window, unit of analysis, and available data before choosing a method. Inspect the supplied schema and data-quality limits; do not invent column names or assume a particular analytics vendor. Use only the sources mapped to this workspace in `BRAIN/integrations.json` when the requested read is authorized and a capable tool is available. Otherwise work from a supplied export or produce a query draft without executing it.

- For cohorts, specify entry event, eligibility, time origin, denominator, and censoring. Exclude future information and distinguish incomplete windows from zero outcomes.
- For experiments, check assignment and exposure units, allocation imbalance, exclusions, and metric definition. Report effect size and uncertainty; do not substitute a p-value for business relevance. Note multiple comparisons and sequential peeking when applicable. Correlation or before/after change alone does not establish causation.
- For queries, name the dialect, parameters, joins, grain, timezone, and null handling. Use bounded read-only queries; verify join cardinality before aggregating. Write operations are outside this analysis workflow.

Save a reproducible analysis using `templates/delivery/analysis.md`, with source references, query or calculation, result, quality limits, and a decision implication. Keep sensitive row-level data out of summaries unless necessary. If data is missing, return the missing-data requirement instead of an invented result. Test calculations on a small known subset or independent calculation where feasible; state exactly what ran.
