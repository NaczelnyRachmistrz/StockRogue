# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.forms import SelectDateWidget

from stock_rogue_app.models import Spolka

STRATEGY_CHOICES = (('A', 'Main'), ('B', 'Naive'), ('C', 'Stable'), ('D', 'Average'),
               ('E', 'Linear Regression'), ('F', 'Polynomial Regression'),
               ('G', 'Huber Regression'))


class DaysStrategyForm(forms.Form):
    '''Formularz do wyboru strategii i liczby dni, na jakie przewidujemy.'''



    strategia = forms.ChoiceField(label='Strategia:',
                                  choices=STRATEGY_CHOICES,
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


class ActionOperationForm(forms.Form):
    act_type = forms.ChoiceField(label='Rodzaj operacji',
                                 choices=[('Kupno', 'Kupno'), ('Sprzedaż', 'Sprzedaż')])

    act_number = forms.IntegerField(required=True,
                                    label='liczba',
                                    initial=0)


class CompanyChooseForm(forms.Form):
    company = forms.ModelChoiceField(label='Spółka',
                                     queryset=Spolka.objects
                                     .filter(typ='SP')
                                     .order_by('skrot'))

class CompareForm(forms.Form):
    company = forms.ModelChoiceField(label='Spółka',
                                     queryset=Spolka.objects
                                     .filter(typ='SP')
                                     .order_by('skrot'))

    YEAR_CHOICES = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017]
    startDate = forms.DateField(label='Początkowa data',
                                widget=SelectDateWidget(years=YEAR_CHOICES))

    days = forms.IntegerField(label='Liczba dni', min_value=True)
    strategy = forms.ChoiceField(label='Strategia:',
                                  choices=STRATEGY_CHOICES,
                                  required=True)

