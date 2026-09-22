from pathlib import Path
import re
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]
OLD_TOOLS = {
    "jev_decide", "jev_rank", "jev_verify", "jev_assess", "jev_context_curate",
    "jev_context_rehydrate", "jev_stats", "jev_nervous_event", "jev_supervise_card",
    "jev_work_event", "jev_work_status", "jev_remote_delegate_task",
    "jev_remote_worker_status", "jev_remote_worker_result", "jev_remote_worker_cancel",
    "jev_remote_worker_control",
}

class NerveIdentityTests(unittest.TestCase):
    def test_canonical_identity(self):
        manifest = (ROOT / "plugin.yaml").read_text()
        project = tomllib.loads((ROOT / "pyproject.toml").read_text())["project"]
        catalog = (ROOT / "packaging/hermes-catalog/nerve.yaml").read_text()
        self.assertRegex(manifest, r"(?m)^name:\s*nerve\s*$")
        self.assertRegex(manifest, r'(?m)^version:\s*["\']?0\.2\.2["\']?\s*$')
        self.assertEqual(project["name"], "hermes-nerve")
        self.assertEqual(project["version"], "0.2.2")
        self.assertRegex(catalog, r"(?m)^name:\s*nerve\s*$")
        self.assertRegex(catalog, r'(?m)^version:\s*["\']?0\.2\.2["\']?\s*$')
        self.assertTrue((ROOT / "hermes_nerve").is_dir())
        self.assertFalse((ROOT / "hermes_jev").exists())
        self.assertFalse((ROOT / "packaging/hermes-catalog/jev.yaml").exists())

    def test_current_public_tools_are_nerve(self):
        text = (ROOT / "plugin.yaml").read_text() + (ROOT / "hermes_nerve/schemas.py").read_text()
        for tool in OLD_TOOLS:
            self.assertIsNone(re.search(rf"\\b{re.escape(tool)}\\b", text), tool)
        for tool in ("nerve_decide", "nerve_verify", "nerve_stats", "nerve_supervise_card", "nerve_remote_delegate_task"):
            self.assertIn(tool, text)

    def test_current_runtime_has_no_legacy_package_identity(self):
        roots = [ROOT / "__init__.py", ROOT / "plugin.yaml", ROOT / "pyproject.toml", ROOT / "README.md", ROOT / "scripts", ROOT / "hermes_nerve", ROOT / ".github"]
        bad = []
        for item in roots:
            files = [item] if item.is_file() else [p for p in item.rglob("*") if p.is_file() and p.suffix in {".py", ".md", ".txt", ".toml", ".yaml", ".yml", ".sh"}]
            for path in files:
                text = path.read_text(errors="ignore")
                for needle in ("Hermes-Jev", "hermes_jev", "plugins/hermes-jev"):
                    if needle in text:
                        bad.append(f"{path.relative_to(ROOT)} contains {needle}")
        self.assertEqual(bad, [])

if __name__ == "__main__":
    unittest.main()
