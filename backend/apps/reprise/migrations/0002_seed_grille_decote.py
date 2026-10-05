from django.db import migrations
from decimal import Decimal


def creer_grille_decote(apps, schema_editor):
    GrilleDecote = apps.get_model("reprise", "GrilleDecote")

    tranches = [
        # (age_min_mois, age_max_mois, km_min, km_max, coefficient)
        (0,   12,  0,      30000,  Decimal("0.920")),  # < 1 an, < 30 000 km
        (0,   12,  30000,  None,   Decimal("0.870")),  # < 1 an, usage intensif
        (12,  24,  0,      50000,  Decimal("0.850")),  # 1-2 ans
        (12,  24,  50000,  None,   Decimal("0.800")),
        (24,  36,  0,      70000,  Decimal("0.780")),  # 2-3 ans
        (24,  36,  70000,  None,   Decimal("0.730")),
        (36,  60,  0,      100000, Decimal("0.680")),  # 3-5 ans
        (36,  60,  100000, None,   Decimal("0.630")),
        (60,  96,  0,      150000, Decimal("0.550")),  # 5-8 ans
        (60,  96,  150000, None,   Decimal("0.480")),
        (96,  None, 0,     None,   Decimal("0.380")),  # 8 ans et plus
    ]

    for age_min, age_max, km_min, km_max, coeff in tranches:
        GrilleDecote.objects.create(
            marque="",  # grille générale, toutes marques
            age_min_mois=age_min,
            age_max_mois=age_max,
            km_min=km_min,
            km_max=km_max,
            coefficient_decote=coeff,
        )


def supprimer_grille_decote(apps, schema_editor):
    GrilleDecote = apps.get_model("reprise", "GrilleDecote")
    GrilleDecote.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("reprise", "0001_initial"),  # adapte au nom réel de ta dernière migration reprise
    ]

    operations = [
        migrations.RunPython(creer_grille_decote, supprimer_grille_decote),
    ]