"""
Utilisateurs de la plateforme Novéa Cameroun.

Un seul modèle (AUTH_USER_MODEL) couvre les clients (particuliers et
entreprises) et le personnel interne (conseillers, chefs des ventes,
responsables stock, direction, administrateurs catalogue), différenciés
par le champ `role`. Les partenaires externes (transitaire, banque/EMF)
ne sont pas gérés comme des comptes classiques : ils accèdent via des
intégrations dédiées (cf. cahier des charges — Intégrations tierces).
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.TextChoices):
    CLIENT_PARTICULIER = "client_particulier", "Client particulier"
    CLIENT_ENTREPRISE = "client_entreprise", "Client entreprise / flotte"
    CONSEILLER = "conseiller", "Conseiller commercial"
    CHEF_VENTES = "chef_ventes", "Chef des ventes / responsable de site"
    RESPONSABLE_STOCK = "responsable_stock", "Responsable stock et logistique"
    DIRECTION = "direction", "Direction commerciale"
    ADMIN_CATALOGUE = "admin_catalogue", "Administrateur catalogue"


class Langue(models.TextChoices):
    FRANCAIS = "fr", "Français"
    ANGLAIS = "en", "Anglais"


class Utilisateur(AbstractUser):
    """
    `username` (hérité d'AbstractUser) reste utilisé pour l'authentification
    du personnel interne ; les clients se connectent plutôt par e-mail ou
    téléphone (à brancher sur un backend d'auth dédié côté API).
    """

    role = models.CharField(max_length=30, choices=Role.choices, default=Role.CLIENT_PARTICULIER)
    telephone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    langue_preferee = models.CharField(max_length=2, choices=Langue.choices, default=Langue.FRANCAIS)

    # Personnel interne uniquement (conseiller, chef des ventes, responsable stock...)
    concession = models.ForeignKey(
        "reseau.Concession",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employes",
        help_text="Concession de rattachement, pour le personnel interne.",
    )

    # Client entreprise / flotte uniquement
    raison_sociale = models.CharField(max_length=255, blank=True)
    numero_contribuable = models.CharField(max_length=50, blank=True)

    # Double authentification (2FA SMS) — cf. besoins non fonctionnels sécurité
    deux_facteurs_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"

    @property
    def est_personnel_interne(self) -> bool:
        return self.role not in {Role.CLIENT_PARTICULIER, Role.CLIENT_ENTREPRISE}
