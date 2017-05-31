# -*- coding: utf-8 -*-

'''Szereg funkcji preprocessingowych dla strategii korzystających z algorytmów
   machine learningowych. Odpowiedzialne m. in. za wektoryzację danych'''
from .auxiliary_functions import collect_wig_data
from sklearn.preprocessing import PolynomialFeatures
# Pomocnicze funkcje do obliczania procentowej zmiany kursu

def percentage_change(prev_value, curr_value):
    '''Zwraca procentową zmianę kursu'''

    return ((curr_value - prev_value) / prev_value) * 100

def percentage_change_dict(stock_dict, field, days_past):
    '''Zwraca wektor procentowej zmiany kursu'''

    def index_oor_handle(i):
        return min(len(stock_dict) - 1, i + days_past)

    percentage_list = [percentage_change(stock_dict[index_oor_handle(i)][field],
                                         stock_dict[i][field])
                       for i in range(max(-days_past, 1), len(stock_dict))]

    return percentage_list

def percentage_change_days(stock_dict, field, days_past_vec, value):
    '''Zwraca wektor procentowej zmiany kursu dla value
        względem wszystkich dni w days_past_vec'''

    def index_oor_handle(days_past):
        return min(len(stock_dict) - 1, days_past)

    value_changes = [percentage_change(stock_dict[index_oor_handle(days)][field],
                                         value) for days in days_past_vec]

    return value_changes

# Pomocnicze funkcje zapisujące nie procentowe zmiany, tylko po
# kursy sprzed odpowiedniej liczby dni

def change_dict(stock_dict, field, days_past):
    '''Zwraca wektor kursów sprzed days_past dni'''

    def index_oor_handle(i):
        return min(len(stock_dict) - 1, i + days_past)

    old_values_list = [stock_dict[index_oor_handle(i)][field]
                       for i in range(max(-days_past, 1), len(stock_dict))]

    return old_values_list

def change_days(stock_dict, field, days_past_vec):
    '''Zwraca wektor kursow sprzed wszystkich dni w days_past_vec'''

    def index_oor_handle(days_past):
        return min(len(stock_dict) - 1, days_past)

    value_changes = [stock_dict[index_oor_handle(days)][field]
                     for days in days_past_vec]

    return value_changes


# Funkcje zwracające training set

def vectorize_data(stock_dict, days_list, field):
    '''Funkcja przygotowująca macierz dla tablicy słowników
        z danymi giełdowymi stock_dict, wymiaru liczba dni x len(days_list)'''

    y_vector = percentage_change_dict(stock_dict, field, -1)
    y_vector = [ 100 / (100 + el) for el in y_vector]

    X_matrix = [[] for el in stock_dict[:-1]]
    for day in days_list:
        percentage_changes = percentage_change_dict(stock_dict, field, day)

        for i in range(len(stock_dict[:-1])):
            X_matrix[i] += [percentage_changes[i]]

    return (X_matrix, y_vector)



def raw_vectorize_data(stock_dict, days_list, field):
    '''Funkcja przygotowująca macierz dla tablicy słowników
            z danymi giełdowymi stock_dict, wymiaru liczba dni x len(days_list),
            nie zapisuje procentowej zmiany, tylko archiwalne ceny kursów'''

    y_vector = change_dict(stock_dict, field, -1)

    X_matrix = [[] for el in stock_dict[:-1]]
    for day in days_list:
        changes = change_dict(stock_dict, field, day)

        for i in range(len(stock_dict[:-1])):
            X_matrix[i] += [changes[i]]

    return (X_matrix, y_vector)

def prepare_data(company_data, days_past, wig_data=True, poly_reg=False):
    "Funkcja przygotowująca dane do formy wymaganej przez modele machine learningowe"

    FIELDS = ("kurs_min", "kurs_max", "kurs_biezacy")
    X_matrix = {}
    y_vector = {}

    for el in FIELDS:
        X_matrix[el], y_vector[el] = vectorize_data(company_data,
                                                    days_past,
                                                    el)

    if wig_data:
        X_matrix_wig = {}
        y_vector_wig = {}
        wig = collect_wig_data()
        for el in FIELDS:
            X_matrix_wig[el], y_vector_wig[el] = vectorize_data(wig,
                                                                days_past,
                                                                el)

            X_matrix[el] += X_matrix_wig[el]
            y_vector[el] += y_vector_wig[el]

    X_matrix_combined = [X_matrix[FIELDS[0]][i] +
                         X_matrix[FIELDS[1]][i] +
                         X_matrix[FIELDS[2]][i]
                         for i in range(len(X_matrix[FIELDS[0]]))]

    if poly_reg:
        poly = PolynomialFeatures(2)
        poly.fit_transform(X_matrix_combined)

    return (X_matrix_combined, y_vector)
