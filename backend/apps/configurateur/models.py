# apps/configurateur/models.py
from django.db import models
import uuid

class ConfigurationVehicule(models.Model):
    """Une configuration en cours ou sauvegardée depuis le configurateur"""

    class Statut(models.TextChoices):
        EN_COURS = "en_cours", "En cours"
        SAUVEGARDEE = "sauvegardee", "Sauvegardée"
        PARTAGEE = "partagee", "Partagée"

    # Identifiant public pour partager un lien de configuration (ex: /configurateur/xxxxx)
    uuid_public = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    carrosserie = models.ForeignKey("catalogue.Carrosserie", on_delete=models.PROTECT)
    motorisation = models.ForeignKey("catalogue.Motorisation", on_delete=models.PROTECT)
    finition = models.ForeignKey("catalogue.Finition", on_delete=models.PROTECT)
    teinte = models.ForeignKey("catalogue.Teinte", on_delete=models.SET_NULL, null=True, blank=True)
    habitacle = models.ForeignKey("catalogue.Habitacle", on_delete=models.SET_NULL, null=True, blank=True)
    options = models.ManyToManyField("catalogue.Option", blank=True)

    prix_total = models.DecimalField(max_digits=12, decimal_places=0)
    statut = models.CharField(max_length=20, choices=Statut.choices, default=Statut.EN_COURS)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)