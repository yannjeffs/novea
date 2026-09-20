from rest_framework import serializers

from .models import Essai, Lead


class LeadCreationSerializer(serializers.ModelSerializer):
    """Utilisé pour le formulaire public (site vitrine) — champs minimaux."""

    class Meta:
        model = Lead
        fields = [
            "nom_contact", "email_contact", "telephone_contact",
            "source", "energie_interet", "configuration", "concession", "notes",
        ]

    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user.is_authenticated and not request.user.est_personnel_interne:
            validated_data["client"] = request.user
        return super().create(validated_data)


class LeadSerializer(serializers.ModelSerializer):
    """Utilisé côté back-office — accès complet en lecture/écriture."""

    delai_premiere_reponse = serializers.DurationField(read_only=True)

    class Meta:
        model = Lead
        fields = "__all__"
        read_only_fields = ["reference", "created_at"]


class EssaiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Essai
        fields = "__all__"