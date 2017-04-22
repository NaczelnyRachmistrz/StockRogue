# {"nazwa":row[0], "kurs_otwarcia":float(row[2]), "data":parser.parse(row[1]), "kurs_max": float(row[3]),
#                 "kurs_min": float(row[4]), "kurs_bieżący": float(row[5]), "obrót": float(row[6])}
from datetime import timedelta, date

from stock_rogue_app.estimator import estimate_values


def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

# print(date.today())
start_date = date(2017, 3, 12)
end_date = date(2017, 4, 21)
max_date_idx = int ((end_date - start_date).days)
dates = [date(2017, 3, 12)] * (max_date_idx)
for idx, single_date in enumerate(daterange(start_date, end_date)):
    # print(single_date.strftime("%Y-%m-%d"))
    dates[max_date_idx - idx - 1] = single_date.strftime("%Y-%m-%d")
    # print(max_date_idx - idx - 1)

company_data = []
# start_date = 2017-04-21
for i in range(40):
    # print(i)
    d = {}
    d['nazwa'] = 'A'
    d['kurs_otwarcia'] = 10.00 + i / 10
    d['kurs_min'] = 9.00 + i / 10
    d['kurs_max'] = 11.00 + i / 10
    d['kurs_bieżący'] = 10.50 + i / 10
    d['obrót'] = 1 + i
    d['data'] = dates[i]
    print(d)
    company_data.append(d)

predicted_data = estimate_values('A', 30, 'D', company_data)
for day in predicted_data:
    print(day)
# print(predicted_data[len(predicted_data) - 1])
