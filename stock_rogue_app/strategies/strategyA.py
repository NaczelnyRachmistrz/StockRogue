# Predicts the future average name value where name value is in ['max_value', 'min_value',
# 'stock_price']
from stock_rogue_app.strategies.StrategyDataContainers import StrategyData
import random


def predict_future_average_values(company_name, number_of_past_days, company_data, result):
    # We decide here number of past days we look at and pick the values alpha, beta, gamma.
    # And put also in strategy_data: company_name and sum of volumes from number_of_days days.
    s = StrategyData(number_of_past_days, 0.3, 0.9, company_name, company_data)

    result[len(result) - 1]['kurs_max'] = s.predict_future_average_name_value('kurs_max')
    result[len(result) - 1]['kurs_min'] = s.predict_future_average_name_value('kurs_min')
    result[len(result) - 1]['kurs_biezacy'] = s.predict_future_average_name_value('kurs_biezacy')

    return result
    pass


def predict_future_values(company_name, number_of_past_days, company_data, result):
    company_data_trends = [{}] * (number_of_past_days - 1)
    for idx, day in zip(range(number_of_past_days - 1), company_data):
        company_data_trends[idx] = {}
        company_data_trends[idx]['data'] = day['data']
        company_data_trends[idx]['obrot'] = day['obrot']
        company_data_trends[idx]['kurs_biezacy'] = (company_data[idx]['kurs_biezacy'] - company_data[idx + 1][
            'kurs_biezacy']) / \
                                                   company_data[idx]['kurs_biezacy']
        company_data_trends[idx]['kurs_max'] = (company_data[idx]['kurs_max'] - company_data[idx + 1]['kurs_max']) / \
                                               company_data[idx]['kurs_max']
        company_data_trends[idx]['kurs_min'] = (company_data[idx]['kurs_min'] - company_data[idx + 1]['kurs_min']) / \
                                               company_data[idx]['kurs_min']

    gamma = 0.9
    s = StrategyData(number_of_past_days, 0.3, 0.9, company_name, company_data_trends)

    counter_for_anomalies_max = 0
    counter_for_anomalies_min = 0
    for idx, day in zip(range(len(result) - 1), result):
        if idx == 0:
            day['kurs_min'] = (s.predict_future_average_name_value('kurs_min') + 1.0) * company_data[0]['kurs_min']
            day['kurs_max'] = (s.predict_future_average_name_value('kurs_max') + 1.0) * company_data[0]['kurs_max']
            day['kurs_biezacy'] = (s.predict_future_average_name_value('kurs_biezacy') + 1.0) * company_data[0][
                'kurs_biezacy']
            continue
        trend_min = s.predict_future_average_name_value('kurs_min')
        trend_max = s.predict_future_average_name_value('kurs_max')
        trend_biezacy = s.predict_future_average_name_value('kurs_biezacy')

        # Tutaj jakaś magia.
        if trend_min > 1.01 * trend_max:
            trend_max, trend_min = trend_min, trend_max
        if result[idx - 1]['kurs_min'] * 1.03 < result[idx - 1]['kurs_max']:
            counter_for_anomalies_max += 1
            counter_for_anomalies_min += 1
            # trend_max *= random.random()
            #
            trend_max *= (-0.5)
            trend_min *= (-0.5)
        if counter_for_anomalies_max % 3 == 0 and counter_for_anomalies_max % 2 == 1:
            trend_max = -(trend_max * 1.03)
        if counter_for_anomalies_max % 6 == 0:
            trend_max *= 1.05

        trend_biezacy = min(1.1 * trend_max, trend_biezacy)
        trend_biezacy = max(1.1 * trend_min, trend_biezacy)
        day['kurs_min'] = (trend_min + 1.0) * result[idx - 1]['kurs_min']
        day['kurs_max'] = (trend_max + 1.0) * result[idx - 1]['kurs_max']

        # magia
        if day['kurs_min'] > day['kurs_max']:
            day['kurs_min'], day['kurs_max'] = day['kurs_max'], day['kurs_min']
        # koniec magii

        day['kurs_biezacy'] = (trend_biezacy + 1.0) * result[idx - 1]['kurs_biezacy']
        s.gamma *= gamma

    return result
    pass


def predict_future(company_name, number_of_past_days, company_data, result):
    result = predict_future_average_values(company_name, number_of_past_days, company_data, result)
    result = predict_future_values(company_name, number_of_past_days, company_data, result)
    return result
    pass
