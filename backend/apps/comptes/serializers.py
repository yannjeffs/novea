# apps/comptes/serializers.py
from rest_framework import serializers
from .models import Utilisateur


class UtilisateurSerializer(serializers.ModelSerializer):
    """Pour afficher un conseiller dans une liste (ex: sélecteur sur une commande)"""
    concession_nom = serializers.CharField(source="concession.nom", read_only=True)

    class Meta:
        model = Utilisateur
        fields = [
            "id", "username", "first_name", "last_name", "email",
            "role", "concession", "concession_nom", "telephone", "photo",
            "note_satisfaction_moyenne",
        ]
        # Jamais de password ici — voir UtilisateurCreationSerializer dédié


class UtilisateurCreationSerializer(serializers.ModelSerializer):
    """Pour créer un compte conseiller depuis le back-office (admin réseau uniquement)"""
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = Utilisateur
        fields = [
            "username", "first_name", "last_name", "email", "password",
            "role", "concession", "telephone",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")
        utilisateur = Utilisateur(**validated_data)
        utilisateur.set_password(password)  # jamais en clair, toujours hashé
        utilisateur.save()
        return utilisateur


class MoiSerializer(serializers.ModelSerializer):
    """Pour l'endpoint /api/auth/moi/ — ce que le front affiche après connexion"""
    concession_nom = serializers.CharField(source="concession.nom", read_only=True)

    class Meta:
        model = Utilisateur
        fields = ["id", "username", "first_name", "last_name", "role", "concession", "concession_nom", "photo"]