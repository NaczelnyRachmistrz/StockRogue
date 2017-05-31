# -*- coding: utf-8 -*-
# Predicts the future average name value where name value is in ['max_value', 'min_value',
# 'stock_price']
from stock_rogue_app.strategies.StrategyDataContainers import StrategyData
import random

value_names = ['kurs_min', 'kurs_max', 'kurs_biezacy']


def predict_future_values_for_day(strategy_data, idx, company_data, trends_data):
    result = strategy_data[idx]

    if idx == 0:
        previous_day = company_data[0]
    else:
        previous_day = strategy_data[idx - 1]

    for name in value_names:
        result[name] = previous_day[name] * trends_data.predict_future_average_name_value(name)

    if result['kurs_min'] > result['kurs_max']:
        result['kurs_min'] = result['kurs_max']
        result['kurs_biezacy'] = result['kurs_min']

    return result


def predict_future_values(company_name, number_of_past_days, company_data, result):
    ''' Nie są skorelowane. '''
    default_volume_importance_coefficient = 0.5
    default_past_time_importance_coefficient = 0.5

    company_data_trends = [{}] * (number_of_past_days - 1)
    for idx, day in zip(range(number_of_past_days - 1), company_data):
        company_data_trends[idx] = day_trend(company_data[idx], company_data[idx + 1])

    trends_data = StrategyData(company_name,
                                 company_data_trends,
                                 number_of_past_days,
                                 default_volume_importance_coefficient,
                                 default_past_time_importance_coefficient)

    for idx, day in zip(range(len(result) - 1), result):
        day = predict_future_values_for_day(result, idx, company_data, trends_data)

    return result


def day_trend(current_day, previous_day):
    trend = dict(current_day)
    for name in value_names:
        trend[name] = (2 * current_day[name] - previous_day[name]) / previous_day[name]
    return trend


def predict_future(company_name, number_of_past_days, company_data, result):
    result = predict_future_values(company_name, number_of_past_days, company_data, result)
    return result
