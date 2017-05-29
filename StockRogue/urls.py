"""StockRogue URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from stock_rogue_app.views import index, companyView, companyFormView, searchView, allView, loginView, logoutView, \
    strategiesView, aboutView, contactView, compareView

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^company/([0-9]+)/$', companyView, name='company'),
    url(r'^company_form/([0-9]+)/$', companyFormView, name='company_form'),
    url(r'^search/', searchView, name='search_view'),
    url(r'^all/([A-Z]*)/$', allView, name='all_view'),
    url(r'^login/$', loginView, name='login'),
    url(r'^logout/$', logoutView, name='logout'),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^strategies/$', strategiesView, name='strategies'),
    url(r'^compare/(?P<strategy>[A-Z])/$', compareView, name='compare'),
    url(r'^contact/$', contactView, name='contact'),
    url(r'^about/$', aboutView, name='about'),
    url(r'^admin/', admin.site.urls)
]
