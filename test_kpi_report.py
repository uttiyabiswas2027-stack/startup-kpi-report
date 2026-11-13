import unittest
from kpi_report import load, summarize, flags, render


class KpiTests(unittest.TestCase):
    def setUp(self):
        self.s = summarize(load("data/sample_metrics.csv"))

    def test_revenue_growth(self):
        self.assertAlmostEqual(self.s["revenue_wow_pct"], -3.846, places=2)

    def test_runway(self):
        self.assertAlmostEqual(self.s["runway_weeks"], 42400 / 2600)

    def test_churn(self):
        self.assertAlmostEqual(self.s["churn_pct"], 8 / 119 * 100)

    def test_burn_multiple_none_when_revenue_falls(self):
        self.assertIsNone(self.s["burn_multiple"])

    def test_flags(self):
        f = flags(self.s)
        self.assertTrue(any("churn" in x for x in f))
        self.assertTrue(any("Revenue fell" in x for x in f))

    def test_render(self):
        self.assertIn("# Weekly KPI report - 2026-W45", render(self.s))

    def test_needs_two_weeks(self):
        with self.assertRaises(ValueError):
            summarize([{"week": "x"}])


if __name__ == "__main__":
    unittest.main()
