# -*- coding: utf-8 -*-
import datetime
import re
from typing import Optional, List, Union
from warnings import warn

from kanjize import number2kanji

from .era_data import EraType, _ERA_DATA_COMMON, _ERA_DATA_GENERAL, _ERA_DATA_DAIKAKUJI, _ERA_DATA_JIMYOUIN
from .parser import _strptime, find_era_and_date, _set_era_data


class Era:
    def __init__(self, kanji: Optional[str], english: Optional[str], since: datetime.date,
                 until: Optional[datetime.date], era_type: EraType):
        self._kanji = kanji
        self._english = english
        self.since = since
        self.until = until
        self.era_type = era_type

    @property
    def kanji(self) -> str:
        return self._kanji or "不明"

    @property
    def english(self) -> str:
        return self._english or "Unknown"

    @property
    def english_vowel_shortened(self) -> str:
        return self.english.lower().replace("ou", "o").replace("uu", "u").title()  # much faster than regex

    @property
    def english_head(self) -> str:
        return self.english[0]

    def relative_year_to_absolute_year(self, relative_year: int) -> int:
        return self.since.year + relative_year - 1

    def absolute_year_to_relative_year(self, absolute_year: int) -> int:
        return absolute_year - self.since.year + 1

    def calc_relative_year(self, date: datetime.date) -> int:
        return self.absolute_year_to_relative_year(date.year)

    def strftime(self, dtt: Union[datetime.date, datetime.datetime], format: str) -> str:
        relative_year = dtt.year - self.since.year + 1
        rep = {"%-K": self.kanji, "%-E": self.english, "%-e": self.english_vowel_shortened,
               "%-h": self.english_head,
               "%-n": "元" if relative_year == 1 else number2kanji(relative_year % 100),
               "%-N": "元" if relative_year == 1 else number2kanji(relative_year),
               "%-y": "{:02}".format(relative_year % 100),
               "%-Y": str(relative_year),
               "%-m": number2kanji(dtt.month),
               "%-d": number2kanji(dtt.day),
               "%-a": '月火水木金土日'[dtt.weekday()]}

        rep = dict((re.escape(k), str(v)) for k, v in rep.items())
        pattern = re.compile("|".join(rep.keys()))
        return datetime.datetime.strftime(dtt, pattern.sub(lambda m: rep[re.escape(m.group(0))], format))

    def strptime(self, date_string: str, format: str) -> "EraDateTime":
        (era_kanji, era_english, era_english_vowel_shortened, era_head, relative_year), \
        (year, month, day, hour, minute, second, weekday, julian, tz, tzname, gmtoff), \
        fraction, gmtoff_fraction = _strptime(date_string, format)
        era_and_dates = find_era_and_date(self.kanji, self.english, None, None, year,
                                          relative_year, month, day, True)
        if not era_and_dates:
            raise ValueError("EraDate not found")

        tz = None
        if gmtoff is not None:
            tzdelta = datetime.timedelta(seconds=gmtoff, microseconds=gmtoff_fraction)
            if tzname:
                tz = datetime.timezone(tzdelta, tzname)
            else:
                tz = datetime.timezone(tzdelta)
        for era, date in era_and_dates:
            if era == self:
                return EraDateTime(date.year, date.month, date.day, hour, minute, second, fraction, tzinfo=tz, era=self)

    def __gt__(self, other):
        since = self.since or datetime.date.min
        if isinstance(other, datetime.datetime):
            return since > other.date()
        elif isinstance(other, datetime.date):
            return since > other
        elif isinstance(other, Era):
            return since > other.since
        raise TypeError(f"unsupported operand type(s) for >: '{type(self).__name__}' and '{type(other).__name__}'")

    def __lt__(self, other):
        until = self.until or datetime.date.max
        if isinstance(other, datetime.datetime):
            return until <= other.date()
        elif isinstance(other, datetime.date):
            return until <= other
        elif isinstance(other, Era):
            return until <= other.since
        raise TypeError(f"unsupported operand type(s) for <: '{type(self).__name__}' and '{type(other).__name__}'")

    def __ge__(self, other):
        since = self.since or datetime.date.min
        if isinstance(other, datetime.datetime):
            return since >= other.date()
        elif isinstance(other, datetime.date):
            return since >= other
        elif isinstance(other, Era):
            return since >= other.since
        raise TypeError(f"unsupported operand type(s) for >=: '{type(self).__name__}' and '{type(other).__name__}'")

    def __le__(self, other):
        return self < other

    def __contains__(self, item: Union[datetime.date, datetime.datetime]):
        since = self.since or datetime.date.min
        until = self.until or datetime.date.max
        if isinstance(item, datetime.datetime):
            return since <= item.date() < until
        elif isinstance(item, datetime.date):
            return since <= item < until
        else:
            raise TypeError(f"unsupported operand type(s) for in: '{type(self).__name__}' and '{type(item).__name__}'")

    def __eq__(self, other):
        if not isinstance(other, Era):
            return False
        return self.kanji == other.kanji and self.english == other.english and self.since == other.since and self.until == other.until and self.era_type == other.era_type

    def __hash__(self):
        return hash((self.kanji, self.english, self.since, self.until, self.era_type))

    def __repr__(self):
        return "Era({!r}, {!r}, {!r}, {!r}, {!r})".format(self.kanji, self.english, self.since, self.until,
                                                          self.era_type)


