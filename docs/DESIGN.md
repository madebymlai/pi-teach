# Pi Teach — university study workspace

Status: **initial provisioning implemented**; rendering and live teaching validation remain open. Installer usage: [README.md](../README.md). User-provided references: [SOURCES.md](SOURCES.md).

## Goal

Help a computer-science university student organize daily study and prepare for exams using their actual course material. Connect lecturer PDFs, exercise sheets, and past papers to a roadmap, useful teaching, independent practice, and evidence of learning. Keep planning lightweight so most study time goes toward learning and practice.

## Confirmed requirements and decisions

- University/exam-oriented, informed by the existing MDL workspace.
- **Use Matt Pocock's `teach` skill as the teaching entry point.** It owns onboarding, the timed recall → lesson → practice routine, teaching, and continuity.
- **Keep planned and actual work separately owned.** `Roadmap.md` is the agreed timeline built during onboarding, edited only through explicit replanning. `learning-records/` captures what actually happened, how the student worked, and where to continue.
- Course materials include lesson PDFs and exercises when available.
- **Topics** are stable, source-grounded subject overviews in Obsidian Markdown, connecting prerequisites, sources, and related lessons.
- **Lessons** are sequentially numbered HTML teaching units following Matt Pocock's Teach convention: `lessons/0001-slug.html`. They open inside Obsidian alongside topic notes and course PDFs.
- `install.py` asks for the subject name and provisions one vault at `cwd/<subject>/`, including the adapted Teach skill and Quiz extension under that vault's `.pi/`.
- **Pi runs alongside Obsidian.** Pi handles tutoring and planning; Obsidian displays and stores the study workspace.
- **Provision Matt Pocock-style stateful teaching memory as a core capability.** `COURSE.md` holds the goal, course facts, constraints, and preferences; `SOURCES.md` indexes trusted material; `learning-records/` preserves learning insights. These steer fresh sessions as well as resumed ones. Proposed contract: [MEMORY.md](MEMORY.md).
- `/home/laimk/git/computer-science/MDL/` is a reference in place. Do not clone, copy, or migrate it without approval.
- No plugins have been installed or vetted for runtime compatibility as part of this design exploration.

## Proposed learning model

The central loop:

**Course evidence → agreed exam timeline → timed study sessions → actual learning records → informed continuation.** Explicit replanning revises the timeline when it becomes unworkable.

A lesson is the primary teaching unit: a persistent, self-contained HTML page that teaches one tightly-scoped capability tied to the course goal. It combines source-grounded explanation, practice, and feedback, and links to related lessons and references. Learning records guide lesson selection and adaptation. Exam readiness is assessed through demonstrated performance.

For each outcome, distinguish:

1. **Understanding:** definitions, assumptions, motivation, connections, and limits.
2. **Performance:** solve, prove, implement, explain, or diagnose without excessive help.
3. **Retention:** demonstrate the capability again after a delay.
4. **Transfer:** apply it to a changed problem without being told which method to use.

Example: “read the induction lesson” is an activity. “Construct an unfamiliar induction proof without hints, using the hypothesis explicitly” is an outcome.

### Adaptive teaching

- New material: a short explanation and a motivated worked example.
- Partial understanding: targeted explanation, worked examples, and completion problems. Hints are available on request.
- Familiar material: independent retrieval and problem solving.
- Exam preparation: mixed tasks under the actual exam's constraints, with feedback afterward.

Bound diagnostics by the current task and available time. Reuse recent evidence and check uncertainties that affect the lesson.

Explain why a method works, when it applies, and which assumptions it requires. Combine understanding with retrieval practice to support retention.

### Assessment should resemble the capability

- Multiple-choice: diagnose specific misconceptions.
- Mathematics: preserve the student's derivation, including handwritten images when useful.
- Programming: assess student-written code through tests, correctness reasoning, and complexity analysis.
- Oral exams: definitions with hypotheses, proof reconstruction, and follow-up questions. Assess spoken delivery through spoken work.
- Open-ended questions: collect full written explanations through `ask_user_question` without options, then assess accuracy, completeness, and reasoning against the sources. Generate practice from course material when exercise sheets are absent.

