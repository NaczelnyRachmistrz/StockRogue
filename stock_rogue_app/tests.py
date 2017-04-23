# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.test import TestCase

# Create your tests here.
from stock_rogue_app.data_selector import select_data
from stock_rogue_app.estimator import estimate_values
from stock_rogue_app.models import Dane
from stock_rogue_app.plot_creator import plot_preprocess, create_plot

company_name = 'ASSECOPOL'
company_data = select_data(company_name)
start_data = company_data[-1]['data']
predicted_data = estimate_values(company_name, 10, 'A', company_data)
predicted_data = predicted_data[0:-1]

plot_data = plot_preprocess(company_data, predicted_data, start_data)
create_plot(plot_data, company_name)