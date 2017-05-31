# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.forms import SelectDateWidget

from stock_rogue_app.models import Spolka


class DaysStrategyForm(forms.Form):
    '''Formularz do wyboru strategii i liczby dni, na jakie przewidujemy.'''

    CHOICES = (('A', 'Main'), ('B', 'Naive'), ('C', 'Stable'), ('D', 'Average'))

    strategia = forms.ChoiceField(label='Strategia:',
                                  choices=CHOICES,
                                  required=True)
    ile_dni = forms.IntegerField(label='Liczba dni:',
                                 min_value=0,
                                 max_value=30,
                                 required=True)


class LoginForm(forms.Form):
    '''Formularz do logowania.'''
    username = forms.CharField(label="Login:",
                               max_length=30)

    password = forms.CharField(label="Hasło:",
                               widget=forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.get(username=username)
            return username
        except ObjectDoesNotExist:
            raise forms.ValidationError("Niepoprawny login")

    def clean_password(self):
        if 'username' in self.cleaned_data:
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            user = User.objects.get(username=username)
            if user.check_password(password):
                return password
            raise forms.ValidationError("Niepoprawne hasło")
        raise forms.ValidationError("Niepoprawny login")


class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True,
                                   label='Przedstaw się')
    contact_email = forms.EmailField(required=True,
                                     label='Podaj e-mail na który będziemy mogli Ci odpisać')
    content = forms.CharField(
        required=True,
        widget=forms.Textarea,
        label=''
    )


class MoneyOperationForm(forms.Form):
    type = forms.ChoiceField(label='Rodzaj operacji',
                             choices=[('Wpłata', 'Wpłata'), ('Wypłata', 'Wypłata')])

    value = forms.FloatField(required=True,
                             label='',
                             help_text='zł',
                             initial=0.00)


class StartGameForm(forms.Form):
    AVAILABLE_YEARS = [
        2012, 2013, 2014, 2015, 2016, 2017
    ]

    # company = forms.ModelChoiceField(label='Spółka',
    #                                 queryset=Spolka.objects
    #                                 .filter(typ='SP')
    #                                 .order_by('skrot'))

    date = forms.DateField(label='Data rozpoczęcia gry',
                           widget=SelectDateWidget(years=AVAILABLE_YEARS,
                                                   empty_label=("Rok", "Miesiąc", "Dzień"),
                                                   ),
                           required=True)

    initial_money = forms.IntegerField(label='Początkowe zasoby pieniężne',
                                       min_value=0,
                                       help_text='zł',
                                       required=True)
