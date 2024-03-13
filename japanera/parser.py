import calendar
import datetime
import time
from _strptime import (_CACHE_MAX_SIZE, IGNORECASE, LocaleTime, _cache_lock,
                       _calc_julian_from_U_or_W, _getlang, _regex_cache,
                       re_compile, re_escape)
from calendar import monthrange
from collections import defaultdict
from typing import List, Optional, Set, Tuple

from kanjize import kanji2number

_ERA_DATA_COMMON, _ERA_DATA_GENERAL, _ERA_DATA_DAIKAKUJI, _ERA_DATA_JIMYOUIN = [], [], [], []

_era_kanji_dict = defaultdict(set)
_era_alphabet_dict = defaultdict(set)
_era_alphabet_vowel_shortened_dict = defaultdict(set)
_era_alphabet_head_dict = defaultdict(set)

_JAPANERA_TimeRE_cache = None


def _set_era_data(era_data_common, era_data_general, era_data_daikakuji, era_data_jimyouin):
    global _ERA_DATA_COMMON, _ERA_DATA_GENERAL, _ERA_DATA_DAIKAKUJI, _ERA_DATA_JIMYOUIN
    _ERA_DATA_COMMON = era_data_common
    _ERA_DATA_GENERAL = era_data_general
    _ERA_DATA_DAIKAKUJI = era_data_daikakuji
    _ERA_DATA_JIMYOUIN = era_data_jimyouin

    for _era in _ERA_DATA_COMMON + _ERA_DATA_GENERAL + _ERA_DATA_DAIKAKUJI + _ERA_DATA_JIMYOUIN:
        _era_kanji_dict[_era.kanji].add(_era)
        _era_alphabet_dict[_era.english].add(_era)
        _era_alphabet_vowel_shortened_dict[_era.english_vowel_shortened].add(_era)
        _era_alphabet_head_dict[_era.english_head].add(_era)

    global _JAPANERA_TimeRE_cache
    _JAPANERA_TimeRE_cache = TimeRE()


