# occasion/models.py
from django.db import models

class VehiculeOccasion(models.Model):
    """Un véhicule physique unique, identifié par son VIN"""

    class Etat(models.TextChoices):
        RECEPTION = "reception", "Réception"
        REMISE_EN_ETAT = "remise_en_etat", "Remise en état"
        PHOTO_ANNONCE = "photo_annonce", "Photo & annonce"
        EN_LIGNE = "en_ligne", "En ligne"
        RESERVE = "reserve", "Réservé"
        VENDU = "vendu", "Vendu"

    class Qualite(models.TextChoices):
        TRES_BON = "tres_bon", "Très bon"
        BON = "bon", "Bon"
        EXCELLENT = "excellent", "Excellent"

    vin = models.CharField(max_length=17, unique=True)   # norme VIN : 17 caractères

    # Filiation catalogue (motorisation/finition d'origine, pour les caractéristiques techniques)
    carrosserie = models.ForeignKey("catalogue.Carrosserie", on_delete=models.PROTECT)
    motorisation = models.ForeignKey("catalogue.Motorisation", on_delete=models.PROTECT)
    finition_origine = models.CharField(max_length=20, blank=True)  # snapshot texte, pas de FK stricte

    teinte = models.CharField(max_length=50)
    habitacle = models.CharField(max_length=100, blank=True)

    annee_mise_circulation = models.PositiveIntegerField()
    kilometrage = models.PositiveIntegerField()
    nombre_proprietaires = models.PositiveSmallIntegerField(default=1)
    etat_general = models.CharField(max_length=20, choices=Qualite.choices)

    concession = models.ForeignKey("reseau.Concession", on_delete=models.PROTECT)
    etape = models.CharField(max_length=20, choices=Etat.choices, default=Etat.RECEPTION)

    origine_reprise = models.OneToOneField(
        "reprise.DemandeReprise", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="vehicule_issu"
    )

    prix_revient = models.DecimalField(max_digits=12, decimal_places=0)   # coût d'acquisition + remise en état
    prix_vente = models.DecimalField(max_digits=12, decimal_places=0)
    garantie_mois = models.PositiveSmallIntegerField(default=6)
    certifie_novea = models.BooleanField(default=False)   # a passé le contrôle 120 points
    est_vehicule_demo = models.BooleanField(default=False)

    date_reception = models.DateField(auto_now_add=True)
    date_mise_en_ligne = models.DateField(null=True, blank=True)
    date_vente = models.DateField(null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)


class PhotoVehicule(models.Model):
    vehicule = models.ForeignKey(VehiculeOccasion, on_delete=models.CASCADE, related_name="photos")
    image = models.ImageField(upload_to="occasion/photos/")
    ordre = models.PositiveIntegerField(default=0)
    est_principale = models.BooleanField(default=False)


class ControleQualite(models.Model):
    """Le contrôle 120 points affiché sur la fiche occasion"""
    vehicule = models.OneToOneField(VehiculeOccasion, on_delete=models.CASCADE, related_name="controle")
    nombre_points_controles = models.PositiveIntegerField(default=120)
    rapport_pdf = models.FileField(upload_to="occasion/rapports/", blank=True, null=True)
    date_controle = models.DateField()
    technicien = models.ForeignKey("comptes.Utilisateur", on_delete=models.SET_NULL, null=True)


class EvenementHistorique(models.Model):
    """Ex : 'Révision 60 000 km hors réseau', 'Première mise en circulation'"""
    vehicule = models.ForeignKey(VehiculeOccasion, on_delete=models.CASCADE, related_name="historique")
    date_evenement = models.DateField()
    libelle = models.CharField(max_length=200)
    kilometrage_a_date = models.PositiveIntegerField(null=True, blank=True)