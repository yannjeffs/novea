"""Utilitaires partagés entre les apps du projet Novéa Cameroun."""
import uuid

from django.db import models


class TimestampedModel(models.Model):
    """Ajoute created_at / updated_at à tout modèle qui en hérite."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def generate_reference(prefix: str) -> str:
    """Génère une référence lisible et unique, ex : CMD-3F2A9B1C."""
    return f"{prefix}-{uuid.uuid4().hex[:8].upper()}"
