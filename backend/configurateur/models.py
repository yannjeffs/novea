"""
Configuration enregistrée par un client (ou par un conseiller pour son
compte) : un modèle, une finition, une teinte, un habitacle et des options,
dont le prix total est recalculé à chaque modification.

Le simulateur de crédit (mensualité) sera branché ici ultérieurement — la
décision de l'intégrer dans le configurateur ou ailleurs est encore ouverte,
d'où le champ `mensualite_estimee` déjà prévu mais non calculé pour l'instant.
"""
from django.conf import settings
from django.db import models

from core.mixins import TimestampedModel, generate_reference


class StatutConfiguration(models.TextChoices):
    BROUILLON = "brouillon", "Brouillon"
    ENREGISTREE = "enregistree", "Enregistrée"
    CONVERTIE = "convertie", "Convertie en commande"


class Configuration(TimestampedModel):
    reference = models.CharField(max_length=20, unique=True, blank=True)
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="configurations",
    )
    modele = models.ForeignKey("catalogue.VehiculeModele", on_delete=models.PROTECT, related_name="configurations")
    finition = models.ForeignKey("catalogue.Finition", on_delete=models.PROTECT, related_name="configurations")
    teinte = models.ForeignKey(
        "catalogue.Teinte", on_delete=models.SET_NULL, null=True, blank=True, related_name="configurations"
    )
    habitacle = models.ForeignKey(
        "catalogue.Habitacle", on_delete=models.SET_NULL, null=True, blank=True, related_name="configurations"
    )
    options = models.ManyToManyField("catalogue.OptionPack", related_name="configurations", blank=True)

    prix_total = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    mensualite_estimee = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    statut = models.CharField(
        max_length=20, choices=StatutConfiguration.choices, default=StatutConfiguration.BROUILLON
    )

    class Meta:
        verbose_name = "Configuration"
        verbose_name_plural = "Configurations"
        ordering = ["-created_at"]

    def __str__(self):
        return self.reference or f"Configuration #{self.pk}"

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = generate_reference("CFG")
        super().save(*args, **kwargs)

    def calculer_prix_total(self) -> int:
        """Recalcule et enregistre le prix total à partir du modèle et des choix."""
        total = self.modele.prix_base + self.finition.supplement_prix
        if self.teinte_id:
            total += self.teinte.supplement_prix
        if self.habitacle_id:
            total += self.habitacle.supplement_prix
        total += sum(self.options.values_list("prix", flat=True))
        self.prix_total = total
        self.save(update_fields=["prix_total"])
        return total
