Easy japanese era tool
======================
Powered by [Yamato Nagata](https://twitter.com/514YJ)

[GitHub](https://github.com/delta114514/Japanera)
[ReadTheDocs](https://japanera.readthedocs.io/en/latest/)

All Information's source is [Wikipedia Page](https://ja.wikipedia.org/wiki/%E5%85%83%E5%8F%B7%E4%B8%80%E8%A6%A7_(%E6%97%A5%E6%9C%AC))

```python
>>> from datetime import date
>>> from japanera import Japanera, EraDate

>>> janera = Japanera()

>>> c_era = janera.era(date.today())
>>> c_era._in(date(2019, 4, 16))
True

>>> "Current Japanese Era is <{}>: <{}>".format(c_era.kanji, c_era.english)
Current Japanese Era is <平成>: <Heisei>

>>> "Current Date is <{}>".format(c_era.strftime(date(2019, 4, 16), "%-E%-O年%m月%d日"))
Current Date is <平成31年04月16日>

>>> # Or you can do same thing in this way
>>> "Current Date is <{}>".format(EraDate(2019, 4, 16).strftime("%-E%-O年%m月%d日"))
```
Instllation
===========

Install with pip
```
   $ pip install japanera
```
How to Use
=======================

You can use `Japanera`, `EraDate`, `EraDateTime`.

```python
from datetime import date
from japanera import (Japanera, EraDate, EraDateTime)

janera = Japanera()

# era of jimyouin_tou style
print(janera.jimyouin_era(date(1340, 1, 1)))    # 暦応: Ryakuou
# era of daikaku_ji style
print(janera.daikaku_era(date(1340, 1, 1)))     # 延元: Engen

print(janera.era_match("R", lambda x: x.english_head, lambda x, y: x == y))
  # [<Era 霊亀:Reiki 07/10/0715 - 28/12/0717>,
  # <Era 暦仁:Ryakunin 06/01/1239 - 20/03/1239>,
  # <Era 令和:Reiwa 01/05/2019 - None>,
  # <Era 暦応:Ryakuou 19/10/1338 - 09/06/1342>]

print(janera.strptime("平成三十一年四月十九日", "%-E%-kO年%-km月%-kd日"))
  # [datetime(2019, 4, 19, 0, 0, 0)]

print(janera.strptime("昭和25年05月01日",
       "%-E%-O年%m月%d日"))                # [datetime.datetime(1950, 5, 1, 0, 0)]

era_of_1950_1_1 = janera.era(date(1950, 1, 1))

print(era_of_1950_1_1.kanji)                    # 昭和
print(era_of_1950_1_1.english)                  # Shouwa
print(era_of_1950_1_1.english_shorten_vowel)    # Showa
print(era_of_1950_1_1.english_head)             # S
print(era_of_1950_1_1.start)                    # datetime.date(1926, 12, 25)
print(era_of_1950_1_1.end)                      # datetime.date(1989, 1, 8)
print(era_of_1950_1_1._in(date(1950, 1, 1)))    # True
print(era_of_1950_1_1.strftime(date(1950, 5, 1),
           "%-E%-O年%m月%d日"))                # 昭和25年05月01日
print(era_of_1950_1_1.strftime(date(1950, 5, 1),
           "%-E%-kO年%-km月%-kd日"))                # 昭和二十五年五月一日
print(repr(era_of_1950_1_1.strptime(
   "昭和25年05月01日", "%-E%-O年%m月%d日")))    # datetime.datetime(1950, 5, 1, 0, 0)
print(repr(era_of_1950_1_1.strptime(
   "昭和二十五年五月一日", "%-E%-kO年%-km月%-kd日")))    # datetime.datetime(1950, 5, 1, 0, 0)

eradate = EraDate(1420, 5, 6)
   # or EraDate.fromdate(datetime.date(1420, 5, 6))

print(eradate.era.kanji)                        # 応永
print(eradate.strftime("%-E%-O年%m月%d日"))     # 応永27年05月06日

eradatetime = EraDateTime(1420, 5, 6)
   # or EraDateTime.fromdatetime(datetime.datetime(1420, 5, 6))

print(eradatetime.era.kanji)                    # 応永
print(eradatetime.strftime("%-E%-O年%m月%d日"))  # 応永27年05月06日

```
Documentation
=============

`Japanera(primary="daikakuji")`
======================================
- `primary`: which style do you prefer want to get `daikakuji` style or `jimyouin` style. This will be set to `self.primary` Default: `"daikakuji"`

`Japanera().era(dt, use_chris=True)`
-------------------------------------------
- `dt`: `datetime.date`, `datetime.datetime`, `japanera.EraDate` or `japanera.EraDateTime`.
- `use_chris`: `bool`, If True, return `self.christ_ad` if there is no `japanera.Era` match

Returns one matched `japanera.Era` object with considering `self.primary`

`Japanera().era_match(value, key=lambda x: x, cmp=lambda x, y: x._in(y), error="warn")`
----------------------------------------------------------------------------------------------
Return all `japanera.Era` objects stored in `self.era_common`, `self.era_daikakuji` or `self.era_jimyouin` which `cmp(key(Era), value)` is `True`.

if `key` is not provided, `key` is `lambda x: x`

if `cmp` is not provided, `cmp` is `lambda x, y: x._in(y)`

`error` sets error level
   - `"ignore"`: ignore all errors occurred while running compare
   - `"warn"`: just warn error - default
   - `"raise"`: raise any errors

Default, this will return all `japanera.Era` which contains given `value` (which must be instance of `datetime.date`) in them.

`Japanera().strftime(dt, fmt, _type=None, allow_before=False, use_chris=True)`
-------------------------------------------------------------------------------------

- `dt`: instance of `datetime.date`.
- `fmt`: format.
- `allow_before`: object can be converted to `bool`. If it's `True` and the given `dt` if before than `self,start`, `%-o` and `%-O` will be `"Unknown"`. If `False`, raise an `ValueError` Default: `False`
- `use_chris`: `bool`, If `True`, use `self.christ_ad` if there is no `japanera.Era` match. Default: `True`


**format**

- `%-E`: Kanji era name
- `%-e`: Alphabet era name vowel shortened
- `%-A`: Alphabet era name
- `%-a`: First letter of alphabet era name
- `%-o`: Two digit year of corresponding era
- `%-O`: Two digit year of corresponding era. But return "元" for the first year
- `%-ko`: Two digit year of corresponding era in Kanji
- `%-kO`: Two digit year of corresponding era in Kanji. But return "元" for the first year
- `%-km`: Month of date in Kanji
- `%-kd`: Day of date in Kanji
- and `datetime.datetime.strftime`'s format


`Japanera().strptime(_str, fmt)`
-------------------------------------------------------------------------------------

Return list of all `datetime.datetime` that returns `_str` with `fmt` by running `Era().strftime(RESULT, fmt)`

    *return list is not the always only one value. There is possibility you get multiple.*


`Japanera().daikaku_era(dt, use_chris=True)`
---------------------------------------------------
- `dt`: instance of `datetime.date`.
- `use_chris`: `bool`. If `True`, return `self.christ_ad` if there is no `japanera.Era`

Return matched `japanera.Era` in `Japanera.era_common_daikakuji`

`Japanera().jimyouin_era(dt, use_chris=True)`
---------------------------------------------------
- `dt`: instance of `datetime.date`.
- `use_chris`: `bool`. If `True`, return `self.christ_ad` if there is no `japanera.Era`

Return matched `japanera.Era` in `Japanera.era_common_jimyouin`

`EraDate(year, month=None, day=None, era=None, use_chris=True)`
======================================================================
- `year`, `month`, `day`: All must be acceptable value for `datetime.date`
- `era`: instance of `japanera.Era`. If not provided, find by `japanera.Japanera(self, use_chris)`
- `use_chris`: `bool`

Return `japanera.EraDate` object.

`EraDate().strftime(fmt, allow_before=False)`
----------------------------------------------------
- `fmt`: format.
- `allow_before`: object can be converted to `bool`. If it's `True` and the given `dt` if before than `self,start`, `%-o` and `%-O` will be `"Unknown"`. If `False`, raise an `ValueError` Default: `False`

**format**

- `%-E`: Kanji era name
- `%-e`: Alphabet era name vowel shortened
- `%-A`: Alphabet era name
- `%-a`: First letter of alphabet era name
- `%-o`: Two digit year of corresponding era
- `%-O`: Two digit year of corresponding era. But return "元" for the first year
- `%-ko`: Two digit year of corresponding era in Kanji
- `%-kO`: Two digit year of corresponding era in Kanji. But return "元" for the first year
- `%-km`: Month of date in Kanji
- `%-kd`: Day of date in Kanji
- and `datetime.date.strftime`'s format

`EraDate().fromdate(dt, era=None, use_chris=True)`
---------------------------------------------------------
- `dt`: instance of `datetime.date`
- `era`: instance of `japanera.Era`
- `use_chris`: `bool`

Return `EraData(year=dt.year, month=dt.month, day=dt.day, era=era, use_chris=use_chris)`

`EraDate().todate()`
---------------------------
Return `datetime.date` object have same time information

`EraDateTime(year, month=None, day=None, hour=0, minute=0, second=0, microsecond=0, tzinfo=None, *, fold=0, era=None, use_chris=True)`
=============================================================================================================================================
- `year`, `month`, `day`, `hour`, `minute`, `second`, `microsecond`, `tzinfo`, `fold`: All must be acceptable value for `datetime.date`
- `era`: instance of `japanera.Era`. If not provided, find by `japanera.Japanera(self, use_chris)`
- `use_chris`: `bool`

Return `japanera.EraDateTime` object.

`EraDateTime().strftime(fmt, allow_before=False)`
--------------------------------------------------------
- `fmt`: format.
- `allow_before`: object can be converted to `bool`. If it's `True` and the given `dt` if before than `self,start`, `%-o` and `%-O` will be `"Unknown"`. If `False`, raise an `ValueError` Default: `False`

**format**

- `%-E`: Kanji era name
- `%-e`: Alphabet era name vowel shortened
- `%-A`: Alphabet era name
- `%-a`: First letter of alphabet era name
- `%-o`: Two digit year of corresponding era
- `%-O`: Two digit year of corresponding era. But return "元" for the first year
- `%-ko`: Two digit year of corresponding era in Kanji
- `%-kO`: Two digit year of corresponding era in Kanji. But return "元" for the first year
- `%-km`: Month of date in Kanji
- `%-kd`: Day of date in Kanji
- and `datetime.datetime.strftime`'s format

`EraDate().fromdatetime(dtt, era=None, use_chris=True)`
--------------------------------------------------------------
- `dtt`: instance of `datetime.datetime`
- `era`: instance of `japanera.Era`
- `use_chris`: `bool`

Return `EraDateTime(year=dtt.year, month=dtt.month, day=dtt.day, hour=dtt.hour, minute=dtt.minute, second=dtt.second, microsecond=dtt.microsecond, tzinfo=dtt.tzinfo, fold=dtt.fold, era=era, use_chris=use_chris)`

`EraDateTime().todatetime()`
-----------------------------------
Return `datetime.datetime` object have same time information

`Era(kanji, english, start, end, _type)`
===============================================
- `kanji` - `str`: kanji letter of era. exp. "大正"
- `english` - `str`: english letter of pronunciation of era. exp. "Taishou"
- `start` - `datetime.date`: start of the era. This day is included to this era.
- `datetime.date`: end of the era. This day is excluded to this era.
- `_type` - `str`: Type of This Era. `"common"`, `"daikakuji"`, `"jimyouin"`  or `"christian"`

`Era().english_shorten_vowel`
------------------------------------
Return `self.english` vowel shortened. exp. "Taishou" -> "Taisho"

`Era().english_head`
--------------------------
Return the first letter of `self.english`

`Era()._in(dt)`
----------------------
Return `dt` object is in between `self.start` and `self.end`. (`self.start` is included, `self.end` is excluded)

`Era().is_after(other)`
------------------------------
Return if other(instance of `datetime.date`) is before than `self.start` or other(instance of `japanera.Era`)'s `end` is before than `self.start`

`Era().is_before(other)`
------------------------------
Return if other(instance of `datetime.date`) is after than `self.end` or other(instance of `japanera.Era`)'s `start` is after than `self.end`


`Era().strftime(dt, fmt, allow_before=False)`
--------------------------------------------------------
- `dt`: instance of `datetime.date`
- `fmt`: format.
- `allow_before`: object can be converted to `bool`. If it's `True` and the given `dt` if before than `self,start`, `%-o` and `%-O` will be `"Unknown"`. If `False`, raise an `ValueError` Default: `False`

**format**

- `%-E`: Kanji era name
- `%-e`: Alphabet era name vowel shortened
- `%-A`: Alphabet era name
- `%-a`: First letter of alphabet era name
- `%-o`: Two digit year of corresponding era
- `%-O`: Two digit year of corresponding era. But return "元" for the first year
- `%-ko`: Two digit year of corresponding era in Kanji
- `%-kO`: Two digit year of corresponding era in Kanji. But return "元" for the first year
- `%-km`: Month of date in Kanji
- `%-kd`: Day of date in Kanji
- and `datetime.datetime.strftime`'s format

`Era().strptime(_str, fmt)`
----------------------------------
Return `datetime.datetime` that returns `_str` with `fmt` by running `Era().strftime(RESULT, fmt)`

In End
======
Sorry for my poor English.
I want **you** to join us and send many pull requests about Doc, code, features and more!!
