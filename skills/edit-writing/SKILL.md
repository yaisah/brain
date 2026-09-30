---
name: edit-writing
description: "Edit a supplied draft for clear, natural language while preserving its meaning, evidence, uncertainty, and intended audience."
---

# Edit writing without changing the evidence

## Resolve scope

Find the nearest enclosing `.brain` marker from this skill and read that toolkit's `docs/OPERATING_GUIDE.md` before private data. Follow its single-workspace routing with `brain.py resolve`; this workflow does not expand a selected workspace into the whole brain.

`TOOLKIT_ROOT` and `BRAIN` both mean the main `Brain/` folder; `PROJECT` is the resolved workspace under its `Projects/`. Shared resource paths below are toolkit-relative; unqualified knowledge and output paths are workspace-relative. Follow `docs/OPERATING_GUIDE.md` for shared evidence, central integrations, maintenance paths, and application access.

Improve a supplied draft's clarity and voice. Do not turn a writing task into a claim of authorship detection, or promise that a detector will classify it a certain way.

## Understand the brief

Identify the audience, purpose, medium, desired tone, and what must remain exact. Use the user's examples or `context/preferences.md` when available.
Read the draft and any supplied supporting sources. Do not inspect unrelated project material just to find a more interesting angle.
For a new draft, establish the message and source facts first. For an edit, preserve the author's substantive choices unless the user requests a stronger revision.

## Edit the argument and prose

Lead with the main point when that serves the audience. Put context and evidence where the reader needs them rather than repeating a summary in every section.
Replace vague claims, inflated language, repetitive transitions, and unnecessary jargon with concrete language.
Vary sentence structure naturally; do not force every sentence to be short or enforce a universal ban on a punctuation mark.
Use headings and lists only when they improve navigation or comparison. Preserve a deliberately conversational or technical voice when it suits the request.
Remove duplicated ideas before compressing every sentence. Explain relationships between ideas instead of assembling disconnected slogans.

## Preserve integrity

Check that edits retain qualifications, numerical units, dates, scope, and distinctions between evidence and inference.
Do not invent quotations, customer reactions, examples presented as real, credentials, results, or commitments.
Keep direct quotations exact or clearly convert them to attributed paraphrases. A grammatical improvement does not authorize changing the quote.
Flag an unsupported claim and propose sourced or qualified wording rather than silently making it sound more certain.
When a stronger opening changes the argument, show the proposed change for decision instead of presenting it as a purely stylistic edit.

## Deliver at the right depth

For a short passage, return the revised text directly. Save a document only when requested or when the user needs a reusable artifact.
Save files to `outputs/YYYY-MM-DD_edited_<topic>.md`, preserving the original unless the user explicitly requests updating a project-owned draft in place.
Mention substantive changes and unresolved factual questions briefly. Do not clutter a light edit with a report about every word choice.
External publication, sending, and changes to brand or preferences are separate actions requiring the user's request.
