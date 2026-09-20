from rest_framework import serializers

from .models import Utilisateur


class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = [
            "id", "username", "first_name", "last_name", "email", "telephone",
            "role", "langue_preferee", "concession", "raison_sociale",
        ]
        read_only_fields = ["role"]