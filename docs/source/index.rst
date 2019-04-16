.. -*- coding: utf-8; -*-

.. Japanera documentation master file, created by
   sphinx-quickstart on Sun Feb 24 01:43:54 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Easy japanese era tool
======================
|image1| |image2|

.. |image1| image:: https://img.shields.io/pypi/v/japanera.svg
   :target: https://pypi.org/project/japanera/
.. |image2| image:: https://img.shields.io/pypi/l/japanera.svg
   :target: https://pypi.org/project/japanera/

Powered by `Yamato Nagata <https://twitter.com/514YJ>`_.

`GitHub <https://github.com/delta114514/Japanera>`_

.. code:: python

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

.. contents::
   :local:
   :backlinks: none

Instllation
===========

Install with pip::

   $ pip install japanera

How to Use
=======================

You can use :code:`Japanera`, :code:`EraDate`, :code:`EraDateTime`.

.. code:: python

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
   print(repr(era_of_1950_1_1.strptime(
       "昭和25年05月01日", "%-E%-O年%m月%d日")))    # datetime.datetime(1950, 5, 1, 0, 0)

   eradate = EraDate(1420, 5, 6)
       # or EraDate.fromdate(datetime.date(1420, 5, 6))

   print(eradate.era.kanji)                        # 応永
   print(eradate.strftime("%-E%-O年%m月%d日"))     # 応永27年05月06日

   eradatetime = EraDateTime(1420, 5, 6)
       # or EraDateTime.fromdatetime(datetime.datetime(1420, 5, 6))

   print(eradatetime.era.kanji)                    # 応永
   print(eradatetime.strftime("%-E%-O年%m月%d日"))  # 応永27年05月06日

Documentation
=============

:code:`Japanera(primary="daikakuji")`
======================================
- :code:`primary`: which style do you prefer want to get :code:`daikakuji` style or :code:`jimyouin` style. This will be set to :code:`self.primary` Default: :code:`"daikakuji"`

:code:`Japanera().era(dt, use_chris=True)`
-------------------------------------------
- :code:`dt`: :code:`datetime.date`, :code:`datetime.datetime`, :code:`japanera.EraDate` or :code:`japanera.EraDateTime`.
- :code:`use_chris`: :code:`bool`, If True, return :code:`self.christ_ad` if there is no :code:`japanera.Era` match

Returns one matched :code:`japanera.Era` object with considering :code:`self.primary`

:code:`Japanera().era_match(value, key=lambda x: x, cmp=lambda x, y: x._in(y), error="warn")`
----------------------------------------------------------------------------------------------
Return all :code:`japanera.Era` objects stored in :code:`self.era_common`, :code:`self.era_daikakuji` or :code:`self.era_jimyouin` which :code:`cmp(key(Era), value)` is :code:`True`.

if :code:`key` is not provided, :code:`key` is :code:`lambda x: x`

if :code:`cmp` is not provided, :code:`cmp` is :code:`lambda x, y: x._in(y)`

:code:`error` sets error level
   - :code:`"ignore"`: ignore all errors occurred while running compare
   - :code:`"warn"`: just warn error - default
   - :code:`"raise"`: raise any errors

Default, this will return all :code:`japanera.Era` which contains given :code:`value` (which must be instance of :code:`datetime.date`) in them.

:code:`Japanera().strftime(dt, fmt, _type=None, allow_before=False, use_chris=True)`
-------------------------------------------------------------------------------------

- :code:`dt`: instance of :code:`datetime.date`.
- :code:`fmt`: format.
- :code:`allow_before`: object can be converted to :code:`bool`. If it's :code:`True` and the given :code:`dt` if before than :code:`self,start`, :code:`%-o` and :code:`%-O` will be :code:`"Unknown"`. If :code:`False`, raise an :code:`ValueError` Default: :code:`False`
- :code:`use_chris`: :code:`bool`, If :code:`True`, use :code:`self.christ_ad` if there is no :code:`japanera.Era` match. Default: :code:`True`


**format**

