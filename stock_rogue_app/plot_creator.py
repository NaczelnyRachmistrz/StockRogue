# -*- coding: utf-8 -*-
import os
import plotly.graph_objs as go
import plotly.offline as off

from StockRogue.settings import BASE_DIR


def plot_preprocess(company_data, predicted_data, start_data):
    """Funkcja preprocessingowa. Zwraca jedynie dane począwszy od start_data
    (w postaci pary (dane_historyczne, dane_przewidziane))"""

    preprocessed_data = []
    for el in company_data:
        if el["data"] >= start_data:
            preprocessed_data.append(el)

    preprocessed_data = (preprocessed_data, predicted_data)

    return preprocessed_data


def create_plot(plot_data, company):
    """Główna funkcja odpowiedzialna za tworzenie wykresów."""

    plot_data[1].pop()
    pl_data = [el["data"] for el in plot_data[0]]
    pl_data_2 = [el["data"] for el in [plot_data[0][0]] + plot_data[1]]
    pl_kurs_max = [el["kurs_max"] for el in plot_data[0]]
    pl_kurs_min = [el["kurs_min"] for el in plot_data[0]]
    predict_max = [el["kurs_max"] for el in [plot_data[0][0]] + plot_data[1]]
    predict_min = [el["kurs_min"] for el in [plot_data[0][0]] + plot_data[1]]
    trace_max = go.Scatter(
        x=pl_data,
        y=pl_kurs_max,
        name=company + " - kurs maksymalny",
        line=dict(color='#17BECF'),
        opacity=0.8)

    trace_min = go.Scatter(
        x=pl_data,
        y=pl_kurs_min,
        name=company + " - kurs minimalny",
        line=dict(color='#7F7F7F'),
        opacity=0.8)

    trace_min_pred = go.Scatter(
        x=pl_data_2,
        y=predict_min,
        name=company + " - przewidywany kurs minimalny",
        line=dict(color='#ff0000'),
        mode='lines',
        opacity=0.8)

    trace_max_pred = go.Scatter(
        x=pl_data_2,
        y=predict_max,
        name=company + " - przewidywany kurs maksymalny",
        line=dict(color='#00ff00'),
        mode='lines',
        opacity=0.8)

    data = [trace_max, trace_min, trace_min_pred, trace_max_pred]

    layout = dict(
        title='Notowania ' + company,
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label='1m',
                         step='month',
                         stepmode='backward'),
                    dict(count=6,
                         label='6m',
                         step='month',
                         stepmode='backward'),
                    dict(step='all')
                ])
            ),
            rangeslider=dict(),
            type='date'
        ),
        yaxis=dict(
            autorange=True,
            fixedrange=False
        )
    )

    fig = dict(data=data, layout=layout)

    return off.plot(fig, include_plotlyjs=False, output_type='div')


def create_compare_plot(plot_data, company):
    """Główna funkcja odpowiedzialna za porównywanie danych z przewidywaniami."""

    pl_data = [el["data"] for el in plot_data[1]]

    data_max = max(pl_data[0], pl_data[-1])
    pl_curr = [el["kurs_biezacy"] for el in plot_data[0]]
    predict_curr = [el["kurs_biezacy"] for el in plot_data[1] if el["data"] <= data_max]

    trace_correct = go.Scatter(
        x=pl_data,
        y=pl_curr,
        name=company + " - kurs bieżący",
        line=dict(color='#17BECF'),
        opacity=0.8)

    trace_predict = go.Scatter(
        x=pl_data,
        y=predict_curr,
        name=company + " - przewidywany kurs bieżący",
        line=dict(color='#7F7F7F'),
        opacity=0.8)

    data = [trace_correct, trace_predict]

    layout = dict(
        title='Test ' + company,
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label='1m',
                         step='month',
                         stepmode='backward'),
                    dict(count=6,
                         label='6m',
                         step='month',
                         stepmode='backward'),
                    dict(step='all')
                ])
            ),
            rangeslider=dict(),
            type='date'
        ),
        yaxis=dict(
            autorange=True,
            fixedrange=False
        )
    )

    fig = dict(data=data, layout=layout)

    return off.plot(fig, include_plotlyjs=False, output_type='div')

def create_past_plot(plot_data, company, last_date):
    """Funkcja odpowiedzialna za rysowanie wykresu dla funkcji do odpowiedniego
        momentu w przeszłości."""

    pl_data = [el["data"] for el in plot_data if el["data"] < last_date]
    pl_kurs_biezacy = [el["kurs_biezacy"] for el in plot_data if el["data"] < last_date]

    trace_curr = go.Scatter(
        x=pl_data,
        y=pl_kurs_biezacy,
        name=company + " - kurs bieżący",
        line=dict(color='#17BECF'),
        opacity=0.8)

    data = [trace_curr]

    layout = dict(
        title='Notowania ' + company,
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label='1m',
                         step='month',
                         stepmode='backward'),
                    dict(count=6,
                         label='6m',
                         step='month',
                         stepmode='backward'),
                    dict(step='all')
                ])
            ),
            rangeslider=dict(),
            type='date'
        ),
        yaxis=dict(
            autorange=True,
            fixedrange=False
        )
    )

    fig = dict(data=data, layout=layout)

    return off.plot(fig, include_plotlyjs=False, output_type='div')
