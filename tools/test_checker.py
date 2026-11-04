import unittest
from pathlib import Path

from tools.check_theme import RULES, check_text, main

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

    def test_html_must_declare_namespaces(self):
        text = (FIXTURES / "ok.xml").read_text().replace(' xmlns:data="http://www.google.com/2005/gml/data"', "")
        self.assertIn("html_attrs: html must declare xmlns:data", "\n".join(check_text(text)))

    def test_head_script_budget(self):
        text = (FIXTURES / "ok.xml").read_text().replace("<body>", '<body><script id="atlas-head">' + "x" * 401 + "</script>")
        self.assertIn("js_budget: script #atlas-head is 401 bytes", "\n".join(check_text(text)))

    def test_hero_lcp_outside_hero(self):
        text = (FIXTURES / "ok.xml").read_text().replace("<body>", '<body><img fetchpriority="high"/>')
        self.assertIn("hero_lcp: exactly one fetchpriority expected, found 2", "\n".join(check_text(text)))
        text = (FIXTURES / "ok.xml").read_text().replace(' fetchpriority="high"', "").replace("<body>", '<body><img fetchpriority="high"/>')
        self.assertIn("hero_lcp: fetchpriority must sit inside section hero", "\n".join(check_text(text)))

    def test_also_missing_path_fails(self):
        self.assertEqual(main([str(FIXTURES / "ok.xml"), "--also", "does-not-exist"]), 1)


if __name__ == "__main__":
    unittest.main()
