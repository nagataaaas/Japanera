from japanera import Japanera

janera = Japanera()
print(janera.strptime("平成31年04月16日", "%-E%-O年%m月%d日"))
print(janera.strptime("宝亀07年04月16日", "%-E%-O年%m月%d日"))