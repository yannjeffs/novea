# apps/catalogue/serializers.py
from rest_framework import serializers
from .models import Carrosserie, Motorisation, Finition, Equipement, Teinte, Habitacle, Option, Devis


# ============ SERIALIZERS PUBLICS (lecture, imbriqués, filtrés sur publié) ============

class EquipementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipement
        fields = ["id", "libelle"]


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ["id", "nom", "description", "prix"]


class HabitacleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habitacle
        fields = ["id", "nom", "supplement_prix"]


class TeinteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teinte
        fields = ["id", "nom", "code_hex", "supplement_prix"]


class FinitionPublicSerializer(serializers.ModelSerializer):
    equipements = EquipementSerializer(many=True, read_only=True)
    options_disponibles = OptionSerializer(many=True, read_only=True)
    habitacles_disponibles = HabitacleSerializer(many=True, read_only=True)

    class Meta:
        model = Finition
        fields = [
            "id", "niveau", "prix_base", "delai_livraison_semaines",
            "equipements", "options_disponibles", "habitacles_disponibles",
        ]


class MotorisationPublicSerializer(serializers.ModelSerializer):
    finitions = serializers.SerializerMethodField()

    class Meta:
        model = Motorisation
        fields = [
            "id", "energie", "designation", "puissance_ch", "couple_nm",
            "transmission", "architecture", "consommation_l_100km",
            "autonomie_km", "acceleration_0_100", "finitions",
        ]

    def get_finitions(self, obj):
        # Ne renvoie que les finitions publiées, même côté public
        finitions_publiees = obj.finitions.filter(publie=True)
        return FinitionPublicSerializer(finitions_publiees, many=True).data


class CarrosseriePublicSerializer(serializers.ModelSerializer):
    motorisations = serializers.SerializerMethodField()
    teintes_disponibles = TeinteSerializer(many=True, read_only=True)

    class Meta:
        model = Carrosserie
        fields = [
            "id", "nom", "type_carrosserie", "description", "image_principale",
            "motorisations", "teintes_disponibles",
        ]

    def get_motorisations(self, obj):
        motorisations_publiees = obj.motorisations.filter(publie=True)
        return MotorisationPublicSerializer(motorisations_publiees, many=True).data


class CarrosserieListeSerializer(serializers.ModelSerializer):
    """Version allégée pour la liste catalogue (pas besoin de tout charger)"""
    prix_a_partir_de = serializers.SerializerMethodField()

    class Meta:
        model = Carrosserie
        fields = ["id", "nom", "type_carrosserie", "image_principale", "prix_a_partir_de"]

    def get_prix_a_partir_de(self, obj):
        finition = Finition.objects.filter(
            motorisation__carrosserie=obj, publie=True
        ).order_by("prix_base").first()
        return finition.prix_base if finition else None


# ============ SERIALIZERS ADMIN (lecture/écriture, plats) ============

class FinitionAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finition
        fields = ["id", "motorisation", "niveau", "prix_base", "delai_livraison_semaines", "publie"]


class MotorisationAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motorisation
        fields = "__all__"


class CarrosserieAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrosserie
        fields = "__all__"


class DevisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Devis
        fields = "__all__"
        read_only_fields = ["reference", "created_at", "updated_at"]