Record the assistance received when interpreting performance. Mark uncertain feedback or transcription for verification.

## Proposed separation of responsibilities

### Course evidence

Original sources, official scope and exam facts, course notation, source-page mappings, and declared gaps. The lecturer's material governs exam scope and conventions. Flag apparent errors or contradictions for clarification.

### Teaching flow

The `teach` skill reads `COURSE.md`, `SOURCES.md`, the fixed timeline, and actual learning records. It compares planned work with the continuation point, then names the recall targets, next lesson, source pages, exercises, and minutes for each phase. Confirmed exam requirements and estimates remain labelled in the course material. The detailed startup and session instructions live in `skills/teach/SKILL.md`.

### Stateful teaching memory

Preserves the mission, trusted resources, established language, preferences, and non-obvious learning insights across sessions. One `learning-records/` directory captures insights, misconceptions, demonstrated understanding, relevant student work, and feedback, together with their implications for future teaching. Evidence can come from exercises, explanations, discussions, and independent recall. For document ownership, loading/updating behavior, provisioning, and continuity tests, use [MEMORY.md](MEMORY.md). Progress views are derived from this evidence.

### Obsidian presentation

Native notes and views expose today's work, sources, learning records, and roadmap. Presentation should remain usable without a custom Obsidian plugin.

Group these responsibilities in a small, tested implementation.

## Vault structure

One subject per vault, created beneath the installer's current working directory. Teaching content is created during actual study; the installer seeds no fictional lessons or learning records.

```text
cwd/<subject>/
├── COURSE.md
├── SOURCES.md
├── Roadmap.md
├── AGENTS.md
├── learning-records/
├── Sources/
├── topics/
├── lessons/
├── assets/
├── .obsidian/app.json
└── .pi/
    ├── settings.json
    ├── skills/teach/
    └── extensions/quiz.ts
```

- Memory documents preserve Teach's stateful behavior through the consolidated ownership defined in [MEMORY.md](MEMORY.md).
- `COURSE.md`: personal exam goal, observable success criteria, syllabus, assessment format/dates, constraints, availability, teaching preferences, course notation, and unresolved questions. Confirm substantive goal changes with the student.
- `SOURCES.md`: annotated index of trusted materials, exact source references, when to use each resource, and declared gaps.
- `Roadmap.md`: the complete dated timeline agreed during onboarding, with topic objectives, planned practice, review, and checkpoints. Changes only during explicit replanning; actual progress and continuation are owned by learning records.
- `Sources/`: original course files and labelled derivatives, indexed in `SOURCES.md`. External references can remain links; local-copy policy is not decided yet.
- `learning-records/`: concise numbered records of actual study, attempts, approach, assistance, feedback, insights, and the stopping point. Distinguish exposure, assisted completion, independent performance, and delayed recall.
- `topics/`: stable subject overviews drawn from course sources, with prerequisite links, exact source references, and an index of related lessons.
- `lessons/`: sequentially numbered HTML teaching units, each developing one capability through explanation, practice, and feedback.
- `assets/`: shared lesson stylesheets, quiz widgets, diagram helpers, and other reusable teaching assets.

A course can add `GLOSSARY.md` when its terminology benefits from a dedicated reference. Exercises can remain in their source sheets or lessons, with student work and feedback in learning records.

The `pi-teach` software repository stays separate from the student's vault. Its existing `sources/` contains design references. Reusable skills, extensions, templates, and setup code belong in the software repository; personal study history belongs in the vault.

### Topics and lessons

A topic page gives the general explanation of a subject area as presented in the sources. For example, `topics/induction.md` explains the induction principle and its scope, cites the lecturer's pages, links prerequisite topics, and indexes the relevant HTML lessons. Its content changes as sources are clarified or expanded.

A lesson develops a tightly-scoped capability through a short teaching sequence adapted to the learner. For example, `lessons/0001-first-induction-proof.html` introduces a motivated example, explains the reasoning, and provides practice with feedback. Several lessons can develop different capabilities within one topic.

Number lessons sequentially within each course using `0001-<dash-case-name>.html`, following the source skill. Preserve numbers when replanning. Topic pages index lesson numbers and titles; sessions resolve the timeline's objective to the appropriate lesson through that index. Creating a new lesson updates its topic index without editing the roadmap.

