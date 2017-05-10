from django.conf import settings
from django.core.management.base import BaseCommand
from stock_rogue_app.models import Dane, Spolka
import os
import csv
from dateutil import parser

class Command(BaseCommand):
    def handle(self, *args, **options):
        '''Wypełnia bazę danych danymi od 2010 roku.'''

        # Folder z archiwalnymi notowaniami giełdowymi.
        path = os.path.join(settings.BASE_DIR, "data", "spolki")

        for company in os.listdir(path):
            with open(os.path.join(path, company), newline='') as csvfile:
                reader = csv.reader(csvfile)
                insert_list = []
                for row in reader:
                    if row[0] != "<TICKER>":
                        if int(row[1]) > 2010000:
                            print(row[0] + " " + row[1])

                            s, created = Spolka.objects.get_or_create(
                             skrot=row[0]
                            )

                            insert_list.append(Dane(
                                spolka=s,
                                kurs_otwarcia=float(row[2]),
                                data=parser.parse(row[1]),
                                kurs_max=float(row[3]),
                                kurs_min=float(row[4]),
                                kurs_biezacy=float(row[5]),
                                obrot=float(row[6]))
                            )
                Dane.objects.bulk_create(insert_list)