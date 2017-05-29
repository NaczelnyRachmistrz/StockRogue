# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Spolka(models.Model):
    '''Model dla spółek i indeksów giełdowych. '''

    SPOLKA = 'SP'
    INDEKS = 'IN'
    INNE = 'OT'

    SpolkaChoices = (
        (SPOLKA, 'Spółka'),
        (INDEKS, 'Indeks'),
        (INNE, 'Inne')
    )

    skrot = models.CharField(max_length=50, unique=True)

    typ = models.CharField(
        max_length=2,
        choices=SpolkaChoices,
        default=INNE
    )

    def __str__(self):
        return str(self.typ) + " : " + str(self.skrot)


class Dane(models.Model):
    '''Model reprezentujący dane o spółce z wybranego dnia.'''

    spolka = models.ForeignKey('Spolka')
    data = models.DateField()
    kurs_otwarcia = models.FloatField()
    kurs_max = models.FloatField()
    kurs_min = models.FloatField()
    kurs_biezacy = models.FloatField()
    obrot = models.FloatField()

    class Meta:
        unique_together = ('spolka', 'data')

    def __str__(self):
        return str(self.spolka.skrot) + " " + str(self.data.strftime('%d/%m/%y'))


class Player(models.Model):
    '''Model reprezentujący dane zarejestrowanego użytkownika.'''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    money = models.FloatField(default=0)

    '''Pamiętamy 5 ostatnich spółek którymi zajmował się gracz'''
    last_played_company1 = models.ForeignKey('Spolka', on_delete=models.SET_NULL,
                                             related_name='1+', null=True)
    last_played_company2 = models.ForeignKey('Spolka', on_delete=models.SET_NULL,
                                             related_name='2+', null=True)
    last_played_company3 = models.ForeignKey('Spolka', on_delete=models.SET_NULL,
                                             related_name='3+', null=True)
    last_played_company4 = models.ForeignKey('Spolka', on_delete=models.SET_NULL,
                                             related_name='4+', null=True)
    last_played_company5 = models.ForeignKey('Spolka', on_delete=models.SET_NULL,
                                             related_name='5+', null=True)