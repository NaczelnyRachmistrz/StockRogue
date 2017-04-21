from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from stock_rogue_app.models import Dane
from StockRogue.downloader import update_data

class Command(BaseCommand):
    def handle(self, *args, **options):
        today = update_data()

        for el in today:
            print("Tworzymy obiekt %s w bazie danych" % el)
            _, created = Dane.objects.get_or_create(
                nazwa=el["nazwa"],
                data=el["data"],
                kurs_otwarcia=el["kurs_otwarcia"],
                kurs_max=el["kurs_max"],
                kurs_min=el["kurs_min"],
                kurs_biezacy=el["kurs_biezacy"],
                obrot=el["obrot"]
            )