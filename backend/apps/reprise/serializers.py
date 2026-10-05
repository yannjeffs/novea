# apps/reprise/serializers.py
from rest_framework import serializers
from django.db import transaction
import uuid
from .models import DemandeReprise, RendezVousExpertise
from .services import calculer_estimation_en_ligne


class RendezVousExpertiseSerializer(serializers.ModelSerializer):
    concession_nom = serializers.CharField(source="concession.nom", read_only=True)

    class Meta:
        model = RendezVousExpertise
        fields = ["id", "demande", "concession", "concession_nom", "date_heure", "realise"]


class DemandeRepriseListeSerializer(serializers.ModelSerializer):
    """Pour le tableau back-office 'Reprises' — vue allégée"""
    ecart_pct = serializers.ReadOnlyField(source="ecart_estimation_expertise_pct")

    class Meta:
        model = DemandeReprise
        fields = [
            "id", "reference", "nom_client", "marque_modele", "etape",
            "estimation_en_ligne", "valeur_expertise", "ecart_pct", "created_at",
        ]


class DemandeRepriseDetailSerializer(serializers.ModelSerializer):
    """Fiche complète — panneau de droite sur la maquette back-office"""
    ecart_pct = serializers.ReadOnlyField(source="ecart_estimation_expertise_pct")
    expert_nom = serializers.CharField(source="expert_assigne.get_full_name", read_only=True)
    rendez_vous = RendezVousExpertiseSerializer(read_only=True)

    class Meta:
        model = DemandeReprise
        fields = [
            "id", "reference", "nom_client", "telephone", "marque_modele", "energie",
            "annee", "kilometrage", "etat_declare", "carnet_entretien_complet",
            "concession", "configuration_liee",
            "estimation_en_ligne", "valeur_expertise", "offre_transmise",
            "offre_validite_jours", "offre_validite_km", "ecart_pct",
            "etape", "expert_assigne", "expert_nom", "rendez_vous",
            "created_at", "updated_at",
        ]
        read_only_fields = ["reference", "estimation_en_ligne", "created_at", "updated_at"]


class DemandeRepriseCreationSerializer(serializers.ModelSerializer):
    """Serializer dédié au formulaire public 'Estimation en ligne'"""
    valeur_neuf_estimee = serializers.DecimalField(
        max_digits=12, decimal_places=0, write_only=True,
        help_text="Valeur déclarative du véhicule à l'état neuf, utilisée pour calculer la décote"
    )

    class Meta:
        model = DemandeReprise
        fields = [
            "nom_client", "telephone", "marque_modele", "energie", "annee",
            "kilometrage", "etat_declare", "carnet_entretien_complet",
            "concession", "valeur_neuf_estimee",
        ]

    def create(self, validated_data):
        valeur_neuf = validated_data.pop("valeur_neuf_estimee")
        estimation = calculer_estimation_en_ligne(
            marque_modele=validated_data["marque_modele"],
            annee=validated_data["annee"],
            kilometrage=validated_data["kilometrage"],
            valeur_neuf_estimee=valeur_neuf,
        )
        return DemandeReprise.objects.create(
            reference=f"RP-{uuid.uuid4().int % 10000:04d}",
            estimation_en_ligne=estimation,
            **validated_data,
        )