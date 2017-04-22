# {"nazwa":row[0], "kurs_otwarcia":float(row[2]), "data":parser.parse(row[1]), "kurs_max": float(row[3]),
#                 "kurs_min": float(row[4]), "kurs_bieżący": float(row[5]), "obrót": float(row[6])}
from datetime import timedelta, date

# This prepares and returns the list of days for a specific company.
# It omits only weekends.
def generate_future_data(company_name, predict_interval, start_date):
    date = start_date
    result = [{}] * (predict_interval + 1)
    for idx in range(predict_interval):
        date += timedelta(1)
        while date.weekday() > 4:
            date += timedelta(1)
        # print(date)
        result[idx] = {'nazwa' : company_name,
                       'data' : date,
                       'kurs_otwarcia' : 0.0,
                       'kurs_max' : 0.0,
                       'kurs_min' : 0.0,
                       'kurs_bieżący' : 0.0,
                       'obrót' : 0
                       }
    return result
