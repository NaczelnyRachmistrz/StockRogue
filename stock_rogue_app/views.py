# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect, HttpResponseForbidden

from stock_rogue_app.models import Spolka, Player, Actions
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt

from stock_rogue_app.stock_rogue import run_stock_rogue_from_view
from stock_rogue_app.forms import DaysStrategyForm, LoginForm, ContactForm, MoneyOperationForm, StartGameForm
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from datetime import date


def index(request):
    '''Widok strony głównej'''
    return render(request, "main_site.html")


def aboutView(request):
    '''Widok informacji o aplikacji'''
    return render(request, "about.html")


def contactView(request):
    '''Widok kontaktowy'''
    form_class = ContactForm

    if request.method == 'POST':
        form = form_class(data=request.POST)
        if form.is_valid():
            contact_name = request.POST['contact_name']
            contact_email = request.POST['contact_email']
            form_content = request.POST['content']
            app_email = getattr(settings, 'DEFAULT_FROM_EMAIL')
            send_mail(
                'Kontakt od użytkownika ' + contact_name,
                'Wiadomość z maila ' + contact_email + ':' + '\n\n' + form_content,
                contact_email,
                [app_email],
                fail_silently=True,
            )
        messages.add_message(request, messages.SUCCESS, 'Dziękujemy za kontakt!')
        HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, 'contact.html', {'form': form_class()})


def strategiesView(request):
    '''Widok strategii'''
    return render(request, "strategies.html")


def gameView(request):
    '''Widok gry'''
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/")

    player, created = Player.objects.get_or_create(
        user=request.user)

    actions = Actions.objects.filter(owner=player)
    money_form_class = MoneyOperationForm
    game_form_class = StartGameForm

    if request.method == 'POST':
        money_form = money_form_class(data=request.POST)
        if money_form.is_valid():
            type = request.POST['type']
            value = float(request.POST['value'])
            if (type == 'Wypłata'):
                value = (-1) * value
            player.money += value
            player.save()
        HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    data = {
        'username': request.user.username,
        'money': player.money,
        'money_form': money_form_class(),
        'game_form': game_form_class(),
        'date': date.today(),
        'actions': actions
    }
    return render(request, "game.html", data)


def allView(request, type):
    '''Widok wszystkich spółek lub indeksów'''

    data = {
        'spolki': Spolka.objects.filter(typ=type).order_by('skrot')
    }

    return render(request, "all.html", data)


def searchView(request):
    '''Widok strony wyszukiwania spółek'''
    if request.method == 'GET' and 'wyszukiwanie' in request.GET:
        nazwa = request.GET["wyszukiwanie"]
        spolki = Spolka.objects.filter(typ=Spolka.SPOLKA).order_by('skrot')
        spolki_do_temp = []
        for spolka in spolki:
            skrot = spolka.skrot.lower()
            if skrot.find(nazwa.lower()) != -1:
                spolki_do_temp.append(spolka)
    data = locals()
    return render(request, "search.html", data)


# @csrf_exempt
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
    '''Widok logowania'''
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
