# -*- coding: utf-8 -*-

'''Szereg funkcji preprocessingowych dla strategii korzystających z algorytmów
   machine learningowych. Odpowiedzialne m. in. za wektoryzację danych'''


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



