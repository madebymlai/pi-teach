# Sources

Index of reference links. Local copies are stored under `sources/`; individual skills include only their skill directory.

| Source | Link | Local copy |
| --- | --- | --- |
| Matt Pocock — Teach skill | [SKILL.md](https://github.com/mattpocock/skills/blob/main/skills/productivity/teach/SKILL.md) | [sources/teach/SKILL.md](../sources/teach/SKILL.md) |
| Amos Blomqvist — Learn | [Repository](https://github.com/amosblomqvist/learn) | Local-only reference clone at `sources/learn/`; excluded from this repository. |
| Computer Science — MDL | [Local directory](/home/laimk/git/computer-science/MDL/) | Referenced in place; not cloned or copied. |

## Installable resources

- `skills/teach/`: university adaptation of the preserved `sources/teach/` snapshot. Course and source formats use the consolidated names; the source snapshot remains unchanged.
- `extensions/quiz.ts`: adapted from Learn's Quiz extension at commit `7cfd8942f82ab9476e63572387e1fe9bcea5082c`; tool guidance is shortened and routes open-ended responses to Ask User Question for tutor review. Grading and UI logic are unchanged. The installer copies this file only; the global `ask_user_question` remains in use.
- `templates/vault/`: Pi Teach's subject-vault scaffolding, installed alongside those local resources.
