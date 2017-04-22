## Naive strategy that looks only at one day past.
##

from stock_rogue_app.strategies import strategyA


def predict_future(company_name, number_of_past_days, company_data, result):
    result = strategyA.predict_future(company_name, 1, company_data, result)
    return result
    pass
