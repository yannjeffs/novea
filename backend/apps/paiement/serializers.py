# apps/paiement/serializers.py
from rest_framework import serializers
from .models import Paiement


class PaiementInitiationSerializer(serializers.Serializer):
    """Pas un ModelSerializer classique : ne crée pas directement l'objet, déclenche l'appel opérateur"""
    methode = serializers.ChoiceField(choices=Paiement.Methode.choices)
    numero_telephone = serializers.CharField(max_length=20)
    montant = serializers.DecimalField(max_digits=12, decimal_places=0)
    lead = serializers.IntegerField(required=False)
    commande = serializers.IntegerField(required=False)


class PaiementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paiement
        fields = "__all__"
        read_only_fields = ["reference_interne", "statut", "payload_webhook", "date_initiation", "date_confirmation"]