ERA_DATA_COMMON = [Era(kanji, english, since, until, _type) for kanji, english, since, until, _type in
                   _ERA_DATA_COMMON]
ERA_DATA_GENERAL = [Era(kanji, english, since, until, _type) for kanji, english, since, until, _type in
                    _ERA_DATA_GENERAL]
ERA_DATA_DAIKAKUJI = [Era(kanji, english, since, until, _type) for kanji, english, since, until, _type in
                      _ERA_DATA_DAIKAKUJI]
ERA_DATA_JIMYOUIN = [Era(kanji, english, since, until, _type) for kanji, english, since, until, _type in
                     _ERA_DATA_JIMYOUIN]

_set_era_data(ERA_DATA_COMMON, ERA_DATA_GENERAL, ERA_DATA_DAIKAKUJI, ERA_DATA_JIMYOUIN)


class EraDate(datetime.date):
    def __new__(cls, year: int, month: Optional[int] = None, day: Optional[int] = None, era: Optional[Era] = None):
        self = super().__new__(cls, year, month, day)
        if era:
            self.era = era
        else:
            result = find_era_and_date(absolute_year=year, month=month, day=day)
            if not result:
                raise ValueError("Era not found")  # Maybe this can't be happened because of Common Era
            self.era = result[-1][0]
        if self not in self.era:
            warn("Date is not in era", RuntimeWarning)
        return self

    @classmethod
    def strptime(cls, date_string: str, format: str, allow_date_after_end_of_era=False) -> List["EraDate"]:
        (era_kanji, era_english, era_english_vowel_shortened, era_head, relative_year), \
        (year, month, day, hour, minute, second, weekday, julian, tz, tzname, gmtoff), \
        fraction, gmtoff_fraction = _strptime(date_string, format)
        era_and_dates = find_era_and_date(era_kanji, era_english, era_english_vowel_shortened, era_head, year,
                                          relative_year, month, day, allow_date_after_end_of_era)
        if not era_and_dates:
            raise ValueError("EraDate not found")
        return [cls.from_date(date, era=era) for era, date in era_and_dates]

    def strftime(self, format: str) -> str:
        """
        %-K: Kanji era name
        %-E: English era name
        %-e: English era name vowel shortened
        %-h: Head of english era name
        %-n: Up to two digit relative year of corresponding era in Kanji. But return "元" for the first year
        %-N: Up to four digit relative year of corresponding era in Kanji. But return "元" for the first year
        %-y: Two digit relative year of corresponding era.
        %-Y: Up to four digit relative year of corresponding era.
        %-m: Month of date in Kanji
        %-d: Day of date in Kanji
        %-a: Weekday of date in Kanji
        + datetime.strftime's format
        """
        relative_year = self.year - self.era.since.year + 1
        rep = {"%-K": self.era.kanji, "%-E": self.era.english, "%-e": self.era.english_vowel_shortened,
               "%-h": self.era.english_head,
               "%-n": "元" if relative_year == 1 else number2kanji(relative_year % 100),
               "%-N": "元" if relative_year == 1 else number2kanji(relative_year),
               "%-y": "{:02}".format(relative_year % 100),
               "%-Y": str(relative_year),
               "%-m": number2kanji(self.month),
               "%-d": number2kanji(self.day),
               "%-a": '月火水木金土日'[self.weekday()]}

        rep = dict((re.escape(k), str(v)) for k, v in rep.items())
        pattern = re.compile("|".join(rep.keys()))
        return datetime.datetime.strftime(self, pattern.sub(lambda m: rep[re.escape(m.group(0))], format))

    @classmethod
    def from_date(cls, dt: datetime.date, era: Optional[Era] = None) -> "EraDate":
        if not era:
            result = find_era_and_date(absolute_year=dt.year, month=dt.month, day=dt.day)
            if not result:
                raise ValueError("Era not found")  # Maybe this can't be happened because of Common Era
            era = result[-1][0]
        return cls(year=dt.year, month=dt.month, day=dt.day, era=era)

    @classmethod
    def list_from_date(cls, dt: datetime.date, eras: Optional[List[Era]] = None) -> List["EraDate"]:
        if not eras:
            result = find_era_and_date(absolute_year=dt.year, month=dt.month, day=dt.day)
            if not result:
                raise ValueError("Era not found")  # Maybe this can't be happened because of Common Era
            eras = [era for era, date in result]
        return [cls(year=dt.year, month=dt.month, day=dt.day, era=era) for era in eras]

    def to_date(self) -> datetime.date:
        return datetime.date(year=self.year, month=self.month, day=self.day)

    def __hash__(self):
        return hash((self.year, self.month, self.day, self.era))

    def __eq__(self, other):
        if isinstance(other, EraDate):
            return self.year == other.year and self.month == other.month and self.day == other.day and self.era == other.era
        else:
            return super().__eq__(other)

    def __repr__(self):
        return "EraDate({!r}, {!r}, {!r}, {!r})".format(self.year, self.month, self.day, self.era)

    def __str__(self):
        return self.strftime("%-K%-y年 %m月%d日")