Each lesson cites authoritative sources, links related lessons and references, and invites follow-up questions in Pi. Use readable typography and a consistent shared stylesheet. Reuse existing assets when authoring new lessons.

### Source fidelity

- Preserve originals. Extraction/OCR is a derivative with a link back to its source.
- Cite exact file, PDF page, exercise number, and where needed the printed-page label or side of a scanned spread.
- Mark verified transcription versus uncertain/unreadable material. Do not fill gaps from guesses.
- Keep official exercises, worked solutions, past papers, and generated variants distinguishable.
- Avoid exposing solutions before an independent attempt.
- Label frequency-based priorities with their evidence and uncertainty. Past papers provide a stronger basis than exercise-sheet counts.
- Keep course materials private by default. Disclose any content sent to the configured model or external OCR service.

## Roadmap and teaching sessions

During onboarding, `teach` establishes the current date, confirmed exam requirements, syllabus, sources, prior learning, and availability. It proposes a complete dated timeline through exam day and saves it after agreement. The creation and replanning procedure lives in `skills/teach/ROADMAP-FORMAT.md`.

Invoke `teach` to continue studying. Each ordinary session reads the timeline and actual learning records, gives the timed briefing, conducts the work, and records what happened. The roadmap remains unchanged, including when a local explanation or recall task needs adjustment. Explicit replanning handles changes to the dated schedule.

Inputs:

- Available study time, including other courses and real commitments.
- Upcoming written/oral/lab assessments and confirmed requirements.
- Relevant learning records: the last lesson actually studied, unfinished work, demonstrated understanding, assistance, unresolved misconceptions, and review needs.
- Essential prerequisites and remaining scope.

Output:

- A small essential session for limited-time days.
- A normal plan that fits the available time, with breaks and slack.
- Optional extras, explicitly outside the essential commitment.
- Exact source pages/tasks and why these were selected.

The ordinary routine has three timed phases: closed-note recall of the previous lesson and older weak points; the next named lesson with explanation and a worked example; and specific independent practice with feedback. Include breaks and closing within the available total. Review and mock-exam days follow their scheduled activity. At a meaningful stopping point, record actual work, assistance, outcomes, and continuation in learning records.

### Recovery and checkpoints

- When delays, substantial prerequisite gaps, or changed constraints make the timeline unworkable, compare remaining work with available time and propose explicit replanning.
- Obtain agreement before changing future rows and checkpoints; record the dated reason in the roadmap. Preserve past scheduled rows and actual learning records.
- Handle a local recall error within the session when possible, recording the result without rewriting the timeline.
- Reserve time for delayed checks and exam-like practice before the final day.
- Ground learning claims in observed or explicitly self-reported evidence.
- Show material at risk and trade-offs honestly. Obtain confirmation for material changes to the exam goal or syllabus coverage.
- Schedule written and oral preparation around their actual dates and format.
- Show observed capabilities and remaining unknowns. Any estimated probability of passing requires defensible calibration.

### Avoid duplicate state

There must be one authoritative location for each course fact and each learning record, including its supporting evidence. Progress summaries are derived from learning records. Keep actual completion marks, last-studied pointers, and daily progress summaries out of the roadmap; its only state is the agreed plan and explicit revisions.

A flashcard scheduler, if adopted, owns card review state. Pi uses that schedule when planning the day and assesses exercise readiness through learning records.

## Rendering: Obsidian topics and HTML lessons

### Native study material

Use Obsidian Markdown for topic overviews, the roadmap, and learning records, with LaTeX/MathJax, Mermaid, callouts, source links, images, PDF embeds, and a small CSS snippet. Example for a PDF stored inside the vault:

```md
![[Sources/lecture-03.pdf#page=7]]
```

Core Bases can expose note properties as filtered course/review views. Templates provide consistent course, topic, and learning-record formats. Check installed Obsidian version before relying on particular features.

### HTML lessons

Each lesson's canonical artifact is its numbered HTML page, linked from Obsidian topic pages and the roadmap. The lesson includes its teaching sequence and can use interactive quizzes, algorithm traces, simulators, or manipulable examples when useful. Shared lesson assets provide consistent styling and rendering of mathematics and diagrams.

