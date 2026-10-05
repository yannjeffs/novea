# apps/reprise/services.py
from decimal import Decimal
from django.db import models
from django.utils import timezone
from .models import GrilleDecote

# Valeur catalogue de référence par énergie/segment — à affiner selon tes données réelles
# (idéalement, ça viendrait d'une table de prix moyens marché, mais en l'absence
# d'équivalent Argus/SIV au Cameroun, on part d'une valeur déclarée + décote)

def calculer_estimation_en_ligne(marque_modele, annee, kilometrage, valeur_neuf_estimee):
    """Applique la grille de décote interne à une valeur déclarée pour obtenir une estimation."""
    age_mois = (timezone.now().year - annee) * 12

    grille = GrilleDecote.objects.filter(
        age_min_mois__lte=age_mois,
        km_min__lte=kilometrage,
    ).filter(
        models.Q(age_max_mois__isnull=True) | models.Q(age_max_mois__gte=age_mois)
    ).filter(
        models.Q(km_max__isnull=True) | models.Q(km_max__gte=kilometrage)
    ).order_by("-age_min_mois").first()

    if not grille:
        # Décote par défaut si aucune tranche ne correspond (sécurité)
        coefficient = Decimal("0.700")
    else:
        coefficient = grille.coefficient_decote

    return round(valeur_neuf_estimee * coefficient, -3)  # arrondi au millier de FCFA