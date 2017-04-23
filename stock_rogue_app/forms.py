# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms

class DaysStrategyForm(forms.Form):
    ile_dni = forms.IntegerField(label='Liczba dni:', max_value=30, min_value=0)
    strategia = forms.CharField(label='Strategia:')