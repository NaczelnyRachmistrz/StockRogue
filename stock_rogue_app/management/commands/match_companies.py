from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from stock_rogue_app.models import Dane, Spolka
from StockRogue.downloader import update_data

class Command(BaseCommand):
    def handle(self, *args, **options):
        for d in Dane.objects.all():
            print(d.nazwa)
            d.spolka = Spolka.objects.get(skrot=d.nazwa)
            d.save()