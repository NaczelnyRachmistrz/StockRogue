import csv
import requests
from datetime import datetime
from dateutil import parser

# Najnowsza sesja
CSV_URL = 'http://bossa.pl/pub/ciagle/mstock/sesjacgl/sesjacgl.prn'

def update_data():

    with requests.Session() as s:
        download = s.get(CSV_URL)

        decoded_content = download.content.decode('utf-8')

        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        today_data = [{"nazwa":row[0], "kurs_otwarcia":float(row[2]), "data":parser.parse(row[1]), "kurs_max": float(row[3]),
                "kurs_min": float(row[4]), "kurs_biezacy": float(row[5]), "obrot": float(row[6])} for row in my_list]
        return today_data