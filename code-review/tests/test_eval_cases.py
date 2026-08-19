import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class EvalCaseTests(unittest.TestCase):
    def test_cfg_split_proof_coverage_case_is_complete(self) -> None:
        case = ROOT / "eval-cases" / "cfg-split-proof-coverage"
        manifest = json.loads((case / "manifest.json").read_text(encoding="utf-8"))
        expected = json.loads((case / manifest["expected_results"]).read_text(encoding="utf-8"))

        self.assertEqual(manifest["finding_count"], len(expected["buggy_findings"]))
        self.assertEqual(expected["fixed_expected_findings"], 0)
        self.assertTrue((case / manifest["buggy_input"]).is_file())
        self.assertTrue((case / manifest["fixed_counterexample"]).is_file())

        mechanisms = " ".join(item["mechanism"] for item in expected["buggy_findings"])
        self.assertIn("host and target state-machine bodies", mechanisms)
        self.assertIn("datatype definition", mechanisms)
        self.assertIn("documented developer command", mechanisms)

        reviewer_prompt = (ROOT / "prompts" / "reviewer.md").read_text(encoding="utf-8")
        rust_checklist = (ROOT / "checklists" / "rust.md").read_text(encoding="utf-8")
        ci_checklist = (ROOT / "checklists" / "ci-configuration.md").read_text(
            encoding="utf-8"
        )
        docs_checklist = (ROOT / "checklists" / "documentation.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("map each body to the tests, proofs, and target runs", reviewer_prompt)
        self.assertIn("structural/definitional lemmas", reviewer_prompt)
        self.assertIn("documented developer command", reviewer_prompt)
        self.assertIn("one-time identical binary comparison", rust_checklist)
        self.assertIn("plausible semantic mutation", rust_checklist)
        self.assertIn("green host test plus a target compile", ci_checklist)
        self.assertIn("structural datatype lemmas", docs_checklist)


if __name__ == "__main__":
    unittest.main()
