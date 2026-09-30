---
name: prep
description: "Prepare a stakeholder meeting brief from one project’s known context, with an engagement plan when the interaction warrants it."
---

# Prepare for a stakeholder conversation

## Resolve scope

Find the nearest enclosing `.brain` marker from this skill and read that toolkit's `docs/OPERATING_GUIDE.md` before private data. Follow its single-workspace routing with `brain.py resolve`; this workflow does not expand a selected workspace into the whole brain.

`TOOLKIT_ROOT` and `BRAIN` both mean the main `Brain/` folder; `PROJECT` is the resolved workspace under its `Projects/`. Shared resource paths below are toolkit-relative; unqualified knowledge and output paths are workspace-relative. Follow `docs/OPERATING_GUIDE.md` for shared evidence, central integrations, maintenance paths, and application access.

Help the user enter a meeting with the other person's priorities and the unresolved work clearly in view. Use `stakeholder-questionnaire` instead when the requested deliverable is a questionnaire for missing facts or decisions.

## Establish the meeting

Identify the person, purpose, date if relevant, and desired outcome. Retrieve those details from the request and selected project before asking. Do not assume two people with similar names are the same person.
Read `Stakeholders/<person>.md`, any private companion note explicitly maintained by the project, relevant decision and hypothesis entries, and recent interaction records.
If there is no stakeholder record, say so. Build from supplied evidence or ask for the missing role and meeting purpose; never invent a personality, influence level, or relationship history.

## Assemble the brief

Use `templates/workflows/stakeholder-brief.md` for a saved output, or return a compact brief in chat when that is all the user needs.
Include:

- Their role and documented priorities, with sources and dates.
- Open requests in both directions, with owner, status, and due date when known.
- The most recent unresolved concern and what has changed since it was raised.
- Relevant decisions or evidence that could affect the conversation.
- A short agenda and questions that advance this meeting's purpose.
- A cadence note using the project's preferences; an old timestamp is a prompt to check context, not proof of neglect.

Distinguish what they said from the user's interpretation of it. Do not present private hypotheses about motivation as established facts.

## Add an engagement plan when needed

For a first interaction, conflict, consequential decision, likely blocker, or a user-requested relationship plan, add:

1. What each side needs from the conversation and which outcomes are negotiable.
2. A framing grounded in the person's stated responsibilities and concerns.
3. A suitable channel and cadence, considering urgency and the recipient's documented preferences.
4. Whose perspective is missing and whether the named stakeholder can reasonably represent that group.
5. One concrete next action with an owner, intended outcome, and date if justified.

Avoid political storytelling unsupported by evidence. Use uncertainty explicitly when influence or priorities are unknown.

## Deliver and follow through

Save requested briefs to `outputs/YYYY-MM-DD_meeting-prep_<person>.md`. Do not send invitations or messages.
After a meeting, record new touchpoints only when the user requests it or supplies the notes for capture. Keep a prepared agenda distinct from what actually happened; route durable meeting evidence through `ingest`.