- :code:`%-E`: Kanji era name
- :code:`%-e`: Alphabet era name vowel shortened
- :code:`%-A`: Alphabet era name
- :code:`%-a`: First letter of alphabet era name
- :code:`%-o`: Two digit year of corresponding era
- :code:`%-O`: Two digit year of corresponding era. But return "元" for the first year
- and :code:`datetime.datetime.strftime`'s format

:code:`Japanera().strptime(_str, fmt)`
-------------------------------------------------------------------------------------

Return list of all :code:`datetime.datetime` that returns :code:`_str` with :code:`fmt` by running :code:`Era().strftime(RESULT, fmt)`

    *return list is not the always only one value. There is possibility you get multiple.*

:code:`Japanera().daikaku_era(dt, use_chris=True)`
---------------------------------------------------
- :code:`dt`: instance of :code:`datetime.date`.
- :code:`use_chris`: :code:`bool`. If :code:`True`, return :code:`self.christ_ad` if there is no :code:`japanera.Era`

Return matched :code:`japanera.Era` in :code:`Japanera.era_common_daikakuji`

:code:`Japanera().jimyouin_era(dt, use_chris=True)`
---------------------------------------------------
- :code:`dt`: instance of :code:`datetime.date`.
- :code:`use_chris`: :code:`bool`. If :code:`True`, return :code:`self.christ_ad` if there is no :code:`japanera.Era`

Return matched :code:`japanera.Era` in :code:`Japanera.era_common_jimyouin`

:code:`EraDate(year, month=None, day=None, era=None, use_chris=True)`
======================================================================
- :code:`year`, :code:`month`, :code:`day`: All must be acceptable value for :code:`datetime.date`
- :code:`era`: instance of :code:`japanera.Era`. If not provided, find by :code:`japanera.Japanera(self, use_chris)`
- :code:`use_chris`: :code:`bool`

Return :code:`japanera.EraDate` object.

:code:`EraDate().strftime(fmt, allow_before=False)`
----------------------------------------------------
- :code:`fmt`: format.
- :code:`allow_before`: object can be converted to :code:`bool`. If it's :code:`True` and the given :code:`dt` if before than :code:`self,start`, :code:`%-o` and :code:`%-O` will be :code:`"Unknown"`. If :code:`False`, raise an :code:`ValueError` Default: :code:`False`

**format**

- :code:`%-E`: Kanji era name
- :code:`%-e`: Alphabet era name vowel shortened
- :code:`%-A`: Alphabet era name
- :code:`%-a`: First letter of alphabet era name
- :code:`%-o`: Two digit year of corresponding era
- :code:`%-O`: Two digit year of corresponding era. But return "元" for the first year
- and :code:`datetime.date.strftime`'s format

:code:`EraDate().fromdate(dt, era=None, use_chris=True)`
---------------------------------------------------------
- :code:`dt`: instance of :code:`datetime.date`
- :code:`era`: instance of :code:`japanera.Era`
- :code:`use_chris`: :code:`bool`

Return :code:`EraData(year=dt.year, month=dt.month, day=dt.day, era=era, use_chris=use_chris)`

:code:`EraDate().todate()`
---------------------------
Return :code:`datetime.date` object have same time information

:code:`EraDateTime(year, month=None, day=None, hour=0, minute=0, second=0, microsecond=0, tzinfo=None, *, fold=0, era=None, use_chris=True)`
=============================================================================================================================================
- :code:`year`, :code:`month`, :code:`day`, :code:`hour`, :code:`minute`, :code:`second`, :code:`microsecond`, :code:`tzinfo`, :code:`fold`: All must be acceptable value for :code:`datetime.date`
- :code:`era`: instance of :code:`japanera.Era`. If not provided, find by :code:`japanera.Japanera(self, use_chris)`
- :code:`use_chris`: :code:`bool`

Return :code:`japanera.EraDateTime` object.

