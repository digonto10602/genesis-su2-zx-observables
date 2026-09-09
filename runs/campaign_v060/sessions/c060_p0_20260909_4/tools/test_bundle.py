"""Synthetic fixtures test packaging only, never physics or research claims."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[5]
TOOL = Path(__file__).with_name("query_bundle.py")
(ROOT / ".work").mkdir(exist_ok=True)


class BundleTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(TOOL.is_file(), "bundle verification tool has not been implemented")
        spec = importlib.util.spec_from_file_location("query_bundle", TOOL)
        assert spec is not None and spec.loader is not None
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)

    def test_manifest_requires_exact_payload_and_matching_hashes(self):
        with tempfile.TemporaryDirectory(prefix="c063-manifest-", dir=ROOT / ".work") as tmp:
            base = Path(tmp)
            payload = b"fixture payload\n"
            (base / "payload.txt").write_bytes(payload)
            manifest = {"files": [{"path": "payload.txt", "bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest()}]}
            (base / "MANIFEST.json").write_text(json.dumps(manifest))
            (base / "MANIFEST.sha256").write_text(hashlib.sha256((base / "MANIFEST.json").read_bytes()).hexdigest() + "  MANIFEST.json\n")
            (base / "SELFTEST.json").write_text("{}\n")
            self.assertTrue(self.module.check_manifest(base)["pass"])
            (base / "extra.txt").write_text("unlisted\n")
            self.assertFalse(self.module.check_manifest(base)["pass"])
            (base / "extra.txt").unlink()
            (base / "payload.txt").write_text("tampered\n")
            self.assertFalse(self.module.check_manifest(base)["pass"])

    def test_links_reject_dangling_and_escaping_targets(self):
        self.assertTrue(hasattr(self.module, "check_links"), "link verifier missing")
        with tempfile.TemporaryDirectory(prefix="c063-links-", dir=ROOT / ".work") as tmp:
            base = Path(tmp)
            (base / "docs").mkdir()
            for name in ("ASK.md", "CLAIMS.md", "docs/GATE_MAP.md"):
                (base / name).write_text("# Fixture\n")
            (base / "docs/readme.md").write_text("# Fixture\n")
            (base / "INDEX.md").write_text("[Read](docs/readme.md)\n")
            self.assertTrue(self.module.check_links(base)["pass"])
            (base / "INDEX.md").write_text("[Missing](docs/missing.md)\n")
            self.assertFalse(self.module.check_links(base)["pass"])
            (base / "INDEX.md").write_text("[Escape](../escape.md)\n")
            self.assertFalse(self.module.check_links(base)["pass"])
    def test_backticked_navigation_paths_resolve_against_the_archive_root(self):
        with tempfile.TemporaryDirectory(prefix="c063-roots-", dir=ROOT / ".work") as tmp:
            base = Path(tmp)
            (base / "docs").mkdir()
            (base / "evidence").mkdir()
            (base / "evidence/present.json").write_text("{}\n")
            for name in ("INDEX.md", "ASK.md", "CLAIMS.md"):
                (base / name).write_text("# Fixture\n")
            (base / "docs/GATE_MAP.md").write_text("Evidence: `evidence/present.json`\n")
            self.assertTrue(self.module.check_links(base)["pass"])
            (base / "docs/GATE_MAP.md").write_text("Evidence: `evidence/absent.json`\n")
            self.assertFalse(self.module.check_links(base)["pass"])


if __name__ == "__main__":
    unittest.main()
