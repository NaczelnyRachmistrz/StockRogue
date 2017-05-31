## Stable values equal to most up-to-date value.
##


def predict_future(company_name, number_of_past_days, company_data, result):
    for day in result:
        day['kurs_biezacy'] = company_data[0]['kurs_biezacy']
        day['kurs_min'] = company_data[0]['kurs_min']
        day['kurs_max'] = company_data[0]['kurs_max']

    return result
    pass