from decimal import Decimal
from apps.catalogue.models import Finition, Teinte, Habitacle, Option


def calculer_prix_configuration(finition_id, teinte_id=None, habitacle_id=None, options_ids=None):
    """Logique de calcul centralisé - seule source de vérite pour le prix d'une configuration"""
    finition = Finition.objects.get(id=finition_id)
    prix = finition.prix_base

    if teinte_id:
        teinte = Teinte.objects.get(id=teinte_id)
        prix += teinte.supplement_prix

    if habitacle_id:
        habitacle = Habitacle.objects.get(id=habitacle_id)
        prix += habitacle.supplement_prix

    if options_ids:
        options = Option.objects.filter(id__in=options_ids)
        prix += sum((opt.prix for opt in options), Decimal("0"))

    return prix