# apps/configurateur/serializers.py
from rest_framework import serializers
from .models import ConfigurationVehicule
from .services import calculer_prix_configuration


class ConfigurationVehiculeSerializer(serializers.ModelSerializer):
    carrosserie_nom = serializers.CharField(source="carrosserie.nom", read_only=True)
    motorisation_designation = serializers.CharField(source="motorisation.designation", read_only=True)
    finition_niveau = serializers.CharField(source="finition.niveau", read_only=True)
    teinte_nom = serializers.CharField(source="teinte.nom", read_only=True, allow_null=True)
    habitacle_nom = serializers.CharField(source="habitacle.nom", read_only=True, allow_null=True)
    options_detail = serializers.SerializerMethodField()

    class Meta:
        model = ConfigurationVehicule
        fields = [
            "id", "uuid_public", "carrosserie", "carrosserie_nom",
            "motorisation", "motorisation_designation",
            "finition", "finition_niveau",
            "teinte", "teinte_nom", "habitacle", "habitacle_nom",
            "options", "options_detail", "prix_total", "statut",
            "created_at", "updated_at",
        ]
        read_only_fields = ["uuid_public", "prix_total", "created_at", "updated_at"]

    def get_options_detail(self, obj):
        return [{"id": o.id, "nom": o.nom, "prix": o.prix} for o in obj.options.all()]

    def validate(self, data):
        """Vérifie la cohérence de la hiérarchie carrosserie → motorisation → finition"""
        motorisation = data.get("motorisation") or getattr(self.instance, "motorisation", None)
        carrosserie = data.get("carrosserie") or getattr(self.instance, "carrosserie", None)
        finition = data.get("finition") or getattr(self.instance, "finition", None)

        if motorisation and carrosserie and motorisation.carrosserie_id != carrosserie.id:
            raise serializers.ValidationError(
                "Cette motorisation n'appartient pas à la carrosserie sélectionnée."
            )
        if finition and motorisation and finition.motorisation_id != motorisation.id:
            raise serializers.ValidationError(
                "Cette finition n'appartient pas à la motorisation sélectionnée."
            )
        return data

    def create(self, validated_data):
        options = validated_data.pop("options", [])
        instance = ConfigurationVehicule(**validated_data)
        instance.prix_total = calculer_prix_configuration(
            finition_id=validated_data["finition"].id,
            teinte_id=validated_data.get("teinte").id if validated_data.get("teinte") else None,
            habitacle_id=validated_data.get("habitacle").id if validated_data.get("habitacle") else None,
            options_ids=[o.id for o in options],
        )
        instance.save()
        instance.options.set(options)
        return instance

    def update(self, instance, validated_data):
        options = validated_data.pop("options", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if options is not None:
            instance.options.set(options)

        # Recalcul systématique à chaque modification (changement de teinte, ajout d'option...)
        instance.prix_total = calculer_prix_configuration(
            finition_id=instance.finition_id,
            teinte_id=instance.teinte_id,
            habitacle_id=instance.habitacle_id,
            options_ids=list(instance.options.values_list("id", flat=True)),
        )
        instance.save()
        return instance