class EraDateTime(EraDate, datetime.datetime):
    def __new__(cls, year: int, month: Optional[int] = None, day: Optional[int] = None, hour: Optional[int] = 0,
                minute: int = 0, second: int = 0, microsecond: int = 0, tzinfo: Optional[datetime.tzinfo] = None, *,
                fold: int = 0, era: Optional[Era] = None):
        self = datetime.datetime.__new__(cls, year=year, month=month, day=day, hour=hour, minute=minute, second=second,
                                         microsecond=microsecond, tzinfo=tzinfo, fold=fold)

        if era:
            self.era = era
        else:
            result = find_era_and_date(absolute_year=year, month=month, day=day)
            if not result:
                raise ValueError("Era not found")  # Maybe this can't be happened because of Common Era
            self.era = result[-1][0]
        if self not in self.era:
            warn("Date is not in era", RuntimeWarning)
        return self

    @classmethod
    def strptime(cls, date_string: str, format: str, allow_date_after_end_of_era=False) -> List["EraDateTime"]:
        (era_kanji, era_english, era_english_vowel_shortened, era_head, relative_year), \
        (year, month, day, hour, minute, second, weekday, julian, tz, tzname, gmtoff), \
        fraction, gmtoff_fraction = _strptime(date_string, format)
        era_and_dates = find_era_and_date(era_kanji, era_english, era_english_vowel_shortened, era_head, year,
                                          relative_year, month, day, allow_date_after_end_of_era)
        if not era_and_dates:
            raise ValueError("EraDate not found")

        tz = None
        if gmtoff is not None:
            tzdelta = datetime.timedelta(seconds=gmtoff, microseconds=gmtoff_fraction)
            if tzname:
                tz = datetime.timezone(tzdelta, tzname)
            else:
                tz = datetime.timezone(tzdelta)
        return [cls(date.year, date.month, date.day, hour, minute, second, fraction, tzinfo=tz, era=era) for era, date
                in era_and_dates]

    @classmethod
    def list_from_datetime(cls, dtt: datetime.datetime, eras: Optional[List[Era]] = None) -> List["EraDateTime"]:
        if not eras:
            result = find_era_and_date(absolute_year=dtt.year, month=dtt.month, day=dtt.day)
            if not result:
                raise ValueError("Era not found")  # Maybe this can't be happened because of Common Era
            eras = [era for era, date in result]
        return [cls(year=dtt.year, month=dtt.month, day=dtt.day, hour=dtt.hour, minute=dtt.minute, second=dtt.second,
                    microsecond=dtt.microsecond, tzinfo=dtt.tzinfo, fold=dtt.fold, era=era) for era in eras]

    @classmethod
    def from_datetime(cls, dtt: datetime.datetime, era: Optional[Era] = None) -> "EraDateTime":
        if not era:
            result = find_era_and_date(absolute_year=dtt.year, month=dtt.month, day=dtt.day)
            if not result:
                raise ValueError("Era not found")  # Maybe this can't be happened because of Common Era
            era = result[-1][0]
        return cls(year=dtt.year, month=dtt.month, day=dtt.day, hour=dtt.hour, minute=dtt.minute, second=dtt.second,
                   microsecond=dtt.microsecond, tzinfo=dtt.tzinfo, fold=dtt.fold, era=era)

    def to_datetime(self) -> datetime.datetime:
        return datetime.datetime(year=self.year, month=self.month, day=self.day, hour=self.hour, minute=self.minute,
                                 second=self.second, microsecond=self.microsecond, tzinfo=self.tzinfo, fold=self.fold)

    def __eq__(self, other):
        if isinstance(other, EraDateTime):
            return self.year == other.year and self.month == other.month and self.day == other.day and self.hour == \
                   other.hour and self.minute == other.minute and self.second == other.second and self.microsecond == \
                   other.microsecond and self.tzinfo == other.tzinfo and self.era == other.era
        else:
            return super().__eq__(other)

    def __hash__(self):
        return hash((
            self.year, self.month, self.day, self.hour, self.minute, self.second, self.microsecond, self.tzinfo,
            self.era))

    def __repr__(self):
        return "EraDatetime({!r}, {!r}, {!r}, {!r}, {!r}, {!r}, {!r}, {!r}, {!r})".format(self.year, self.month,
                                                                                          self.day, self.hour,
                                                                                          self.minute, self.second,
                                                                                          self.microsecond, self.tzinfo,
                                                                                          self.era)

    def __str__(self):
        return self.strftime("%-K%-y年 %m月%d日 %H時%M分%S秒")
