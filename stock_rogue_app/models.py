from __future__ import unicode_literals
from django.db import models

class Dane(models.Model):
    nazwa = models.CharField(max_length=50)
    data = models.DateField()
    kurs_otwarcia = models.FloatField()
    kurs_max = models.FloatField()
    kurs_min = models.FloatField()
    kurs_biezacy = models.FloatField()
    obrot = models.FloatField()

    def __str__(self):
        return str(self.nazwa) + " " + str(self.data.strftime('%d/%m/%y'))