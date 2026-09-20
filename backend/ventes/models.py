"""
Commandes, stock physique (VIN) et paiements (acomptes MoMo / Orange Money /
virement / carte).
"""
from django.conf import settings
from django.db import models

from core.mixins import TimestampedModel, generate_reference


class StatutVehiculePhysique(models.TextChoices):
    EN_PREPARATION = "en_preparation", "En préparation"
    DISPONIBLE = "disponible", "Disponible"
    RESERVE = "reserve", "Réservé"
    VENDU = "vendu", "Vendu"
    ARCHIVE = "archive", "Archivé"


class VehiculePhysique(TimestampedModel):
    """Un exemplaire physique identifié par son VIN — distinct du modèle au catalogue."""

    vin = models.CharField(max_length=17, unique=True)
    modele = models.ForeignKey("catalogue.VehiculeModele", on_delete=models.PROTECT, related_name="unites")
    finition = models.ForeignKey(
        "catalogue.Finition", on_delete=models.PROTECT, null=True, blank=True, related_name="unites"
    )
    teinte = models.ForeignKey(
        "catalogue.Teinte", on_delete=models.SET_NULL, null=True, blank=True, related_name="unites"
    )
    habitacle = models.ForeignKey(
        "catalogue.Habitacle", on_delete=models.SET_NULL, null=True, blank=True, related_name="unites"
    )
    statut = models.CharField(
        max_length=20, choices=StatutVehiculePhysique.choices, default=StatutVehiculePhysique.EN_PREPARATION
    )
    concession = models.ForeignKey(
        "reseau.Concession", on_delete=models.SET_NULL, null=True, blank=True, related_name="stock"
    )
    date_arrivee = models.DateField(null=True, blank=True)
    kilometrage = models.PositiveIntegerField(default=0, help_text="Utile pour les véhicules de démonstration.")

    class Meta:
        verbose_name = "Véhicule physique"
        verbose_name_plural = "Véhicules physiques (stock VIN)"
        ordering = ["-date_arrivee"]

    def __str__(self):
        return f"{self.vin} — {self.modele}"


class FinancementType(models.TextChoices):
    COMPTANT = "comptant", "Comptant"
    CREDIT = "credit", "Crédit"
    LOA = "loa", "LOA"


class EtapeCommande(models.TextChoices):
    NOUVELLE = "nouvelle", "Nouvelle"
    FINANCEMENT_EN_COURS = "financement_en_cours", "Financement en cours"
    EN_PRODUCTION = "en_production", "En production"
    EN_TRANSIT = "en_transit", "Fret maritime en transit"
    DEDOUANEMENT = "dedouanement", "Dédouanement Douala"
    PRETE_LIVRAISON = "prete_livraison", "Prête à la livraison"
    LIVREE = "livree", "Livrée"
    ANNULEE = "annulee", "Annulée"


class Commande(TimestampedModel):
    reference = models.CharField(max_length=20, unique=True, blank=True)
    lead = models.ForeignKey(
        "commercial.Lead", on_delete=models.SET_NULL, null=True, blank=True, related_name="commandes"
    )
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="commandes")
    configuration = models.ForeignKey(
        "configurateur.Configuration", on_delete=models.PROTECT, related_name="commandes"
    )
    vehicule_physique = models.OneToOneField(
        VehiculePhysique, on_delete=models.SET_NULL, null=True, blank=True, related_name="commande"
    )
    concession = models.ForeignKey("reseau.Concession", on_delete=models.PROTECT, related_name="commandes")

    montant_total = models.DecimalField(max_digits=12, decimal_places=0)
    acompte_montant = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    financement_type = models.CharField(
        max_length=15, choices=FinancementType.choices, default=FinancementType.COMPTANT
    )
    etape = models.CharField(max_length=25, choices=EtapeCommande.choices, default=EtapeCommande.NOUVELLE)
    date_prevue_livraison = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
        ordering = ["-created_at"]

    def __str__(self):
        return self.reference or f"Commande #{self.pk}"

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = generate_reference("CMD")
        super().save(*args, **kwargs)


class CanalPaiement(models.TextChoices):
    MOMO = "momo", "MTN Mobile Money"
    ORANGE_MONEY = "orange_money", "Orange Money"
    VIREMENT = "virement", "Virement bancaire"
    CARTE = "carte", "Carte bancaire"
    ESPECES = "especes", "Espèces (en concession)"


class StatutPaiement(models.TextChoices):
    EN_ATTENTE = "en_attente", "En attente"
    VALIDE = "valide", "Validé"
    ECHOUE = "echoue", "Échoué"
    REMBOURSE = "rembourse", "Remboursé"


class Paiement(TimestampedModel):
    reference = models.CharField(max_length=20, unique=True, blank=True)
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name="paiements")
    canal = models.CharField(max_length=15, choices=CanalPaiement.choices)
    montant = models.DecimalField(max_digits=12, decimal_places=0)
    statut = models.CharField(max_length=15, choices=StatutPaiement.choices, default=StatutPaiement.EN_ATTENTE)
    reference_externe = models.CharField(
        max_length=100,
        blank=True,
        help_text="Identifiant de transaction renvoyé par MoMo / Orange Money / la banque.",
    )

    class Meta:
        verbose_name = "Paiement"
        verbose_name_plural = "Paiements"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.reference} — {self.get_canal_display()} ({self.montant} FCFA)"

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = generate_reference("PAY")
        super().save(*args, **kwargs)
