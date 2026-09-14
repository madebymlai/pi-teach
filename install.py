#!/usr/bin/env python3
"""Create a subject vault beneath the caller's current directory."""

import argparse
import json
from pathlib import Path
import shlex
import sys

ROOT = Path(__file__).resolve().parent
VAULT_DIRECTORIES = ("Sources", "topics", "lessons", "assets", "learning-records")


def vault_files(subject):
    """Read the local distribution before making any destination changes."""
    files = {}
    for source, destination in (
        (ROOT / "templates/vault", Path(".")),
        (ROOT / "skills/teach", Path(".pi/skills/teach")),
        (ROOT / "plugins", Path(".obsidian/plugins")),
    ):
        if not source.is_dir():
            raise FileNotFoundError(f"Missing installer resources: {source}")
        for path in sorted(source.rglob("*")):
            if path.is_file():
                content = path.read_bytes()
                if source == ROOT / "templates/vault":
                    content = content.replace(b"{{subject}}", subject.encode("utf-8"))
                files[destination / path.relative_to(source)] = content
    files[Path(".pi/extensions/quiz.ts")] = (ROOT / "extensions/quiz.ts").read_bytes()
    # Resolve global extensions in project scope so these filters take precedence.
    extensions = str(Path.home() / ".pi/agent/extensions")
    settings = {"extensions": [
        extensions,
        "!" + extensions + "/**",
        "+" + extensions + "/ask-user-question.ts",
        "+" + extensions + "/web-search/index.ts",
        "+" + extensions + "/web-fetch/index.ts",
    ]}
    files[Path(".pi/settings.json")] = (json.dumps(settings, indent=2) + "\n").encode("utf-8")
    return files


def destination_directories(files):
    directories = {Path(name) for name in VAULT_DIRECTORIES}
    for relative in files:
        directories.update(relative.parents)
    return sorted(directories, key=lambda path: (len(path.parts), str(path)))


def check_destination(vault, files, directories):
    """Reject redirects and path-type conflicts before creating anything."""
    for relative in [*directories, *files]:
        target = vault / relative
        if target.is_symlink():
            raise ValueError(f"Refusing symlink destination: {target}")
        if target.exists():
            if relative in files and not target.is_file():
                raise ValueError(f"Expected a file destination: {target}")
            if relative not in files and not target.is_dir():
                raise ValueError(f"Expected a directory destination: {target}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing files")
    args = parser.parse_args()
    subject = input("Subject name: ").strip()
    if (not subject or subject.startswith(".") or "/" in subject or "\\" in subject
            or any(ord(char) < 32 or ord(char) == 127 for char in subject)):
        raise ValueError("Use one visible subject folder name, not a path (for example: Linear Algebra).")
    vault = Path.cwd() / subject
    files = vault_files(subject)
    directories = destination_directories(files)
    check_destination(vault, files, directories)
    if args.dry_run:
        print(f"Would set up vault: {vault}")
        for directory in directories:
            print(f"Ensure directory {directory}/")
        for relative in files:
            action = "Keep existing" if (vault / relative).exists() else "Create"
            print(f"{action} {relative}")
        return
    for directory in directories:
        (vault / directory).mkdir(exist_ok=True)
    for relative, content in files.items():
        target = vault / relative
        try:
            with target.open("xb") as output:
                output.write(content)
            print(f"Created {relative}")
        except FileExistsError:
            print(f"Kept existing {relative}")
    print(f"\nVault: {vault}")
    print("Open this folder as a vault in Obsidian; click lessons for its index, or open lessons/lessons.md.")
    print("If plugin settings already existed, enable Folder Notes and Style HTML Viewer manually.")
    print("Keep other HTML viewers disabled; existing plugin settings are preserved.")
    print(f"Start Pi: cd {shlex.quote(str(vault))} && pi")
    print("Trust the project when prompted, then run /skill:teach.")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nInstallation cancelled.", file=sys.stderr)
        sys.exit(1)
    except (OSError, ValueError) as error:
        print(f"Installation failed: {error}", file=sys.stderr)
        sys.exit(1)
