from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from stock_rogue_app.models import Dane, Spolka
from StockRogue.downloader import update_data

class Command(BaseCommand):
    def handle(self, *args, **options):
        for d in Dane.objects.all():
            _, created = Spolka.objects.get_or_create(skrot=d.nazwa)
            if created == 1:
                print("Tworzymy spolke: " + d.nazwa)