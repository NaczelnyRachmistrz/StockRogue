#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys

from StockRogue.downloader import update_data
from stock_rogue_app.data_selector import select_data
from .estimator import estimate_values
from .plot_creator import plot_preprocess, create_plot

# Dictionary with program parameters
flag = {}

def read_flags(flags_list):
    """ Reads flags from flags_list array. """

    # Creates parser arguments informations
    parser = argparse.ArgumentParser(prog='stock_rogue', argument_default=argparse.SUPPRESS)

    # Name of company for which to predict stock prices
    parser.add_argument('-cmp', type=str, required=True,
                        help='Name of company.')

    # Output file (with generated plot)
    parser.add_argument('--out', type=argparse.FileType('w'), default='stock_plot.png',
                        help='Output file name.')

    # Number of consecutive days with stock price predictions
    parser.add_argument('--d', type=int, default=1,
                        help='Number of consecutive days with stock price predictions.')

    # Number of previous days presented on plot
    parser.add_argument('--pr', type=int, default=10,
                        help='Number of previous days presented on plot.')

    # Chosen strategy
    parser.add_argument('--str', type=str, default='basic',
                        help='Name of chosen strategy.')

    # Parse data from flags_table to global variable flag
    parse_data = parser.parse_args(flags_list)
    global flag
    flag = vars(parse_data)

def run_stock_rogue():
    """ Main 1st iteration Stock Rogue function. Performs program sequence. """

    # Updates stock data if necessary
    update_data()

    # Gathers company data from a database
    company_data = select_data(flag['cmp'])

    # Predicts stock prices for a given interval of time using specific strategy
    predicted_data = estimate_values(flag['cmp'], flag['d'], flag['str'], company_data)

    # Preprocess of data used for plot creating
    plot_data = plot_preprocess(company_data, predicted_data, flag['d'], flag['pr'])


    # Creates plot
    plot = create_plot(plot_data, flag['cmp'])

    #Saving plot to a file
    save_plot(plot, flag['out'])

def run_stock_rogue2(name, interval_length, strategy_name):
    # Gathers company data from a database
    company_data = select_data(name)

    # Predicts stock prices for a given interval of time using specific strategy
    predicted_data = estimate_values(name, interval_length, strategy_name, company_data)

    # Preprocess of data used for plot creating
    plot_data = plot_preprocess(company_data, predicted_data, company_data[-1]["data"])

    # Creates plot
    plot = create_plot(plot_data, name)

    #Saving plot to a file
    return plot


if __name__ == "__main__":
    """ Preprocess before running stock_rogue. """

    read_flags(sys.argv[1:])

    run_stock_rogue()