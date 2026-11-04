import unittest
from pathlib import Path

from tools.check_theme import RULES, check_text

FIXTURES = Path(__file__).parent / "fixtures"


class ThemeCheckerTests(unittest.TestCase):
    def test_ok_fixture(self):
        self.assertEqual(check_text((FIXTURES / "ok.xml").read_text()), [])

    def test_bad_fixture_reports_each_parseable_rule(self):
        errors = "\n".join(check_text((FIXTURES / "bad.xml").read_text()))
        for name, _ in RULES[1:]:
            self.assertIn(f"{name}:", errors)

    def test_malformed_xml_stops_after_well_formed(self):
        errors = check_text("<html>")
        self.assertTrue(errors[0].startswith("well_formed:"))
        self.assertEqual(len(errors), 1)


if __name__ == "__main__":
    unittest.main()
