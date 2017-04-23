# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseRedirect
from stock_rogue_app.models import Dane, Spolka
from django.shortcuts import  render_to_response, get_object_or_404
from stock_rogue_app.data_selector import select_data
from StockRogue.downloader import update_data
from .estimator import estimate_values
from .plot_creator import plot_preprocess, create_plot
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .forms import DaysStrategyForm
from stock_rogue_app.stock_rogue import *

def index(request):
    data = {
        'spolki': Spolka.objects.all()
    }

    return render_to_response("main_site.html", data)

@csrf_exempt
def companyView(request, comp_id):
    if request.method == "POST":
        days_strategy_form = DaysStrategyForm(request.POST)
        if not days_strategy_form.is_valid():
            #Jezeli pewne pole w formularzu nie zostało wprowadzone, przekierowujemy z powrotem do formularza
            HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    spolka = get_object_or_404(Spolka, id=comp_id)

    run_stock_rogue2(spolka.skrot, int(request.POST["ile_dni"]), request.POST["strategia"])

    data = {
        'skrot': spolka.skrot
    }

    return render_to_response("company.html", data)

def companyFormView(request, comp_id):
    data = {}
    spolka = get_object_or_404(Spolka, id=comp_id)
    data["form"] = DaysStrategyForm()
    data["skrot"] = spolka.skrot
    data['id'] = comp_id

    return render_to_response("company_form.html", data)
