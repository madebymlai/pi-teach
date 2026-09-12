# Learning record format

Learning records live in `./learning-records/` and use sequential numbering: `0001-slug.md`, `0002-slug.md`, etc. Create the directory if needed when writing the first record.

They preserve what the student actually studied and did, how they worked, and what that means for future teaching. They carry the continuation point and learning evidence across sessions; `Roadmap.md` carries the agreed timeline.

## Write at a meaningful milestone or stopping point

Record the lesson or source studied, recall attempted, or exercise worked on when it changes where the next session should begin. Include partial work and interruptions. Record demonstrated understanding, disclosed prior knowledge, misconceptions, and goal shifts when they occur. This can be one concise paragraph; a daily archive or transcript is unnecessary.

Exposure is a valid activity to record, with understanding explicitly unverified. A completed exercise with hints establishes an assisted result. Claims of independent performance or retention require corresponding evidence.

## Template

```md
# {Short title of the work or insight}

{Date. What was actually studied or attempted, with lesson, source-page, or exercise links.}
{How the student approached it, assistance received, and the observed result or uncertainty.}
{Where they stopped, unfinished work, and the specific recall or follow-up the evidence calls for.}
```

Use only fields that apply. Include actual time spent when known, and distinguish it from the planned budget. Label work done outside Pi and prior knowledge as self-reported until verified. Ask about missing activity rather than inferring it from file timestamps, lesson numbering, or the planned date.

## Evidence

For claims about performance or understanding, include the dated answer, derivation, code, explanation, or recall supporting the claim, plus assistance and verification status. Preserve the student's original work separately from corrections and feedback, inline or as linked attachments.

Track persistent errors across recalls, including whether the student answered before seeing notes or hints. A same-session correction and a successful delayed recall are different observations. Record both when they occur.

Optional sections such as **Evidence**, **Implications**, or **Status** are useful when a paragraph would obscure those distinctions. Keep terminology definitions in `GLOSSARY.md`; link them when relevant to the learning evidence.

## Numbering and updates

Scan `./learning-records/` for the highest existing number and increment by one for a new record. Re-read a record before adding a same-session continuation so earlier student work is preserved. Save at milestones rather than relying on an end-of-day command.

When later evidence changes an earlier interpretation, retain the old evidence and mark its interpretation superseded with a link to the replacement. Read follow-up and superseding records before treating an older difficulty as current.

An agreed goal shift belongs in `COURSE.md` and can be linked from the relevant learning record. A change to the dated study schedule goes through the explicit replanning procedure in [ROADMAP-FORMAT.md](./ROADMAP-FORMAT.md).
