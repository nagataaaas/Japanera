"""
    Japanera
    -----------

    Easy japanese era tool
    All Information's source is [Wikipedia Page](https://ja.wikipedia.org/wiki/%E5%85%83%E5%8F%B7%E4%B8%80%E8%A6%A7_(%E6%97%A5%E6%9C%AC))
    Powered by [Yamato Nagata](https://twitter.com/514YJ)

    [GitHub](https://github.com/nagataaaas/Japanera)
    [ReadTheDocs](https://japanera.readthedocs.io/en/latest/)

    :copyright: (c) 2019-2023 by Yamato Nagata.
    :license: MIT.
"""

from .__about__ import __version__
from .japanera import (Era, EraDate, EraDateTime, ERA_DATA_COMMON, ERA_DATA_DAIKAKUJI, ERA_DATA_JIMYOUIN,
                       ERA_DATA_GENERAL)
from .era_data import (EraType)

__all__ = [
    __version__,
    "Era",
    "EraDate",
    "EraDateTime",
    "EraType",
    "ERA_DATA_COMMON",
    "ERA_DATA_DAIKAKUJI",
    "ERA_DATA_JIMYOUIN",
    "ERA_DATA_GENERAL",
]
