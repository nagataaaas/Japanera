import unittest
from datetime import date, timedelta

import kanjize

from japanera import parser, era_data, Era, ERA_DATA_COMMON, ERA_DATA_JIMYOUIN, ERA_DATA_DAIKAKUJI, ERA_DATA_GENERAL


class TestStrPTime(unittest.TestCase):
    def test_vanilla_use_timezone(self):
        (era_kanji, era_english, era_english_vowel_shortened, era_head, relative_year), \
        (year, month, day, hour, minute, second, weekday, julian, tz, tzname, gmtoff), \
        fraction, gmtoff_fraction = parser._strptime("2020-10-23(Fri) 11:30:42.345678:UTC",
                                                     "%Y-%m-%d(%a) %H:%M:%S.%f:%Z")
        self.assertEqual([(era_kanji, era_english, era_english_vowel_shortened, era_head, relative_year),
                          (year, month, day, hour, minute, second, weekday, julian, tz, tzname,
                           gmtoff), fraction, gmtoff_fraction],
                         [(None, None, None, None, None),
                          (2020, 10, 23, 11, 30, 42, 4, None, 0, 'UTC', None),
                          345678, 0])

    def test_vanilla_use_offset(self):
        (era_kanji, era_english, era_english_vowel_shortened, era_head, relative_year), \
        (year, month, day, hour, minute, second, weekday, julian, tz, tzname, gmtoff), \
        fraction, gmtoff_fraction = parser._strptime("2020-10-23(Sun) 11:30:42.345678:+0900",
                                                     "%Y-%m-%d(%a) %H:%M:%S.%f:%z")
        self.assertEqual([(era_kanji, era_english, era_english_vowel_shortened, era_head, relative_year),
                          (year, month, day, hour, minute, second, weekday, julian, tz, tzname,
                           gmtoff), fraction, gmtoff_fraction],
                         [(None, None, None, None, None),
                          (2020, 10, 23, 11, 30, 42, 6, None, -1, None, 32400),
                          345678, 0])

    def test_era_name_parse(self):
        (era_kanji, era_english, era_english_vowel_shortened, era_head, relative_year), \
        (year, month, day, hour, minute, second, weekday, julian, tz, tzname, gmtoff), \
        fraction, gmtoff_fraction = parser._strptime("宝暦(Houreki, Horeki, H)", "%-K(%-E, %-e, %-h)")
        self.assertEqual([(era_kanji, era_english, era_english_vowel_shortened, era_head, relative_year),
                          (year, month, day, hour, minute, second, weekday, julian, tz, tzname,
                           gmtoff), fraction, gmtoff_fraction],
                         [("宝暦", "Houreki", "Horeki", "H", None),
                          (None, None, None, 0, 0, 0, None, None, -1, None, None),
                          0, 0])

    def test_era_name_parse_error(self):
        self.assertRaises(ValueError, parser._strptime, "玲和", "%-K")
        self.assertRaises(ValueError, parser._strptime, "Rewa", "%-E")
        self.assertRaises(ValueError, parser._strptime, "Rewa", "%-e")
        self.assertRaises(ValueError, parser._strptime, "Q", "%-h")

    def test_parse_kanji_date(self):
        self.assertEqual(parser._strptime("2000", "%-Y")[1][0], 2000)
        self.assertEqual(parser._strptime("二千", "%-N")[1][0], 2000)
        self.assertEqual(parser._strptime("二千百四十六", "%-N")[1][0], 2146)
        self.assertEqual(parser._strptime("千十", "%-N")[1][0], 1010)
        self.assertEqual(parser._strptime("四百九十八", "%-N")[1][0], 498)
        self.assertEqual(parser._strptime("元", "%-N")[1][0], 1)
        self.assertEqual(parser._strptime("元", "%-Y")[1][0], 1)
        self.assertRaises(ValueError, parser._strptime, "四万", "%-N")  # out of range
        self.assertRaises(ValueError, parser._strptime, "4千", "%-N")  # invalid format
        self.assertRaises(ValueError, parser._strptime, "4000", "%-N")  # invalid format
        self.assertRaises(ValueError, parser._strptime, "四千", "%-Y")  # invalid format

        self.assertEqual(parser._strptime("20", "%-y")[0][4], 20)
        self.assertEqual(parser._strptime("三十八", "%-n")[0][4], 38)
        self.assertEqual(parser._strptime("十一", "%-n")[0][4], 11)
        self.assertEqual(parser._strptime("十", "%-n")[0][4], 10)
        self.assertEqual(parser._strptime("元", "%-y")[0][4], 1)
        self.assertEqual(parser._strptime("元", "%-n")[0][4], 1)
        self.assertRaises(ValueError, parser._strptime, "二千", "%-n")  # out of range
        self.assertRaises(ValueError, parser._strptime, "五百二十一", "%-n")  # out of range
        self.assertRaises(ValueError, parser._strptime, "五百二十一", "%-y")  # out of range
        self.assertRaises(ValueError, parser._strptime, "50", "%-n")  # invalid format
        self.assertRaises(ValueError, parser._strptime, "二十", "%-y")  # invalid format

        for month in range(1, 13):
            self.assertEqual(parser._strptime(kanjize.number2kanji(month), "%-m")[1][1], month)
            self.assertEqual(parser._strptime(str(month), "%-m")[1][1], month)
        self.assertRaises(ValueError, parser._strptime, "十三", "%-m")  # out of range
        self.assertRaises(ValueError, parser._strptime, "元", "%-m")  # invalid character

        for day in range(1, 32):
            self.assertEqual(parser._strptime(kanjize.number2kanji(day), "%-d")[1][2], day)
            self.assertEqual(parser._strptime(str(day), "%-d")[1][2], day)
        self.assertRaises(ValueError, parser._strptime, "三十二", "%-d")  # out of range
        self.assertRaises(ValueError, parser._strptime, "元", "%-d")  # invalid character

        today = date.today()
        for offset in range(7):
            target = today + timedelta(days=offset)
            self.assertEqual(parser._strptime('月火水木金土日'[target.weekday()], "%-a")[1][6],
                             parser._strptime(target.strftime("%a"), "%a")[1][6])
            self.assertEqual('月火水木金土日'[target.weekday()],
                             {0: '月', 1: '火', 2: '水', 3: '木', 4: '金', 5: '土',
                              6: '日'}[parser._strptime(target.strftime("%a"), "%a")[1][6]])  # check weekday assignment
        self.assertRaises(ValueError, parser._strptime, "元", "%-a")  # invalid character
        self.assertRaises(ValueError, parser._strptime, "天", "%-a")  # invalid character


