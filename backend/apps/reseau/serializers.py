# apps/reseau/serializers.py
from rest_framework import serializers
from .models import Concession
from apps.commercial.models import Commande, EssaiPlanifie


class ConcessionSerializer(serializers.ModelSerializer):
    vehicules_en_parc = serializers.SerializerMethodField()
    commandes_en_cours = serializers.SerializerMethodField()
    essais_planifies = serializers.SerializerMethodField()

    class Meta:
        model = Concession
        fields = [
            "id", "nom", "ville", "adresse", "telephone",
            "latitude", "longitude", "capacite_essais_simultanes", "active",
            "vehicules_en_parc", "commandes_en_cours", "essais_planifies",
        ]

    def get_vehicules_en_parc(self, obj):
        return obj.vehiculeoccasion_set.count() if hasattr(obj, "vehiculeoccasion_set") else 0

    def get_commandes_en_cours(self, obj):
        return Commande.objects.filter(
            concession=obj
        ).exclude(etape=Commande.Etape.LIVREE).count()

    def get_essais_planifies(self, obj):
        return EssaiPlanifie.objects.filter(
            concession=obj, statut__in=["a_confirmer", "confirme"]
        ).count()