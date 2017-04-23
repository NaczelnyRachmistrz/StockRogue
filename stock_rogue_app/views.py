# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseRedirect
from stock_rogue_app.models import Dane, Spolka
from django.shortcuts import  render_to_response, get_object_or_404
from stock_rogue_app.data_selector import select_data
from StockRogue.downloader import update_data
from .estimator import estimate_values
from .plot_creator import plot_preprocess, create_plot
from stock_rogue_app.stock_rogue import *

def index(request):
    data = {
        'spolki': Spolka.objects.all()
    }

    return render_to_response("main_site.html", data)

def companyView(request, comp_id):
    spolka = get_object_or_404(Spolka, id=comp_id)

    run_stock_rogue2(spolka.skrot, 10, "A")

    data = {
        'skrot': spolka.skrot,
    }

    return render_to_response("company.html", data)
# Create your views here.
