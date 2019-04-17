"""
    Japanera
    -----------

    Easy japanese era tool
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