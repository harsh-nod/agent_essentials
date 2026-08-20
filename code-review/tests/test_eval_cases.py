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

    def test_review_gate_robustness_case_is_complete(self) -> None:
        case = ROOT / "eval-cases" / "review-gate-robustness"
        manifest = json.loads((case / "manifest.json").read_text(encoding="utf-8"))
        expected = json.loads(
            (case / manifest["expected_results"]).read_text(encoding="utf-8")
        )

        self.assertEqual(manifest["finding_count"], len(expected["buggy_findings"]))
        self.assertEqual(expected["fixed_expected_findings"], 0)
        self.assertTrue((case / manifest["buggy_input"]).is_file())
        self.assertTrue((case / manifest["fixed_counterexample"]).is_file())

        mechanisms = " ".join(item["mechanism"] for item in expected["buggy_findings"])
        self.assertIn("comments fail CI", mechanisms)
        self.assertIn("never exercise the CLI", mechanisms)
        self.assertIn("attribute strings", mechanisms)
        self.assertIn("delete the checker", mechanisms)
        self.assertIn("expansion context", mechanisms)
        self.assertIn("absolute archive digest", mechanisms)
        self.assertIn("both comparison roles", mechanisms)

        reviewer_prompt = (ROOT / "prompts" / "reviewer.md").read_text(
            encoding="utf-8"
        )
        rust_checklist = (ROOT / "checklists" / "rust.md").read_text(
            encoding="utf-8"
        )
        ci_checklist = (ROOT / "checklists" / "ci-configuration.md").read_text(
            encoding="utf-8"
        )
        docs_checklist = (ROOT / "checklists" / "documentation.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("comment/string/whitespace controls", reviewer_prompt)
        self.assertIn("For macros, probe call-site", reviewer_prompt)
        self.assertIn("name shadowing", reviewer_prompt)
        self.assertIn("exact checker CLI", ci_checklist)
        self.assertIn("trusted-base checker", ci_checklist)
        self.assertIn("same resolved path or inode", ci_checklist)
        self.assertIn("`$crate::`", rust_checklist)
        self.assertIn("Do not relabel a golden-text", docs_checklist)
        self.assertIn("pin as semantic", docs_checklist)

    def test_proof_oracle_portability_case_is_complete(self) -> None:
        case = ROOT / "eval-cases" / "proof-oracle-portability"
        manifest = json.loads((case / "manifest.json").read_text(encoding="utf-8"))
        expected = json.loads(
            (case / manifest["expected_results"]).read_text(encoding="utf-8")
        )

        self.assertEqual(manifest["finding_count"], len(expected["buggy_findings"]))
        self.assertEqual(expected["fixed_expected_findings"], 0)
        self.assertTrue((case / manifest["buggy_input"]).is_file())
        self.assertTrue((case / manifest["fixed_counterexample"]).is_file())

        mechanisms = " ".join(item["mechanism"] for item in expected["buggy_findings"])
        self.assertIn("drift in lockstep", mechanisms)
        self.assertIn("outside the typed code image", mechanisms)
        self.assertIn("no verified consumer", mechanisms)
        self.assertIn("commented-out no-default command", mechanisms)
        self.assertIn("absolute sysroot paths", mechanisms)

        reviewer_prompt = (ROOT / "prompts" / "reviewer.md").read_text(
            encoding="utf-8"
        )
        rust_checklist = (ROOT / "checklists" / "rust.md").read_text(
            encoding="utf-8"
        )
        python_checklist = (ROOT / "checklists" / "python.md").read_text(
            encoding="utf-8"
        )
        shell_checklist = (ROOT / "checklists" / "shell-build.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("Map every material postcondition", reviewer_prompt)
        self.assertIn("extra accepted rows outside the typed image", reviewer_prompt)
        self.assertIn("Build a consumer map", rust_checklist)
        self.assertIn("accepted rows are in the typed code image", rust_checklist)
        self.assertIn("Self-asserted commit", python_checklist)
        self.assertIn("active shell commands", shell_checklist)
        self.assertIn("embedded absolute source", shell_checklist)


if __name__ == "__main__":
    unittest.main()
