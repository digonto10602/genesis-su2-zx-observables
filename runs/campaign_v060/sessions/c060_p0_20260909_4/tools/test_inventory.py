"""Documentation-tool tests only; never import the archived physics package."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[5]
SCRIPT = ROOT / "tools/function_inventory.py"
(ROOT / ".work").mkdir(exist_ok=True)


class InventoryTests(unittest.TestCase):
    def test_custom_roots_cannot_overwrite_reserved_legacy_output(self):
        with tempfile.TemporaryDirectory(prefix="c063-reserved-", dir=ROOT / ".work") as tmp:
            fixture = Path(tmp)
            (fixture / "input/src").mkdir(parents=True)
            (fixture / "input/src/probe.py").write_text("def visible():\n    return 1\n")
            (fixture / "docs").mkdir()
            output = fixture / "docs/CODE_FUNCTION_INVENTORY.md"
            output.write_text("preserved legacy fixture\n")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--base", "input", "--roots", "src"],
                cwd=fixture, env=dict(os.environ, PYTHONPATH=str(ROOT / "src")), capture_output=True, text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("legacy output is reserved for the original roots", result.stderr)
            self.assertEqual(output.read_text(), "preserved legacy fixture\n")

    def test_output_cannot_escape_invocation_root(self):
        with tempfile.TemporaryDirectory(prefix="c063-output-", dir=ROOT / ".work") as tmp:
            fixture = Path(tmp) / "inside"
            (fixture / "src").mkdir(parents=True)
            (fixture / "src/probe.py").write_text("def visible():\n    return 1\n")
            output = Path(tmp) / "outside.md"
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--roots", "src", "--output", "../outside.md"],
                cwd=fixture, env=dict(os.environ, PYTHONPATH=str(ROOT / "src")), capture_output=True, text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("path escapes project root", result.stderr)
            self.assertFalse(output.exists())

    def test_default_output_is_byte_identical_to_committed_inventory(self):
        reference = subprocess.check_output(["git", "show", "HEAD:docs/CODE_FUNCTION_INVENTORY.md"], cwd=ROOT)
        result = subprocess.run(
            [sys.executable, str(SCRIPT)], cwd=ROOT,
            env=dict(os.environ, PYTHONPATH=str(ROOT / "src")), capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((ROOT / "docs/CODE_FUNCTION_INVENTORY.md").read_bytes(), reference)

    def test_gate_roots_extract_assertions_and_duplicate_roots_are_deduplicated(self):
        with tempfile.TemporaryDirectory(prefix="c063-gates-", dir=ROOT / ".work") as tmp:
            base = Path(tmp)
            for directory in ("gates", "src"):
                (base / directory).mkdir()
                (base / directory / "probe.py").write_text("@decorate(True)\ndef check(x=1):\n    assert x > 0\n")
            output = base / "inventory.md"
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--base", str(base), "--roots", "gates", "gates", "src", "--output", str(output)],
                cwd=ROOT, env=dict(os.environ, PYTHONPATH=str(ROOT / "src")), capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            text = output.read_text()
            self.assertEqual(text.count("## [gates/probe.py]"), 1)
            gate, source = text.split("## [src/probe.py]", 1)
            self.assertIn("Decorator: `decorate(True)`", gate)
            self.assertIn("```python\nassert x > 0\n```", gate)
            self.assertNotIn("```python", source)
            self.assertNotIn("Decorator:", source)

    def test_directory_symlinks_are_rejected(self):
        with tempfile.TemporaryDirectory(prefix="c063-linkdir-", dir=ROOT / ".work") as tmp:
            base = Path(tmp) / "inside"
            base.mkdir()
            sibling = Path(tmp) / "sibling"
            sibling.mkdir()
            (sibling / "probe.py").write_text("def visible():\n    return 1\n")
            (base / "linked").symlink_to(sibling, target_is_directory=True)
            output = Path(tmp) / "inventory.md"
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--base", str(base), "--roots", ".", "--output", str(output)],
                cwd=ROOT, env=dict(os.environ, PYTHONPATH=str(ROOT / "src")), capture_output=True, text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("symlink source is not allowed", result.stderr)
            self.assertFalse(output.exists())

    def test_source_symlinks_are_rejected_before_parsing(self):
        with tempfile.TemporaryDirectory(prefix="c063-symlink-", dir=ROOT / ".work") as tmp:
            base = Path(tmp) / "inside"
            base.mkdir()
            outside = Path(tmp) / "outside.py"
            outside.write_text("def hidden():\n    return 1\n")
            (base / "linked.py").symlink_to(outside)
            output = Path(tmp) / "inventory.md"
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--base", str(base), "--roots", ".", "--output", str(output)],
                cwd=ROOT, env=dict(os.environ, PYTHONPATH=str(ROOT / "src")), capture_output=True, text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("symlink source is not allowed", result.stderr)
            self.assertFalse(output.exists())

    def test_source_roots_cannot_escape_selected_base(self):
        with tempfile.TemporaryDirectory(prefix="c063-boundary-", dir=ROOT / ".work") as tmp:
            base = Path(tmp) / "inside"
            base.mkdir()
            sibling = Path(tmp) / "sibling"
            sibling.mkdir()
            (sibling / "probe.py").write_text("def visible():\n    return 1\n")
            output = Path(tmp) / "inventory.md"
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--base", str(base), "--roots", "../sibling", "--output", str(output)],
                cwd=ROOT, env=dict(os.environ, PYTHONPATH=str(ROOT / "src")), capture_output=True, text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("source root escapes selected base", result.stderr)
            self.assertFalse(output.exists())

    def test_explicit_roots_emit_separate_ast_only_inventory(self):
        with tempfile.TemporaryDirectory(prefix="c063-inventory-", dir=ROOT / ".work") as tmp:
            base = Path(tmp)
            (base / "src").mkdir()
            (base / "src/probe.py").write_text(
                '"""Sentinel module: inventory must never execute it."""\n'
                'raise RuntimeError("MUST NOT IMPORT")\n'
                'def public(x=3):\n'
                '    """A source-only callable."""\n'
                '    return zeta(alpha(x))\n'
            )
            output = base / "inventory.md"
            env = dict(os.environ, PYTHONPATH=str(ROOT / "src"), PYTHONDONTWRITEBYTECODE="1")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--base", str(base), "--roots", "src", "--output", str(output)],
                cwd=ROOT, env=env, capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(output.is_file(), "explicit output was not emitted; CLI scope is missing")
            text = output.read_text()
            self.assertIn("## [src/probe.py]", text)
            self.assertIn("../src/probe.py", text)
            self.assertIn("### `public(x=3)` — line 3", text)
            self.assertIn("Direct call expressions: `alpha`, `zeta`", text)
            self.assertNotIn("src/su2zx/core.py", text)


if __name__ == "__main__":
    unittest.main()
