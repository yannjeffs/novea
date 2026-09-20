from django.db import models


class Concession(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    ville = models.CharField(max_length=100)
    adresse = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    capacite_essai_quotidienne = models.PositiveSmallIntegerField(
        default=4, help_text="Nombre d'essais routiers pouvant être planifiés par jour."
    )
    horaires = models.CharField(
        max_length=255,
        blank=True,
        help_text="Ex : Lun-Ven 8h-18h, Sam 9h-13h",
    )
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    actif = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Concession"
        verbose_name_plural = "Concessions"
        ordering = ["ville", "nom"]

    def __str__(self):
        return f"{self.nom} ({self.ville})"
