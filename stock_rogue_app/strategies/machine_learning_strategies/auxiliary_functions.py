# -*- coding: utf-8 -*-

#
# Dodatkowe funkcje wykorzystywane do algorytmów machine learningowych
#
from stock_rogue_app import data_selector

DEFAULT_TABLE = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 25,
                 30, 35, 40, 45, 50, 60, 70, 80, 90, 100, 120, 140, 160,
                 180, 200, 250, 300, 350, 450, 550, 700, 850, 1000, 1400)

DEFAULT_TABLE_MEDIUM = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12,
                        14, 16, 18, 20, 25, 30, 35, 40, 45, 50,
                        60, 70, 80, 90, 100, 120, 140, 160)

DEFAULT_TABLE_SMALL = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12,
                       14, 16, 18, 20, 25, 30, 35, 40)

DEFAULT_TABLE_MINIMUM = (0, 1, 2, 3, 4, 5, 7, 9, 11, 13, 15)

DEFAULT_TABLE_POLY = (0, 1, 2, 3, 4, 5, 10, 30, 60, 180, 360)

def default_table_picker(company_data, poly_reg=False):
    '''Wybiera domyślną tablicę w zależności od liczby rekordów
     danej spółki'''

    if poly_reg:
        return DEFAULT_TABLE_POLY

    if len(company_data) < 100:
        return DEFAULT_TABLE_MINIMUM
    if len(company_data) < 250:
        return DEFAULT_TABLE_SMALL
    elif len(company_data) < 750:
        return DEFAULT_TABLE_MEDIUM
    else:
        return DEFAULT_TABLE

def collect_wig_data():
    '''Funkcja pobiera dane dotyczące indeksu WIG'''
    return data_selector.select_data("WIG")