class TimeRE(dict):
    """Handle conversion from format directives to regexes."""

    def __init__(self, locale_time=None):
        """Create keys/values.

        Order of execution is important for dependency reasons.

        """
        if locale_time:
            self.locale_time = locale_time
        else:
            self.locale_time = LocaleTime()
        base = super()

        base.__init__({
            # Added for Japanera
            '-K': self.__seqToRE(_era_kanji_dict.keys(), '_K'),
            '-E': self.__seqToRE(_era_alphabet_dict.keys(), '_E'),
            '-e': self.__seqToRE(_era_alphabet_vowel_shortened_dict.keys(), '_e'),
            '-h': self.__seqToRE(_era_alphabet_head_dict.keys(), '_h'),
            '-n': r"(?P<_n>[一二三四五六七八九]?十[一二三四五六七八九]?|"
                  r"[一二三四五六七八九]|"
                  r"元)",
            '-N': r"(?P<_N>"
                  r"[一二三四五六七八九]?千([一二三四五六七八九]?百)?([一二三四五六七八九]?十)?[一二三四五六七八九]?|"
                  r"[一二三四五六七八九]?百([一二三四五六七八九]?十)?[一二三四五六七八九]?|"
                  r"[一二三四五六七八九]?十[一二三四五六七八九]?|"
                  r"[一二三四五六七八九]|"
                  r"元)",
            '-y': r"(?P<_y>\d\d|\d|"
                  r"元)",
            '-Y': r"(?P<_Y>\d{1,4}|"
                  r"元)",
            '-m': r"(?P<_m>1[0-2]|0[1-9]|[1-9]|十[一二]?|[一二三四五六七八九])",
            '-d': r"(?P<_d>3[0-1]|[1-2]\d|0[1-9]|[1-9]| [1-9]|三十一?|二?十[一二三四五六七八九]?|[一二三四五六七八九])",
            '-a': r"(?P<_a>[月火水木金土日])",

            # Default below
            # The " [1-9]" part of the regex is to make %c from ANSI C work
            'd': r"(?P<d>3[0-1]|[1-2]\d|0[1-9]|[1-9]| [1-9])",
            'f': r"(?P<f>[0-9]{1,6})",
            'H': r"(?P<H>2[0-3]|[0-1]\d|\d)",
            'I': r"(?P<I>1[0-2]|0[1-9]|[1-9])",
            'G': r"(?P<G>\d\d\d\d)",
            'j': r"(?P<j>36[0-6]|3[0-5]\d|[1-2]\d\d|0[1-9]\d|00[1-9]|[1-9]\d|0[1-9]|[1-9])",
            'm': r"(?P<m>1[0-2]|0[1-9]|[1-9])",
            'M': r"(?P<M>[0-5]\d|\d)",
            'S': r"(?P<S>6[0-1]|[0-5]\d|\d)",
            'U': r"(?P<U>5[0-3]|[0-4]\d|\d)",
            'w': r"(?P<w>[0-6])",
            'u': r"(?P<u>[1-7])",
            'V': r"(?P<V>5[0-3]|0[1-9]|[1-4]\d|\d)",
            # W is set below by using 'U'
            'y': r"(?P<y>\d\d|\d)",
            # XXX: Does 'Y' need to worry about having less or more than
            #     4 digits?
            'Y': r"(?P<Y>\d\d\d\d)",
            'z': r"(?P<z>[+-]\d\d:?[0-5]\d(:?[0-5]\d(\.\d{1,6})?)?|Z)",
            'A': self.__seqToRE(self.locale_time.f_weekday, 'A'),
            'a': self.__seqToRE(self.locale_time.a_weekday, 'a'),
            'B': self.__seqToRE(self.locale_time.f_month[1:], 'B'),
            'b': self.__seqToRE(self.locale_time.a_month[1:], 'b'),
            'p': self.__seqToRE(self.locale_time.am_pm, 'p'),
            'Z': self.__seqToRE((tz for tz_names in self.locale_time.timezone
                                 for tz in tz_names),
                                'Z'),
            '%': '%'})
        base.__setitem__('W', base.__getitem__('U').replace('U', 'W'))
        base.__setitem__('c', self.pattern(self.locale_time.LC_date_time))
        base.__setitem__('x', self.pattern(self.locale_time.LC_date))
        base.__setitem__('X', self.pattern(self.locale_time.LC_time))

    def __seqToRE(self, to_convert, directive):
        """Convert a list to a regex string for matching a directive.

        Want possible matching values to be from longest to shortest.  This
        prevents the possibility of a match occurring for a value that also
        a substring of a larger value that should have matched (e.g., 'abc'
        matching when 'abcdef' should have been the match).

        """
        to_convert = sorted(to_convert, key=len, reverse=True)
        for value in to_convert:
            if value != '':
                break
        else:
            return ''
        regex = '|'.join(re_escape(stuff) for stuff in to_convert)
        regex = '(?P<%s>%s' % (directive, regex)
        return '%s)' % regex

    def pattern(self, format):
        """Return regex pattern for the format string.

        Need to make sure that any characters that might be interpreted as
        regex syntax are escaped.

        """
        processed_format = ''
        # The sub() call escapes all characters that might be misconstrued
        # as regex syntax.  Cannot use re.escape since we have to deal with
        # format directives (%m, etc.).
        regex_chars = re_compile(r"([\\.^$*+?\(\){}\[\]|])")
        format = regex_chars.sub(r"\\\1", format)
        whitespace_replacement = re_compile(r'\s+')
        format = whitespace_replacement.sub(r'\\s+', format)
        while '%' in format:
            directive_index = format.index('%') + 1
            if format[directive_index] == '-':
                directive = format[directive_index:directive_index + 2]
            else:
                directive = format[directive_index]
            processed_format = "%s%s%s" % (processed_format,
                                           format[:directive_index - 1],
                                           self[directive])
            format = format[directive_index + len(directive):]
        return "%s%s" % (processed_format, format)

    def compile(self, format):
        """Return a compiled re object for the format string."""
        return re_compile(self.pattern(format), IGNORECASE)


