# -*- coding: utf-8 -*-
from datetime import timedelta, date
from stock_rogue_app.models import Dane
# This prepares and returns the list of days for a specific company.
# It omits only weekends.
def generate_future_data(company_name, predict_interval, start_date):
    date = start_date
    result = [{}] * (predict_interval + 1)
    for idx in range(predict_interval):
        date += timedelta(1)
        while date.weekday() > 4:
            date += timedelta(1)

        #proponuję zmienić na:
        # result[idx] = Dane.objects.get(nazwa=company_name, data=date).__dict__
        result[idx] = {'nazwa' : company_name,
                       'data' : date,
                       'kurs_otwarcia' : 0.0,
                       'kurs_max' : 0.0,
                       'kurs_min' : 0.0,
                       'kurs_biezacy' : 0.0,
                       'obrot' : 0
                       }
    return result
