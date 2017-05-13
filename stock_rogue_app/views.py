# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.template import RequestContext
from django.template.loader import get_template

from stock_rogue_app.models import Spolka
from django.shortcuts import render_to_response, get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt

from stock_rogue_app.stock_rogue import run_stock_rogue_from_view
from stock_rogue_app.forms import DaysStrategyForm, LoginForm
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout

def index(request):
    '''Widok strony głównej aplikacji'''
    return render(request, "main_site.html")


def aboutView(request):
    '''Widok strony głównej aplikacji'''
    return render(request, "about.html")

def strategiesView(request):
    '''Widok strony głównej aplikacji'''
    return render(request, "strategies.html")

def allView(request, type):
    '''Widok wszystkich spółek lub indeksów'''

    data = {
        'spolki': Spolka.objects.filter(typ=type)
    }

    return render(request, "all.html", data)


def searchView(request):
    '''Widok strony wyszukiwania spółek'''
    if request.method == 'GET' and 'wyszukiwanie' in request.GET:
        nazwa = request.GET["wyszukiwanie"]
        spolki = Spolka.objects.filter(typ=Spolka.SPOLKA)
        spolki_do_temp = []
        for spolka in spolki:
            skrot = spolka.skrot.lower()
            if skrot.find(nazwa.lower()) != -1:
                spolki_do_temp.append(spolka)
    data = locals()
    return render(request, "search.html", data)


@csrf_exempt
def companyView(request, comp_id):
    '''Widok wykresu wybranej spółki'''

    if request.method == "GET":
        days_strategy_form = DaysStrategyForm(request.GET)
        if not days_strategy_form.is_valid():
            # Jeżeli pewne pole w formularzu nie zostało wprowadzone,
            # przekierowujemy z powrotem do formularza
            HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    spolka = get_object_or_404(Spolka, id=comp_id)

    run_stock_rogue_from_view(spolka.skrot, int(request.GET["ile_dni"]), request.GET["strategia"])

    data = spolka.__dict__

    return render(request, "company.html", data)


def companyFormView(request, comp_id):
    '''Widok formularza wyboru liczby dni i strategii'''

    data = {}
    spolka = get_object_or_404(Spolka, id=comp_id)
    data["form"] = DaysStrategyForm()
    data["skrot"] = spolka.skrot
    data['id'] = comp_id

    return render(request, "company_form.html", data)

@require_POST
def logoutView(request):
    url = request.POST["redirect"]
    logout(request)
    return HttpResponseRedirect(url)


def loginView(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            return HttpResponseForbidden("Bad username or password.")
    else:
        form = LoginForm()
        return render(request, "registration/login.html", locals())
