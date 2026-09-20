from rest_framework import serializers

from catalogue.models import Finition, Habitacle, OptionPack, Teinte, VehiculeModele
from .models import Configuration


class ConfigurationSerializer(serializers.ModelSerializer):
    modele = serializers.PrimaryKeyRelatedField(queryset=VehiculeModele.objects.all())
    finition = serializers.PrimaryKeyRelatedField(queryset=Finition.objects.all())
    teinte = serializers.PrimaryKeyRelatedField(queryset=Teinte.objects.all(), required=False, allow_null=True)
    habitacle = serializers.PrimaryKeyRelatedField(queryset=Habitacle.objects.all(), required=False, allow_null=True)
    options = serializers.PrimaryKeyRelatedField(queryset=OptionPack.objects.all(), many=True, required=False)

    class Meta:
        model = Configuration
        fields = [
            "id", "reference", "client", "modele", "finition", "teinte", "habitacle",
            "options", "prix_total", "mensualite_estimee", "statut", "created_at",
        ]
        read_only_fields = ["reference", "client", "prix_total", "created_at"]

    def validate(self, attrs):
        modele = attrs.get("modele") or getattr(self.instance, "modele", None)
        finition = attrs.get("finition") or getattr(self.instance, "finition", None)
        if finition and modele and finition.modele_id != modele.id:
            raise serializers.ValidationError("Cette finition n'appartient pas au modèle sélectionné.")
        return attrs