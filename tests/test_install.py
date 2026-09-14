"""Exercise the installer CLI against disposable working directories."""

import hashlib
import json
import os
import re
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "install.py"


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.cwd = Path(self.temp.name)

    def install(self, *args, answer="Algoritmi e complessità\n", home=None):
        env = os.environ.copy()
        if home is not None:
            env["HOME"] = str(home)
        return subprocess.run(
            [sys.executable, str(INSTALLER), *args],
            cwd=self.cwd,
            env=env,
            input=answer,
            text=True,
            encoding="utf-8",
            capture_output=True,
            timeout=10,
        )

    def test_prompts_for_subject_and_installs_inside_that_folder(self):
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Subject", result.stdout)
        vault = self.cwd / "Algoritmi e complessità"
        self.assertEqual(list(self.cwd.iterdir()), [vault])
        self.assertIn("Algoritmi e complessità", (vault / "COURSE.md").read_text())
        for name in ("SOURCES.md", "Roadmap.md", "AGENTS.md"):
            self.assertTrue((vault / name).is_file(), name)
        for name in ("Sources", "topics", "lessons", "assets", "learning-records", ".obsidian"):
            self.assertTrue((vault / name).is_dir(), name)
        self.assertEqual(list((vault / "learning-records").iterdir()), [])
        json.loads((vault / ".obsidian/app.json").read_text())
        for name in ("SKILL.md", "GLOSSARY-FORMAT.md", "LEARNING-RECORD-FORMAT.md", "agents/openai.yaml"):
            self.assertEqual(
                (vault / ".pi/skills/teach" / name).read_bytes(),
                (ROOT / "skills/teach" / name).read_bytes(),
            )
        self.assertEqual(
            (vault / ".pi/extensions/quiz.ts").read_bytes(),
            (ROOT / "extensions/quiz.ts").read_bytes(),
        )
        self.assertFalse((vault / ".pi/extensions/ask-user-question.ts").exists())

    def test_seeds_lesson_folder_index_without_inventing_content(self):
        result = self.install(answer="MDL\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        vault = self.cwd / "MDL"
        index = vault / "lessons/lessons.md"
        self.assertTrue(index.is_file(), "Missing lessons/lessons.md folder note")
        self.assertEqual(list((vault / "lessons").iterdir()), [index])
        self.assertEqual(list((vault / "topics").iterdir()), [])
        self.assertEqual(list((vault / "learning-records").iterdir()), [])
        self.assertNotIn("[[", index.read_text(), "An empty vault has no topics or lessons to link")

    def test_installs_pinned_html_viewer_by_default(self):
        result = self.install(answer="MDL\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        obsidian = self.cwd / "MDL/.obsidian"
        self.assertEqual(
            json.loads((obsidian / "community-plugins.json").read_text()),
            ["style-html-viewer", "folder-notes"],
        )
        plugin = obsidian / "plugins/style-html-viewer"
        # Digests published with upstream release 1.0.5, not derived from our bundle.
        for name, digest in {
            "main.js": "3e2e2c9b5e0ff38c226efd4ec70ba66e3664fa0774115de96c916cdc07a7f4ad",
            "manifest.json": "af789c30a9c88f6ddf75b0d2fb243590422cb33292e6296df7628337920faf5d",
            "styles.css": "f77d192438c2fa40b156b94bb060fa9efc14efd3313363bfbd99ab4ca8045807",
        }.items():
            self.assertEqual(hashlib.sha256((plugin / name).read_bytes()).hexdigest(), digest, name)
        self.assertIn("Permission is hereby granted", (plugin / "LICENSE").read_text())

    def test_installs_pinned_folder_notes_for_clickable_markdown_index(self):
        result = self.install(answer="MDL\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        plugin = self.cwd / "MDL/.obsidian/plugins/folder-notes"
        self.assertTrue(plugin.is_dir(), "Folder Notes must be bundled for offline setup")
        # Published GitHub release 1.8.26 digests, independent of our local bundle.
        for name, digest in {
            "main.js": "83d7b91819abac39626349c1b20aef2503a7cb4339334d52115650aec011a216",
            "manifest.json": "d68704cb787fb687a3d6261a77e93d39c9409ef1dab4e37bfc67a6f96b493536",
            "styles.css": "c736732880c7737a30f713d5496f36612a4f64cce96bab0315397ce14b975f6b",
        }.items():
            self.assertEqual(hashlib.sha256((plugin / name).read_bytes()).hexdigest(), digest, name)
        self.assertIn("GNU AFFERO GENERAL PUBLIC LICENSE", (plugin / "LICENSE").read_text())
        self.assertIn("1.8.26", (plugin / "SOURCE.md").read_text())
        settings = json.loads((plugin / "data.json").read_text())
        # Upstream settings schema: an inside-folder Markdown note, plain click,
        # and no automatic creation, rename, move, or deletion of other notes.
        self.assertEqual(settings["folderNoteName"], "{{folder_name}}")
        self.assertEqual(settings["storageLocation"], "insideFolder")
        self.assertEqual(settings["supportedFileTypes"], ["md"])
        self.assertFalse(settings["openWithCtrl"])
        self.assertFalse(settings["openWithAlt"])
        for name in ("autoCreate", "autoCreateForFiles", "autoCreateForAttachmentFolder",
                     "syncFolderName", "syncMove", "syncDelete"):
            self.assertFalse(settings[name], name)

    def test_subject_settings_keep_only_selected_global_extensions(self):
        home = self.cwd / 'Home "quotes" è'
        result = self.install(answer="MDL\n", home=home)
        self.assertEqual(result.returncode, 0, result.stderr)
        settings = json.loads((self.cwd / "MDL/.pi/settings.json").read_text())
        extensions = str(home / ".pi/agent/extensions")
        self.assertEqual(settings, {"extensions": [
            extensions,
            "!" + extensions + "/**",
            "+" + extensions + "/ask-user-question.ts",
            "+" + extensions + "/web-search/index.ts",
            "+" + extensions + "/web-fetch/index.ts",
        ]})
        self.assertFalse(home.exists(), "Installer must not modify the global agent directory")

    def test_rerun_preserves_notes_settings_extensions_and_history(self):
        first = self.install(answer="MDL\n")
        self.assertEqual(first.returncode, 0, first.stderr)
        vault = self.cwd / "MDL"
        for name, content in {
            "COURSE.md": "My confirmed exam goal\n",
            "lessons/lessons.md": "# Lessons\n\n## [[topics/induction|Induction]]\n- [[lessons/0001-induction.html|0001 — Induction]]\n\nMy annotation.\n",
            "lessons/0001-induction.html": "<h1>My actual lesson</h1>\n",
            "learning-records/0001-induction.md": "Needed two hints; independent use unverified.\n",
            ".pi/extensions/quiz.ts": "// My locally adjusted extension\n",
            ".pi/settings.json": '{"theme": "light"}\n',
            ".obsidian/app.json": '{"vimMode": true}\n',
            ".obsidian/community-plugins.json": '["my-other-plugin"]\n',
            ".obsidian/plugins/style-html-viewer/main.js": "// My locally adjusted viewer\n",
            ".obsidian/plugins/style-html-viewer/data.json": '{"myPreference": true}\n',
            ".obsidian/plugins/folder-notes/main.js": "// My locally adjusted folder notes plugin\n",
            ".obsidian/plugins/folder-notes/data.json": '{"storageLocation": "parentFolder", "myPreference": true}\n',
        }.items():
            (vault / name).write_text(content)
        before = {
            path.relative_to(vault): (path.read_bytes(), path.stat().st_mtime_ns)
            for path in vault.rglob("*") if path.is_file()
        }
        second = self.install(answer="MDL\n")
        self.assertEqual(second.returncode, 0, second.stderr)
        after = {
            path.relative_to(vault): (path.read_bytes(), path.stat().st_mtime_ns)
            for path in vault.rglob("*") if path.is_file()
        }
        self.assertEqual(after, before)

    def test_dry_run_previews_subject_vault_without_writing(self):
        result = self.install("--dry-run")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Algoritmi e complessità", result.stdout)
        self.assertIn(".pi/extensions/quiz.ts", result.stdout)
        self.assertIn("COURSE.md", result.stdout)
        self.assertEqual(list(self.cwd.iterdir()), [])

    def test_subject_must_be_one_visible_folder_name(self):
        sandbox = self.cwd
        self.cwd = sandbox / "work"
        self.cwd.mkdir()
        for name in ("", ".", "..", "../escape", str(sandbox / "escape"), "child/subject", r"child\subject", ".pi"):
            with self.subTest(subject=name):
                result = self.install(answer=name + "\n")
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn("Traceback", result.stderr)
                self.assertEqual(list(sandbox.rglob("*")), [self.cwd])

    def test_symlink_destination_is_rejected_before_any_writes(self):
        vault = self.cwd / "MDL"
        outside = self.cwd / "outside"
        vault.mkdir()
        outside.mkdir()
        (vault / ".pi").symlink_to(outside, target_is_directory=True)
        result = self.install(answer="MDL\n")
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(list(vault.iterdir()), [vault / ".pi"])
        self.assertEqual(list(outside.iterdir()), [])

    def test_file_directory_conflict_is_rejected_before_any_writes(self):
        vault = self.cwd / "MDL"
        (vault / ".pi/extensions/quiz.ts").mkdir(parents=True)
        before = sorted(vault.rglob("*"))
        result = self.install(answer="MDL\n")
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(sorted(vault.rglob("*")), before)

    def test_installed_teach_uses_consolidated_course_files_and_bundled_formats(self):
        result = self.install(answer="MDL\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        skill_dir = self.cwd / "MDL/.pi/skills/teach"
        skill = (skill_dir / "SKILL.md").read_text()
        for reference in ("COURSE.md", "SOURCES.md", "Roadmap.md", "topics/", "lessons/lessons.md", "learning-records/"):
            self.assertIn(reference, skill)
        for path in skill_dir.rglob("*.md"):
            text = path.read_text()
            for retired in ("MISSION.md", "RESOURCES.md", "NOTES.md", "./reference/"):
                self.assertNotIn(retired, text, str(path))
            for link in re.findall(r"\]\((\./[^)#]+)(?:#[^)]*)?\)", text):
                self.assertTrue((path.parent / link).is_file(), f"Broken format link: {link}")


if __name__ == "__main__":
    unittest.main()
