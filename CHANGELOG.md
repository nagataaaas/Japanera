# 2.1.0
- support Python3.12. (contributed by mytabata)
- fix type annotation. (pointed out by tnagano22)

# 2.0.0
- Destructive change: Many methods are renamed, new written, and deleted.
- Core `strptime` and `strftime` are rewritten.
- Removed `japanera.Japanera` class. Upgrade carefully.

# 1.1.0
- Support kanjize 1.3.0
- Support `dt in Era` Syntax

# 1.0.1
- Now this can parse single digit year.

# 1.0.0
- Fixed bug that unable to parse single-digit months or dates

# 0.0.8
- Fixed bug that leap year could not be parsed properly.

# 0.0.7
- Bug fix about end date of "大正" era.

# v0.0.6
- Bug fix

# v0.0.5
- Fixed The bug `strptime` don't return collect result when "%-kY" in `fmt`

# v0.0.4
- Added `%-kY`, `%-ky`, `%-km` and `%-kd` directive to every `strftime` and `strptime`. It's so useful to use Kainji-Number.

# v0.0.3
- Fixed `ModuleNotFoundError: No module named 'japanera.0'` error when `from japanera import *`

# v0.0.2
- Added `Japanera().strptime(_str, fmt)`

# v0.0.1
- Conception
