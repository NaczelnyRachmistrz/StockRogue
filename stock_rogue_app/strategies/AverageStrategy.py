# -*- coding: utf-8 -*-

## Naive strategy that looks only at one day past.
##

from stock_rogue_app.strategies import MainStrategy

from stock_rogue_app.strategies.StrategyDataContainers import StrategyData


def predict_future(company_name, number_of_past_days, company_data, result):

    ## Only 5 days past - we take the arithmetic average = (alpha = 0, beta = 1, gamma = 1)
    s = StrategyData(company_name, company_data, 5, 0.0, 1.0)

    avg_values = {}
    avg_values['kurs_min'] = s.predict_future_average_name_value('kurs_min')
    avg_values['kurs_max'] = s.predict_future_average_name_value('kurs_max')
    avg_values['kurs_biezacy'] = s.predict_future_average_name_value('kurs_biezacy')
    for day in result:
        day['kurs_min'] = avg_values['kurs_min']
        day['kurs_max'] = avg_values['kurs_max']
        day['kurs_biezacy'] = avg_values['kurs_biezacy']
    return result
    pass
