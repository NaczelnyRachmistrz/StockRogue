## TODO : Main strategy - description will be added soon.
##



# Predicts the future average name value where name value is in ['max_value', 'min_value',
# 'stock_price']
def predict_future_average_name_value(strategy_data, company_data, name):
    result = 0.0
    gamma_acc = strategy_data['beta']
    gamma_max = pow(strategy_data['gamma'], strategy_data['number_of_past_days'])
    if gamma_max == 1.0 or gamma_max == 0.0:
        gamma_factor = 1 / strategy_data['number_of_past_days']
    else:
        gamma_factor = (1 - strategy_data['gamma']) / (1 - gamma_max)

    for _, day in zip(range(strategy_data['number_of_past_days']), company_data):
        result += day[name] * (strategy_data['alpha'] * (day['obrot'] / strategy_data['sum_volume']) +
                               gamma_acc * gamma_factor)
        gamma_acc *= strategy_data['gamma']

    # if name == 'kurs_min' or name == 'kurs_biezacy':
    #     print(result, name)
    return result
    pass


def sum_volume(company_name, number_of_past_days, company_data):
    result = 0
    for idx, day in enumerate(company_data):
        if idx >= number_of_past_days:
            break
        result += day['obrot']
    return result
    pass


def predict_future_average_values(company_name, number_of_past_days, company_data, result):
    # TODO : Should be turned into class.
    # We decide here number of past days we look at and pick the values alpha, beta, gamma.
    # And put also in strategy_data: company_name and sum of volumes from number_of_days days.
    strategy_data = {}
    strategy_data['number_of_past_days'] = number_of_past_days
    strategy_data['alpha'] = 0.1
    strategy_data['beta'] = 1.0 - strategy_data['alpha']
    # gamma from range [0, 1]
    strategy_data['gamma'] = 0.9
    strategy_data['company_name'] = company_name
    strategy_data['sum_volume'] = sum_volume(company_name, number_of_past_days, company_data)

    result[len(result) - 1]['kurs_max'] = predict_future_average_name_value(strategy_data,
                                                                             company_data,
                                                                             'kurs_max')
    result[len(result) - 1]['kurs_min'] = predict_future_average_name_value(strategy_data,
                                                                             company_data,
                                                                             'kurs_min')
    result[len(result) - 1]['kurs_biezacy'] = predict_future_average_name_value(strategy_data,
                                                                               company_data,
                                                                               'kurs_biezacy')

    return result
    pass


def predict_future_values(company_name, number_of_past_days, company_data, result):
    company_data_trends = [{}] * (number_of_past_days - 1)
    # for day in company_data_trends:
    #     print(day)
    for idx, day in zip(range(number_of_past_days - 1), company_data):
        company_data_trends[idx] = {}
        company_data_trends[idx]['data'] = day['data']
        company_data_trends[idx]['obrot'] = day['obrot']
        company_data_trends[idx]['kurs_biezacy'] = (company_data[idx]['kurs_biezacy'] - company_data[idx + 1]['kurs_biezacy']) / \
                                                company_data[idx]['kurs_biezacy']
        company_data_trends[idx]['kurs_max'] = (company_data[idx]['kurs_max'] - company_data[idx + 1]['kurs_max']) / \
                                            company_data[idx]['kurs_max']
        company_data_trends[idx]['kurs_min'] = (company_data[idx]['kurs_min'] - company_data[idx + 1]['kurs_min']) / \
                                            company_data[idx]['kurs_min']
        # print(company_data_trends[idx])
    # for idx, day in enumerate(company_data_trends):
    #     print(idx, company_data_trends[idx])

    # print("HEJA")

    gamma = 0.95
    # TODO : Should be turned into class.
    strategy_data = {}
    strategy_data['number_of_past_days'] = number_of_past_days
    strategy_data['alpha'] = 0.3
    strategy_data['beta'] = 1.0 - strategy_data['alpha']
    # gamma from range [0, 1]
    strategy_data['gamma'] = gamma
    strategy_data['company_name'] = company_name
    # TODO this is computed again.
    strategy_data['sum_volume'] = sum_volume(company_name, number_of_past_days, company_data)

    for idx, day in zip(range(len(result) - 1), result):
        if idx == 0:
            day['kurs_min'] = (
                              predict_future_average_name_value(strategy_data, company_data_trends, 'kurs_min') + 1.0) * \
                              company_data[0]['kurs_min']
            day['kurs_max'] = (
                              predict_future_average_name_value(strategy_data, company_data_trends, 'kurs_max') + 1.0) * \
                              company_data[0]['kurs_max']
            day['kurs_biezacy'] = (predict_future_average_name_value(strategy_data, company_data_trends,
                                                                     'kurs_biezacy') + 1.0) * company_data[0]['kurs_biezacy']
            continue
        trend_min = predict_future_average_name_value(strategy_data, company_data_trends, 'kurs_min')
        trend_max = predict_future_average_name_value(strategy_data, company_data_trends, 'kurs_max')
        trend_biezacy = predict_future_average_name_value(strategy_data, company_data_trends, 'kurs_biezacy')
        if trend_min > trend_max:
            trend_max, trend_min = trend_min, trend_max
        if result[idx - 1]['kurs_min'] * 1.03 < result[idx - 1]['kurs_max']:
            trend_max = -trend_max
        trend_biezacy = min(1.1 * trend_max, trend_biezacy)
        trend_biezacy = max(1.1 * trend_min, trend_biezacy)
        day['kurs_min'] = (trend_min + 1.0) * result[idx - 1]['kurs_min']
        day['kurs_max'] = (trend_max + 1.0) * result[idx - 1]['kurs_max']
        # print(predict_future_average_name_value(strategy_data, company_data_trends, 'kurs_biezacy'))
        # print("HEJO")
        day['kurs_biezacy'] = (trend_biezacy + 1.0) * result[idx - 1]['kurs_biezacy']
        strategy_data['gamma'] *= gamma

    return result
    pass


def predict_future(company_name, number_of_past_days, company_data, result):
    result = predict_future_average_values(company_name, number_of_past_days, company_data, result)
    result = predict_future_values(company_name, number_of_past_days, company_data, result)
    return result
    pass
