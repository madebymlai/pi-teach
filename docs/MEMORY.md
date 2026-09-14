# Stateful teaching memory

Status: course scaffolding and the adapted Teach loading instructions are provisioned by `install.py`; live teaching-continuity validation is pending. Read this when designing provisioning, course selection, teaching-session startup, learning updates, or session recovery. Broader proposal: [DESIGN.md](DESIGN.md).

## What must survive

Matt Pocock's Teach organizes learning in a persistent, multi-session workspace. Pi Teach preserves that model: the next session should know why the student is learning, what resources to trust, what terminology has been established, what has been demonstrated, which misconceptions remain, and how the student prefers to work.

Course files are the authoritative learning memory. Pi conversation history, compaction summaries, and extension custom entries help resume the immediate interaction.

The installer creates one subject vault per folder: `cwd/<subject>/`. Each vault maintains its own mission, learning records, progress, and local `.pi/` resources.

## The persistent documents

| Document | Meaning and ownership |
| --- | --- |
| `COURSE.md` | Personal exam goal, observable success criteria, syllabus, assessment format/dates, constraints, availability, teaching preferences, course notation, and unresolved questions. Confirm substantive goal changes with the student. Date temporary working context. |
| `SOURCES.md` | Annotated source index: what each source covers, when to use it, exact references, and gaps. Includes lecturer PDFs, exercise sheets, past papers, and appropriate human resources such as office hours. |
| `Roadmap.md` | The agreed timeline from onboarding through exam day: dates, objectives, planned practice, review, and checkpoints. Edited only through explicit replanning. |
| `learning-records/NNNN-slug.md` | What the student actually studied and did, how they approached it, assistance, recall results, insights, and difficulties. Includes supporting work, feedback, and the continuation point. |

These documents consolidate Teach's goal, resource, and preference memory into the university workspace. The remaining artifacts support teaching and navigation:

- Optional `GLOSSARY.md`: compressed terminology established with the learner. Add terms after demonstrated understanding and revise definitions as it deepens. Course-wide notation lives in `COURSE.md`; current recall is checked through review.
- Student work and feedback belong in the relevant learning record, with attachments when needed.
- `topics/`: university-style synopses grounded in course sources, with prerequisites, definitions, hypotheses, principal results, and conceptual connections; no lesson lists or study state.
- `lessons/lessons.md`: the navigation index, grouped under headings linking to topic synopses. Its entries identify existing lessons, not lessons studied.
- `lessons/0001-slug.html`: sequentially numbered HTML teaching units, each developing one capability through explanation, practice, and feedback. Lesson scope and selection are adapted using learning records.

`SOURCES.md` indexes the original materials and labelled derivatives stored in `Sources/`.

## Learning record semantics

Keep the original sequential `0001-slug.md` format and short, decision-relevant prose. Record actual work at meaningful milestones and stopping points, including the lesson or exercise, how it went, and where to continue. This includes exposure or unfinished attempts with understanding explicitly unverified, as well as insights that change future teaching. A daily archive is unnecessary.

For a demonstrated capability or misconception, identify the dated evidence and assistance received in the record, including relevant work inline or as a linked attachment. This makes the original optional Evidence field necessary when interpreting performance. Label self-reported prior knowledge explicitly so the next tutor can interpret the evidence.

Example:

```md
# Induction: can state the hypothesis, needs help using it

On 2026-09-12, the student completed exercise 1 on sheet 2 with two hints.
They selected the base case independently, but initially substituted the
inductive conclusion for the hypothesis.

Evidence: when asked to state the hypothesis, they wrote the conclusion
for n+1 instead of the assumed statement for n. They corrected it after
a hint; applying it inside the next inequality required another hint.

Next teaching implication: use a changed inequality and ask the student
to show exactly where the hypothesis enters. Independent use is unverified.
```

If a later record changes an earlier interpretation, retain the history and mark the earlier record superseded, linking its replacement. Interpret each result in its context. Record same-session corrections and check retention later.

## Loading memory

Before teaching after startup, a new session, compaction, or a course switch:

1. Resolve the course from the selected task/workspace. Ask when ambiguous.
2. Load `COURSE.md`, `SOURCES.md`, the current roadmap, and a map of the course's available learning records.
3. Read the latest actual study record and records for the planned outcome, prerequisites, unresolved misconceptions, and any superseding evidence. Load `lessons/lessons.md`, the relevant topic synopsis, source references, and glossary entries if a glossary exists.
4. Compare the dated timeline with the actual continuation point. Present a timed recall → lesson → practice-and-feedback briefing; recall includes the previous lesson actually studied and persistent errors. Resolve uncertain activity by asking the student rather than inferring it from existing lesson files.

Start with direct files. Small courses can load all learning records. If growth later requires an index, use a rebuildable navigation aid with coverage and freshness checks. Read the relevant source records and check retrieval coverage before concluding that history is absent.