:code:`EraDateTime().strftime(fmt, allow_before=False)`
--------------------------------------------------------
- :code:`fmt`: format.
- :code:`allow_before`: object can be converted to :code:`bool`. If it's :code:`True` and the given :code:`dt` if before than :code:`self,start`, :code:`%-o` and :code:`%-O` will be :code:`"Unknown"`. If :code:`False`, raise an :code:`ValueError` Default: :code:`False`

**format**

- :code:`%-E`: Kanji era name
- :code:`%-e`: Alphabet era name vowel shortened
- :code:`%-A`: Alphabet era name
- :code:`%-a`: First letter of alphabet era name
- :code:`%-o`: Two digit year of corresponding era
- :code:`%-O`: Two digit year of corresponding era. But return "元" for the first year
- and :code:`datetime.datetime.strftime`'s format

:code:`EraDate().fromdatetime(dtt, era=None, use_chris=True)`
--------------------------------------------------------------
- :code:`dtt`: instance of :code:`datetime.datetime`
- :code:`era`: instance of :code:`japanera.Era`
- :code:`use_chris`: :code:`bool`

Return :code:`EraDateTime(year=dtt.year, month=dtt.month, day=dtt.day, hour=dtt.hour, minute=dtt.minute, second=dtt.second, microsecond=dtt.microsecond, tzinfo=dtt.tzinfo, fold=dtt.fold, era=era, use_chris=use_chris)`

:code:`EraDateTime().todatetime()`
-----------------------------------
Return :code:`datetime.datetime` object have same time information

:code:`Era(kanji, english, start, end, _type)`
===============================================
- :code:`kanji` - :code:`str`: kanji letter of era. exp. "大正"
- :code:`english` - :code:`str`: english letter of pronunciation of era. exp. "Taishou"
- :code:`start` - :code:`datetime.date`: start of the era. This day is included to this era.
- :code:`datetime.date`: end of the era. This day is excluded to this era.
- :code:`_type` - :code:`str`: Type of This Era. :code:`"common"`, :code:`"daikakuji"`, :code:`"jimyouin"`  or :code:`"christian"`

:code:`Era().english_shorten_vowel`
------------------------------------
Return :code:`self.english` vowel shortened. exp. "Taishou" -> "Taisho"

:code:`Era().english_head`
--------------------------
Return the first letter of :code:`self.english`

:code:`Era()._in(dt)`
----------------------
Return :code:`dt` object is in between :code:`self.start` and :code:`self.end`. (:code:`self.start` is included, :code:`self.end` is excluded)

:code:`Era().is_after(other)`
------------------------------
Return if other(instance of :code:`datetime.date`) is before than :code:`self.start` or other(instance of :code:`japanera.Era`)'s :code:`end` is before than :code:`self.start`

:code:`Era().is_before(other)`
------------------------------
Return if other(instance of :code:`datetime.date`) is after than :code:`self.end` or other(instance of :code:`japanera.Era`)'s :code:`start` is after than :code:`self.end`


:code:`Era().strftime(dt, fmt, allow_before=False)`
--------------------------------------------------------
- :code:`dt`: instance of :code:`datetime.date`
- :code:`fmt`: format.
- :code:`allow_before`: object can be converted to :code:`bool`. If it's :code:`True` and the given :code:`dt` if before than :code:`self,start`, :code:`%-o` and :code:`%-O` will be :code:`"Unknown"`. If :code:`False`, raise an :code:`ValueError` Default: :code:`False`

**format**

- :code:`%-E`: Kanji era name
- :code:`%-e`: Alphabet era name vowel shortened
- :code:`%-A`: Alphabet era name
- :code:`%-a`: First letter of alphabet era name
- :code:`%-o`: Two digit year of corresponding era
- :code:`%-O`: Two digit year of corresponding era. But return "元" for the first year
- and :code:`datetime.datetime.strftime`'s format

:code:`Era().strptime(_str, fmt)`
----------------------------------
Return :code:`datetime.datetime` that returns :code:`_str` with :code:`fmt` by running :code:`Era().strftime(RESULT, fmt)`

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


In End
======
Sorry for my poor English.
I want **you** to join us and send many pull requests about Doc, code, features and more!!
