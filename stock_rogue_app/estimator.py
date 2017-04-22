import datetime
from stock_rogue_app.strategies import strategyA
from stock_rogue_app.strategies import strategyB
from stock_rogue_app.strategies import strategyC
from stock_rogue_app.strategies import strategyD
from stock_rogue_app.strategies.futureDataGenerator import generate_future_data

##TODO : Zakladam, ze company_data zawiera tylko spolke company_name + company_data jest posortowane malejaco po datach
#        Tzn. od najwczesniejszej do najpozniejszej. Wynikiem jest tablica rozmiaru predict_interval + 1, gdzie
#        w ostatnim polu jest przewidywany sredni kurs przyszly (tzn. wycena ile de facto jest spolka warta).
#        Wyliczane wartosci przyszle to: kurs_biezacy, kurs_min, kurs_max
##
def estimate_values(company_name, predict_interval, strategy, company_data):
    # We assume first there is only one strategy

    result = generate_future_data(company_name, predict_interval, datetime.date.today())

    # We assume we look only on max 30 days back
    number_of_past_days = min(30, len(company_data))
    if strategy == 'A':
        future_values = strategyA.predict_future(company_name,
                                                 number_of_past_days,
                                                 company_data,
                                                 result)
    elif strategy == 'B':
        future_values = strategyB.predict_future(company_name,
                                                 number_of_past_days,
                                                 company_data,
                                                 result)
    elif strategy == 'C':
        future_values = strategyC.predict_future(company_name,
                                                 number_of_past_days,
                                                 company_data,
                                                 result)
    elif strategy == 'D':
        future_values = strategyD.predict_future(company_name,
                                                 number_of_past_days,
                                                 company_data,
                                                 result)
    # strategyC
    else:
        future_values = strategyC.predict_future(company_name,
                                                 number_of_past_days,
                                                 company_data,
                                                 result)
    return future_values
    pass
