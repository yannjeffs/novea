from rest_framework import serializers

from .models import Commande, Paiement, VehiculePhysique


class VehiculePhysiqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehiculePhysique
        fields = "__all__"


class PaiementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paiement
        fields = "__all__"
        read_only_fields = ["reference", "created_at"]


class CommandeSerializer(serializers.ModelSerializer):
    paiements = PaiementSerializer(many=True, read_only=True)

    class Meta:
        model = Commande
        fields = "__all__"
        read_only_fields = ["reference", "created_at"]