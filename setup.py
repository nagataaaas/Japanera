"""
Easy japanese era tool
-----------
Powered by [Yamato Nagata](https://twitter.com/514YJ)

[GitHub](https://github.com/delta114514/Japanera)
[ReadTheDocs](https://japanera.readthedocs.io/en/latest/)


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
"""

from setuptools import setup
from os import path

about = {}
with open("japanera/__about__.py") as f:
    exec(f.read(), about)

here = path.abspath(path.dirname(__file__))

setup(name=about["__title__"],
      version=about["__version__"],
      url=about["__url__"],
      license=about["__license__"],
      author=about["__author__"],
      author_email=about["__author_email__"],
      description=about["__description__"],
      long_description=__doc__,
      packages=["japanera"],
      zip_safe=False,
      platforms="any",
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Environment :: Other Environment",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules"
      ])
