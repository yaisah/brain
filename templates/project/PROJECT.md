# {{PROJECT_NAME}}

Workspace ID: `{{PROJECT_SLUG}}`  
Type: {{WORKSPACE_TYPE}}  
Purpose: {{WORKSPACE_PURPOSE}}

Browse [knowledge](wiki/INDEX.md), [sources and evidence gaps](SOURCES.md), and
[current work and pending decisions](STORY.md). SOURCES.md is generated from intake
metadata; update the source receipt metadata and regenerate it instead of editing
the catalog by hand.

This private workspace holds one coherent area of work or life. Its type describes
its subject, not its access permissions. Read the main Brain folder's docs/OPERATING_GUIDE.md before using
its content. Keep this workspace's context, interpretations, knowledge, and
outputs here. Shared sources, connections, and run records belong in the main
Brain folder's private raw/, integrations.json, and maintenance/ locations;
shared methods and blank templates live alongside them in the toolkit directories.

Start with [profile](context/profile.md), [goals](context/goals.md), and
[preferences](context/preferences.md). Missing facts remain unknown.

## Organize as needed

Use wiki topics for ongoing areas, context/goals.md for desired outcomes, and
STORY.md for current focus and next actions. Preserve original records in the
main Brain folder's shared raw/ and cite the source ID, revision/digest, and resolving relative
link from source-backed summaries. A topic such as pet care or career
development does not require its own workspace.

Add initiatives/ for finite efforts, Stakeholders/ for useful people profiles,
or Hypotheses/ for tracked tests only when needed. If a task tracker is useful,
choose one canonical tracker and link to it from STORY.md. Keep each fact in one
canonical place and link related pages; avoid copies that can drift apart.

An application can live in app/ or in an explicitly referenced external repository.
Record its location in the brain registry. General brain planning and maintenance
skip application code; a coding request establishes its own working directory and
required filesystem permissions.

For longer delegated assignments, follow the main Brain folder's
`docs/COORDINATION.md`. Use existing task records, or create a work card under
`coordination/tasks/` only when no canonical tracker exists. Link the task from
STORY.md; keep run plans and worker handoffs in shared `maintenance/runs/`.
