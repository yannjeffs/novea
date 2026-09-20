from rest_framework import serializers

from .models import (
    DocumentVehicule,
    Finition,
    Habitacle,
    MediaVehicule,
    Motorisation,
    OptionPack,
    Teinte,
    VehiculeModele,
)


class MotorisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motorisation
        fields = "__all__"


class FinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finition
        fields = "__all__"


class TeinteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teinte
        fields = "__all__"


class HabitacleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habitacle
        fields = "__all__"


class MediaVehiculeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaVehicule
        fields = "__all__"


class DocumentVehiculeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentVehicule
        fields = "__all__"


class OptionPackSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionPack
        fields = "__all__"


class VehiculeModeleListSerializer(serializers.ModelSerializer):
    """Version légère pour les listes/catalogue (pas de médias/documents imbriqués)."""

    photo_principale = serializers.SerializerMethodField()

    class Meta:
        model = VehiculeModele
        fields = [
            "id", "nom", "slug", "carrosserie", "energie", "prix_base",
            "autonomie_km", "consommation_l_100km", "puissance_ch",
            "disponible", "photo_principale",
        ]

    def get_photo_principale(self, obj):
        media = obj.medias.filter(type_media="photo").order_by("ordre").first()
        request = self.context.get("request")
        if media and request:
            return request.build_absolute_uri(media.fichier.url)
        return None


class VehiculeModeleDetailSerializer(serializers.ModelSerializer):
    """Version complète pour la fiche véhicule."""

    motorisations = MotorisationSerializer(many=True, read_only=True)
    finitions = FinitionSerializer(many=True, read_only=True)
    teintes = TeinteSerializer(many=True, read_only=True)
    habitacles = HabitacleSerializer(many=True, read_only=True)
    medias = MediaVehiculeSerializer(many=True, read_only=True)
    documents = DocumentVehiculeSerializer(many=True, read_only=True)
    options = OptionPackSerializer(many=True, read_only=True)

    class Meta:
        model = VehiculeModele
        fields = "__all__"