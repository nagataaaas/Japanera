# Easy japanese era tool

Powered by [Yamato Nagata](https://twitter.com/514YJ)

[GitHub](https://github.com/nagataaaas/Japanera)
[ReadTheDocs](https://japanera.readthedocs.io/en/latest/)

All Information's source
is [Wikipedia Page](https://ja.wikipedia.org/wiki/%E5%85%83%E5%8F%B7%E4%B8%80%E8%A6%A7_(%E6%97%A5%E6%9C%AC))

```
>>> from datetime import date
>>> from japanera import EraDate

>>> today = EraDate.from_date(date.today())
>>> date(2020, 4, 16) in today.era
True

>>> "Current Japanese Era is <{}>: <{}>".format(today.era.kanji, today.era.english)
Current
Japanese
Era is <令和>: <Reiwa>

>>> "Current Date is <{}>".format(today.strftime("%-K%-y年%m月%d日"))
Current
Date is <令和05年03月07日>
```

# Installation

Install with pip

```
 $ pip install japanera
```

# How to Use

You can use `Era`, `EraDate`, `EraDateTime`.

```python
from datetime import date, datetime
from japanera import EraDate, EraDateTime, Era

print(EraDate(2023, 1, 1))
# 令和05年 01月01日
print(EraDate(2019, 4, 30))  # automatically detect border of Era
# 平成31年 04月30日
print(EraDate(2019, 5, 1))
# 令和01年 05月01日

print(EraDate.strptime("平成三十一年四月十九日", "%-K%-n年%-m月%-d日"))
# [EraDate(2019, 4, 19, Era('平成', 'Heisei', datetime.date(1989, 1, 8), datetime.date(2019, 5, 1), <EraType.GENERAL: 'general'>))]

print(EraDate.strptime("昭和25年05月01日", "%-K%-y年%m月%d日"))
# [EraDate(1950, 5, 1, Era('昭和', 'Shouwa', datetime.date(1926, 12, 25), datetime.date(1989, 1, 8), <EraType.GENERAL: 'general'>))]

era_of_1950_1_1: Era = EraDate(1950, 1, 1).era

print(era_of_1950_1_1.kanji)  # 昭和
print(era_of_1950_1_1.english)  # Shouwa
print(era_of_1950_1_1.english_vowel_shortened)  # Showa
print(era_of_1950_1_1.english_head)  # S
print(era_of_1950_1_1.since)  # datetime.date(1926, 12, 25)
print(era_of_1950_1_1.until)  # datetime.date(1989, 1, 8)
print(date(1950, 1, 1) in era_of_1950_1_1)  # True
print(date(1926, 12, 25) in era_of_1950_1_1)  # True
print(date(1989, 1, 8) in era_of_1950_1_1)  # False
print(era_of_1950_1_1.strftime(date(1950, 5, 1), "%-K%-y年 %m月%d日"))  # 昭和25年05月01日
print(era_of_1950_1_1.strftime(date(1950, 5, 1), "%-K%-n年 %-m月%-d日"))  # 昭和二十五年 五月一日
print(era_of_1950_1_1.strftime(date(1926, 12, 25), "%-K%-n年 %-m月%-d日"))  # 昭和元年 十二月二十五日  # 元 for 1st year
print(repr(era_of_1950_1_1.strptime("昭和25年05月01日", "%-K%-y年%m月%d日")))
# EraDatetime(1950, 5, 1, 0, 0, 0, 0, None, Era('昭和', 'Shouwa', datetime.date(1926, 12, 25), datetime.date(1989, 1, 8), <EraType.GENERAL: 'general'>))

era_date = EraDate(1420, 5, 6)
# or EraDate.from_date(date(1420, 5, 6))
print(era_date.era.kanji)  # 応永
print(era_date.strftime("%-K(%-E)%-Y年%m月%d日"))  # 応永(Ouei)27年05月06日

era_datetime = EraDateTime(1420, 5, 6, 12)
# or EraDateTime.from_datetime(datetime(1420, 5, 6, 12))
print(era_datetime.era.kanji)  # 応永
print(era_datetime.strftime("%-K(%-e)%-Y年%m月%d日(%-a) %H時"))  # 応永(Oei)27年05月06日(土) 12時

```

# Documentation

## Additional format codes

| Directive | Meaning                                                                                     | Example                       |
|-----------|---------------------------------------------------------------------------------------------|-------------------------------|
| `%-K`     | Era's name in Kanji                                                                         | 令和, 平成, 昭和, e.t.c.            |
| `%-E`     | Era's name in English                                                                       | Reiwa, Heisei, Shouwa, e.t.c. |
| `%-e`     | Era's name in English but redundant vowels(ou, ei) are shortened. e.g. 'Shouwa' -> 'Showa'. | Reiwa, Heisei, Showa, e.t.c.  |
| `%-h`     | Head of Era's name in English.                                                              | R, H, S, e.t.c.               |
| `%-n`     | Relative year to beginning of Era in Kanji. parse '元' as 1. Up to 99.                       | 元, 一, 二, ..., 九十九,            |
| `%-N`     | Relative year to beginning of Era in Kanji. parse '元' as 1. Up to 9999.                     | 元, 一, 二, ..., 九千九百九十九         |
| `%-y`     | Relative year to beginning of Era in Arabic number. parse '元' as 1. Up to 99.               | 元, 1, 2, ..., 99,             |
| `%-Y`     | Relative year to beginning of Era in Arabic number. parse '元' as 1. Up to 9999.             | 元, 1, 2, ..., 9999            |
| `%-m`     | Month of the date in Kanji.                                                                 | 一, 二, ..., 十二                 |
| `%-d`     | Day of the date in Kanji.                                                                   | 一, 二, ..., 三十一                |
| `%-a`     | Weekday of the date in Kanji.                                                               | 月, 火, 水, 木, 金, 土, 日           |

## `EraDate(datetime.date)`
### properties
- `instance.era`: `japanera.Era` object

> and members inherited from `datetime.date`

### `EraDate(year: int, month: Optional[int]=None, day: Optional[int]=None, era: Era=None)`

- `year`, `month`, `day`: All must be acceptable value for `datetime.date`
- `era`: instance of `japanera.Era`. If not provided, find by `japanera.parser.find_era_and_date(absolute_year=year, month=month, day=day)`

If multiple `Era` are available, The one starting latest is used. If no Japanese `Era` is found, use Common Era(`西暦`).
Return `japanera.EraDate` object.

### `EraDate().strftime(format: str)`

- `format`: format.

Directives above and `datetime.date.strftime` directives are available.

Return `str`

### `EraDate.strptime(date_string: str, format: str, allow_date_after_end_of_era: bool=False)`

- `date_string`: date string
- `format`: format.
- `allow_date_after_end_of_era`: If `True`, allow date after end of era. For example, if `allow_date_after_end_of_era`
  is `True`,
  `EraDate().strftime("昭和99年01月01日", "%-K%-y年%m月%d日")` will be valid although Showa is only 64 years long.

Directives above and `datetime.date.strftime` directives are available.
Return list of `EraDate` for earliest date in every possible Era.

### `EraDate.from_date(dt: datetime.date, era: Optional[Era]=None)`

- `dt`: instance of `datetime.date`
- `era`: instance of `japanera.Era`

Return `EraData(year=dt.year, month=dt.month, day=dt.day, era=era)`

### `EraDate.list_from_date(dt: datetime.date, eras: Optional[List[Era]]=[])`

- `dt`: instance of `datetime.date`
- `eras`: list of `japanera.Era`

Return `EraData(year=dt.year, month=dt.month, day=dt.day, era=era)` for every `era` in `eras`.
If `eras` is empty, return `EraData(year=dt.year, month=dt.month, day=dt.day, era=era)` for every `era` that includes provided date.

### `EraDate().to_date()`
Return `datetime.date` object have same time information

## `EraDateTime(EraDate, datetime.datetime)`
### properties
- `instance.era`: `japanera.Era` object

> and members inherited from `datetime.datetime`
> 
### `EraDateTime(year: int, month: Optional[int]=None, day: Optional[int]=None, hour: int=0, minute: int=0, second: int=0, microsecond: int=0, tzinfo: Optional[datetime.tzinfo]=None, *, fold: int=0, era: Optional[Era]=None)`


- `year`, `month`, `day`, `hour`, `minute`, `second`, `microsecond`, `tzinfo`, `fold`: All must be acceptable value
  for `datetime.datetime`
- `era`: instance of `japanera.Era`. If not provided, find by `japanera.parser.find_era_and_date(absolute_year=year, month=month, day=day)`

Return `japanera.EraDateTime` object.

### `EraDateTime().strftime(format: str)`

- `format`: format.

same as `EraDate().strftime(format)`

### `EraDate().from_datetime(dtt: datetime.datetime, era: Optional[Era]=None)`

- `dtt`: instance of `datetime.datetime`
- `era`: instance of `japanera.Era`

Return `EraDateTime(year=dtt.year, month=dtt.month, day=dtt.day, hour=dtt.hour, minute=dtt.minute, second=dtt.second, microsecond=dtt.microsecond, tzinfo=dtt.tzinfo, fold=dtt.fold, era=era)`

### `EraDateTime.list_from_datetime(dtt: datetime.datetime, eras: Optional[List[Era]]=None)`
- `dtt`: instance of `datetime.datetime`
- `eras`: list of `japanera.Era`

Return `EraDateTime(year=dtt.year, month=dtt.month, day=dtt.day, hour=dtt.hour, minute=dtt.minute, second=dtt.second, microsecond=dtt.microsecond, tzinfo=dtt.tzinfo, fold=dtt.fold, era=era)` for every `era` in `eras`.
If `eras` is empty, return `EraDateTime(year=dtt.year, month=dtt.month, day=dtt.day, hour=dtt.hour, minute=dtt.minute, second=dtt.second, microsecond=dtt.microsecond, tzinfo=dtt.tzinfo, fold=dtt.fold, era=era)` for every `era` that includes provided datetime.

### `EraDateTime().to_datetime()`
Return `datetime.datetime` object have same time information

## Era(kanji, english, since, until, era_type)

- `kanji` - `str`: kanji letter of era. e.g. "大正"
- `english` - `str`: english letter of pronunciation of era. e.g. "Taishou"
- `since` - `datetime.date`: start of the era. This day is included to this era.
- `until` - `datetime.date`: end of the era. This day is excluded to this era.
- `era_type` - `japanera.EraType`: Type of This Era. `EraType.COMMON`, `EraType.GENERAL`, `EraType.JIMYOUIN`  or `EraType.DAIKAKUJI`. `EraType.COMMON` is a Western style common era.

### `Era().english_vowel_shortened -> str`
Return `self.english` vowel shortened. exp. "Taishou" -> "Taisho"

### `Era().english_head -> str`
Return the first letter of `self.english`

### `Era().relative_year_to_absolute_year(relative_year: int) -> int`
Convert relative year to absolute year. e.g. `Era("大正", "Taishou", datetime.date(1912, 7, 30), datetime.date(1926, 12, 25), EraType.GENERAL).relative_year_to_absolute_year(2)` will be `1913`

### `Era().absolute_year_to_relative_year(absolute_year: int) -> int`
Convert absolute year to relative year. e.g. `Era("大正", "Taishou", datetime.date(1912, 7, 30), datetime.date(1926, 12, 25), EraType.GENERAL).absolute_year_to_relative_year(1913)` will be `2`

### `Era().calc_absolute_year(dt: datetime.date) -> int`
Return absolute year of `dt` in this era. e.g. `Era("大正", "Taishou", datetime.date(1912, 7, 30), datetime.date(1926, 12, 25), EraType.GENERAL).calc_absolute_year(datetime.date(1913, 1, 1))` will be `2`

### `Era().strftime(dtt: Union[datetime.date, datetime.datetime], format: str) -> str`
- `dtt`: instance of `datetime.date` or `datetime.datetime`
- `format`: format.

return formatted string. e.g. `Era("大正", "Taishou", datetime.date(1912, 7, 30), datetime.date(1926, 12, 25), EraType.GENERAL).strftime(datetime.date(1913, 1, 1), "%-K%-y年")` will be `"大正二年"`

### `Era().strptime(date_string: str, format: str) -> EraDateTime`
- `date_string`: date string
- `format`: format.

return `EraDateTime` object. e.g. `Era("大正", "Taishou", datetime.date(1912, 7, 30), datetime.date(1926, 12, 25), EraType.GENERAL).strptime("大正二年", "%-K%-y年")` will be `EraDateTime(1913, 1, 1, era=Era("大正", "Taishou", datetime.date(1912, 7, 30), datetime.date(1926, 12, 25), EraType.GENERAL))`
Even if `date_string` is after this era, `EraDateTime` object will be returned.

# In End
Sorry for my poor English.
I want **you** to join us and send many pull requests about Doc, code, features and more!!
