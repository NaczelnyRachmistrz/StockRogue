from StockRogue.downloader import update_data
from stock_rogue_app.models import Dane
from datetime import datetime
from dateutil import parser
import os
import csv

def daily_update():
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

# Sets up stock data since 01.01.2010
def database_set_up():

    # Directory with archive stock files
    arch_dir = "../spolki"
    iter = 0
    for company in os.listdir(arch_dir):
        iter += 1
        with open("../spolki/" + company, newline='') as csvfile:
            print(iter, company)
            reader = csv.reader(csvfile)
            insert_list = []
            for row in reader:
                if row[0] != "<TICKER>":
                    if int(row[1]) > 20120000:
                        insert_list.append(Dane(
                            nazwa=row[0],
                            kurs_otwarcia=float(row[2]),
                            data=parser.parse(row[1]),
                            kurs_max=float(row[3]),
                            kurs_min=float(row[4]),
                            kurs_biezacy=float(row[5]),
                            obrot=float(row[6]))
                            )
            Dane.objects.bulk_create(insert_list)
