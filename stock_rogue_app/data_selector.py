# -*- coding: utf-8 -*-

from stock_rogue_app.models import Dane


def select_data(nazwa):
    '''Funkcja odpowiedzialna za pobieranie z bazy danych informacji dotyczących wybranej spółki.'''

    result = Dane.objects.filter(spolka__skrot=nazwa)
    result = result.values()[::-1]
    return result

def select_period_data(name, start_data):
    '''Funkcja odpowiedzialna za pobieranie z bazy danych informacji dotyczących wybranej spółki.'''

    result_temp = Dane.objects.filter(spolka__skrot=name)
    result = result_temp.filter(data__gte=start_data)

    return (result_temp.values()[::-1], len(result) - 1)