import datetime
from stock_rogue_app.strategies import strategyA
from stock_rogue_app.strategies import strategyB
from stock_rogue_app.strategies import strategyC
from stock_rogue_app.strategies import strategyD
from stock_rogue_app.strategies.futureDataGenerator import generate_future_data
from stock_rogue_app.strategies.machine_learning_strategies import strategy_linear_regression
from stock_rogue_app.strategies.machine_learning_strategies import auxiliary_functions
from stock_rogue_app.strategies.machine_learning_strategies import vector_preprocess

#Under construction

def estimate_past_values(start_date, predict_interval, strategy, company_data):
    '''Funkcja zwraca przewidywane kursy akcji na podstawie wybranej strategii
       w wybranym okresie w przesżłości'''

    table, poly_reg =  choose_table_and_poly(company_data, strategy)

    X_matrix, y_vector = vector_preprocess.prepare_data(company_data,
                 table,
                 True,
                 poly_reg)

    model = give_model(X_matrix, y_vector, strategy)

    prediction = duplicate_table(start_date, predict_interval)

    for

    return predicted_values
