# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from stock_rogue_app.models import Spolka
from django.shortcuts import  render_to_response, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .forms import DaysStrategyForm
from stock_rogue_app.stock_rogue import *

def index(request):
    '''Widok strony głównej aplikacji'''
    return render_to_response("main_site.html")


def allView(request):
    '''Widok wszystkich spółek'''

    data = {
        'spolki': Spolka.objects.all()
    }

    return render_to_response("all.html", data)


def searchView(request):
    '''Widok wszystkich spółek'''
    if request.method == 'GET' and 'wyszukiwanie' in request.GET:
        nazwa = request.GET["wyszukiwanie"]
        spółki = Spolka.objects.all()
        spółki_do_temp = []
        for spółka in spółki:
            skrót = spółka.skrot.lower()
            if skrót.find(nazwa.lower()) != -1:
                spółki_do_temp.append(spółka)
    data = locals()
    return render_to_response("search.html", data)
@csrf_exempt
def companyView(request, comp_id):
    '''Widok wykresu wybranej spółki'''

    if request.method == "GET":
        days_strategy_form = DaysStrategyForm(request.GET)
        if not days_strategy_form.is_valid():
            #Jeżeli pewne pole w formularzu nie zostało wprowadzone, przekierowujemy z powrotem do formularza
            HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    spolka = get_object_or_404(Spolka, id=comp_id)

    run_stock_rogue_from_view(spolka.skrot, int(request.GET["ile_dni"]), request.GET["strategia"])

    #Chyba tak lepiej
    data = spolka.__dict__
    #data = {
    #    'skrot': spolka.skrot
    #}

    return render_to_response("company.html", data)

def companyFormView(request, comp_id):
    '''Widok formularza wyboru liczby dni i strategii'''

    data = {}
    spolka = get_object_or_404(Spolka, id=comp_id)
    data["form"] = DaysStrategyForm()
    data["skrot"] = spolka.skrot
    data['id'] = comp_id

    return render_to_response("company_form.html", data)
