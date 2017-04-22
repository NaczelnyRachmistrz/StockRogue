from stock_rogue_app.models import Dane


def select_data(company_name):
    result = Dane.objects.filter(nazwa=company_name)
    result = result.values()[::-1]
    return result