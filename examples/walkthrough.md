# Fictional end-to-end scenario

Use an isolated demonstration brain and workspace, never actual private data for evaluation.

1. Create `harbor-demo` with the CLI and set its profile to a fictional coworking operator.
2. Ask `ingest` to capture `examples/first-note.md` for that workspace. The original
   text must be preserved once in shared `raw/`; its intake receipt must name the
   destination. The workspace synthesis must distinguish observation from untested demand,
   and any wiki page must point to the shared source with its ID and revision/digest.
3. Ask `think-discovery` to examine the daily booking-change digest. It should expose
   demand, reliability and feasibility gaps without treating one interview as validation.
4. Ask `write-product-brief` for a testable first experiment. Scope should address
   late cancellations; include an owner placeholder and measurable acceptance criteria.
5. Ask `redteam` to critique that saved draft. Each objection needs impact, evidence
   or a declared assumption, and a practical way to resolve it.
6. Revise the brief using that critique, retaining open uncertainty and a change record.

Expected: shared raw → workspace synthesis → discovery → brief → critique → revision.
Actual filenames are chosen by the agent and reported in its reply. Repeat capture of the
same source revision must reuse its original. Shared capture and workspace synthesis have
separate completion states; a failed synthesis can be retried without another raw copy.
Run optional generators with the three fictional JSON fixtures in examples/artifacts.
The generated model is a demonstration, not a financial forecast for a real business.