def _calc_julian_from_V(iso_year, iso_week, iso_weekday):
    """Calculate the Julian day based on the ISO 8601 year, week, and weekday.
    ISO weeks start on Mondays, with week 01 being the week containing 4 Jan.
    ISO week days range from 1 (Monday) to 7 (Sunday).
    """
    correction = datetime_date(iso_year, 1, 4).isoweekday() + 3
    ordinal = (iso_week * 7) + iso_weekday - correction
    # ordinal may be negative or 0 now, which means the date is in the previous
    # calendar year
    if ordinal < 1:
        ordinal += datetime_date(iso_year, 1, 1).toordinal()
        iso_year -= 1
        ordinal -= datetime_date(iso_year, 1, 1).toordinal()
    return iso_year, ordinal


def _strptime(data_string, format="%a %b %d %H:%M:%S %Y"):
    """Return a 2-tuple consisting of a time struct and an int containing
    the number of microseconds based on the input string and the
    format string."""

    for index, arg in enumerate([data_string, format]):
        if not isinstance(arg, str):
            msg = "strptime() argument {} must be str, not {}"
            raise TypeError(msg.format(index, type(arg)))

    with _cache_lock:
        global _JAPANERA_TimeRE_cache
        locale_time = _JAPANERA_TimeRE_cache.locale_time
        if (_getlang() != locale_time.lang or
                time.tzname != locale_time.tzname or
                time.daylight != locale_time.daylight):
            _JAPANERA_TimeRE_cache = TimeRE()
            _regex_cache.clear()
            locale_time = _JAPANERA_TimeRE_cache.locale_time
        if len(_regex_cache) > _CACHE_MAX_SIZE:
            _regex_cache.clear()
        format_regex = _regex_cache.get(format)
        if not format_regex:
            try:
                format_regex = _JAPANERA_TimeRE_cache.compile(format)
            # KeyError raised when a bad format is found; can be specified as
            # \\, in which case it was a stray % but with a space after it
            except KeyError as err:
                bad_directive = err.args[0]
                if bad_directive == "\\":
                    bad_directive = "%"
                del err
                raise ValueError("'%s' is a bad directive in format '%s'" %
                                 (bad_directive, format)) from None
            # IndexError only occurs when the format string is "%"
            except IndexError:
                raise ValueError("stray %% in format '%s'" % format) from None
            _regex_cache[format] = format_regex
    found = format_regex.match(data_string)
    if not found:
        raise ValueError("time data %r does not match format %r" %
                         (data_string, format))
    if len(data_string) != found.end():
        raise ValueError("unconverted data remains: %s" %
                         data_string[found.end():])

    iso_year = year = None
    month = day = None
    hour = minute = second = fraction = 0
    tz = -1
    gmtoff = None
    gmtoff_fraction = 0
    # Default to -1 to signify that values not known; not critical to have,
    # though
    iso_week = week_of_year = None
    week_of_year_start = None
    # weekday and julian defaulted to None so as to signal need to calculate
    # values
    weekday = julian = None
    found_dict = found.groupdict()

    era_kanji = era_english = era_english_vowel_shortened = era_head = None
    relative_year = None

    for group_key in found_dict.keys():
        # Directives not explicitly handled below:
        #   c, x, X
        #      handled by making out of other directives
        #   U, W
        #      worthless without day of the week
        #  ===== ADDED BY JAPANERA BELOW =====
        if group_key == '_K':
            era_kanji = found_dict['_K']
        elif group_key == '_E':
            era_english = found_dict['_E']
        elif group_key == '_e':
            era_english_vowel_shortened = found_dict['_e']
        elif group_key == '_h':
            era_head = found_dict['_h']
        elif group_key == '_n':
            found_relative_year = found_dict['_n']

            if found_relative_year == '元':
                relative_year = 1
            else:
                relative_year = kanji2number(found_relative_year)
        elif group_key == '_N':
            found_absolute_year = found_dict['_N']

            if found_absolute_year == '元':
                year = 1
            else:
                year = kanji2number(found_absolute_year)
        elif group_key == '_y':
            found_relative_year = found_dict['_y']

            if found_relative_year == '元':
                relative_year = 1
            else:
                relative_year = int(found_relative_year)
        elif group_key == '_Y':
            found_absolute_year = found_dict['_Y']

            if found_absolute_year == '元':
                year = 1
            else:
                year = kanji2number(found_absolute_year)
        elif group_key == '_m':
            month = kanji2number(found_dict['_m'])
        elif group_key == '_d':
            day = kanji2number(found_dict['_d'])
        elif group_key == '_a':
            weekday = '月火水木金土日'.index(found_dict['_a'])
        #  ===== ADDED BY JAPANERA ABOVE =====

        elif group_key == 'y':
            year = int(found_dict['y'])
            # Open Group specification for strptime() states that a %y
            # value in the range of [00, 68] is in the century 2000, while
            # [69,99] is in the century 1900
            if year <= 68:
                year += 2000
            else:
                year += 1900
        elif group_key == 'Y':
            year = int(found_dict['Y'])
        elif group_key == 'G':
            iso_year = int(found_dict['G'])
        elif group_key == 'm':
            month = int(found_dict['m'])
        elif group_key == 'B':
            month = locale_time.f_month.index(found_dict['B'].lower())
        elif group_key == 'b':
            month = locale_time.a_month.index(found_dict['b'].lower())
        elif group_key == 'd':
            day = int(found_dict['d'])
        elif group_key == 'H':
            hour = int(found_dict['H'])
        elif group_key == 'I':
            hour = int(found_dict['I'])
            ampm = found_dict.get('p', '').lower()
            # If there was no AM/PM indicator, we'll treat this like AM
            if ampm in ('', locale_time.am_pm[0]):
                # We're in AM so the hour is correct unless we're
                # looking at 12 midnight.
                # 12 midnight == 12 AM == hour 0
                if hour == 12:
                    hour = 0
            elif ampm == locale_time.am_pm[1]:
                # We're in PM so we need to add 12 to the hour unless
                # we're looking at 12 noon.
                # 12 noon == 12 PM == hour 12
                if hour != 12:
                    hour += 12
        elif group_key == 'M':
            minute = int(found_dict['M'])
        elif group_key == 'S':
            second = int(found_dict['S'])
        elif group_key == 'f':
            s = found_dict['f']
            # Pad to always return microseconds.
            s += "0" * (6 - len(s))
            fraction = int(s)
        elif group_key == 'A':
            weekday = locale_time.f_weekday.index(found_dict['A'].lower())
        elif group_key == 'a':
            weekday = locale_time.a_weekday.index(found_dict['a'].lower())
        elif group_key == 'w':
            weekday = int(found_dict['w'])
            if weekday == 0:
                weekday = 6
            else:
                weekday -= 1
        elif group_key == 'u':
            weekday = int(found_dict['u'])
            weekday -= 1
        elif group_key == 'j':
            julian = int(found_dict['j'])
        elif group_key in ('U', 'W'):
            week_of_year = int(found_dict[group_key])
            if group_key == 'U':
                # U starts week on Sunday.
                week_of_year_start = 6
            else:
                # W starts week on Monday.
                week_of_year_start = 0
        elif group_key == 'V':
            iso_week = int(found_dict['V'])
        elif group_key == 'z':
            z = found_dict['z']
            if z == 'Z':
                gmtoff = 0
            else:
                if z[3] == ':':
                    z = z[:3] + z[4:]
                    if len(z) > 5:
                        if z[5] != ':':
                            msg = f"Inconsistent use of : in {found_dict['z']}"
                            raise ValueError(msg)
                        z = z[:5] + z[6:]
                hours = int(z[1:3])
                minutes = int(z[3:5])
                seconds = int(z[5:7] or 0)
                gmtoff = (hours * 60 * 60) + (minutes * 60) + seconds
                gmtoff_remainder = z[8:]
                # Pad to always return microseconds.
                gmtoff_remainder_padding = "0" * (6 - len(gmtoff_remainder))
                gmtoff_fraction = int(gmtoff_remainder + gmtoff_remainder_padding)
                if z.startswith("-"):
                    gmtoff = -gmtoff
                    gmtoff_fraction = -gmtoff_fraction
        elif group_key == 'Z':
            # Since -1 is default value only need to worry about setting tz if
            # it can be something other than -1.
            found_zone = found_dict['Z'].lower()
            for value, tz_values in enumerate(locale_time.timezone):
                if found_zone in tz_values:
                    # Deal with bad locale setup where timezone names are the
                    # same and yet time.daylight is true; too ambiguous to
                    # be able to tell what timezone has daylight savings
                    if (time.tzname[0] == time.tzname[1] and
                            time.daylight and found_zone not in ("utc", "gmt")):
                        break
                    else:
                        tz = value
                        break
    # Deal with the cases where ambiguities arize
    # don't assume default values for ISO week/year
    if year is None and iso_year is not None:
        if iso_week is None or weekday is None:
            raise ValueError("ISO year directive '%G' must be used with "
                             "the ISO week directive '%V' and a weekday "
                             "directive ('%A', '%a', '%w', or '%u').")
        if julian is not None:
            raise ValueError("Day of the year directive '%j' is not "
                             "compatible with ISO year directive '%G'. "
                             "Use '%Y' instead.")
    elif week_of_year is None and iso_week is not None:
        if weekday is None:
            raise ValueError("ISO week directive '%V' must be used with "
                             "the ISO year directive '%G' and a weekday "
                             "directive ('%A', '%a', '%w', or '%u').")
        else:
            raise ValueError("ISO week directive '%V' is incompatible with "
                             "the year directive '%Y'. Use the ISO year '%G' "
                             "instead.")
    tzname = found_dict.get("Z")

    # If we know the week of the year and what day of that week, we can figure
    # out the Julian day of the year.
    if julian is None and weekday is not None:
        if week_of_year is not None:
            week_starts_Mon = True if week_of_year_start == 0 else False
            julian = _calc_julian_from_U_or_W(year, week_of_year, weekday,
                                              week_starts_Mon)
        elif iso_year is not None and iso_week is not None:
            year, julian = _calc_julian_from_V(iso_year, iso_week, weekday + 1)
        if julian is not None and julian <= 0:
            year -= 1
            yday = 366 if calendar.isleap(year) else 365
            julian += yday
    return (era_kanji, era_english, era_english_vowel_shortened,
            era_head, relative_year), \
        (year, month, day,
         hour, minute, second,
         weekday, julian, tz, tzname,
         gmtoff), fraction, gmtoff_fraction


