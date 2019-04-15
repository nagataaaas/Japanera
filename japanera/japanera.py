# -*- coding: utf-8 -*-

from datetime import date, datetime
import re
import locale

from warnings import warn
from bisect import bisect_right


class Era:
    def __init__(self, kanji, english, start, end, _type):
        """

        :param kanji - str: kanji letter of era. exp. "大正"
        :param english - str: english letter of pronunciation of era. exp. "Taishou"
        :param start - datetime.date: start of the era. This day is included to this era.
        :param end - datetime.date: end of the era. This day is excluded to this era.
        :param _type:
        """
        self.kanji = kanji
        self.english = english
        self.start = start
        self.end = end
        self.type = _type

    @property
    def english_shorten_vowel(self):
        """
        Return self.english vowel shortened. exp. "Taishou" -> "Taisho"
        :return: str

        Didn't use str.replace for scalability
        """
        try:
            english = self.english.lower()
        except AttributeError:
            return None

        table = {"ou": "o", "uu": "u"}

        pattern = re.compile("|".join(table.keys()))
        return pattern.sub(lambda m: table[re.escape(m.group(0))], english).title()

    @property
    def english_head(self):
        """
        Return the first letter of self.english
        :return:
        """
        return self.english[0]

    def _in(self, _date):
        """
        Return if given date is in between self.start and self.end
        :param _date: datetime.date
        :return: bool
        """
        if self.start and self.end:
            return self.start <= _date < self.end
        elif self.start:
            return self.start <= _date
        elif self.end:
            return _date < self.end
        return False

    def is_after(self, other):
        """
        Return if given object (datetime.date or japanera.Era) is placed after this era.
        :param other - datetime.date or japanera.Era:
        :return: bool
        """
        return other < self

    def is_before(self, other):
        """
        Return if given object (datetime.date or japanera.Era) is placed before this era.
        :param other - datetime.date or japanera.Era:
        :return: bool
        """
        return self < other

    def strftime(self, _date, _format, allow_before=False):
        """
        %-E: Kanji era name
        %-A: Alphabet era name
        %-a: First letter of alphabet era name
        %-o: Year of corresponding era
        %-O: Year of corresponding era. But return "元" for the first year
        + datetime.strftime's format

        allow_before: object can be converted to bool. If it's true and the given _date if before than self,start,
                     %-o and %-O will be "Unknown". If False, raise an ValueError. Default: False
        """
        if self.is_after(_date):
            raise ValueError("Given datetime.date is before than This Era.start")
        try:
            year = _date.year - self.start.year + 1
            rep = {"%-E": self.kanji, "%-A": self.english, "%-a": self.english[0], "%-o": str(year % 100).zfill(2),
                   "%-O": "元" if year == 1 else str(year % 100).zfill(2)}
        except AttributeError:
            try:
                rep = {"%-E": "不明", "%-A": "Unknown", "%-a": "U", "%-o": str(year % 100).zfill(2),
                       "%-O": "元" if year == 1 else str(year % 100).zfill(2)}
            except (AttributeError, UnboundLocalError):
                if not allow_before:
                    raise ValueError("Given date is too early to format")
                rep = {"%-E": "不明", "%-A": "Unknown", "%-a": "U", "%-o": "Unknown",
                       "%-O": "Unknown"}

        rep = dict((re.escape(k), str(v)) for k, v in rep.items())
        pattern = re.compile("|".join(rep.keys()))
        return _date.strftime(pattern.sub(lambda m: rep[re.escape(m.group(0))], _format))

    def strptime(self, _str, _format):
        """
        %-E: Kanji era name
        %-A: Alphabet era name
        %-a: First letter of alphabet era name
        %-o: Year of corresponding era
        %-O: Year of corresponding era. But return "元" for the first year
        + datetime.strftime's format
        """
        try:
            rep = {"%-E": self.kanji, "%-A": self.english, "%-a": self.english[0], "%-s": self.english_shorten_vowel}
        except TypeError:
            rep = {"%-E": "不明", "%-A": "Unknown", "%-a": "U", "%-s": "Unknown"}

        rep = dict((re.escape(k), str(v)) for k, v in rep.items())
        pattern = re.compile("|".join(rep.keys()))

        _format = pattern.sub(lambda m: rep[re.escape(m.group(0))], _format)

        if "%-O" in _format:
            _format = _format.replace("元", "01")
            _str = _str.replace("元", "01")

        _format = re.compile("%-[oO]").sub(lambda m: "%y", _format)
        _date = datetime.strptime(_str, _format)
        return _date.replace(year=(_date.year % 1000) + self.start.year - 1)

    def __gt__(self, other):
        if isinstance(other, Era):
            return other.start < self.start
        elif isinstance(other, (datetime, date)):
            return other < self.start

    def __lt__(self, other):
        if isinstance(other, Era):
            return self.start < other.start
        elif isinstance(other, (datetime, date)):
            return self.end < other

    def __eq__(self, other):
        try:
            for key in ("kanji", "english", "start", "end", "type"):
                if getattr(self, key) != getattr(other, key):
                    return False
            return True
        except AttributeError:
            return False

    def __repr__(self):
        start_time = self.start.strftime("%d/%m/%Y") if self.start else "None"
        end_time = self.end.strftime("%d/%m/%Y") if self.end else "None"
        return "<Era {}:{} {} - {}>".format(self.kanji, self.english, start_time, end_time)

    def __str__(self):
        return "{}: {}".format(self.kanji, self.english)


