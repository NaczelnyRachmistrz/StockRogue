from stock_rogue_app.models import Dane


def select_data(comp_id):
    result = Dane.objects.filter(spolka_id=comp_id)
    result = result.values()[::-1]
    return result