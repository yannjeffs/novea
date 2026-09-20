"""
Gestion commerciale : leads (demandes d'essai, de reprise, de réservation)
et planification des essais routiers.
"""
from django.conf import settings
from django.db import models

from core.mixins import TimestampedModel, generate_reference


class SourceLead(models.TextChoices):
    SITE_WEB = "site_web", "Site web"
    TELEPHONE = "telephone", "Téléphone"
    WHATSAPP = "whatsapp", "WhatsApp"
    SHOWROOM = "showroom", "Showroom"
    SALON = "salon", "Salon / événement"


class StatutLead(models.TextChoices):
    NOUVEAU = "nouveau", "Nouveau"
    QUALIFIE = "qualifie", "Qualifié"
    ESSAI_PLANIFIE = "essai_planifie", "Essai planifié"
    DEVIS_ENVOYE = "devis_envoye", "Devis envoyé"
    GAGNE = "gagne", "Gagné"
    PERDU = "perdu", "Perdu"


class Lead(TimestampedModel):
    reference = models.CharField(max_length=20, unique=True, blank=True)
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="leads"
    )
    # Coordonnées reprises même si le client n'a pas encore de compte
    nom_contact = models.CharField(max_length=150, blank=True)
    email_contact = models.EmailField(blank=True)
    telephone_contact = models.CharField(max_length=20, blank=True)

    source = models.CharField(max_length=20, choices=SourceLead.choices, default=SourceLead.SITE_WEB)
    statut = models.CharField(max_length=20, choices=StatutLead.choices, default=StatutLead.NOUVEAU)
    energie_interet = models.CharField(max_length=25, blank=True)
    montant_estime = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True)

    configuration = models.ForeignKey(
        "configurateur.Configuration", on_delete=models.SET_NULL, null=True, blank=True, related_name="leads"
    )
    concession = models.ForeignKey(
        "reseau.Concession", on_delete=models.SET_NULL, null=True, blank=True, related_name="leads"
    )
    conseiller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="leads_attribues",
    )
    notes = models.TextField(blank=True)
    premier_contact_le = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Lead"
        verbose_name_plural = "Leads"
        ordering = ["-created_at"]

    def __str__(self):
        return self.reference or f"Lead #{self.pk}"

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = generate_reference("LEAD")
        super().save(*args, **kwargs)

    @property
    def delai_premiere_reponse(self):
        """Utilisé pour l'indicateur 'délai moyen de première réponse à un lead'."""
        if self.premier_contact_le:
            return self.premier_contact_le - self.created_at
        return None


class StatutEssai(models.TextChoices):
    PLANIFIE = "planifie", "Planifié"
    CONFIRME = "confirme", "Confirmé"
    REALISE = "realise", "Réalisé"
    ANNULE = "annule", "Annulé"
    ABSENCE = "absence", "Absence client"


class Essai(TimestampedModel):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name="essais")
    concession = models.ForeignKey("reseau.Concession", on_delete=models.PROTECT, related_name="essais")
    conseiller = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="essais_geres"
    )
    vehicule_demo = models.ForeignKey(
        "ventes.VehiculePhysique", on_delete=models.SET_NULL, null=True, blank=True, related_name="essais"
    )
    date_heure = models.DateTimeField()
    duree_minutes = models.PositiveSmallIntegerField(default=45)
    statut = models.CharField(max_length=15, choices=StatutEssai.choices, default=StatutEssai.PLANIFIE)
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = "Essai"
        verbose_name_plural = "Essais"
        ordering = ["date_heure"]

    def __str__(self):
        return f"Essai {self.lead.reference} — {self.date_heure:%d/%m/%Y %H:%M}"
