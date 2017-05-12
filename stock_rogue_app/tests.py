# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.test import TestCase

# Create your tests here.
from stock_rogue_app.data_selector import select_data
from stock_rogue_app.estimator import estimate_values
from stock_rogue_app.models import Dane
from stock_rogue_app.plot_creator import plot_preprocess, create_plot

#TODO Tu się powinny pokazać prawdziwe testy
from stock_rogue_app.models import Spolka


class TestOfTests(TestCase):

    def setUp(self):
        self.jeden = 1
        self.dwa = 2

    def testTests(self):
        self.assertEquals(self.jeden + self.jeden, self.dwa)
        # self.assertEquals(True, False)


class IndexViewTest(TestCase):

    def setUp(self):
        pass

    def testIndexView(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

class ViewTests(TestCase):

    # Spolka musi mieć co najmniej 1 wiersz w tabeli dane!
    def setUp(self):
        self.spolka1 = Spolka.objects.create(id=1, typ='SP', skrot='blabla')
        self.dane1 = Dane.objects.create(spolka=self.spolka1,
                                         data=datetime.today(),
                                         kurs_otwarcia=10,
                                         kurs_min=10,
                                         kurs_max=10,
                                         kurs_biezacy=10,
                                         obrot=10)

    def testCompanyFormView(self):
        response = self.client.get('/company_form/1/')
        self.assertEquals(response.status_code, 200)

    def testCompanyView(self):
        response = self.client.get('/company/1/', {'ile_dni' : 1, 'strategia' : ('B', 'Naive')})
        self.assertEquals(response.status_code, 200)
        response_wrong = self.client.get('/company/2/', {'ile_dni' : 1, 'strategia' : ('B', 'Naive')})
        self.assertEquals(response_wrong.status_code, 404)

    def testAllView(self):
        response = self.client.post('/all/SP/')
        self.assertEquals(response.status_code, 200)

    def testNoArgumentsSearchView(self):
        response = self.client.get('/search/')
        self.assertEquals(response.status_code, 200)

    def testSearchView(self):
        response = self.client.get('/search/', { 'wyszukiwanie' : '' })
        self.assertEquals(response.status_code, 200)