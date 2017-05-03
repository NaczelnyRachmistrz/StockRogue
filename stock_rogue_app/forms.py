# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms

class DaysStrategyForm(forms.Form):
    '''Formularz do wyboru strategii i liczby dni, na jakie przewidujemy.'''

    CHOICES = (('A', 'Main'), ('B', 'Naive'), ('C', 'Stable'), ('D', 'Average'))
    strategia = forms.ChoiceField(label='Strategia:', choices=CHOICES)
    ile_dni = forms.IntegerField(label='Liczba dni:', max_value=30, min_value=0)