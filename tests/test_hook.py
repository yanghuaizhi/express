"""Protocol tests, not an assessment of writing quality or host integration."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "skills/express/references/core.md"
HOOK = ROOT / "hooks/session_start.py"


class SessionStartHookTests(unittest.TestCase):
    def run_hook(self, hook=HOOK, payload="{}", cwd=None):
        return subprocess.run(
            [sys.executable, str(hook)], input=payload, text=True,
            encoding="utf-8", capture_output=True, cwd=cwd, timeout=5,
        )

    def test_all_sources_return_complete_packaged_context(self):
        for source in ("startup", "resume", "clear", "compact", "fork"):
            with self.subTest(source=source), tempfile.TemporaryDirectory() as cwd:
                payload = json.dumps({
                    "hook_event_name": "SessionStart", "source": source,
                    "session_id": "synthetic-session", "cwd": cwd,
                    "model": "test-model", "permission_mode": "default",
                    "transcript_path": "nonexistent-session-file",
                })
                result = self.run_hook(payload=payload, cwd=cwd)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stderr, "")
                self.assertEqual(json.loads(result.stdout), {
                    "hookSpecificOutput": {
                        "hookEventName": "SessionStart",
                        "additionalContext": CORE.read_text(encoding="utf-8"),
                    }
                })

    def test_session_input_is_not_required_or_echoed(self):
        result = self.run_hook(payload="THIS INPUT IS NOT JSON AND MUST NOT BE ECHOED")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("MUST NOT BE ECHOED", result.stdout)
        self.assertIn("共同表达原则", json.loads(result.stdout)["hookSpecificOutput"]["additionalContext"])

    def test_package_in_path_with_spaces_and_unicode(self):
        with tempfile.TemporaryDirectory(prefix="express 测试 ") as temp:
            package = Path(temp) / "插件 空格"
            (package / "hooks").mkdir(parents=True)
            target = package / "skills/express/references/core.md"
            target.parent.mkdir(parents=True)
            shutil.copy2(HOOK, package / "hooks/session_start.py")
            shutil.copy2(CORE, target)
            result = self.run_hook(hook=package / "hooks/session_start.py", cwd=temp)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["hookSpecificOutput"]["additionalContext"], target.read_text(encoding="utf-8"))

    @unittest.skipUnless(os.name == "posix", "The registered shell command is verified on POSIX hosts")
    def test_registered_command_runs_from_an_unrelated_directory(self):
        definition = json.loads((ROOT / "hooks/hooks.json").read_text(encoding="utf-8"))
        command = definition["hooks"]["SessionStart"][0]["hooks"][0]["command"]
        with tempfile.TemporaryDirectory(prefix="express 入口 测试 ") as temp:
            package = Path(temp) / "插件 空格"
            (package / "hooks").mkdir(parents=True)
            core = package / "skills/express/references/core.md"
            core.parent.mkdir(parents=True)
            shutil.copy2(HOOK, package / "hooks/session_start.py")
            shutil.copy2(CORE, core)
            hook_env = os.environ.copy()
            hook_env["PLUGIN_ROOT"] = str(package)
            result = subprocess.run(
                command, shell=True, env=hook_env, cwd=temp,
                input="{}", text=True, encoding="utf-8", capture_output=True, timeout=5,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stderr, "")
            self.assertEqual(json.loads(result.stdout)["hookSpecificOutput"]["additionalContext"], core.read_text(encoding="utf-8"))

    def test_missing_empty_or_invalid_core_fails_without_context(self):
        for content in (None, b" \n", b"\xff"):
            with self.subTest(content=content), tempfile.TemporaryDirectory() as temp:
                package = Path(temp)
                (package / "hooks").mkdir()
                shutil.copy2(HOOK, package / "hooks/session_start.py")
                if content is not None:
                    core = package / "skills/express/references/core.md"
                    core.parent.mkdir(parents=True)
                    core.write_bytes(content)
                result = self.run_hook(hook=package / "hooks/session_start.py")
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, "")
                self.assertTrue(result.stderr.startswith("Express:"))
                self.assertNotIn(temp, result.stderr)


if __name__ == "__main__":
    unittest.main()
