## Naive strategy that looks only at one day past.
##

from stock_rogue_app.strategies import strategyA


def predict_future(company_name, number_of_past_days, company_data, result):

    ## TODO : trnasform into class
    ## Only 5 days past - we take the arithmetic average = (alpha = 0, beta = 1, gamma = 1)
    strategy_data = {}
    strategy_data['number_of_past_days'] = 5
    #może powinniśmy przekazywać liczbę dni jako argument, ewentualnie można to opakować bardziej
    strategy_data['alpha'] = 0.0
    strategy_data['beta'] = 1.0 - strategy_data['alpha']
    # gamma from range [0, 1] - 1 = all days are equal
    strategy_data['gamma'] = 1
    strategy_data['company_name'] = company_name
    #sum_volume można wydzielić ze strategii A, skoro jest wykorzystywane nie tylko tam
    strategy_data['sum_volume'] = strategyA.sum_volume(company_name, number_of_past_days, company_data)

    avg_values = {}
    avg_values['kurs_min'] = strategyA.predict_future_average_name_value(strategy_data, company_data, 'kurs_min')
    avg_values['kurs_max'] = strategyA.predict_future_average_name_value(strategy_data, company_data, 'kurs_max')
    avg_values['kurs_biezacy'] = strategyA.predict_future_average_name_value(strategy_data, company_data, 'kurs_biezacy')

    for day in result:
        day['kurs_min'] = avg_values['kurs_min']
        day['kurs_max'] = avg_values['kurs_max']
        day['kurs_biezacy'] = avg_values['kurs_biezacy']
    return result
    pass
