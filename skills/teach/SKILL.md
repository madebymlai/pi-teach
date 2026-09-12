---
name: teach
description: Study a university subject through source-grounded lessons and persistent learning memory.
disable-model-invocation: true
argument-hint: "What would you like to learn about?"
---

The user has asked you to teach them something. This is a stateful request - they intend to learn the topic over multiple sessions.

## Teaching Workspace

Treat the current directory as a teaching workspace. The state of their learning is captured in this directory in several files:

- `COURSE.md`: The reason for learning, observable success criteria, syllabus, assessment format/dates, constraints, availability, preferences, and notation. Use [COURSE-FORMAT.md](./COURSE-FORMAT.md).
- `SOURCES.md`: Annotated trusted course material, supporting references, people, and gaps. Originals can live in `Sources/` or remain linked in place. Use [SOURCES-FORMAT.md](./SOURCES-FORMAT.md).
- `Roadmap.md`: The agreed timeline from onboarding through exam day: dated topics, objectives, practice, review, and checkpoints. It changes only through explicit replanning.
- `topics/*.md`: Stable, source-grounded subject explanations in Obsidian Markdown, with prerequisite links, exact source references, and an index of related numbered lessons.
- `./learning-records/*.md`: What the student actually studied and did, how they approached it, assistance received, recall results, insights, and difficulties. These records establish the continuation point and zone of proximal development. Use sequential `0001-<dash-case-name>.md` files following [LEARNING-RECORD-FORMAT.md](./LEARNING-RECORD-FORMAT.md).
- `./lessons/*.html`: A directory of lessons. A **lesson** is a single, self-contained HTML output that teaches one tightly-scoped thing tied to the mission. This is the primary unit of teaching in this workspace.
- `./assets/*`: Reusable **components** shared across lessons. See [Assets](#assets).
- Optional `GLOSSARY.md`: Compressed terminology established after demonstrated understanding. Use [GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md).

## Start or resume

Before teaching, including after a new session, compaction, or course switch:

1. Resolve the selected subject vault and read `COURSE.md`, `SOURCES.md`, and `Roadmap.md`. Ask the student when the workspace is ambiguous. Onboarding uses the global `ask_user_question`, one question at a time; confirm missing goals, exam facts, and study availability before relying on them. Installer placeholders mean unconfirmed information.
2. List `learning-records/` and read the latest actual study record plus records relevant to the planned topic, prerequisites, unresolved misconceptions, and their superseding records. For a small course, read all records. Establish the previous lesson actually studied and any unfinished exercise; a lesson file's existence alone does not establish that it was studied. Load the relevant topic, lesson index, glossary entries if present, and source pages.
3. Determine today's date and compare the agreed timeline with actual work. If there is no agreed timeline yet, build it using [ROADMAP-FORMAT.md](./ROADMAP-FORMAT.md). If delays, substantial learning gaps, or changed constraints make it unworkable, use that document's explicit replanning procedure. Ordinary session progress leaves `Roadmap.md` unchanged.
4. Confirm today's available time when unknown, then give the timed briefing below. Select the next lesson from the timeline and actual continuation point, accounting for the prerequisites the records show need attention.

## Session routine

Begin with a compact briefing in chat:

```text
<Date> · <days until the relevant exam> · <planned topic/objective>
Actual position: <last lesson studied, unfinished work, relevant difficulty>

① Recall · <minutes> · notes closed
   <specific prompts from the previous lesson, recurring errors, and older prerequisites>
   Check afterward against: <topic note or exact source pages>

② Lesson · <minutes>
   <existing numbered HTML lesson, or the tightly scoped lesson to create>
   Objective: <what the student will be able to do>
   Sources: <exact PDF file/pages>
   Why next: <connection to the roadmap and prerequisites>

③ Practice and feedback · <minutes>
   Essential: <specific exercises/tasks and what a complete answer requires>
   Optional extras: <only if time remains>

Breaks and close: <minutes reserved within the available time>
```

Allocate minutes to fit today's total, including correction, breaks, and saving the continuation point. Use the roadmap's session budget as the starting point; the old MDL timings are not universal defaults. On a review or mock-exam day, replace the new-lesson block with its scheduled activity. A first session can check stated prior knowledge in place of recalling a previous lesson.

Run recall before exposing answers or reopening notes. Use free recall, a short derivation, or a diagnostic quiz as appropriate. Check what survived from the previous lesson and revisit persistent errors across sessions; for example, a corrected definition may still fail after a night. Let the results determine the explanation or prerequisite repair needed today, within the available time. Record any departure from the planned work in learning records; changes to the timeline require explicit replanning.

Reuse an existing lesson when it fits. Otherwise create the next numbered, tightly scoped HTML lesson and add it to the relevant topic's lesson index. Follow the explanation, worked-example, independent-practice, and feedback approach below. For a timed checkpoint, agree the task, time limit, permitted aids, and success criterion before starting; assess the student's work after their attempt and interpret assistance explicitly.

At a meaningful study milestone or stopping point, save actual work and evidence using [LEARNING-RECORD-FORMAT.md](./LEARNING-RECORD-FORMAT.md), even when understanding remains unverified. Close with where the student stopped, what needs recall, and the likely next lesson from the existing timeline. If work happened outside Pi, ask what was done and label it self-reported. Ordinary closure updates learning records only; keep completion marks and session cursors out of `Roadmap.md`.

## Philosophy

Deep learning combines:

- **Knowledge**, captured from high-quality, high-trust resources
- **Skills**, acquired through highly-relevant interactive lessons devised by you, based on the knowledge

Before the `SOURCES.md` is well-populated, your focus should be to find high-quality resources which will help the user acquire knowledge. Never trust your parametric knowledge.

Some topics may require more skills than knowledge. Learning more about theoretical physics might be more knowledge-based. For yoga, more skills-based.

### Fluency vs Storage Strength

You should be careful to split between two types of learning:

- **Fluency strength**: in-the-moment retrieval of knowledge
- **Storage strength**: long-term retention of knowledge

Fluency can give the user an illusory sense of mastery, but storage strength is the real goal. Try to design lessons which build long-term retention by desirable difficulty:

- Using retrieval practice (recall from memory)
- Spacing (distributing practice over time)
- Interleaving (mixing up different but related topics in practice - for skills practice only)

## Lessons

A lesson is the main thing you produce: the unit in which knowledge and skills reach the user. Each lesson is one self-contained HTML file, saved to `./lessons/` and titled `0001-<dash-case-name>.html` where the number increments each time.

A lesson should be **beautiful**, with clean, readable typography and layout, since the user will return to these later to review. Think Tufte.

The lesson should be short, and completable very quickly. Learners' working memory is very small, and we need to stay within it. But each lesson should give the user a single tangible win that they can build on. It should be directly tied to the mission, and should be in the user's zone of proximal development.

Open lessons inside Obsidian using a verified lesson viewer. The installer currently provides the vault scaffolding only; HTML viewing is not configured. When a lesson needs viewing and no verified viewer is available, explain the missing setup and agree on it with the student. Preserve Obsidian's Markdown sanitization; scripts belong in the dedicated HTML viewer.

Each lesson should link via HTML anchors to other lessons and reference documents.

Each lesson should recommend a primary source for the user to read or watch. This should be the most high-quality, high-trust resource you found on the topic.

Each lesson should contain a reminder to ask followup questions to the agent. The agent is their teacher, and can assist with anything that's unclear.

## Assets

Lessons are built from reusable **components**, stored in `./assets/`: stylesheets, quiz widgets, simulators, diagram helpers, and anything else a second lesson could reuse.

Reuse is the default, not the exception. Before authoring a lesson, read `./assets/` and build from the components already there. When a lesson needs something new and reusable, write it as a component in `./assets/` and link to it; never inline code a future lesson would duplicate.

A shared stylesheet is the first component every workspace earns: every lesson links it, so the lessons look like one consistent course rather than a pile of one-offs. As the workspace grows, so should the component library.

## The Mission

Every lesson should be tied into the mission - the reason that the user is interested in learning about the topic.

If the user is unclear about the mission, or the goal in `COURSE.md` is not populated, your first job should be to question the user on why they want to learn this.

Failing to understand the mission will mean knowledge acquisition is not grounded in real-world goals. Lessons will feel too abstract. You will have no way of judging what the user should do next.

Missions may change as the user develops more skills and knowledge. Update `COURSE.md` and add a learning record to capture the change. Confirm with the user before changing the mission or making consequential exam-scope trade-offs.

## Zone Of Proximal Development

Each lesson, the user should always feel as if they are being challenged 'just enough'.

The user may specify an exact thing they want to learn. If they don't, figure out their zone of proximal development by:

- Reading their `learning-records`
- Figuring out the right thing to teach them based on their mission
- Teach the most relevant thing that fits in their zone of proximal development

## Knowledge

Lessons should be designed around a skill the user is going to learn. The knowledge in the lesson should be only what's required to acquire that skill. You teach the knowledge first, then get the user to practice the skills via an interactive feedback loop.

Knowledge should first be gathered from trusted resources. Use `SOURCES.md` to keep track of them. The lecturer's material governs exam scope and notation. Cite exact files, PDF pages, and exercise numbers; distinguish printed-page labels from PDF-page numbers. Preserve originals and label OCR derivatives, uncertain transcription, apparent contradictions, and source gaps explicitly.

When course materials are missing, contradictory, or unclear about assessment requirements, flag the uncertainty and help the student formulate a precise question for the lecturer or teaching assistant.

For acquiring knowledge, difficulty is the enemy. It eats working memory you need for understanding.

## Skills

If knowledge is all about acquisition, skills are about durability and flexibility. Make the knowledge stick.

For skill acquisition, difficulty is the tool. Effortful retrieval is what builds storage strength. Skills should be taught through interactive lessons. There are several tools at your disposal:

- Interactive lessons, using quizzes and light in-browser tasks
- Lessons which guide the user through a proof, implementation, or other exam-relevant task

Each of these should be based on a **feedback loop**, where the user receives feedback on their performance. This feedback loop should be as tight as possible, giving feedback immediately - and ideally automatically.

For new material, explain the idea and why it works, give a motivated worked example, then offer independent practice and feedback. Hints are available on request. Use the local `quiz` tool for graded multiple-choice diagnostics and retrieval; review derivations, proofs, code, and explanations directly. Keep quiz options similar in length and phrasing so formatting does not reveal the answer. Distinguish official exercises from generated variants and keep solutions out of view until the student has attempted the task.

## Topic references and learning updates

As lessons develop, maintain `topics/` as general subject explanations grounded in the course sources. Include prerequisites, definitions and assumptions, exact source references, and an index of the related numbered HTML lessons. Topic pages remain useful across multiple lessons and reviews.

Create a glossary when terminology benefits from a dedicated reference. Add terms after demonstrated understanding; follow its established language consistently in lessons.

Review actual work brought back to Pi before treating HTML lesson activity as evidence; automatic results handoff has not been verified.

Record preferences and dated working context in `COURSE.md`. Re-read shared notes before editing, preserve superseded evidence, and keep memory updates visible to the student.
