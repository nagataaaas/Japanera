import datetime
import unittest
from datetime import date

from japanera import EraDate, Era, EraType, EraDateTime, ERA_DATA_GENERAL, ERA_DATA_COMMON


class TestEraDate(unittest.TestCase):
    def test_new(self):
        self.assertWarns(RuntimeWarning, EraDate, 2019, 1, 1,
                         Era("Test", "test", date(2000, 1, 1), date(2000, 1, 2), EraType.GENERAL))

    def test_strptime_normal(self):
        result = EraDate.strptime("2020-01-01", "%Y-%m-%d")
        self.assertEqual(len(result), 2)
        self.assertSetEqual(set(result),
                            {EraDate(2020, 1, 1, ERA_DATA_GENERAL[-1]), EraDate(2020, 1, 1, ERA_DATA_COMMON[0])})

        result = EraDate.strptime("300-01-01", "%-Y-%m-%d")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], EraDate(300, 1, 1, ERA_DATA_COMMON[0]))

    def test_strptime_era_name(self):
        result = EraDate.strptime("令和-05-01", "%-K-%m-%d")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], EraDate(2019, 5, 1, ERA_DATA_GENERAL[-1]))

        result = EraDate.strptime("令和-04-01", "%-K-%m-%d")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], EraDate(2020, 4, 1, ERA_DATA_GENERAL[-1]))

    def test_strptime_kanji_date(self):
        result = EraDate.strptime("令和 五月三十一日", "%-K %-m月%-d日")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], EraDate(2019, 5, 31, ERA_DATA_GENERAL[-1]))

        result = EraDate.strptime("令和三年 4月1日", "%-K%-n年 %-m月%-d日")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], EraDate(2021, 4, 1, ERA_DATA_GENERAL[-1]))
        self.assertRaises(ValueError, EraDate.strptime, "令和元年 四月三十一日",
                          "%-K%-n年 %-m月%-d日")  # invalid date and year combination

        result = EraDate.strptime("令和三年 十二月二十四日", "%-K%-n年 %-m月%-d日")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], EraDate(2021, 12, 24, ERA_DATA_GENERAL[-1]))

        result = EraDate.strptime("西暦2023年 1月1日", "%-K%-Y年 %-m月%-d日")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], EraDate(2023, 1, 1, ERA_DATA_COMMON[0]))

    def test_strftime(self):
        era_date = EraDate(1950, 12, 24, ERA_DATA_GENERAL[-3])  # 昭和
        self.assertEqual(era_date.strftime("%-K(%-E, %-e, %-h)%-n年 %-m月%-d日 %H:%M:%S"),
                         "昭和(Shouwa, Showa, S)二十五年 十二月二十四日 00:00:00")

        era_date = EraDate(1926, 12, 24, ERA_DATA_GENERAL[-3])
        self.assertEqual(era_date.strftime("%-K(%-E, %-e, %-h)%-n年 %-m月%-d日(%-a) %H:%M:%S"),
                         "昭和(Shouwa, Showa, S)元年 十二月二十四日(金) 00:00:00")

    def test_from_date(self):
        self.assertEqual(EraDate.from_date(date(300, 1, 1)).era, ERA_DATA_COMMON[0])
        self.assertEqual(EraDate.from_date(date(2300, 1, 1)).era, ERA_DATA_GENERAL[-1])
        self.assertEqual(EraDate.from_date(date(2300, 1, 1), ERA_DATA_COMMON[0]).era, ERA_DATA_COMMON[0])

    def test_to_date(self):
        self.assertEqual(EraDate.from_date(date(300, 1, 1)).to_date(), date(300, 1, 1))
        self.assertEqual(EraDate.from_date(date(2300, 1, 1)).to_date(), date(2300, 1, 1))
        self.assertEqual(EraDate.from_date(date(2300, 1, 1), ERA_DATA_COMMON[0]).to_date(), date(2300, 1, 1))


class TestEraDateTime(unittest.TestCase):
    def test_new(self):
        self.assertWarns(RuntimeWarning, EraDateTime, 2019, 1, 1,
                         era=Era("Test", "test", date(2000, 1, 1), date(2000, 1, 2), EraType.GENERAL))
        self.assertEqual(EraDateTime(2019, 1, 1, era=ERA_DATA_COMMON[0]).era, ERA_DATA_COMMON[0])
        self.assertEqual(EraDateTime(2019, 1, 1).era, ERA_DATA_GENERAL[-2])

    def test_strptime(self):
        result = EraDateTime.strptime("令和-05-01 00:00:00", "%-K-%m-%d %H:%M:%S")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], EraDateTime(2019, 5, 1, 0, 0, 0, era=ERA_DATA_GENERAL[-1]))

        result = EraDateTime.strptime("令和-04-01 00:00:00", "%-K-%m-%d %H:%M:%S")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], EraDateTime(2020, 4, 1, 0, 0, 0, era=ERA_DATA_GENERAL[-1]))

        result = EraDateTime.strptime("令和-04-01 12:34:56.12345", "%-K-%m-%d %H:%M:%S.%f")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], EraDateTime(2020, 4, 1, 12, 34, 56, 123450, era=ERA_DATA_GENERAL[-1]))

        result = EraDateTime.strptime("昭和45年 1/1", "%-K%-y年 %m/%d")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], EraDateTime(1970, 1, 1, era=ERA_DATA_GENERAL[-3]))
        result = EraDateTime.strptime("昭和45年 1/2 UTC+0930", "%-K%-y年 %m/%d %Z%z")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0],
                         EraDateTime(1970, 1, 2,
                                     tzinfo=datetime.timezone(
                                         datetime.timedelta(seconds=9 * 3600 + 30 * 60)),
                                     era=ERA_DATA_GENERAL[-3]))
        self.assertEqual(result[0].timestamp(),
                         datetime.datetime.strptime("1970 1/2 UTC+0930", "%Y %m/%d %Z%z").timestamp())
        result = EraDateTime.strptime("昭和45年 1/1 GMT", "%-K%-y年 %m/%d %Z")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], EraDateTime(1970, 1, 1, era=ERA_DATA_GENERAL[-3]))

    def test_strftime(self):
        era_date = EraDateTime(1950, 12, 24, 12, 34, 56, era=ERA_DATA_GENERAL[-3])
        self.assertEqual(era_date.strftime("%-K(%-E, %-e, %-h)%-n年 %-m月%-d日 %H:%M:%S"),
                         "昭和(Shouwa, Showa, S)二十五年 十二月二十四日 12:34:56")

        era_date = EraDateTime(1926, 12, 24, 12, 34, 56, era=ERA_DATA_GENERAL[-3])
        self.assertEqual(era_date.strftime("%-K(%-E, %-e, %-h)%-n年 %-m月%-d日(%-a) %H:%M:%S"),
                         "昭和(Shouwa, Showa, S)元年 十二月二十四日(金) 12:34:56")


if __name__ == '__main__':
    unittest.main()
