# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.test import TestCase

# Create your tests here.
from stock_rogue_app.estimator import estimate_values
from stock_rogue_app.models import Dane

x = {}
x = Dane.objects.filter(nazwa='06MAGNA')

y = estimate_values(x[0]['nazwa'], 30, 'C', x)