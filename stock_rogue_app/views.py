# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseRedirect
from stock_rogue_app.models import Dane, Spolka
from django.shortcuts import  render_to_response

def index(request):
    data = {
        'spolki': Spolka.objects.all()
    }

    render_to_response("main_site.html", data)

def companyView(request, comp):
    data = {

    }

    render_to_response("company.html", data)
# Create your views here.
