# Sources

Upstream references and provenance for the bundled resources.

| Source | Link | Local copy |
| --- | --- | --- |
| Matt Pocock — Teach skill | [SKILL.md](https://github.com/mattpocock/skills/blob/main/skills/productivity/teach/SKILL.md) | [sources/teach/SKILL.md](../sources/teach/SKILL.md) |
| Amos Blomqvist — Learn | [Repository](https://github.com/amosblomqvist/learn) | Local-only reference clone at `sources/learn/`; excluded from this repository. |
| Style HTML Viewer — Robin Tan | [Release 1.0.5](https://github.com/taihoe/style-html-viewer/releases/tag/1.0.5) | `plugins/style-html-viewer/`: unchanged release assets and MIT license. |
| Folder Notes — Lost Paul | [Release 1.8.26](https://github.com/LostPaul/obsidian-folder-notes/releases/tag/1.8.26) | `plugins/folder-notes/`: unchanged release assets, AGPL license, and [corresponding-source directions](../plugins/folder-notes/SOURCE.md). |
| Computer Science — MDL | [Local directory](/home/laimk/git/computer-science/MDL/) | Referenced in place; not cloned or copied. |

## Installable resources

- `skills/teach/`: university adaptation of the preserved `sources/teach/` snapshot. Course and source formats use the consolidated names; the source snapshot remains unchanged.
- `extensions/quiz.ts`: adapted from Learn's Quiz extension at commit `7cfd8942f82ab9476e63572387e1fe9bcea5082c`; tool guidance is shortened and routes open-ended responses to Ask User Question for tutor review. Grading and UI logic are unchanged. The installer copies this file only; the global `ask_user_question` remains in use.
- `plugins/style-html-viewer/`: pinned 1.0.5 release, installed under `.obsidian/plugins/style-html-viewer/` by default. GitHub's published SHA-256 digests for `main.js`, `manifest.json`, and `styles.css` are checked in the installer tests. The MIT license is included. Installation uses these bundled files without network access.
- `plugins/folder-notes/`: pinned 1.8.26 release with GitHub-published SHA-256 digests checked in installer tests. License and corresponding-source/submodule directions are included in the installed plugin directory. The upstream settings schema and relevant startup/click/create source paths were inspected; this is not a complete security audit. Folder-click behavior in Obsidian remains unverified.
- `templates/vault/`: Pi Teach's subject-vault scaffolding, including `lessons/lessons.md`, the default Obsidian plugin selection, and minimal Folder Notes settings. Existing destination files are preserved.
