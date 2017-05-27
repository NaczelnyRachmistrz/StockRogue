from django.core.management.base import BaseCommand
from StockRogue.settings import BASE_DIR
from stock_rogue_app.models import Dane, Spolka
import os
import csv
from dateutil import parser
from StockRogue.downloader import update_data

def companies_and_indexes_names():
    all = update_data()
    companies = []
    indexes = []

    for position in all:
        if position['nazwa'].__contains__('WIG'):
            indexes.append(position['nazwa'])
        else:
            companies.append(position['nazwa'])

    return companies, indexes


def choose_type(name, companies, indexes):
    if name in companies:
        return Spolka.SPOLKA
    elif name in indexes:
        return Spolka.INDEKS
    else:
        return Spolka.INNE


class Command(BaseCommand):
    def handle(self, *args, **options):
        '''Wypełnia bazę danych danymi od 2016 roku.'''

        # Folder z archiwalnymi notowaniami giełdowymi.
        path = os.path.join(BASE_DIR, "data", "spolki")

        # Pobieramy listę spółek i indeksów
        companies, indexes = companies_and_indexes_names()

        for company in os.listdir(path):
            with open(os.path.join(path, company), newline='') as csvfile:
                reader = csv.reader(csvfile)
                insert_list = []
                for row in reader:
                    if row[0] != "<TICKER>":
                        #Pobieramy notowania spółek od 1 stycznia 2016 roku
                        if int(row[1]) > 2016 * 100 * 100:
                            print(row[0] + " " + row[1])

                            s, created = Spolka.objects.get_or_create(
                             skrot=row[0], typ=choose_type(row[0], companies, indexes)
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