# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User


class DaysStrategyForm(forms.Form):
    '''Formularz do wyboru strategii i liczby dni, na jakie przewidujemy.'''

    CHOICES = (('A', 'Main'), ('B', 'Naive'), ('C', 'Stable'), ('D', 'Average'),
               ('E', 'Linear Regression'), ('F', 'Polynomial Regression'),
               ('G', 'Huber Regression'))
    strategia = forms.ChoiceField(label='Strategia:', choices=CHOICES, required=True)
    ile_dni = forms.IntegerField(label='Liczba dni:', min_value=0, max_value=30, required=True)


class LoginForm(forms.Form):
    '''Formularz do logowania.'''
    username = forms.CharField(label="Login:", max_length=30)
    password = forms.CharField(label="Hasło:", widget=forms.PasswordInput())

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
    contact_name = forms.CharField(required=True, label='Przedstaw się')
    contact_email = forms.EmailField(required=True, label='Podaj e-mail na który będziemy mogli Ci odpisać')
    content = forms.CharField(
        required=True,
        widget=forms.Textarea,
        label=''
    )