def find_era_and_date(era_kanji: Optional[str] = None,
                      era_english: Optional[str] = None,
                      era_english_vowel_shortened: Optional[str] = None,
                      era_head_english: Optional[str] = None,
                      absolute_year: Optional[int] = None,
                      relative_year: Optional[int] = None,
                      month: Optional[int] = None,
                      day: Optional[int] = None,
                      allow_date_after_end_of_era: bool = False,
                      ) -> List[Tuple["Era", datetime.date]]:
    """
    Find era and date from given information.
    Args:
        era_kanji: Kanji of era name
        era_english: English of era name
        era_english_vowel_shortened: English of era name with vowel shortened
        era_head_english: English of era name with only first letter
        absolute_year: Absolute year
        relative_year: Relative year from era
        month: Month
        day: Day
        allow_date_after_end_of_era: If True, allow date after end of era

    Returns: List of era and date

    """
    era_set = None

    for text, _dict in zip((era_kanji, era_english, era_english_vowel_shortened, era_head_english),
                           (_era_kanji_dict, _era_alphabet_dict, _era_alphabet_vowel_shortened_dict,
                            _era_alphabet_head_dict)):
        if text:
            _found = _dict[text]
            era_set = era_set & _found if era_set else _found
    if absolute_year is not None:
        _found = find_eras_with_year(absolute_year)
        era_set = era_set & _found if era_set else _found
    if (era_kanji or era_english or era_english_vowel_shortened or
        era_head_english or absolute_year is not None) and not era_set:
        raise ValueError("Era_ information given but no match era found.")

    era_set = era_set or _ERA_DATA_GENERAL + _ERA_DATA_COMMON + _ERA_DATA_DAIKAKUJI + _ERA_DATA_JIMYOUIN
    era_list = sorted(era_set, key=lambda x: (x.since, x.era_type.value))

    result = []
    for era in era_list:
        dt = era.since
        if absolute_year is not None and absolute_year != dt.year:
            # if absolute_year is different from era's since year, we can make result new years day
            dt = datetime.date(absolute_year, 1, 1)
        elif relative_year is not None and relative_year > 1:
            # relative_year starts from 1, so we need to add 1 to relative_year
            dt = datetime.date(dt.year + relative_year - 1, 1, 1)
        if month is not None:
            if dt.year != era.since.year or month != dt.month:
                # if month is specified to be different from `since` month, 1st of the month is most early date
                dt = dt.replace(month=month, day=1)
                if absolute_year is None and relative_year is None and dt < era.since:
                    dt = dt.replace(year=dt.year + 1)
            if day is not None:  # if month is specified, we can't use loop below to find the month
                if month == 2 and day == 29:
                    if absolute_year is None and relative_year is None:
                        # if month is February and day is 29 and no year is specified, we need to find next leap year
                        dt = dt.replace(year=find_closest_leap_year(dt.year))
                try:
                    dt = dt.replace(day=day)
                except ValueError:  # out of range
                    continue
        elif day is not None:
            while True:  # we know `day` is not more than 31 because of legit regex
                try:
                    dt = dt.replace(day=day)
                    break
                except ValueError:  # out of range
                    days_in_month = monthrange(dt.year, dt.month)[1]
                    dt += datetime.timedelta(days=days_in_month)

        if allow_date_after_end_of_era:
            if dt < era.since:
                continue
        elif dt not in era:
            continue
        result.append((era, dt))
    return result


