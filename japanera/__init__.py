"""
    Japanera
    -----------

    Easy japanese era tool
    All Information's source is [Wikipedia Page](https://ja.wikipedia.org/wiki/%E5%85%83%E5%8F%B7%E4%B8%80%E8%A6%A7_(%E6%97%A5%E6%9C%AC))
    Powered by [Yamato Nagata](https://twitter.com/514YJ)

    [GitHub](https://github.com/delta114514/Japanera)
    [ReadTheDocs](https://japanera.readthedocs.io/en/latest/)

    :copyright: (c) 2019 by Yamato Nagata.
    :license: MIT.
"""

import locale

from .__about__ import __version__
from .japanera import (Japanera, Era, EraDate, EraDateTime)


locale.setlocale(locale.LC_ALL, '')

__all__ = [
    __version__,
    "Japanera",
    "Era",
    "EraDate",
    "EraDateTime",
]