class Japanera:
    era_common = [Era("大化", "Taika", date(645, 7, 20), date(650, 3, 25), "common"),
                  Era("白雉", "Hakuchi", date(650, 3, 25), date(654, 11, 27), "common"),
                  Era(None, None, date(654, 11, 27), date(686, 8, 17), "common"),
                  Era("朱鳥", "Shucho", date(686, 8, 17), date(686, 10, 4), "common"),
                  Era(None, None, date(686, 10, 4), date(701, 5, 7), "common"),
                  Era("大宝", "Taiho", date(701, 5, 7), date(704, 6, 20), "common"),
                  Era("慶雲", "Keiun", date(704, 6, 20), date(708, 2, 11), "common"),
                  Era("和銅", "Wado", date(708, 2, 11), date(715, 10, 7), "common"),
                  Era("霊亀", "Reiki", date(715, 10, 7), date(717, 12, 28), "common"),
                  Era("養老", "Yourou", date(717, 12, 28), date(724, 3, 7), "common"),
                  Era("神亀", "Jinki", date(724, 3, 7), date(729, 9, 6), "common"),
                  Era("天平", "Tempyou", date(729, 9, 6), date(749, 5, 8), "common"),
                  Era("天平感宝", "TempyoKampou", date(749, 5, 8), date(749, 8, 23), "common"),
                  Era("天平勝宝", "TempyoSyouhou", date(749, 8, 23), date(757, 9, 10), "common"),
                  Era("天平宝字", "TempyoHouji", date(757, 9, 10), date(765, 2, 5), "common"),
                  Era("天平神護", "TempyoJingo", date(765, 2, 5), date(767, 9, 17), "common"),
                  Era("神護景雲", "JingoKeiun", date(767, 9, 17), date(770, 10, 27), "common"),
                  Era("宝亀", "Houki", date(770, 10, 27), date(781, 2, 3), "common"),
                  Era("天応", "Tennou", date(781, 2, 3), date(782, 10, 4), "common"),
                  Era("延暦", "Enryaku", date(782, 10, 4), date(806, 6, 12), "common"),
                  Era("大同", "Daidou", date(806, 6, 12), date(810, 10, 24), "common"),
                  Era("弘仁", "Kounin", date(810, 10, 24), date(824, 2, 12), "common"),
                  Era("天長", "Tencho", date(824, 2, 12), date(834, 2, 18), "common"),
                  Era("承和", "Jouwa", date(834, 2, 18), date(848, 7, 20), "common"),
                  Era("嘉祥", "Kashou", date(848, 7, 20), date(851, 6, 5), "common"),
                  Era("仁寿", "Ninju", date(851, 6, 5), date(854, 12, 27), "common"),
                  Era("斉衡", "Saikou", date(854, 12, 27), date(857, 3, 24), "common"),
                  Era("天安", "Tennan", date(857, 3, 24), date(859, 5, 24), "common"),
                  Era("貞観", "Jougan", date(859, 5, 24), date(877, 6, 5), "common"),
                  Era("元慶", "Gangyo", date(877, 6, 5), date(885, 3, 15), "common"),
                  Era("仁和", "Ninna", date(885, 3, 15), date(889, 6, 3), "common"),
                  Era("寛平", "Kampyou", date(889, 6, 3), date(898, 5, 24), "common"),
                  Era("昌泰", "Syoutai", date(898, 5, 24), date(901, 9, 5), "common"),
                  Era("延喜", "Engi", date(901, 9, 5), date(923, 6, 3), "common"),
                  Era("延長", "Enchou", date(923, 6, 3), date(931, 5, 21), "common"),
                  Era("承平", "Jouhei", date(931, 5, 21), date(938, 6, 27), "common"),
                  Era("天慶", "Tengyou", date(938, 6, 27), date(947, 5, 20), "common"),
                  Era("天暦", "Tenryaku", date(947, 5, 20), date(957, 11, 26), "common"),
                  Era("天徳", "Tentoku", date(957, 11, 26), date(961, 3, 10), "common"),
                  Era("応和", "Ouwa", date(961, 3, 10), date(964, 8, 24), "common"),
                  Era("康保", "Kouhou", date(964, 8, 24), date(968, 9, 13), "common"),
                  Era("安和", "Anna", date(968, 9, 13), date(970, 5, 8), "common"),
                  Era("天禄", "Tenroku", date(970, 5, 8), date(974, 1, 21), "common"),
                  Era("天延", "Tenen", date(974, 1, 21), date(976, 8, 16), "common"),
                  Era("貞元", "Jougen", date(976, 8, 16), date(979, 1, 5), "common"),
                  Era("天元", "Tengen", date(979, 1, 5), date(983, 6, 3), "common"),
                  Era("永観", "Eikan", date(983, 6, 3), date(985, 5, 24), "common"),
                  Era("寛和", "Kanna", date(985, 5, 24), date(987, 5, 10), "common"),
                  Era("永延", "Eien", date(987, 5, 10), date(989, 9, 15), "common"),
                  Era("永祚", "Eiso", date(989, 9, 15), date(990, 12, 1), "common"),
                  Era("正暦", "Syouryaku", date(990, 12, 1), date(995, 3, 30), "common"),
                  Era("長徳", "Choutoku", date(995, 3, 30), date(999, 2, 6), "common"),
                  Era("長保", "Chouhou", date(999, 2, 6), date(1004, 8, 14), "common"),
                  Era("寛弘", "Kankou", date(1004, 8, 14), date(1013, 2, 14), "common"),
                  Era("長和", "Chouwa", date(1013, 2, 14), date(1017, 5, 27), "common"),
                  Era("寛仁", "Kannin", date(1017, 5, 27), date(1021, 3, 23), "common"),
                  Era("治安", "Jian", date(1021, 3, 23), date(1024, 8, 25), "common"),
                  Era("万寿", "Manju", date(1024, 8, 25), date(1028, 8, 24), "common"),
                  Era("長元", "Chougen", date(1028, 8, 24), date(1037, 5, 15), "common"),
                  Era("長暦", "Chouryaku", date(1037, 5, 15), date(1040, 12, 22), "common"),
                  Era("長久", "Choukyuu", date(1040, 12, 22), date(1044, 12, 22), "common"),
                  Era("寛徳", "Kantoku", date(1044, 12, 22), date(1046, 5, 28), "common"),
                  Era("永承", "Eishou", date(1046, 5, 28), date(1053, 2, 8), "common"),
                  Era("天喜", "Tenki", date(1053, 2, 8), date(1058, 9, 25), "common"),
                  Era("康平", "Kouhei", date(1058, 9, 25), date(1065, 9, 10), "common"),
                  Era("治暦", "Jiryaku", date(1065, 9, 10), date(1069, 5, 12), "common"),
                  Era("延久", "Enkyuu", date(1069, 5, 12), date(1074, 9, 22), "common"),
                  Era("承保", "Jouhou", date(1074, 9, 22), date(1077, 12, 11), "common"),
                  Era("承暦", "Jouryaku", date(1077, 12, 11), date(1081, 3, 28), "common"),
                  Era("永保", "Eihou", date(1081, 3, 28), date(1084, 3, 21), "common"),
                  Era("応徳", "Outoku", date(1084, 3, 21), date(1087, 5, 17), "common"),
                  Era("寛治", "Kanji", date(1087, 5, 17), date(1095, 1, 29), "common"),
                  Era("嘉保", "Kahou", date(1095, 1, 29), date(1097, 1, 9), "common"),
                  Era("永長", "Eichou", date(1097, 1, 9), date(1098, 1, 2), "common"),
                  Era("承徳", "Joutoku", date(1098, 1, 2), date(1099, 9, 21), "common"),
                  Era("康和", "Kouwa", date(1099, 9, 21), date(1104, 3, 15), "common"),
                  Era("長治", "Chouji", date(1104, 3, 15), date(1106, 5, 20), "common"),
                  Era("嘉承", "Kashou", date(1106, 5, 20), date(1108, 9, 16), "common"),
                  Era("天仁", "Tennin", date(1108, 9, 16), date(1110, 8, 7), "common"),
                  Era("天永", "Tennei", date(1110, 8, 7), date(1113, 9, 1), "common"),
                  Era("永久", "Eikyuu", date(1113, 9, 1), date(1118, 5, 2), "common"),
                  Era("元永", "Gennei", date(1118, 5, 2), date(1120, 5, 16), "common"),
                  Era("保安", "Houan", date(1120, 5, 16), date(1124, 5, 25), "common"),
                  Era("天治", "Tenji", date(1124, 5, 25), date(1126, 2, 22), "common"),
                  Era("大治", "Daiji", date(1126, 2, 22), date(1131, 3, 7), "common"),
                  Era("天承", "Tenshou", date(1131, 3, 7), date(1132, 9, 28), "common"),
                  Era("長承", "Choushou", date(1132, 9, 28), date(1135, 6, 17), "common"),
                  Era("保延", "Houen", date(1135, 6, 17), date(1141, 8, 20), "common"),
                  Era("永治", "Eiji", date(1141, 8, 20), date(1142, 6, 1), "common"),
                  Era("康治", "Kouji", date(1142, 6, 1), date(1144, 4, 4), "common"),
                  Era("天養", "Tennyou", date(1144, 4, 4), date(1145, 8, 19), "common"),
                  Era("久安", "Kyuuan", date(1145, 8, 19), date(1151, 2, 21), "common"),
                  Era("仁平", "Ninmpei", date(1151, 2, 21), date(1154, 12, 11), "common"),
                  Era("久寿", "Kyuuju", date(1154, 12, 11), date(1156, 5, 25), "common"),
                  Era("保元", "Hougen", date(1156, 5, 25), date(1159, 5, 16), "common"),
                  Era("平治", "Heiji", date(1159, 5, 16), date(1160, 2, 25), "common"),
                  Era("永暦", "Eiryaku", date(1160, 2, 25), date(1161, 10, 1), "common"),
                  Era("応保", "Ouhou", date(1161, 10, 1), date(1163, 5, 11), "common"),
                  Era("長寛", "Choukan", date(1163, 5, 11), date(1165, 7, 21), "common"),
                  Era("永万", "Eiman", date(1165, 7, 21), date(1166, 9, 30), "common"),
                  Era("仁安", "Ninnan", date(1166, 9, 30), date(1169, 5, 13), "common"),
                  Era("嘉応", "Kaou", date(1169, 5, 13), date(1171, 6, 3), "common"),
                  Era("承安", "Syouan", date(1171, 6, 3), date(1175, 8, 23), "common"),
                  Era("安元", "Angen", date(1175, 8, 23), date(1177, 9, 5), "common"),
                  Era("治承", "Jishou", date(1177, 9, 5), date(1181, 9, 1), "common"),
                  Era("養和", "Youwa", date(1181, 9, 1), date(1182, 7, 6), "common"),
                  Era("寿永", "Juei", date(1182, 7, 6), date(1184, 6, 3), "common"),
                  Era("元暦", "Genryaku", date(1184, 6, 3), date(1185, 9, 16), "common"),
                  Era("文治", "Bunji", date(1185, 9, 16), date(1190, 5, 23), "common"),
                  Era("建久", "Kenkyuu", date(1190, 5, 23), date(1199, 5, 30), "common"),
                  Era("正治", "Syouji", date(1199, 5, 30), date(1201, 3, 26), "common"),
                  Era("建仁", "Kennin", date(1201, 3, 26), date(1204, 3, 30), "common"),
                  Era("元久", "Genkyuu", date(1204, 3, 30), date(1206, 6, 12), "common"),
                  Era("建永", "Kennei", date(1206, 6, 12), date(1207, 11, 23), "common"),
                  Era("承元", "Jougen", date(1207, 11, 23), date(1211, 4, 30), "common"),
                  Era("建暦", "Kenryaku", date(1211, 4, 30), date(1214, 1, 25), "common"),
                  Era("建保", "Kempou", date(1214, 1, 25), date(1219, 6, 3), "common"),
                  Era("承久", "Joukyuu", date(1219, 6, 3), date(1222, 6, 1), "common"),
                  Era("貞応", "Jouou", date(1222, 6, 1), date(1225, 1, 7), "common"),
                  Era("元仁", "Gennin", date(1225, 1, 7), date(1225, 6, 4), "common"),
                  Era("嘉禄", "Karoku", date(1225, 6, 4), date(1228, 1, 25), "common"),
                  Era("安貞", "Antei", date(1228, 1, 25), date(1229, 4, 7), "common"),
                  Era("寛喜", "Kanki", date(1229, 4, 7), date(1232, 4, 30), "common"),
                  Era("貞永", "Jouei", date(1232, 4, 30), date(1233, 6, 1), "common"),
                  Era("天福", "Tempuku", date(1233, 6, 1), date(1234, 12, 4), "common"),
                  Era("文暦", "Bunryaku", date(1234, 12, 4), date(1235, 11, 8), "common"),
                  Era("嘉禎", "Katei", date(1235, 11, 8), date(1239, 1, 6), "common"),
                  Era("暦仁", "Ryakunin", date(1239, 1, 6), date(1239, 3, 20), "common"),
                  Era("延応", "Ennou", date(1239, 3, 20), date(1240, 8, 12), "common"),
                  Era("仁治", "Ninji", date(1240, 8, 12), date(1243, 3, 25), "common"),
                  Era("寛元", "Kangen", date(1243, 3, 25), date(1247, 4, 12), "common"),
                  Era("宝治", "Houji", date(1247, 4, 12), date(1249, 5, 9), "common"),
                  Era("建長", "Kenchou", date(1249, 5, 9), date(1256, 10, 31), "common"),
                  Era("康元", "Kougen", date(1256, 10, 31), date(1257, 4, 7), "common"),
                  Era("正嘉", "Syouka", date(1257, 4, 7), date(1259, 4, 27), "common"),
                  Era("正元", "Syougen", date(1259, 4, 27), date(1260, 5, 31), "common"),
                  Era("文応", "Bunnou", date(1260, 5, 31), date(1261, 3, 29), "common"),
                  Era("弘長", "Kouchou", date(1261, 3, 29), date(1264, 4, 3), "common"),
                  Era("文永", "Bunnei", date(1264, 4, 3), date(1275, 5, 29), "common"),
                  Era("建治", "Kenji", date(1275, 5, 29), date(1278, 3, 30), "common"),
                  Era("弘安", "Kouan", date(1278, 3, 30), date(1288, 6, 5), "common"),
                  Era("正応", "Syouou", date(1288, 6, 5), date(1293, 9, 13), "common"),
                  Era("永仁", "Einin", date(1293, 9, 13), date(1299, 6, 1), "common"),
                  Era("正安", "Syouan", date(1299, 6, 1), date(1302, 12, 18), "common"),
                  Era("乾元", "Kengen", date(1302, 12, 18), date(1303, 9, 24), "common"),
                  Era("嘉元", "Kagen", date(1303, 9, 24), date(1307, 1, 26), "common"),
                  Era("徳治", "Tokuji", date(1307, 1, 26), date(1308, 11, 30), "common"),
                  Era("延慶", "Enkyou", date(1308, 11, 30), date(1311, 5, 25), "common"),
                  Era("応長", "Ouchou", date(1311, 5, 25), date(1312, 5, 5), "common"),
                  Era("正和", "Syouwa", date(1312, 5, 5), date(1317, 3, 24), "common"),
                  Era("文保", "Bumpou", date(1317, 3, 24), date(1319, 5, 26), "common"),
                  Era("元応", "Gennou", date(1319, 5, 26), date(1321, 3, 30), "common"),
                  Era("元亨", "Gennkou", date(1321, 3, 30), date(1325, 1, 2), "common"),
                  Era("正中", "Syouchuu", date(1325, 1, 2), date(1326, 6, 5), "common"),
                  Era("嘉暦", "Karyaku", date(1326, 6, 5), date(1329, 9, 30), "common"),
                  Era("応永", "Ouei", date(1394, 8, 10), date(1428, 6, 19), "common"),
                  Era("正長", "Syouchou", date(1428, 6, 19), date(1429, 10, 12), "common"),
                  Era("永享", "Eikyou", date(1429, 10, 12), date(1441, 3, 19), "common"),
                  Era("嘉吉", "Kakitsu", date(1441, 3, 19), date(1444, 3, 3), "common"),
                  Era("文安", "Bunnann", date(1444, 3, 3), date(1449, 8, 25), "common"),
                  Era("宝徳", "Houtoku", date(1449, 8, 25), date(1452, 8, 19), "common"),
                  Era("享徳", "Kyoutoku", date(1452, 8, 19), date(1455, 9, 15), "common"),
                  Era("康正", "Koushou", date(1455, 9, 15), date(1457, 10, 25), "common"),
                  Era("長禄", "Chouroku", date(1457, 10, 25), date(1461, 2, 10), "common"),
                  Era("寛正", "Kannshou", date(1461, 2, 10), date(1466, 3, 23), "common"),
                  Era("文正", "Bunnshou", date(1466, 3, 23), date(1467, 4, 18), "common"),
                  Era("応仁", "Ouninn", date(1467, 4, 18), date(1469, 6, 17), "common"),
                  Era("文明", "Bunnmei", date(1469, 6, 17), date(1487, 8, 18), "common"),
                  Era("長享", "Choukyou", date(1487, 8, 18), date(1489, 9, 25), "common"),
                  Era("延徳", "Entoku", date(1489, 9, 25), date(1492, 8, 21), "common"),
                  Era("明応", "Meiou", date(1492, 8, 21), date(1501, 3, 28), "common"),
                  Era("文亀", "Bunnki", date(1501, 3, 28), date(1504, 3, 26), "common"),
                  Era("永正", "Eishou", date(1504, 3, 26), date(1521, 10, 3), "common"),
                  Era("大永", "Daiei", date(1521, 10, 3), date(1528, 9, 13), "common"),
                  Era("享禄", "Kyouroku", date(1528, 9, 13), date(1532, 9, 8), "common"),
                  Era("天文", "Tennbunn", date(1532, 9, 8), date(1555, 11, 17), "common"),
                  Era("弘治", "Kouji", date(1555, 11, 17), date(1558, 3, 28), "common"),
                  Era("永禄", "Eiroku", date(1558, 3, 28), date(1570, 6, 6), "common"),
                  Era("元亀", "Gennki", date(1570, 6, 6), date(1573, 9, 4), "common"),
                  Era("天正", "Tennshou", date(1573, 9, 4), date(1593, 1, 10), "common"),
                  Era("文禄", "Bunnroku", date(1593, 1, 10), date(1596, 12, 16), "common"),
                  Era("慶長", "Keichou", date(1596, 12, 16), date(1615, 9, 5), "common"),
                  Era("元和", "Genna", date(1615, 9, 5), date(1624, 4, 17), "common"),
                  Era("寛永", "Kannei", date(1624, 4, 17), date(1645, 1, 13), "common"),
                  Era("正保", "Syouhou", date(1645, 1, 13), date(1648, 4, 7), "common"),
                  Era("慶安", "Keian", date(1648, 4, 7), date(1652, 10, 20), "common"),
                  Era("承応", "Jouou", date(1652, 10, 20), date(1655, 5, 18), "common"),
                  Era("明暦", "Meireki", date(1655, 5, 18), date(1658, 8, 21), "common"),
                  Era("万治", "Manji", date(1658, 8, 21), date(1661, 5, 23), "common"),
                  Era("寛文", "Kannbunn", date(1661, 5, 23), date(1673, 10, 30), "common"),
                  Era("延宝", "Empou", date(1673, 10, 30), date(1681, 11, 9), "common"),
                  Era("天和", "Tenna", date(1681, 11, 9), date(1684, 4, 5), "common"),
                  Era("貞享", "Joukyou", date(1684, 4, 5), date(1688, 10, 23), "common"),
                  Era("元禄", "Genroku", date(1688, 10, 23), date(1704, 4, 16), "common"),
                  Era("宝永", "Houei", date(1704, 4, 16), date(1711, 6, 11), "common"),
                  Era("正徳", "Syoutoku", date(1711, 6, 11), date(1716, 8, 9), "common"),
                  Era("享保", "Kyouhou", date(1716, 8, 9), date(1736, 6, 7), "common"),
                  Era("元文", "Gennbunn", date(1736, 6, 7), date(1741, 4, 12), "common"),
                  Era("寛保", "Kampou", date(1741, 4, 12), date(1744, 4, 3), "common"),
                  Era("延享", "Enkyou", date(1744, 4, 3), date(1748, 8, 5), "common"),
                  Era("寛延", "Kannenn", date(1748, 8, 5), date(1751, 12, 14), "common"),
                  Era("宝暦", "Houreki", date(1751, 12, 14), date(1764, 6, 30), "common"),
                  Era("明和", "Meiwa", date(1764, 6, 30), date(1772, 12, 10), "common"),
                  Era("安永", "Annei", date(1772, 12, 10), date(1781, 4, 25), "common"),
                  Era("天明", "Tennmei", date(1781, 4, 25), date(1789, 2, 19), "common"),
                  Era("寛政", "Kannsei", date(1789, 2, 19), date(1801, 3, 19), "common"),
                  Era("享和", "Kyouwa", date(1801, 3, 19), date(1804, 3, 22), "common"),
                  Era("文化", "Bunnka", date(1804, 3, 22), date(1818, 5, 26), "common"),
                  Era("文政", "Bunnsei", date(1818, 5, 26), date(1831, 1, 23), "common"),
                  Era("天保", "Tenmpou", date(1831, 1, 23), date(1845, 1, 9), "common"),
                  Era("弘化", "Kouka", date(1845, 1, 9), date(1848, 4, 1), "common"),
                  Era("嘉永", "Kaei", date(1848, 4, 1), date(1855, 1, 15), "common"),
                  Era("安政", "Ansei", date(1855, 1, 15), date(1860, 4, 8), "common"),
                  Era("万延", "Mannei", date(1860, 4, 8), date(1861, 3, 29), "common"),
                  Era("文久", "Bunnkyuu", date(1861, 3, 29), date(1864, 3, 27), "common"),
                  Era("元治", "Genji", date(1864, 3, 27), date(1865, 5, 1), "common"),
                  Era("慶応", "Keiou", date(1865, 5, 1), date(1868, 10, 23), "common"),
                  Era("明治", "Meiji", date(1868, 1, 23), date(1912, 7, 30), "common"),
                  Era("大正", "Taishou", date(1912, 7, 30), date(1926, 12, 24), "common"),
                  Era("昭和", "Shouwa", date(1926, 12, 25), date(1989, 1, 8), "common"),
                  Era("平成", "Heisei", date(1989, 1, 8), date(2019, 5, 1), "common"),
                  Era("令和", "Reiwa", date(2019, 5, 1), None, "common")
                  ]

    era_daikakuji = [Era("元徳", "Gentoku", date(1329, 9, 30), date(1331, 9, 19), "daikakuji"),
                     Era("元弘", "Genkou", date(1331, 9, 19), date(1334, 3, 13), "daikakuji"),
                     Era("建武", "Kenmu", date(1334, 3, 13), date(1336, 4, 19), "daikakuji"),
                     Era("延元", "Engen", date(1336, 4, 19), date(1340, 6, 2), "daikakuji"),
                     Era("興国", "Koukoku", date(1340, 6, 2), date(1347, 1, 28), "daikakuji"),
                     Era("正平", "Syouhei", date(1347, 1, 28), date(1370, 8, 24), "daikakuji"),
                     Era("建徳", "Kentoku", date(1370, 8, 24), date(1372, 5, 9), "daikakuji"),
                     Era("文中", "Bunchuu", date(1372, 5, 9), date(1375, 7, 4), "daikakuji"),
                     Era("天授", "Tenju", date(1375, 7, 4), date(1381, 3, 14), "daikakuji"),
                     Era("弘和", "Kouwa", date(1381, 3, 14), date(1384, 5, 26), "daikakuji"),
                     Era("元中", "Genchuu", date(1384, 5, 26), date(1392, 11, 27), "daikakuji")
                     ]

    era_jimyouin = [Era("元徳", "Gentoku", date(1329, 9, 30), date(1332, 5, 31), "jimyouin"),
                    Era("正慶", "Shoukyou", date(1332, 5, 31), date(1333, 7, 15), "jimyouin"),
                    Era("建武", "Kenmu", date(1334, 3, 13), date(1338, 10, 19), "jimyouin"),
                    Era("暦応", "Ryakuou", date(1338, 10, 19), date(1342, 6, 9), "jimyouin"),
                    Era("康永", "Kouei", date(1342, 6, 9), date(1345, 11, 23), "jimyouin"),
                    Era("貞和", "Jouwa", date(1345, 11, 23), date(1350, 4, 12), "jimyouin"),
                    Era("観応", "Kannou", date(1350, 4, 12), date(1352, 11, 12), "jimyouin"),
                    Era("文和", "Bunna", date(1352, 11, 12), date(1356, 5, 7), "jimyouin"),
                    Era("延文", "Enbun", date(1356, 5, 7), date(1361, 5, 12), "jimyouin"),
                    Era("康安", "Kouan", date(1361, 5, 12), date(1362, 10, 19), "jimyouin"),
                    Era("貞治", "Jouji", date(1362, 10, 19), date(1368, 3, 15), "jimyouin"),
                    Era("応安", "Ouan", date(1368, 3, 15), date(1375, 4, 6), "jimyouin"),
                    Era("永和", "Eiwa", date(1375, 4, 6), date(1379, 4, 17), "jimyouin"),
                    Era("康暦", "Kouryaku", date(1379, 4, 17), date(1381, 3, 28), "jimyouin"),
                    Era("永徳", "Eitoku", date(1381, 3, 28), date(1384, 3, 27), "jimyouin"),
                    Era("至徳", "Sitoku", date(1384, 3, 27), date(1387, 10, 13), "jimyouin"),
                    Era("嘉慶", "Kakyou", date(1387, 10, 13), date(1389, 3, 15), "jimyouin"),
                    Era("康応", "Kouou", date(1389, 3, 15), date(1389, 3, 15), "jimyouin"),
                    Era("明徳", "Meitoku", date(1390, 4, 20), date(1394, 8, 10), "jimyouin")
                    ]

    era_common_daikakuji = sorted(era_common + era_daikakuji)
    era_common_jimyouin = sorted(era_common + era_jimyouin)

    def __init__(self, primary="daikakuji"):
        if primary not in {"daikakuji", "jimyouin"}:
            raise ValueError("only 'daikakuji' or 'jimyouin' are acceptable for argument 'primary'")
        locale.setlocale(locale.LC_ALL, '')
        self.primary = primary

    def era(self, _date):
        if self.primary == "daikakuji":
            ind = bisect_right(self.era_common_daikakuji, _date)
            if ind == 0:
                return None
            if self.era_common_daikakuji[ind - 1]._in(_date):
                return self.era_common_daikakuji[ind - 1]
            return None
        else:
            ind = bisect_right(self.era_common_jimyouin, _date)
            if ind == 0:
                return None
            if self.era_common_jimyouin[ind - 1]._in(_date):
                return self.era_common_jimyouin[ind - 1]
            return None

    def era_match(self, value, key=lambda x: x, cmp=lambda x, y: x._in(y), error="warn"):
        """
        Return all Era objects stored in self.era_common or self.era_daikakuji or self.era_jimyouin which
        cmp(key(Era), value) is True.
        if key is not provided, key is lambda x: x
        if cmp is not provided, cmp is lambda x, y: x._in(y)

        error sets error level
            "ignore": ignore all errors occurred while running compare
            "warn": just warn error - default
            "raise": raise any errors

        Default, this will return eras which contains given value(which must be datetime.date) in them.
        """
        eras = []
        for era in self.era_common + self.era_daikakuji + self.era_jimyouin:
            try:
                if cmp(key(era), value):
                    eras.append(era)
            except Exception:
                if error == "warn":
                    warn("There was error running cmp(key(Era), value) but skipped because ignore_error=True")
                elif error == "raise":
                    raise
        return eras

    def strftime(self, _date, _format, _type=None, allow_before=False):
        """
        %-E: Kanji era name
        %-A: Alphabet era name
        %-a: First letter of alphabet era name
        %-o: Year of corresponding era
        %-O: Year of corresponding era. But return "元" for the first year
        + datetime.strftime's format

        allow_before: object can be converted to bool. If it's true and the given _date if before than self,start,
                     %-o and %-O will be "Unknown". If False, raise an ValueError Default: False
        """
        if not _type:
            era = self.era(_date)
        elif _type == "daikakuji":
            era = self.daikaku_era(_date)
        elif _type == "jimyouin":
            era = self.jimyouin_era(_date)
        else:
            raise ValueError("_type must be 'daikakuji' or 'jimyouin'")
        try:
            year = _date.year - era.start.year + 1
            rep = {"%-E": era.kanji, "%-A": era.english, "%-a": era.english[0], "%-s": era.english_shorten_vowel,
                   "%-o": str(year % 100).zfill(2),
                   "%-O": "元" if year == 1 else str(year % 100).zfill(2)}
        except AttributeError:
            try:
                rep = {"%-E": "不明", "%-A": "Unknown", "%-a": "U", "%-s": "Unknown", "%-o": str(year % 100).zfill(2),
                       "%-O": "元" if year == 1 else str(year % 100).zfill(2)}
            except (AttributeError, UnboundLocalError):
                if not allow_before:
                    raise ValueError("Given date is too early to format")
                rep = {"%-E": "不明", "%-A": "Unknown", "%-a": "U", "%-s": "Unknown", "%-o": "Unknown",
                       "%-O": "Unknown"}

        rep = dict((re.escape(k), str(v)) for k, v in rep.items())
        pattern = re.compile("|".join(rep.keys()))
        return _date.strftime(pattern.sub(lambda m: rep[re.escape(m.group(0))], _format))

    def daikaku_era(self, _date):
        ind = bisect_right(self.era_common_daikakuji, _date)
        if ind == 0:
            return None
        if self.era_common_daikakuji[ind - 1]._in(_date):
            return self.era_common_daikakuji[ind - 1]
        return None

    def jimyouin_era(self, _date):
        ind = bisect_right(self.era_common_jimyouin, _date)
        if ind == 0:
            return None
        if self.era_common_jimyouin[ind - 1]._in(_date):
            return self.era_common_jimyouin[ind - 1]
        return None
