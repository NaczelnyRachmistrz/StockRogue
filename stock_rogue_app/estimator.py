# -*- coding: utf-8 -*-

import datetime
from stock_rogue_app.strategies import strategyA
from stock_rogue_app.strategies import strategyB
from stock_rogue_app.strategies import strategyC
from stock_rogue_app.strategies import strategyD
from stock_rogue_app.strategies.futureDataGenerator import generate_future_data

# Zakladam, ze company_data zawiera tylko spolke company_name + company_data jest posortowane malejaco po datach
#        Tzn. od najwczesniejszej do najpozniejszej. Wynikiem jest tablica rozmiaru predict_interval + 1, gdzie
#        w ostatnim polu jest przewidywany sredni kurs przyszly (tzn. wycena ile de facto jest spolka warta).
#        Wyliczane wartosci przyszle to: kurs_biezacy, kurs_min, kurs_max.
#

def estimate_values(comp_id, predict_interval, strategy, company_data):
    '''Funkcja zwraca przewidywane kursy akcji na podstawie wybranej strategii.'''

    result = generate_future_data(comp_id, predict_interval, datetime.date.today())

    # Zaimplementowane strategie patrzą jedynie 50 dni wstecz
    number_of_past_days = min(50, len(company_data))
    if strategy == 'A':
        future_values = strategyA.predict_future(comp_id,
                                                 number_of_past_days,
                                                 company_data,
                                                 result)
    elif strategy == 'B':
        future_values = strategyB.predict_future(comp_id,
                                                 number_of_past_days,
                                                 company_data,
                                                 result)
    elif strategy == 'C':
        future_values = strategyC.predict_future(comp_id,
                                                 number_of_past_days,
                                                 company_data,
                                                 result)
    elif strategy == 'D':
        future_values = strategyD.predict_future(comp_id,
                                                 number_of_past_days,
                                                 company_data,
                                                 result)
    # strategyC
    else:
        future_values = strategyC.predict_future(comp_id,
                                                 number_of_past_days,
                                                 company_data,
                                                 result)
    return future_values