class TestFindClosestLeapYear(unittest.TestCase):
    def test(self):
        self.assertEqual(parser.find_closest_leap_year(2000), 2000)
        self.assertEqual(parser.find_closest_leap_year(1999), 2000)
        self.assertEqual(parser.find_closest_leap_year(2100), 2104)
        self.assertEqual(parser.find_closest_leap_year(2099), 2104)
        self.assertEqual(parser.find_closest_leap_year(2039), 2040)
        self.assertEqual(parser.find_closest_leap_year(2040), 2040)
        self.assertEqual(parser.find_closest_leap_year(2041), 2044)


class TestFindErasWithYear(unittest.TestCase):
    def test_only_general(self):
        self.assertSetEqual(parser.find_eras_with_year(1000),
                            {
                                Era("長保", "Chouhou", date(999, 2, 6),
                                           date(1004, 8, 14), era_data.EraType.GENERAL),
                                Era("西暦", "Seireki", date(1, 1, 1), None, era_data.EraType.COMMON),
                            })

    def test_both_nambokucho(self):
        self.assertSetEqual(parser.find_eras_with_year(1331),
                            {
                                Era("元徳", "Gentoku", date(1329, 9, 30),
                                           date(1331, 9, 19), era_data.EraType.DAIKAKUJI),
                                Era("元弘", "Genkou", date(1331, 9, 19),
                                           date(1334, 3, 13), era_data.EraType.DAIKAKUJI),
                                Era("元徳", "Gentoku", date(1329, 9, 30),
                                           date(1332, 5, 31), era_data.EraType.JIMYOUIN),
                                Era("西暦", "Seireki", date(1, 1, 1), None, era_data.EraType.COMMON),
                            })

    def test_nambokucho_only_jimyouin(self):
        self.assertSetEqual(parser.find_eras_with_year(1393),
                            {
                                Era("明徳", "Meitoku", date(1390, 4, 20),
                                           date(1394, 8, 10), era_data.EraType.JIMYOUIN),
                                Era("西暦", "Seireki", date(1, 1, 1), None, era_data.EraType.COMMON),
                            })

    def test_before_era(self):
        self.assertSetEqual(parser.find_eras_with_year(1),
                            {
                                Era("西暦", "Seireki", date(1, 1, 1), None, era_data.EraType.COMMON)
                            })

    def test_latest(self):
        self.assertSetEqual(parser.find_eras_with_year(3000),
                            {
                                ERA_DATA_GENERAL[-1],
                                Era("西暦", "Seireki", date(1, 1, 1), None, era_data.EraType.COMMON),
                            })


