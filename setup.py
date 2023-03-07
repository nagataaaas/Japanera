"""
Easy japanese era tool
----------------------
Powered by [Yamato Nagata](https://twitter.com/514YJ)

[GitHub](https://github.com/delta114514/Japanera)
[ReadTheDocs](https://japanera.readthedocs.io/en/latest/)


```python
>>> from datetime import date
>>> from japanera import EraDate

>>> today = EraDate.from_date(date.today())
>>> date(2020, 4, 16) in today.era
True

>>> "Current Japanese Era is <{}>: <{}>".format(today.era.kanji, today.era.english)
Current Japanese Era is <令和>: <Reiwa>

>>> "Current Date is <{}>".format(today.strftime("%-K%-y年%m月%d日"))
Current Date is <令和05年03月07日>
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
      long_description_content_type="text/markdown",
      install_requires=["kanjize==1.3.0"],
      packages=["japanera"],
      zip_safe=False,
      platforms="any",
      classifiers=[
          "Development Status :: 4 - Beta",
          "Environment :: Other Environment",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules"
      ])
