# Folder Notes 1.8.26

Unmodified release by Lost Paul, bundled as a separate third-party Obsidian plugin under GNU AGPL v3; see `LICENSE`. Pi Teach's configuration is supplied separately as `data.json` by the vault template.

- Release and executable assets: https://github.com/LostPaul/obsidian-folder-notes/releases/tag/1.8.26
- Corresponding source, build scripts, and dependency lockfile: https://github.com/LostPaul/obsidian-folder-notes/tree/1.8.26
- Source archive: https://github.com/LostPaul/obsidian-folder-notes/archive/refs/tags/1.8.26.tar.gz
- Required `src/obsidian-folder-overview` submodule source: https://github.com/LostPaul/obsidian-folder-overview/tree/f047859cc9a7f1c04ad35ecdc440a31a300bc6c2

To obtain the source including its submodule, clone the upstream repository at tag `1.8.26` with `--recurse-submodules`. The tag archive alone omits submodule contents. Build instructions are in upstream `package.json` and `esbuild.config.mjs`. These source locations accompany the executable under AGPL section 6(d); any redistribution must keep corresponding source available and these directions with the bundle.

Release assets were checked against GitHub's published SHA-256 digests:

| File | SHA-256 |
| --- | --- |
| `main.js` | `83d7b91819abac39626349c1b20aef2503a7cb4339334d52115650aec011a216` |
| `manifest.json` | `d68704cb787fb687a3d6261a77e93d39c9409ef1dab4e37bfc67a6f96b493536` |
| `styles.css` | `c736732880c7737a30f713d5496f36612a4f64cce96bab0315397ce14b975f6b` |

The installer copies these resources locally without contacting upstream. Folder Notes executes third-party code with vault access. Configuration and relevant startup/click/create source paths were inspected; this is not a complete security audit or an Obsidian runtime test.
