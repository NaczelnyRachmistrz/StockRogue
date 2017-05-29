#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys

from StockRogue.downloader import update_data
from stock_rogue_app.data_selector import select_data
from .estimator import estimate_values
from .plot_creator import plot_preprocess, create_plot

def run_stock_rogue_from_view(name, interval_length, strategy_name):
    # Zbiera dane spółki z bazy danych
    company_data = select_data(name)

    # Przewiduje wartość akcji spółki w zadanym okresie na podstawie wybranej strategii
    predicted_data = estimate_values(name, interval_length, strategy_name, company_data)

    # Preprocessing danych do stworzenia wykresu
    plot_data = plot_preprocess(company_data, predicted_data, company_data[-1]["data"])

    # Tworzy wykres i zwraca diva go zawierającego
    plot = create_plot(plot_data, name)

    return plot