# -*- coding: utf-8 -*-

from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures

from . import vector_preprocess

from . import auxiliary_functions


def predict_future(company_data, result, days_past,
                   wig_data=True, poly_reg=False, huber_reg=False):
    '''Strategia wykorzystująca różne techniki regresji liniowej. Przyjmuje za czynniki
        zmiany kursu w stosunku do wartości sprzed liczby dni podanych w tablicy days_past'''

    lin_model = {}

    FIELDS = ("kurs_min", "kurs_max", "kurs_biezacy")
    X_matrix_combined, y_vector = vector_preprocess.prepare_data(company_data,
                                                                 days_past,
                                                                 wig_data,
                                                                 poly_reg)

    company_data_copy = list(company_data)

    for el in FIELDS:
        lin_model[el] = linear_model.HuberRegressor() \
            if huber_reg else linear_model.LinearRegression()

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
        if poly_reg:
            X_vector_combined = [X_vector_combined]
            poly = PolynomialFeatures(2)
            poly.fit_transform(X_vector_combined)
            X_vector_combined = X_vector_combined[0]

        for el in FIELDS:
            value = company_data_copy[0][el]
            day[el] = lin_model[el].predict(X_vector_combined)[0]
            day[el] *= value

        if day["kurs_min"] > day["kurs_max"]:
            day["kurs_min"] = day["kurs_max"]
            day["kurs_biezacy"] = day["kurs_min"]

        company_data_copy = [day] + company_data_copy

    # TODO Dodatkowy rekord, do wywalenia będzie
    result += {}
    return result
