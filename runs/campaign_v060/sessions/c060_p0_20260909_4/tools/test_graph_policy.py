"""Smoke-test bundle graph exclusion without touching the production graph."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[5]


class GraphPolicyTests(unittest.TestCase):
    def test_stale_out_of_corpus_document_is_excluded_and_asserted(self):
        ignore = (ROOT / ".graphifyignore").read_text()
        self.assertIn("docs/REFERENCES.md", ignore)
        graph = json.loads((ROOT / "graphify-out" / "graph.json").read_text())
        excluded = [n for n in graph["nodes"] if n.get("source_file") == "docs/REFERENCES.md"]
        self.assertEqual(len(excluded), 0, "the actual graph refresh has not been run or the exclusion failed")
        report = (ROOT / "graphify-out" / "GRAPH_REPORT.md").read_text()
        first_screen = "\n".join(report.splitlines()[:25])
        self.assertIn("Community labels are stale", first_screen)
        self.assertIn("docs/REFERENCES.md", first_screen)


if __name__ == "__main__":
    unittest.main()
