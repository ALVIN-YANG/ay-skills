from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import tempfile
import tomllib
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]


def load_runner(name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


RUNNERS = [load_runner("run_behavior_evals"), load_runner("run_routing_evals")]


class CodexSkillIsolationTests(unittest.TestCase):
    def test_global_paths_are_disabled_without_disabling_workspace_copies(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            home = root / "home"
            configured = root / "custom codex"
            global_skill = home / ".agents/skills/retired/SKILL.md"
            legacy_skill = configured / "skills/legacy/SKILL.md"
            nested_skill = home / ".agents/skills/parent/modes/child/SKILL.md"
            workspace_skill = root / "workspace/.agents/skills/retired/SKILL.md"
            for path in (global_skill, legacy_skill, nested_skill, workspace_skill):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("original content\n")
            (configured / "skills/alias").symlink_to(global_skill.parent, target_is_directory=True)

            for runner in RUNNERS:
                with self.subTest(runner=runner.__name__), patch.object(runner.Path, "home", return_value=home), patch.dict(runner.os.environ, {"CODEX_HOME": str(configured)}):
                    args = runner.codex_skill_isolation_args()
                    self.assertEqual(args[0], "-c")
                    entries = tomllib.loads(args[1])["skills"]["config"]
                    paths = [entry["path"] for entry in entries]
                    for path in (global_skill, legacy_skill, nested_skill):
                        self.assertEqual(paths.count(str(path.resolve())), 1)
                        self.assertEqual(path.read_text(), "original content\n")
                    self.assertNotIn(str(workspace_skill.resolve()), paths)
                    self.assertTrue(all(entry["enabled"] is False for entry in entries))


if __name__ == "__main__":
    unittest.main()
