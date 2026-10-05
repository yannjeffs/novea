# apps/occasion/serializers.py
from rest_framework import serializers
from .models import VehiculeOccasion, PhotoVehicule, ControleQualite, EvenementHistorique


# ============ SERIALIZERS PUBLICS ============

class PhotoVehiculeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoVehicule
        fields = ["id", "image", "ordre", "est_principale"]


class ControleQualiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ControleQualite
        fields = ["nombre_points_controles", "rapport_pdf", "date_controle"]


class EvenementHistoriqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvenementHistorique
        fields = ["date_evenement", "libelle", "kilometrage_a_date"]


class VehiculeOccasionListeSerializer(serializers.ModelSerializer):
    """Pour l'affichage des cartes dans les résultats de recherche (hors ES, ex: 'Autres' sur la fiche)"""
    photo_principale = serializers.SerializerMethodField()
    carrosserie_nom = serializers.CharField(source="carrosserie.nom", read_only=True)
    energie = serializers.CharField(source="motorisation.energie", read_only=True)

    class Meta:
        model = VehiculeOccasion
        fields = [
            "id", "vin", "carrosserie_nom", "energie", "annee_mise_circulation",
            "kilometrage", "prix_vente", "teinte", "certifie_novea", "photo_principale",
        ]

    def get_photo_principale(self, obj):
        photo = obj.photos.filter(est_principale=True).first()
        return photo.image.url if photo else None


class VehiculeOccasionDetailSerializer(serializers.ModelSerializer):
    """Fiche complète d'un véhicule d'occasion"""
    photos = PhotoVehiculeSerializer(many=True, read_only=True)
    controle = ControleQualiteSerializer(read_only=True)
    historique = EvenementHistoriqueSerializer(many=True, read_only=True)
    carrosserie_nom = serializers.CharField(source="carrosserie.nom", read_only=True)
    motorisation_designation = serializers.CharField(source="motorisation.designation", read_only=True)
    energie = serializers.CharField(source="motorisation.energie", read_only=True)
    concession_nom = serializers.CharField(source="concession.nom", read_only=True)

    class Meta:
        model = VehiculeOccasion
        fields = [
            "id", "vin", "carrosserie_nom", "motorisation_designation", "energie",
            "teinte", "habitacle", "annee_mise_circulation", "kilometrage",
            "nombre_proprietaires", "etat_general", "concession_nom",
            "prix_vente", "garantie_mois", "certifie_novea",
            "photos", "controle", "historique",
        ]
        # Volontairement absents : prix_revient, etape, est_vehicule_demo (infos internes)


# ============ SERIALIZER ADMIN ============

class VehiculeOccasionAdminSerializer(serializers.ModelSerializer):
    marge = serializers.SerializerMethodField()

    class Meta:
        model = VehiculeOccasion
        fields = "__all__"

    def get_marge(self, obj):
        return obj.prix_vente - obj.prix_revient