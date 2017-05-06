# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models


class Spolka(models.Model):
    '''Model dla spółek i indeksów giełdowych. '''

    skrot = models.CharField(max_length=50, unique=True)


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