def find_closest_leap_year(year: int) -> int:
    """
    Find the closest leap year from `year`. If `year` is leap year, return `year`.
    Args:
        year: year to find

    Returns: closest leap year from `year`

    """
    if not year % 100 and year % 400:
        return year + 4
    if not year % 4:
        return year
    if (year % 100 > 96) and (year % 400 <= 396):
        return year + (8 - year % 4)
    return year + (4 - year % 4)


def find_eras_with_year(year: int) -> Set["Era"]:
    """
    Find all eras that contains `year`.
    Args:
        year: year to find

    Returns: set of Era that contains `year`
    """

    def _find_first_era_after_year_index(era_list: List["Era"]) -> int:
        # return the index of first era that starts after `year`
        ok = len(era_list)
        ng = -1
        while abs(ok - ng) > 1:
            mid = (ok + ng) // 2
            if era_list[mid].since.year <= year:
                ng = mid
            else:
                ok = mid
        return ok

    result = set(_ERA_DATA_COMMON)
    for era_list in (_ERA_DATA_GENERAL, _ERA_DATA_DAIKAKUJI, _ERA_DATA_JIMYOUIN):
        for i in range(_find_first_era_after_year_index(era_list) - 1, -1, -1):
            era = era_list[i]
            # we know that this era must be started before or exact `year`
            # so we can check the `era.until.year` to see if it contains
            # `year`. and notice that current `era`'s until can be None
            if era.until and year > era.until.year:
                break
            result.add(era)

    return result
