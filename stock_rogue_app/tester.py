import datetime
from stock_rogue_app.strategies import strategyA
from stock_rogue_app.strategies import strategyB
from stock_rogue_app.strategies import strategyC
from stock_rogue_app.strategies import strategyD
from stock_rogue_app.strategies.futureDataGenerator import generate_future_data
from stock_rogue_app.strategies.machine_learning_strategies import strategy_linear_regression
from stock_rogue_app.strategies.machine_learning_strategies import auxiliary_functions
from stock_rogue_app.strategies.machine_learning_strategies import vector_preprocess

from sklearn import linear_model

# Funkcje pomocnicze

def choose_table_and_poly(company_data, strategy):
    '''Pomocnicza funkcja, wybierająca tablicę dni w przeszłości i czy
        chcemy regresję wielomianową'''
    if strategy == 'E':
        return auxiliary_functions.default_table_picker(company_data), False
    elif strategy == 'F':
        return auxiliary_functions.default_table_picker(company_data, True), True
    elif strategy == 'G':
        return auxiliary_functions.default_table_picker(company_data, True), False



def give_model(X_matrix, y_vector, strategy):
    '''Wybiera model dla danej strategii'''

    if (strategy == 'E') or (strategy == 'F'):
        model = linear_model.LinearRegression()
    elif strategy == 'G':
        model = linear_model.HuberRegressor()

    model.fit(X_matrix, y_vector)

    return model

# Funkcja główna

def estimate_past_values(strategy, company_data, start_index, interval_length):
    '''Funkcja zwraca przewidywane kursy akcji na podstawie wybranej strategii
       w wybranym okresie w przesżłości'''

    table, poly_reg =  choose_table_and_poly(company_data, strategy)

    X_matrix, y_vector = vector_preprocess.prepare_data(company_data,
                 table,
                 True,
                 poly_reg)

    model = give_model(X_matrix, y_vector["kurs_biezacy"], strategy)

    X_matrix_test = X_matrix[(start_index - interval_length):(start_index + 1)]

    predicted_values = [{"kurs_biezacy": model.predict([X_matrix_test[i + 1]])[0]*
                                         company_data[start_index + i - interval_length + 1]["kurs_biezacy"],
                         "data": company_data[start_index - interval_length + i]["data"]}
                        for i in range(interval_length)]

    values = [{"kurs_biezacy": company_data[start_index + i - interval_length]["kurs_biezacy"],
                "data": company_data[start_index - interval_length + i]["data"]}
                        for i in range(interval_length)]

    return (predicted_values, values)
