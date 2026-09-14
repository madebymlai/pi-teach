# Pi Teach

Create a single-subject Obsidian vault with a local Pi teaching skill, Quiz extension, HTML lesson viewer, and topic-grouped lesson folder note.

## Install a subject

Requires Python 3. Run from the directory that should contain the new subject folder:

```sh
python3 /path/to/pi-teach/install.py
```

The installer asks for a subject name. Entering `Linear Algebra` creates `./Linear Algebra/` with:

```text
Linear Algebra/
├── COURSE.md
├── SOURCES.md
├── Roadmap.md
├── AGENTS.md
├── Sources/
├── topics/
├── lessons/
│   └── lessons.md          # Index grouped by linked topic headings
├── assets/
├── learning-records/
├── .obsidian/
│   ├── app.json
│   ├── community-plugins.json
│   └── plugins/
│       ├── style-html-viewer/
│       └── folder-notes/
└── .pi/
    ├── settings.json      # Subject-local global-extension allowlist
    ├── skills/teach/       # Teach plus all supporting formats and metadata
    └── extensions/quiz.ts
```

Open the subject folder using Obsidian's **Open folder as vault** and enable its bundled plugins when prompted. Start your existing Pi installation from that same folder, trust the project when prompted, and invoke `/skill:teach` for onboarding. Open generated `.html` lessons directly in Obsidian; no local server is needed. The global `ask_user_question` is reused; no duplicate is installed.

Preview without creating anything:

```sh
python3 /path/to/pi-teach/install.py --dry-run
```

Reruns create missing files and preserve every existing file, including edited skills, extensions, plugins, notes, and settings. Existing files are reported as kept; this is not an updater. Destination symlinks and file/directory conflicts are rejected before writes. Run one installer at a time against a vault.

The generated `.pi/settings.json` keeps global Ask User Question, Web Search, and Web Fetch, and excludes the other extensions auto-discovered under `~/.pi/agent/extensions/`, including CBMem. Local Quiz remains enabled. The paths use the installing user's home directory and the existing global entrypoints (`ask-user-question.ts`, `web-search/index.ts`, `web-fetch/index.ts`); missing global tools are not installed. Additional extensions later added under that global directory are also excluded in the subject. Global package-based extensions are outside this directory filter.

Existing `.pi/settings.json` files are preserved on reruns, so an existing vault's extension selection is not automatically upgraded. Restart Pi from the subject folder after changing its settings.

The installer works offline, copies local resources including Style HTML Viewer 1.0.5 and Folder Notes 1.8.26, and leaves global Pi and Obsidian configuration alone. It does not install Pi or Obsidian, download resources, copy external courses, or launch a server. Unknown course facts remain marked unconfirmed until onboarding.

If `.obsidian/community-plugins.json` already exists, its plugin selection is preserved. Enable **Style HTML Viewer** and **Folder Notes** manually under Community plugins if needed, with other HTML viewers disabled. Existing Folder Notes settings are also preserved: the index uses the `{{folder_name}}` name template and `insideFolder` storage. Review those settings before changing them in an established vault.

## Lesson navigation

Click the **lessons folder name** to open `lessons/lessons.md`; its disclosure arrow still expands/collapses the folder. Without Folder Notes, open the Markdown file directly. Teach maintains this plain index; no dynamic overview or Dataview is required.

The index groups existing lessons under headings linking to their topic synopsis:

```md
## [[topics/induction|Induction]]
- [[lessons/0001-first-induction-proof.html|0001 — First induction proof]]
```

Topic pages are university-style synopses: scope, definitions, hypotheses, principal results, and conceptual connections with precise sources. They do not list lessons or track progress. The index points to topics, not the reverse. Lesson pages link back to the index and their synopsis. New vaults start with an empty index; lesson availability never implies completion.

Folder Notes is configured for navigation without automatic note creation, rename/move/delete synchronization, or generated overviews. Its AGPL license and corresponding-source directions are shipped with the unmodified plugin; see [provenance](docs/SOURCES.md). Folder-click behavior still needs a live Obsidian smoke test.

## Study routine

Onboarding builds and agrees `Roadmap.md` as the dated timeline through exam day. It changes only through explicit replanning when delays, substantial learning gaps, or changed constraints require it.

Each `/skill:teach` session reads that timeline and the learning records, then gives a timed recall → lesson → practice-and-feedback briefing. Recall targets the previous lesson actually studied and persistent difficulties. The briefing names the next lesson objective, sources, practice, and a budget that includes breaks and closing. Practice can use supplied exercises, generated questions, multiple-choice quizzes, or full written explanations; exercise sheets are optional.

`learning-records/` preserves what actually happened, how the student worked, assistance, results, and where to resume. Ordinary sessions leave the roadmap unchanged. These are skill instructions; live behavioral validation is still pending.

## Current scope

Teach is adapted from [Matt Pocock's skill](https://github.com/mattpocock/skills/tree/main/skills/productivity/teach) to use `COURSE.md`, `SOURCES.md`, the roadmap, topics, and evidence-bearing learning records. Matt's original snapshot remains under `sources/teach/`. The Learn reference clone at `sources/learn/` is local-only and excluded from Git; the imported Quiz file is included.

Quiz comes from [Amos Blomqvist's Learn](https://github.com/amosblomqvist/learn), with shorter tool guidance distinguishing multiple-choice grading from open-ended answers collected through Ask User Question and reviewed by the tutor. Its grading and UI logic are unchanged. It runs in Pi's interactive terminal. Resource loading was smoke-tested with Pi 0.85.1; interactive Quiz behavior and teaching continuity still need manual validation.

HTML viewing uses the bundled [Style HTML Viewer](https://github.com/taihoe/style-html-viewer). Shared CSS/JavaScript, images, native MathML, interactive answer feedback, and HTML/Markdown navigation were smoke-tested in Obsidian 1.13.7 on Linux. KaTeX/MathJax, mobile behavior, and automatic results handoff remain unverified. See [the design](docs/DESIGN.md) and [memory contract](docs/MEMORY.md).

## Tests

From this repository:

```sh
python3 -m unittest discover -s tests -v
```

Optional resource-loading and extension-filtering smoke test against an installed Pi (uses disposable global-extension fixtures; no model calls or real global resources):

```sh
node tests/smoke-pi.mjs "$(npm root -g)/@earendil-works/pi-coding-agent/dist/index.js"
```
