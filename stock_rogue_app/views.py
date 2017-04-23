# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseRedirect
from stock_rogue_app.models import Dane, Spolka
from django.shortcuts import  render_to_response, get_object_or_404

def index(request):
    data = {
        'spolki': Spolka.objects.all()
    }

    return render_to_response("main_site.html", data)

def companyView(request, comp_id):
    spolka = get_object_or_404(Spolka, id=comp_id)

    data = {
        'skrot': spolka.skrot
    }

    return render_to_response("company.html", data)
# Create your views here.
