# -*- coding: utf-8 -*-

import datetime
from stock_rogue_app.strategies import MainStrategy
from stock_rogue_app.strategies import NaiveStrategy
from stock_rogue_app.strategies import StableStrategy
from stock_rogue_app.strategies import AverageStrategy
from stock_rogue_app.strategies.futureDataGenerator import generate_future_data
from stock_rogue_app.strategies.machine_learning_strategies import strategy_linear_regression
from stock_rogue_app.strategies.machine_learning_strategies import auxiliary_functions
# Zakladam, ze company_data zawiera tylko spolke company_name + company_data jest posortowane malejaco po datach
#        Tzn. od najwczesniejszej do najpozniejszej. Wynikiem jest tablica rozmiaru predict_interval + 1, gdzie
#        w ostatnim polu jest przewidywany sredni kurs przyszly (tzn. wycena ile de facto jest spolka warta).
#        Wyliczane wartosci przyszle to: kurs_biezacy, kurs_min, kurs_max.
from stock_rogue_app.strategies.machine_learning_strategies import strategy_linear_regression


# Zakladam, ze company_data zawiera tylko spolke company_name + company_data
# jest posortowane malejaco po datach, tzn. od najwczesniejszej do najpozniejszej.
# Wynikiem jest tablica rozmiaru predict_interval + 1, gdzie w ostatnim polu
# jest przewidywany sredni kurs przyszly (tzn. wycena ile de facto jest spolka warta).
# Wyliczane wartosci przyszle to: kurs_biezacy, kurs_min, kurs_max.
#

def estimate_values(comp_id, predict_interval, strategy, company_data):
    '''Funkcja zwraca przewidywane kursy akcji na podstawie wybranej strategii.'''

    result = generate_future_data(comp_id, predict_interval, datetime.date.today())

    # Zaimplementowane strategie patrzą jedynie 50 dni wstecz
    number_of_past_days = min(50, len(company_data))
    if strategy == 'A':
        future_values = MainStrategy.predict_future(comp_id,
                                                    number_of_past_days,
                                                    company_data,
                                                    result)
    elif strategy == 'B':
        future_values = NaiveStrategy.predict_future(comp_id,
                                                     number_of_past_days,
                                                     company_data,
                                                     result)
    elif strategy == 'C':
        future_values = StableStrategy.predict_future(comp_id,
                                                      number_of_past_days,
                                                      company_data,
                                                      result)
    elif strategy == 'D':
        future_values = AverageStrategy.predict_future(comp_id,
                                                       number_of_past_days,
                                                       company_data,
                                                       result)

    elif strategy == 'E':
        table = auxiliary_functions.default_table_picker(company_data)
        future_values = strategy_linear_regression.predict_future(company_data=company_data,
                                                                  result=result,
                                                                  days_past=table)

    elif strategy == 'F':
        table = auxiliary_functions.default_table_picker(company_data,
                                                         True)

        future_values = strategy_linear_regression.predict_future(company_data=company_data,
                                                                  result=result,
                                                                  days_past=table,
                                                                  poly_reg=True)

    elif strategy == 'G':
        table = auxiliary_functions.default_table_picker(company_data, True)

        future_values = strategy_linear_regression.predict_future(company_data=company_data,
                                                                  result=result,
                                                                  days_past=table,
                                                                  huber_reg=True)

    else:
        future_values = StableStrategy.predict_future(comp_id,
                                                      number_of_past_days,
                                                      company_data,
                                                      result)
    return future_values