The setup provisions the university-adapted `teach` skill and an explicit Pi context pointer/loading path. The skill owns these reads when teaching starts or resumes, including after compaction and course switches. It uses the roadmap to scope the session and learning records to preserve continuity.

## Updating memory

- Persist actual work and evidence at meaningful milestones and stopping points so the continuation point survives interruptions.
- Create `Roadmap.md` during onboarding and edit it only through explicit, agreed replanning. Ordinary completion, recall outcomes, and local session adjustments belong in learning records; leave timeline rows unchanged.
- Within a learning record, distinguish the student's original work from corrections and feedback. Feedback must not replace their answer with the tutor's solution.
- Update `COURSE.md` when goals, constraints, preferences, or course facts change; update `SOURCES.md` when source coverage or reliability changes.
- Keep updates visible and allow corrections. Confirm changes to the student's goals and consequential planning trade-offs.
- Re-read before writing and detect conflicting edits. Pi and Obsidian share files; neither should silently overwrite the other's changes.
- Use one writer for shared learning state. Research and visualization helpers return findings to that writer.

Derive session briefings and progress summaries from the timeline and learning evidence, retaining dates, assistance, and verification status. Keep those summaries in chat rather than adding progress state to the roadmap.

## Provisioning

Vault setup provisions the adapted `teach` skill, reusable templates, and Pi memory-loading instructions using the consolidated file names. Adding a course creates `COURSE.md`, `SOURCES.md`, and an unplanned `Roadmap.md` scaffold. During onboarding, populate the course context from student answers and verified sources, then agree the full exam timeline using `skills/teach/ROADMAP-FORMAT.md` (installed under `.pi/skills/teach/`). Create optional reference documents as the course needs them.

`learning-records/` can be created lazily when the first genuine record is written, as in the source skill. Empty templates must not contain fictional prior knowledge, capabilities, or learning records. Re-running setup preserves existing state.

Support both resuming a Pi session and starting an entirely fresh session against the same course. Persistent memory remains readable and editable in Obsidian without a database or chat-log plugin.

## Continuity acceptance tests

These are live behavioral checks; installer and resource-loading tests do not establish that an agent follows the routine.

- **Initial timeline:** with confirmed dates, syllabus, sources, and availability, onboarding proposes a complete dated route through exam day, including recall, lesson objectives, exact practice where sources permit, independent checkpoints, review, and buffer time. It obtains agreement before saving the initial plan; an unknown or past exam date triggers clarification.
- **Timed routine:** given 90 minutes and a previous lesson with a persistent misconception, the briefing names that recall target, the next lesson objective and source pages, and specific practice. All phases, breaks, correction, and closing fit within the available time. Results are assessed after the student's attempt.
- **No exercise sheets:** given a conceptual chapter, the tutor creates source-grounded practice and collects a full explanation through `ask_user_question` without options. It waits for the answer, assesses accuracy, completeness, and reasoning, and records the student's response, assistance, and remaining gaps. Multiple-choice checks use Quiz; the timeline stays unchanged.
- **Stable roadmap:** save the roadmap bytes before an ordinary session. Complete a lesson, attempt exercises, correct a misconception, and create a follow-up lesson if needed. Learning records reflect the actual work and the folder index lists the new lesson under its linked topic heading; the roadmap bytes remain unchanged.
- **Partial work:** stop after reading a lesson and starting an exercise. The record identifies both activities and the stopping point, with understanding unverified. A fresh session resumes from that evidence instead of assuming the day's planned work was completed.
- **Explicit replanning:** simulate missed sessions or changed availability that make the remaining schedule unworkable. The tutor presents the mismatch and trade-offs, leaves the roadmap unchanged until approval, then revises affected future rows and checkpoints consistently with a dated reason. Existing learning records remain intact.
- **Fresh session:** start from `COURSE.md`, `SOURCES.md`, the roadmap, and learning records after an assisted induction exercise; the tutor identifies the troublesome step, proposes a follow-up, and marks independent performance as unverified.
- **Compaction:** relevant misconception and latest plan remain recoverable from files after conversation compaction.
- **Course switch:** selecting another course uses its mission and records; returning restores the original course context.
- **Correction:** a later successful independent exercise supersedes the earlier interpretation while preserving the evidence history.
- **Preferences:** the next session applies the recorded teaching preferences.
- **Lesson navigation:** creating a lesson adds its numbered link under a heading linked to the topic synopsis in `lessons/lessons.md`. The synopsis remains an academic reference without lesson links. Renaming a lesson repairs the index link while preserving annotations; neither operation invents study completion. Check these behaviors live, not through installer tests alone.
- **Safe provisioning:** a second setup run leaves real memory, lesson index annotations, and plugin settings unchanged and creates no invented progress.
- **Interruption:** recorded milestones survive even when there is no end-of-day command.

An optional transcript mirror provides a readable session history alongside the course memory.