class TestFindEraAndDate(unittest.TestCase):
    def test_only_kanji(self):
        self.assertListEqual(parser.find_era_and_date(era_kanji="令和"),
                             [(Era("令和", "Reiwa", date(2019, 5, 1), None, era_data.EraType.GENERAL),
                               date(2019, 5, 1))])
        self.assertListEqual(parser.find_era_and_date(era_kanji="元徳"),
                             [
                                 (Era("元徳", "Gentoku", date(1329, 9, 30),
                                             date(1331, 9, 19), era_data.EraType.DAIKAKUJI),
                                  date(1329, 9, 30)),
                                 (Era("元徳", "Gentoku", date(1329, 9, 30),
                                             date(1332, 5, 31), era_data.EraType.JIMYOUIN),
                                  date(1329, 9, 30)),
                             ])
        self.assertRaises(ValueError, parser.find_era_and_date, era_kanji="無効")

    def test_only_english(self):
        self.assertListEqual(parser.find_era_and_date(era_english="Reiwa"),
                             [(Era("令和", "Reiwa", date(2019, 5, 1), None, era_data.EraType.GENERAL),
                               date(2019, 5, 1))])
        self.assertListEqual(parser.find_era_and_date(era_english="Kouwa"),
                             [
                                 (Era("康和", "Kouwa", date(1099, 9, 21),
                                             date(1104, 3, 15), era_data.EraType.GENERAL),
                                  date(1099, 9, 21)),
                                 (Era("弘和", "Kouwa", date(1381, 3, 14),
                                             date(1384, 5, 26), era_data.EraType.DAIKAKUJI),
                                  date(1381, 3, 14)),
                             ])
        self.assertRaises(ValueError, parser.find_era_and_date, era_english="Invalid")

    def test_only_english_vowel_shortened(self):
        self.assertListEqual(parser.find_era_and_date(era_english_vowel_shortened="Tengyo"),
                             [(Era("天慶", "Tengyou", date(938, 6, 27), date(947, 5, 20),
                                          era_data.EraType.GENERAL),
                               date(938, 6, 27))])
        self.assertRaises(ValueError, parser.find_era_and_date, era_english_vowel_shortened="Tengyou")  # not shortened
        self.assertRaises(ValueError, parser.find_era_and_date, era_english_vowel_shortened="Invalid")

    def test_only_english_head(self):
        self.assertListEqual(parser.find_era_and_date(era_head_english="W"),
                             [(Era("和銅", "Wadou", date(708, 2, 11), date(715, 10, 7),
                                          era_data.EraType.GENERAL),
                               date(708, 2, 11))])
        self.assertRaises(ValueError, parser.find_era_and_date, era_english_vowel_shortened="Wadou")  # not shortened
        self.assertRaises(ValueError, parser.find_era_and_date, era_english_vowel_shortened="Q")  # no era starts with Q

    def test_only_absolute_year(self):
        self.assertListEqual(parser.find_era_and_date(absolute_year=710),
                             [(Era("西暦", "Seireki", date(1, 1, 1), None, era_data.EraType.COMMON),
                               date(710, 1, 1)),
                              (Era("和銅", "Wadou", date(708, 2, 11), date(715, 10, 7),
                                          era_data.EraType.GENERAL),
                               date(710, 1, 1))])
        self.assertListEqual(parser.find_era_and_date(absolute_year=715),  # 2 eras
                             [(Era("西暦", "Seireki", date(1, 1, 1), None, era_data.EraType.COMMON),
                               date(715, 1, 1)),
                              (Era("和銅", "Wadou", date(708, 2, 11), date(715, 10, 7),
                                          era_data.EraType.GENERAL),
                               date(715, 1, 1)),
                              (Era("霊亀", "Reiki", date(715, 10, 7), date(717, 12, 28),
                                          era_data.EraType.GENERAL),
                               date(715, 10, 7)),
                              ])
        self.assertListEqual(parser.find_era_and_date(absolute_year=1225),  # 3 eras
                             [(Era("西暦", "Seireki", date(1, 1, 1), None, era_data.EraType.COMMON),
                               date(1225, 1, 1)),
                              (Era("貞応", "Jouou", date(1222, 6, 1), date(1225, 1, 7),
                                          era_data.EraType.GENERAL),
                               date(1225, 1, 1)),
                              (Era("元仁", "Gennin", date(1225, 1, 7), date(1225, 6, 4),
                                          era_data.EraType.GENERAL),
                               date(1225, 1, 7)),
                              (Era("嘉禄", "Karoku", date(1225, 6, 4), date(1228, 1, 25),
                                          era_data.EraType.GENERAL),
                               date(1225, 6, 4)),
                              ])
        self.assertListEqual(parser.find_era_and_date(absolute_year=2500),
                             [(Era("西暦", "Seireki", date(1, 1, 1), None, era_data.EraType.COMMON),
                               date(2500, 1, 1)),
                              (ERA_DATA_GENERAL[-1],
                               date(2500, 1, 1)),
                              ])
        self.assertListEqual(parser.find_era_and_date(absolute_year=1),
                             [(Era("西暦", "Seireki", date(1, 1, 1), None, era_data.EraType.COMMON),
                               date(1, 1, 1)),
                              ])

    def test_only_relative_year(self):
        self.assertEqual(len(parser.find_era_and_date(relative_year=1)),
                         len(ERA_DATA_GENERAL + ERA_DATA_JIMYOUIN +
                             ERA_DATA_DAIKAKUJI + ERA_DATA_COMMON))
        self.assertListEqual([e.kanji for e, _ in parser.find_era_and_date(relative_year=50)],
                             ["西暦", "昭和", "令和"])
        self.assertListEqual([e.kanji for e, _ in parser.find_era_and_date(relative_year=100)],
                             ["西暦", "令和"])

    def test_combination_era_name(self):
        self.assertListEqual(parser.find_era_and_date(era_kanji="康和", era_english="Kouwa"),
                             [
                                 (Era("康和", "Kouwa", date(1099, 9, 21),
                                             date(1104, 3, 15), era_data.EraType.GENERAL),
                                  date(1099, 9, 21)),
                             ])

        self.assertListEqual(
            parser.find_era_and_date(era_english="Kouwa", era_english_vowel_shortened="Kowa", era_head_english="K"),
            [
                (Era("康和", "Kouwa", date(1099, 9, 21),
                            date(1104, 3, 15), era_data.EraType.GENERAL),
                 date(1099, 9, 21)),
                (Era("弘和", "Kouwa", date(1381, 3, 14),
                            date(1384, 5, 26), era_data.EraType.DAIKAKUJI),
                 date(1381, 3, 14)),
            ])

    def test_combination_era_name_year_and_date(self):
        self.assertListEqual(parser.find_era_and_date(era_english="Kouwa", relative_year=4),
                             [
                                 (Era("康和", "Kouwa", date(1099, 9, 21),
                                             date(1104, 3, 15), era_data.EraType.GENERAL),
                                  date(1102, 1, 1)),
                                 (Era("弘和", "Kouwa", date(1381, 3, 14),
                                             date(1384, 5, 26), era_data.EraType.DAIKAKUJI),
                                  date(1384, 1, 1)),
                             ])
        self.assertListEqual(parser.find_era_and_date(era_english="Kouwa", relative_year=5),
                             [
                                 (Era("康和", "Kouwa", date(1099, 9, 21),
                                             date(1104, 3, 15), era_data.EraType.GENERAL),
                                  date(1103, 1, 1)),
                             ])

        self.assertListEqual(parser.find_era_and_date(era_english="Kouwa", relative_year=4, month=5, day=25),
                             [
                                 (Era("康和", "Kouwa", date(1099, 9, 21),
                                             date(1104, 3, 15), era_data.EraType.GENERAL),
                                  date(1102, 5, 25)),
                                 (Era("弘和", "Kouwa", date(1381, 3, 14),
                                             date(1384, 5, 26), era_data.EraType.DAIKAKUJI),
                                  date(1384, 5, 25)),
                             ])
        self.assertListEqual(parser.find_era_and_date(era_english="Kouwa", relative_year=4, month=5, day=26),
                             [
                                 (Era("康和", "Kouwa", date(1099, 9, 21),
                                             date(1104, 3, 15), era_data.EraType.GENERAL),
                                  date(1102, 5, 26)),
                             ])
        self.assertRaises(ValueError, parser.find_era_and_date, era_english="Kouwa", absolute_year=1500)

    def test_date(self):
        self.assertEqual(parser.find_era_and_date(era_kanji="大正")[0][1], date(1912, 7, 30))
        self.assertEqual(parser.find_era_and_date(era_kanji="大正", relative_year=1)[0][1], date(1912, 7, 30))
        self.assertEqual(parser.find_era_and_date(era_kanji="大正", relative_year=2)[0][1], date(1913, 1, 1))
        self.assertEqual(parser.find_era_and_date(era_kanji="大正", month=8)[0][1], date(1912, 8, 1))
        self.assertEqual(parser.find_era_and_date(era_kanji="大正", month=1)[0][1], date(1913, 1, 1))
        self.assertEqual(parser.find_era_and_date(era_kanji="大正", month=2, day=29)[0][1], date(1916, 2, 29))
        self.assertEqual(len(parser.find_era_and_date(absolute_year=2019, month=4, day=30)), 2)

    def test_allow_date_after_end_of_era(self):
        self.assertListEqual(parser.find_era_and_date(era_kanji="平成", relative_year=31, month=4, day=30),
                             [
                                 (Era("平成", "Heisei", date(1989, 1, 8),
                                             date(2019, 5, 1), era_data.EraType.GENERAL),
                                  date(2019, 4, 30)),
                             ])
        self.assertListEqual(parser.find_era_and_date(era_kanji="平成", relative_year=31, month=5, day=1), [])
        self.assertListEqual(parser.find_era_and_date(era_kanji="平成", relative_year=31, month=5, day=1,
                                                      allow_date_after_end_of_era=True),
                             [
                                 (Era("平成", "Heisei", date(1989, 1, 8),
                                             date(2019, 5, 1), era_data.EraType.GENERAL),
                                  date(2019, 5, 1)),
                             ])


if __name__ == '__main__':
    unittest.main()
