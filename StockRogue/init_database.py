from StockRogue.downloader import update_data
from stock_rogue_app.models import Dane
today = update_data()

for el in today:
    _, created = Dane.objects.get_or_create(
        nazwa=el["nazwa"],
        data=el["data"],
        kurs_otwarcia=el["kurs_otwarcia"],
        kurs_max=el["kurs_max"],
        kurs_min=el["kurs_min"],
        kurs_biezacy=el["kurs_biezacy"],
        obrot=el["obrot"]
    )