HTML lessons open in an Obsidian tab or split pane. The first implementation candidate is the desktop core Web viewer loading locally served lesson pages. Verify it with the installed Obsidian version before adopting it. If it cannot meet the lesson requirements, evaluate an explicitly approved HTML-viewer plugin. In-Obsidian viewing is an acceptance requirement.

Obsidian sanitizes HTML inside Markdown notes, including scripts. Use the dedicated lesson viewer and preserve Markdown sanitization. If a local server is needed, serve only the intended lesson and asset directories on loopback; do not expose the whole vault or a generic filesystem-write endpoint. Provision explicit server startup and shutdown behavior.

Test navigation from topic notes to lesson pages and back to course sources, plus rendering of mathematics, diagrams, and interactive exercises inside Obsidian. Validate the results handoff before using lesson activity as learning evidence. Until then, the student brings their work back to Pi for review.

## Setup script

Implemented in `install.py` using the Python standard library:

- Ask for one subject folder name and create `cwd/<subject>/`; spaces and Unicode are supported.
- Preview the same destination with `--dry-run` without writing files.
- Create course-memory scaffolding, content directories, and minimal Obsidian configuration that shows unsupported file types.
- Copy the adapted `teach` skill with all supporting formats and metadata into `.pi/skills/teach/`, and Quiz into `.pi/extensions/quiz.ts`.
- Generate subject-local `.pi/settings.json` using the installing user's home path. Keep global Ask User Question, Web Search, and Web Fetch; exclude other auto-discovered extensions under `~/.pi/agent/extensions/`, including CBMem. Keep local Quiz enabled. Global configuration and extension files remain unchanged. Existing project settings are preserved; global package-based extensions are outside this directory filter.
- Install an `AGENTS.md` context pointer for the memory-loading behavior in [MEMORY.md](MEMORY.md).
- Create missing files on reruns and preserve existing notes, settings, skills, extensions, and learning records. Report preserved files; automatic upgrades are outside this initial installer.
- Reject invalid subject paths, destination symlinks, and file/directory conflicts before writes.
- Work offline without changing global settings, installing applications or plugins, launching processes, configuring sync, publishing, or migrating external study directories.
- Open the resulting folder as a vault manually in Obsidian; run Pi from that folder and approve project trust when prompted.

Filesystem provisioning has CLI tests; Quiz and Teach resource loading has a Pi smoke test. Interactive Quiz behavior and the continuity acceptance tests still need live validation.

In-Obsidian HTML viewing remains pending. Showing HTML files in the vault does not render them. Select and verify the viewer before adding its configuration, any loopback serving support, and rendering smoke tests. Community plugins require explicit approval and reviewed/pinned provenance; preserve restricted mode unless the student approves a specific plugin.

## First prototype

Prove one real study day before expanding the system:

1. Register a small course slice and its real PDF/exercise sources.
2. Define one assessable outcome and a realistic session.
3. Navigate the relevant PDF page from Obsidian.
4. Invoke `teach` to select or create a lesson from the roadmap and learning records, then work through it with the student.
5. Record help, result, misconception, and next action.
6. Start a fresh Pi session and verify it uses the saved mission, preferences, and learning record to select tomorrow's work without duplicate progress updates.
7. Open a topic overview in Obsidian and follow its link to a numbered HTML lesson in an Obsidian tab or split pane. Verify mathematics, diagrams, interactions, shared assets, and navigation back to course sources.

Keep the prototype focused on this complete study-and-resume loop.

## Open decisions

1. Exam-revision sprint, ongoing semester study, or both?
2. Main assessment formats and realistic weekly availability?
3. Existing Obsidian version, desktop/mobile requirements, and handwriting workflow?
4. Source copy/reference policy and privacy constraints?
5. Topic-note appearance, HTML lesson styling, and the choice of in-Obsidian HTML viewer?
6. Whether a separate review scheduler is needed as the course grows?
7. Whether to adopt Spaced Repetition, an Anki bridge, or neither initially?

Resolve these questions incrementally as they affect the design.
