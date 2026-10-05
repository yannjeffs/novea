# apps/paiement/models.py
from django.db import models

class Paiement(models.Model):
    """Une transaction de paiement mobile money, liée à une réservation ou une commande"""

    class Methode(models.TextChoices):
        MTN_MOMO = "mtn_momo", "MTN Mobile Money"
        ORANGE_MONEY = "orange_money", "Orange Money"

    class Statut(models.TextChoices):
        EN_ATTENTE = "en_attente", "En attente"
        REUSSI = "reussi", "Réussi"
        ECHOUE = "echoue", "Échoué"
        ANNULE = "annule", "Annulé"

    # Lien optionnel : un paiement peut concerner un acompte de réservation (lead)
    # ou un paiement sur une commande déjà créée
    lead = models.ForeignKey("commercial.Lead", on_delete=models.SET_NULL, null=True, blank=True)
    commande = models.ForeignKey("commercial.Commande", on_delete=models.SET_NULL, null=True, blank=True)

    methode = models.CharField(max_length=20, choices=Methode.choices)
    numero_telephone = models.CharField(max_length=20)
    montant = models.DecimalField(max_digits=12, decimal_places=0)

    reference_interne = models.CharField(max_length=30, unique=True)   # générée par nous
    reference_operateur = models.CharField(max_length=100, blank=True)  # renvoyée par MTN/Orange
    statut = models.CharField(max_length=20, choices=Statut.choices, default=Statut.EN_ATTENTE)

    payload_webhook = models.JSONField(null=True, blank=True)   # réponse brute, utile pour audit/debug

    date_initiation = models.DateTimeField(auto_now_add=True)
    date_confirmation = models.DateTimeField(null=True, blank=True)