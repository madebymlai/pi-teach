// Usage: node tests/smoke-pi.mjs /path/to/pi-coding-agent/dist/index.js
// Loads only a disposable vault's resources; no model requests or global config.
import assert from "node:assert/strict";
import { mkdtempSync, mkdirSync, writeFileSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath, pathToFileURL } from "node:url";

if (!process.argv[2]) throw new Error("Pass the installed Pi dist/index.js path.");
const pi = await import(pathToFileURL(resolve(process.argv[2])).href);
const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const temporary = mkdtempSync(join(tmpdir(), "pi-teach-smoke-"));
try {
  const home = join(temporary, "home");
  const agentDir = join(home, ".pi/agent");
  const globalExtensions = join(agentDir, "extensions");
  const keep = ["ask-user-question.ts", "web-search/index.ts", "web-fetch/index.ts"];
  const disable = ["cbmem.ts", "custom-header.ts", "browser/index.ts"];
  for (const name of [...keep, ...disable]) {
    const path = join(globalExtensions, name);
    mkdirSync(dirname(path), { recursive: true });
    writeFileSync(path, "export default function () {}\n");
  }
  const globalSettings = '{"theme":"light"}\n';
  writeFileSync(join(agentDir, "settings.json"), globalSettings);
  const installed = spawnSync("python3", [join(root, "install.py")], {
    cwd: temporary, input: "Smoke test\n", encoding: "utf8",
    env: { ...process.env, HOME: home },
  });
  assert.equal(installed.status, 0, installed.stderr);
  const vault = join(temporary, "Smoke test");
  // New global extensions must also remain excluded after installation.
  disable.push("added-later.ts");
  writeFileSync(join(globalExtensions, "added-later.ts"), "export default function () {}\n");
  const resources = async cwd => new pi.DefaultPackageManager({
    cwd, agentDir,
    settingsManager: pi.SettingsManager.create(cwd, agentDir, { projectTrusted: true }),
  }).resolve();
  const subject = await resources(vault);
  const enabled = subject.extensions.filter(extension => extension.enabled).map(extension => extension.path);
  assert.deepEqual(enabled.sort(), [
    ...keep.map(name => join(globalExtensions, name)), join(vault, ".pi/extensions/quiz.ts"),
  ].sort());
  const outside = await resources(temporary);
  for (const name of [...keep, ...disable]) {
    assert.equal(outside.extensions.find(extension => extension.path === join(globalExtensions, name))?.enabled, true, name);
  }
  assert.equal(readFileSync(join(agentDir, "settings.json"), "utf8"), globalSettings);
  // Load only the selected paths, with empty auto-discovery locations.
  const loaded = await pi.discoverAndLoadExtensions(enabled, join(temporary, "empty-project"), join(temporary, "empty-agent"));
  assert.deepEqual(loaded.errors, []);
  assert.deepEqual(loaded.extensions.flatMap(extension => [...extension.tools.keys()]), ["quiz"]);
  const skills = pi.loadSkillsFromDir({ dir: join(vault, ".pi/skills"), source: "project" });
  assert.deepEqual(skills.diagnostics, []);
  assert.deepEqual(skills.skills.map(skill => skill.name), ["teach"]);
  console.log("Installed Quiz and Teach load; subject-only global-extension filtering verified.");
} finally {
  rmSync(temporary, { recursive: true, force: true });
}
