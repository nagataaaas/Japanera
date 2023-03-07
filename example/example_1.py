import datetime

from japanera import EraDate

"""
[out] Input the date you want to know how to say in Japanese!
[out] format: [yyyy-mm-dd]
[input] 0001-01-01
[out] We don't have japanese era for given date...
[out] Input the date you want to know how to say in Japanese!
[out] format: [yyyy-mm-dd]
[input] 1200-01-01
[out] ----- 正治02年01月01日 -----
[out] Input the date you want to know how to say in Japanese!
[out] format: [yyyy-mm-dd]
[input] 1199-12-12
[out] ----- 正治元年12月12日 -----
[out] Input the date you want to know how to say in Japanese!
[out] format: [yyyy-mm-dd]
[input] 1199-01-01
[out] ----- 建久10年01月01日 -----
[out] Input the date you want to know how to say in Japanese!
[out] format: [yyyy-mm-dd]

"""

while True:
    print("Input the date you want to know how to say in Japanese!\nformat: [yyyy-mm-dd]")
    s = input()
    try:
        _date = datetime.datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        print("Input correctly!!")
        continue
    try:
        print("-" * 5, EraDate.from_date(_date).strftime("%-K%-Y年%m月%d日"), "-" * 5)
    except AttributeError:
        print("We don't have japanese era for given date...")
