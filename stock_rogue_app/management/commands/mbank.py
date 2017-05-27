from django.core.management import BaseCommand

from stock_rogue_app.models import Dane


class Command(BaseCommand):
    def handle(self, *args, **options):
        for d in Dane.objects.filter(spolka__skrot="MBANK"):
            print(str(d.data) + " " + "MBANK " +  "MAX: " + str(d.kurs_max) + " MIN: " + str(d.kurs_min))