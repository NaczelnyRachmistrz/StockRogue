# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User


class DaysStrategyForm(forms.Form):
    '''Formularz do wyboru strategii i liczby dni, na jakie przewidujemy.'''

    CHOICES = (('A', 'Main'), ('B', 'Naive'), ('C', 'Stable'), ('D', 'Average'))
    strategia = forms.ChoiceField(label='Strategia:', choices=CHOICES, required=True)
    ile_dni = forms.IntegerField(label='Liczba dni:', min_value=0, max_value=30, required=True)


class LoginForm(forms.Form):
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


class RegistrationForm(forms.Form):
    username = forms.CharField(label="Login:", max_length=30, required=True)
    password = forms.CharField(label="Hasło:", widget=forms.PasswordInput(), required=True)
    password_confirm = forms.CharField(label="Powtórz hasło:", widget=forms.PasswordInput(), required=True)
    email = forms.CharField(label="Email:", widget=forms.PasswordInput(), required=True)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.get(username=username)
            raise forms.ValidationError("Ten login jest już zajęty")
        except ObjectDoesNotExist:
            return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if "todo":
            raise forms.ValidationError("Email jest niepoprawny")

    def clean_password(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        email = self.cleaned_data['email']
        password_confirm = self.cleaned_data['password_confirm']
        if password != password_confirm:
            raise forms.ValidationError("Podane hasła różnią się")
        user = User.objects.create(username=username, password=password, email=email)
