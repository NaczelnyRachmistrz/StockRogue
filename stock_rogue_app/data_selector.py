from stock_rogue_app.models import Dane


def select_data(nazwa):
    result = Dane.objects.filter(spolka__skrot=nazwa)
    result = result.values()[::-1]
    return result