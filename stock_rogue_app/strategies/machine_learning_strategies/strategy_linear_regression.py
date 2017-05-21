# -*- coding: utf-8 -*-

from sklearn import linear_model

from . import vector_preprocess

from . import auxiliary_functions

def predict_future(company_data, result, days_past, wig_data=True):
    '''Prosta strategia wykorzystująca regresję liniową. Przyjmuje za czynniki
        zmiany kursu w stosunku do wartości sprzed liczby dni podanych w tablicy days_past'''

    FIELDS = ("kurs_min", "kurs_max", "kurs_biezacy")
    X_matrix = {}
    y_vector = {}
    lin_model = {}

    company_data_copy = list(company_data)

    for el in FIELDS:
        X_matrix[el], y_vector[el] = vector_preprocess.vectorize_data(company_data,
                                                                      days_past,
                                                                      el)
        lin_model[el] = linear_model.LinearRegression()

    if wig_data:
        X_matrix_wig = {}
        y_vector_wig = {}
        wig = auxiliary_functions.collect_wig_data()
        for el in FIELDS:
            X_matrix_wig[el], y_vector_wig[el] = vector_preprocess.vectorize_data(wig,
                                                             days_past,
                                                             el)

            X_matrix[el] += X_matrix_wig[el]
            y_vector[el] += y_vector_wig[el]

    X_matrix_combined = [X_matrix[FIELDS[0]][i] +
                         X_matrix[FIELDS[1]][i] +
                         X_matrix[FIELDS[2]][i]
                         for i in range(len(X_matrix[FIELDS[0]]))]

    for el in FIELDS:
        lin_model[el].fit(X_matrix_combined,
                          y_vector[el])


    X_vector = {}
    for day in result:
        X_vector.clear()
        for el in FIELDS:
            value = company_data_copy[0][el]
            X_vector[el] = vector_preprocess.percentage_change_days(company_data_copy,
                                                  el,
                                                  days_past,
                                                  value)

        X_vector_combined = X_vector[FIELDS[0]] + \
                            X_vector[FIELDS[1]] + \
                            X_vector[FIELDS[2]]

        for el in  FIELDS:
            value = company_data_copy[0][el]
            day[el] = lin_model[el].predict(X_vector_combined)[0]
            day[el] *= value

        if day["kurs_min"] > day["kurs_max"]:
            day["kurs_min"] = day["kurs_max"]
            day["kurs_biezacy"] = day["kurs_min"]


        company_data_copy = [day] + company_data_copy

    #TODO Dodatkowy rekord, do wywalenia będzie
    result += {}
    return result


def raw_predict_future(company_data, result, days_past):
    '''Prosta strategia wykorzystująca regresję liniową. Przyjmuje za czynniki
        zmiany kursu w stosunku do wartości sprzed liczby dni podanych w tablicy days_past'''

    FIELDS = ("kurs_min", "kurs_max", "kurs_biezacy")
    X_matrix = {}
    y_vector = {}
    lin_model = {}

    company_data_copy = list(company_data)

    for el in FIELDS:
        X_matrix[el], y_vector[el] = vector_preprocess.raw_vectorize_data(company_data,
                                                                          days_past,
                                                                          el)
        lin_model[el] = linear_model.LinearRegression()

    X_matrix_combined = [X_matrix[FIELDS[0]][i] +
                         X_matrix[FIELDS[1]][i] +
                         X_matrix[FIELDS[2]][i]
                         for i in range(len(X_matrix[FIELDS[0]]))]

    for el in FIELDS:
        lin_model[el].fit(X_matrix_combined,
                          y_vector[el])


    X_vector = {}
    for day in result:
        X_vector.clear()
        for el in FIELDS:
            X_vector[el] = vector_preprocess.change_days(company_data_copy,
                                                  el,
                                                  days_past)

        X_vector_combined = X_vector[FIELDS[0]] + \
                            X_vector[FIELDS[1]] + \
                            X_vector[FIELDS[2]]

        for el in  FIELDS:
            day[el] = lin_model[el].predict(X_vector_combined)[0]

        company_data_copy = [day] + company_data_copy

    #TODO Dodatkowy rekord, do wywalenia będzie
    result += {}
    return result


