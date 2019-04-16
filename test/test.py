import unittest
import sys

from datetime import date, datetime

sys.path.append('../japanera')

from japanera import Japanera, Era, EraDate, EraDateTime


class TestJapanera(unittest.TestCase):
    """
    test class of japera
    """

    japera = Japanera()

    def test_before_era(self):
        actual = self.japera.era(date(645, 7, 19))
        self.assertEqual(None, actual)

    def test_start_of_era(self):
        actual = self.japera.era(date(645, 7, 20))
        self.assertEqual(Era("大化", "Taika", date(645, 7, 20), date(650, 3, 25), "common"), actual)

    def test_end_of_era(self):
        actual = self.japera.era(date(650, 3, 25))
        self.assertNotEqual(Era("大化", "Taika", date(645, 7, 20), date(650, 3, 25), "common"), actual)

    def test_has_no_name(self):
        actual = self.japera.era(date(654, 11, 27))
        self.assertEqual(Era(None, None, date(654, 11, 27), date(686, 8, 17), "common"), actual)

    def test_daikaku_era(self):
        actual = self.japera.daikaku_era(date(1336, 12, 19))
        self.assertEqual(Era("延元", "Engen", date(1336, 4, 19), date(1340, 6, 2), "daikakuji"), actual)

    def test_jimyouin_era(self):
        actual = self.japera.jimyouin_era(date(1336, 12, 19))
        self.assertEqual(Era("建武", "Kenmu", date(1334, 3, 13), date(1338, 10, 19), "jimyouin"), actual)

    def test_primary_jimyouin(self):
        japera_c = Japanera("jimyouin")
        actual = japera_c.era(date(1336, 12, 19))
        self.assertEqual(Era("建武", "Kenmu", date(1334, 3, 13), date(1338, 10, 19), "jimyouin"), actual)

    def test_strftime_jimyouin_O_not_first_year(self):
        actual = self.japera.jimyouin_era(date(1336, 12, 19)).strftime(date(1336, 12, 19), "%-E%-O年%m月%d日")
        self.assertEqual("建武03年12月19日", actual)

    def test_strftime_jimyouin_O_first_year(self):
        actual = self.japera.jimyouin_era(date(1334, 6, 19)).strftime(date(1334, 6, 19), "%-E%-O年%m月%d日")
        self.assertEqual("建武元年06月19日", actual)

    def test_strftime_jimyouin_o_first_year(self):
        actual = self.japera.jimyouin_era(date(1334, 6, 19)).strftime(date(1334, 6, 19), "%-E%-o年%m月%d日")
        self.assertEqual("建武01年06月19日", actual)

    def test_strftime_future_o_first_year(self):
        actual = self.japera.jimyouin_era(date(2019, 5, 1)).strftime(date(2019, 5, 1), "%-E%-o年%m月%d日")
        self.assertEqual("令和01年05月01日", actual)

    def test_strftime_future_O_first_year(self):
        actual = self.japera.jimyouin_era(date(2019, 5, 1)).strftime(date(2019, 5, 1), "%-E%-O年%m月%d日")
        self.assertEqual("令和元年05月01日", actual)

    def test_strftime_future_far(self):
        actual = self.japera.jimyouin_era(date(2048, 5, 1)).strftime(date(2048, 5, 1), "%-E%-O年%m月%d日")
        self.assertEqual("令和30年05月01日", actual)

    def test_strftime_japera_dot_strftime(self):
        actual = self.japera.strftime(date(2048, 5, 1), "%-E%-O年%m月%d日")
        self.assertEqual("令和30年05月01日", actual)

    def test_strftime_and_strptime_O(self):
        actual = self.japera.era(date(1500, 1, 1)).strptime(
            self.japera.era(date(1500, 1, 1)).strftime(date(1500, 1, 1), "%-E%-O年%m月%d日"), "%-E%-O年%m月%d日").date()
        self.assertEqual(date(1500, 1, 1), actual)

    def test_strftime_and_strptime_o(self):
        actual = self.japera.era(date(1500, 1, 1)).strptime(
            self.japera.era(date(1500, 1, 1)).strftime(date(1500, 1, 1), "%-E%-o年%m月%d日"), "%-E%-o年%m月%d日").date()
        self.assertEqual(date(1500, 1, 1), actual)

    def test_in_first_day(self):
        actual = self.japera.era(date(729, 9, 7))._in(date(729, 9, 6))
        self.assertTrue(actual)

    def test_in_middle(self):
        actual = self.japera.era(date(729, 9, 7))._in(date(749, 1, 6))
        self.assertTrue(actual)

    def test_in_last_day(self):
        actual = self.japera.era(date(729, 9, 7))._in(date(749, 5, 8))
        self.assertFalse(actual)

    def test_english_chorten_vowel(self):
        actual = self.japera.era(date(729, 9, 7)).english_shorten_vowel
        self.assertEqual("Tempyo", actual)

    def test_english_head(self):
        actual = self.japera.era(date(729, 9, 7)).english_head
        self.assertEqual("T", actual)

    def test_is_after_real_after(self):
        actual = self.japera.era(date(729, 9, 7)).is_after(date(500, 1, 1))
        self.assertTrue(actual)

    def test_is_after_not_after_first_day(self):
        actual = self.japera.era(date(729, 9, 7)).is_after(date(729, 9, 6))
        self.assertFalse(actual)

    def test_is_after_not_after_middle(self):
        actual = self.japera.era(date(729, 9, 7)).is_after(date(735, 9, 6))
        self.assertFalse(actual)

    def test_is_after_not_after_last_day(self):
        actual = self.japera.era(date(729, 9, 7)).is_after(date(749, 5, 8))
        self.assertFalse(actual)

    def test_is_after_not_after_after_day(self):
        actual = self.japera.era(date(729, 9, 7)).is_after(date(750, 5, 8))
        self.assertFalse(actual)

    def test_is_before_not_before(self):
        actual = self.japera.era(date(729, 9, 7)).is_before(date(500, 1, 1))
        self.assertFalse(actual)

    def test_is_before_not_before_first_day(self):
        actual = self.japera.era(date(729, 9, 7)).is_before(date(729, 9, 6))
        self.assertFalse(actual)

    def test_is_before_not_before_middle(self):
        actual = self.japera.era(date(729, 9, 7)).is_before(date(735, 9, 6))
        self.assertFalse(actual)

    def test_is_before_not_before_last_day(self):
        actual = self.japera.era(date(729, 9, 7)).is_before(date(749, 5, 8))
        self.assertFalse(actual)

    def test_is_before_real_before_before_day(self):
        actual = self.japera.era(date(729, 9, 7)).is_before(date(750, 5, 8))
        self.assertTrue(actual)

    def test_match(self):
        actual = self.japera.era_match(date(1370, 1, 1))
        self.assertEqual({"正平", "応安"}, set(map(lambda x: x.kanji, actual)))

    def test_match_func_given(self):
        actual = self.japera.era_match("S", lambda x: x.english_head, lambda x, y: x == y)
        self.assertEqual({"S"}, set(map(lambda x: x.english_head, actual)))

    def test_check_all_english_head_lower(self):
        eras = self.japera.era_common_daikakuji + self.japera.era_common_jimyouin
        for era in eras:
            try:
                self.assertEqual(era.english_head, era.english_head.lower())
            except:
                pass

    def test_eradate(self):
        Era("天平", "Tempyou", date(729, 9, 6), date(749, 5, 8), "common")
        era = self.japera.era(date(730, 1, 1))
        test_eradate = EraDate.fromdate(date(730, 5, 2), era)
        self.assertEqual(test_eradate.era, era)

    def test_EraDate(self):
        era = EraDate.fromdate(date(2020, 1, 1))
        self.assertEqual(era.era.kanji, "令和")
        self.assertEqual(str(era), "令和-2020-01-01")

    def test_EraDateTime(self):
        era = EraDateTime.fromdatetime(datetime(2019, 1, 1, 1, 1))
        self.assertEqual(era.era.kanji, "平成")
        self.assertEqual(str(era), "平成-2019-01-01 01:01:00")

    def test_EraDatetime_strftime(self):
        actual = EraDate.fromdate(date(749, 5, 8)).strftime("%-E%-e%-A%-a%-o%-O")
        self.assertEqual(actual, "天平感宝TempyokampoTempyouKampouT01元")

if __name__ == "__main__":
    unittest.main()
