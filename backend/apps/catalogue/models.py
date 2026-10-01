# catalogue/models.py
from django.db import models

class Carrosserie(models.Model):
    """Ex : Novéa A1, A4, S6, P2, GT"""
    nom = models.CharField(max_length=50, unique=True)          # "Novéa S6"
    type_carrosserie = models.CharField(max_length=30)           # citadine, berline, SUV, pick-up, coupé
    description = models.TextField(blank=True)
    image_principale = models.ImageField(upload_to="carrosseries/")
    publie = models.BooleanField(default=False)                  # visible côté site public
    ordre_affichage = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Motorisation(models.Model):
    """Ex : '2.4 Diesel 190 ch 4x4' pour la S6"""
    class TypeEnergie(models.TextChoices):
        ESSENCE = "essence", "Essence"
        DIESEL = "diesel", "Diesel"
        HYBRIDE = "hybride", "Hybride"
        HYBRIDE_RECHARGEABLE = "hybride_rechargeable", "Hybride rechargeable"
        ELECTRIQUE = "electrique", "Électrique"

    carrosserie = models.ForeignKey(Carrosserie, on_delete=models.CASCADE, related_name="motorisations")
    energie = models.CharField(max_length=25, choices=TypeEnergie.choices)
    designation = models.CharField(max_length=100)     # "2.4 Turbo diesel NX-D24"
    puissance_ch = models.PositiveIntegerField()
    couple_nm = models.PositiveIntegerField(null=True, blank=True)
    transmission = models.CharField(max_length=50)      # "Boîte manuelle 6 rapports"
    architecture = models.CharField(max_length=100)     # "Traction avant, moteur thermique"
    consommation_l_100km = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    autonomie_km = models.PositiveIntegerField(null=True, blank=True)   # pour hybride/électrique
    acceleration_0_100 = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    reservoir_capacite = models.CharField(max_length=50, blank=True)
    publie = models.BooleanField(default=False)


class Finition(models.Model):
    """Ex : Essentiel / Confort / Prestige"""
    class Niveau(models.TextChoices):
        ESSENTIEL = "essentiel", "Essentiel"
        CONFORT = "confort", "Confort"
        PRESTIGE = "prestige", "Prestige"

    motorisation = models.ForeignKey(Motorisation, on_delete=models.CASCADE, related_name="finitions")
    niveau = models.CharField(max_length=20, choices=Niveau.choices)
    prix_base = models.DecimalField(max_digits=12, decimal_places=0)   # FCFA, pas de décimales
    delai_livraison_semaines = models.PositiveIntegerField(default=8)
    publie = models.BooleanField(default=False)

    class Meta:
        unique_together = ("motorisation", "niveau")


class Equipement(models.Model):
    """Liste d'équipements liés à une finition (freinage d'urgence, alerte franchissement...)"""
    finition = models.ForeignKey(Finition, on_delete=models.CASCADE, related_name="equipements")
    libelle = models.CharField(max_length=150)


class Teinte(models.Model):
    nom = models.CharField(max_length=50)          # "Bleu Abysse"
    code_hex = models.CharField(max_length=7)       # "#1B3A5C" pour affichage swatch
    supplement_prix = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    carrosseries = models.ManyToManyField(Carrosserie, related_name="teintes_disponibles")


class Habitacle(models.Model):
    """Ex : Similicuir sable, Cuir noir ventilé..."""
    nom = models.CharField(max_length=100)
    supplement_prix = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    finitions = models.ManyToManyField(Finition, related_name="habitacles_disponibles")


class Option(models.Model):
    """Ex : Pack Routes Dégradées, Attelage et galerie de toit..."""
    nom = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    prix = models.DecimalField(max_digits=10, decimal_places=0)
    finitions = models.ManyToManyField(Finition, related_name="options_disponibles")


class Devis(models.Model):
    """Snapshot figé d'une configuration au moment de la génération du PDF."""

    class Statut(models.TextChoices):
        GENERE = "genere", "Généré"
        ENVOYE = "envoye", "Envoyé"
        EXPIRE = "expire", "Expiré"
        CONVERTI = "converti", "Converti en commande"

    reference = models.CharField(max_length=20, unique=True)  # ex: "DV-2418"
    configuration = models.ForeignKey(
        "configurateur.ConfigurationVehicule",
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name="devis"
    )
    lead = models.ForeignKey(
        "commercial.Lead", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="devis"
    )

    # --- Snapshot figé (indépendant du catalogue live) ---
    carrosserie_nom = models.CharField(max_length=50)
    motorisation_designation = models.CharField(max_length=100)
    finition_niveau = models.CharField(max_length=20)
    teinte_nom = models.CharField(max_length=50)
    habitacle_nom = models.CharField(max_length=100, blank=True)
    options_snapshot = models.JSONField(default=list)   # [{"nom": "...", "prix": ...}, ...]
    prix_total = models.DecimalField(max_digits=12, decimal_places=0)

    fichier_pdf = models.FileField(upload_to="devis/", blank=True, null=True)
    statut = models.CharField(max_length=20, choices=Statut.choices, default=Statut.GENERE)
    valide_jusquau = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)