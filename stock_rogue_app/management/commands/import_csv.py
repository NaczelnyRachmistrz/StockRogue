from django.core.management.base import BaseCommand
from stock_rogue_app.models import Dane, Spolka
from StockRogue.downloader import update_data

class Command(BaseCommand):
    def handle(self, *args, **options):
        '''Funkcja uzupełniająca bazę danych o nowe dane.'''
        today = update_data()

        for el in today:
            print("Tworzymy obiekt %s w bazie danych" % el)
            s, created = Spolka.objects.get_or_create(
                skrot=el["nazwa"]
            )

            _, created = Dane.objects.get_or_create(
                spolka=s,
                data=el["data"],
                kurs_otwarcia=el["kurs_otwarcia"],
                kurs_max=el["kurs_max"],
                kurs_min=el["kurs_min"],
                kurs_biezacy=el["kurs_biezacy"],
                obrot=el["obrot"]
            )