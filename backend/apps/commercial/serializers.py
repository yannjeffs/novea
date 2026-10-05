# apps/commercial/serializers.py
from rest_framework import serializers
from django.db import transaction
from .models import Lead, EssaiPlanifie, Commande, EtapeHistorique
import uuid


class EssaiPlanifieSerializer(serializers.ModelSerializer):
    conseiller_nom = serializers.CharField(source="conseiller.get_full_name", read_only=True)
    concession_nom = serializers.CharField(source="concession.nom", read_only=True)

    class Meta:
        model = EssaiPlanifie
        fields = [
            "id", "lead", "concession", "concession_nom", "conseiller", "conseiller_nom",
            "vehicule_essai", "date_heure", "duree_minutes", "statut", "created_at",
        ]
        read_only_fields = ["created_at"]


class LeadSerializer(serializers.ModelSerializer):
    conseiller_nom = serializers.CharField(source="conseiller.get_full_name", read_only=True)
    concession_nom = serializers.CharField(source="concession.nom", read_only=True)
    configuration_resume = serializers.SerializerMethodField()
    essais = EssaiPlanifieSerializer(many=True, read_only=True)

    class Meta:
        model = Lead
        fields = [
            "id", "reference", "nom_client", "telephone", "email", "source",
            "concession", "concession_nom", "conseiller", "conseiller_nom",
            "configuration", "configuration_resume", "montant_estime", "statut",
            "essais", "created_at", "updated_at",
        ]
        read_only_fields = ["reference", "created_at", "updated_at"]

    def get_configuration_resume(self, obj):
        if not obj.configuration:
            return None
        c = obj.configuration
        return f"{c.carrosserie.nom} {c.finition.niveau}"

    def create(self, validated_data):
        # Génère la référence LD-xxxx automatiquement (pas saisie par le conseiller)
        validated_data["reference"] = f"LD-{uuid.uuid4().int % 10000:04d}"
        return super().create(validated_data)


class EtapeHistoriqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = EtapeHistorique
        fields = ["id", "etape", "date_passage", "commentaire"]


class CommandeSerializer(serializers.ModelSerializer):
    conseiller_nom = serializers.CharField(source="conseiller.get_full_name", read_only=True)
    concession_nom = serializers.CharField(source="concession.nom", read_only=True)
    client_nom = serializers.CharField(source="lead.nom_client", read_only=True, default="")
    vehicule_libelle = serializers.SerializerMethodField()
    historique_etapes = EtapeHistoriqueSerializer(many=True, read_only=True)

    class Meta:
        model = Commande
        fields = [
            "id", "reference", "lead", "client_nom", "devis", "reprise",
            "concession", "concession_nom", "conseiller", "conseiller_nom",
            "montant_total", "type_financement", "acompte",
            "etape", "vehicule_libelle", "date_livraison_prevue", "date_livraison_reelle",
            "historique_etapes", "created_at", "updated_at",
        ]
        read_only_fields = ["reference", "created_at", "updated_at"]

    def get_vehicule_libelle(self, obj):
        if obj.devis:
            return f"{obj.devis.carrosserie_nom} {obj.devis.finition_niveau}"
        return None

    def create(self, validated_data):
        validated_data["reference"] = f"CM-{uuid.uuid4().int % 100000:05d}"
        with transaction.atomic():
            commande = super().create(validated_data)
            # Trace la première étape dans l'historique dès la création
            EtapeHistorique.objects.create(commande=commande, etape=commande.etape)
        return commande

    def update(self, instance, validated_data):
        ancienne_etape = instance.etape
        instance = super().update(instance, validated_data)
        # Si l'étape a changé, on l'enregistre automatiquement dans l'historique
        if "etape" in validated_data and validated_data["etape"] != ancienne_etape:
            EtapeHistorique.objects.create(commande=instance, etape=instance.etape)
        return instance