# -*- coding: utf-8 -*-

from stock_rogue_app.models import Dane


def select_data(nazwa):
    '''Funkcja odpowiedzialna za pobieranie z bazy danych informacji dotyczących wybranej spółki.'''

    result = Dane.objects.filter(spolka__skrot=nazwa)
    result = result.values()[::-1]
    return result