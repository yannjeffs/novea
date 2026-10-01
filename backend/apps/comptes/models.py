# comptes/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class Utilisateur(AbstractUser):
    """Étend l'utilisateur Django standard — hérite déjà de username, email, password, etc."""

    class Role(models.TextChoices):
        CONSEILLER = "conseiller", "Conseiller"
        CONSEILLER_PRINCIPAL = "conseiller_principal", "Conseillère/Conseiller principal"
        RESPONSABLE_SITE = "responsable_site", "Responsable de site"
        EXPERT_REPRISE = "expert_reprise", "Expert reprise"
        TECHNICIEN = "technicien", "Technicien"
        ADMIN_RESEAU = "admin_reseau", "Admin réseau"

    role = models.CharField(max_length=25, choices=Role.choices)
    concession = models.ForeignKey(
        "reseau.Concession", on_delete=models.SET_NULL, null=True, blank=True, related_name="employes"
    )
    telephone = models.CharField(max_length=20, blank=True)
    photo = models.ImageField(upload_to="utilisateurs/", blank=True, null=True)
    note_satisfaction_moyenne = models.DecimalField(
        max_digits=2, decimal_places=1, null=True, blank=True
    )   # calculée périodiquement, pas saisie à la main