# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.test import TestCase

# Create your tests here.
from stock_rogue_app.estimator import estimate_values
from stock_rogue_app.models import Dane

x = {}
x = Dane.objects.filter(nazwa='MBANK')
z = x.values()[::-1]
# z = z.reverse()

y = estimate_values(z[0]['nazwa'], 10, 'A', z)
# for day in y:
#     print(day)