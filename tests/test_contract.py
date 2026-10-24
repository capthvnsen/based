import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]

class Contract(unittest.TestCase):
    def test_frontmatter(self):
        text = (ROOT / "SKILL.md").read_text()
        self.assertTrue(text.startswith("---\n"))
        self.assertIn("name: based", text.split("---", 2)[1])
        description = re.search(r'description: "([^"\n]+)"', text).group(1)
        self.assertLessEqual(len(description), 60)

    def test_local_links(self):
        for path in ROOT.rglob("*.md"):
            for target in re.findall(r"\]\(([^)]+)\)", path.read_text()):
                if not target.startswith(("https:", "http:", "#")):
                    self.assertTrue((path.parent / target).is_file(), target)

    def test_panel_and_review_contract(self):
        text = (ROOT / "SKILL.md").read_text()
        for requirement in ("exactly THREE", "FOURTH", "fresh", "model/provider", "No judge sees", "privacy", "Three judgments are not three independent empirical confirmations"):
            if requirement == "privacy":
                self.assertIn("private information", text)
            else:
                self.assertIn(requirement, text)
        self.assertIn("PASS or REVISE", (ROOT / "references/reviewer.md").read_text())

if __name__ == "__main__":
    unittest.main()
