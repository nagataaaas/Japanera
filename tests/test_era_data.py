import unittest
from datetime import date

from japanera import Era, EraType


class TestEra(unittest.TestCase):
    def test_compare_era(self):
        before_era = Era("前", "Mae", date(2000, 1, 1), date(2001, 1, 1), EraType.GENERAL)
        between_era = Era("間", "Aida", date(2001, 5, 1), date(2001, 6, 1), EraType.GENERAL)
        after_era = Era("後", "Ato", date(2001, 1, 1), date(2002, 1, 1), EraType.GENERAL)

        before_before = date(1999, 12, 31)
        start_before = date(2000, 1, 1)
        in_before = date(2000, 6, 1)
        last_before = date(2001, 1, 1)

        self.assertTrue(before_before < before_era)
        self.assertTrue(before_era > before_before)
        self.assertFalse(start_before < before_era)
        self.assertTrue(start_before <= before_era)
        self.assertTrue(in_before in before_era)
        self.assertFalse(last_before in before_era)
        self.assertTrue(last_before not in before_era)
        self.assertFalse(last_before < before_era)
        self.assertFalse(last_before <= before_era)
        self.assertTrue(last_before > before_era)
        self.assertTrue(last_before >= before_era)

        self.assertTrue(in_before in before_era)

        self.assertTrue(before_era < after_era)
        self.assertTrue(before_era <= after_era)
        self.assertTrue(before_era <= between_era)
        self.assertTrue(between_era >= after_era)


if __name__ == '__main__':
    unittest.main()
