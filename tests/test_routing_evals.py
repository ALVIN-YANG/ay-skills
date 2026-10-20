from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "run_routing_evals", ROOT / "scripts" / "run_routing_evals.py"
)
assert SPEC and SPEC.loader
routing = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = routing
SPEC.loader.exec_module(routing)


class RoutingEvalTests(unittest.TestCase):
    def test_connection_failure_is_infrastructure_error(self) -> None:
        result = routing.Result(
            "case", False, "", "error", "", "API Error: Unable to connect to API (ConnectionRefused)"
        )
        self.assertTrue(routing.is_infrastructure_error(result))

    def test_dns_failure_is_infrastructure_error(self) -> None:
        result = routing.Result(
            "case",
            False,
            "",
            "error",
            "",
            "failed to lookup address information; stream disconnected before completion",
        )
        self.assertTrue(routing.is_infrastructure_error(result))

    def test_wrong_route_is_not_infrastructure_error(self) -> None:
        result = routing.Result("case", False, "ay-ui", "ay-product", "wrong boundary")
        self.assertFalse(routing.is_infrastructure_error(result))

    def test_rejected_account_model_is_infrastructure_error(self) -> None:
        result = routing.Result(
            "case", False, "ay-write", "error", "",
            "The 'gpt-5.5' model is not supported when using Codex with a ChatGPT account.",
        )
        self.assertTrue(routing.is_infrastructure_error(result))

    def test_fixture_catalog_includes_real_overlap_cases(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            installed = Path(directory) / "skills"
            installed.mkdir()
            routing.install_catalog(installed, "fixture")
            self.assertTrue((installed / "ay-store-screenshots" / "SKILL.md").is_file())
            self.assertTrue((installed / "ay-write" / "references" / "integration-docs.md").is_file())
            self.assertFalse((installed / "ay-integration-docs").exists())
            self.assertTrue((installed / "ship-app-store" / "SKILL.md").is_file())
            self.assertTrue((installed / "app-icon-studio" / "SKILL.md").is_file())

    def test_ay_only_catalog_has_no_competitor_stubs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            installed = Path(directory) / "skills"
            installed.mkdir()
            routing.install_catalog(installed, "ay-only")
            self.assertTrue((installed / "ay-store-screenshots" / "SKILL.md").is_file())
            self.assertFalse((installed / "ship-app-store").exists())

    def test_fixture_preserves_explicit_only_alternative(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            installed = Path(directory) / "skills"
            installed.mkdir()
            routing.install_catalog(installed, "fixture")
            policy = (installed / "human-writing/agents/openai.yaml").read_text()
            self.assertIn("allow_implicit_invocation: false", policy)
            primary = (installed / "ay-write/agents/openai.yaml").read_text()
            self.assertNotIn("allow_implicit_invocation: false", primary)


if __name__ == "__main__":
    unittest.main()
