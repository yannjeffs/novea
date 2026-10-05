# apps/reprise/views.py
from rest_framework import viewsets, permissions
from .models import DemandeReprise
from .serializers import (
    DemandeRepriseListeSerializer, DemandeRepriseDetailSerializer,
    DemandeRepriseCreationSerializer,
)


class DemandeRepriseCreationView(viewsets.mixins.CreateModelMixin, viewsets.GenericViewSet):
    """POST public : /api/reprise/estimation/"""
    queryset = DemandeReprise.objects.all()
    serializer_class = DemandeRepriseCreationSerializer
    permission_classes = [permissions.AllowAny]


class DemandeRepriseAdminViewSet(viewsets.ModelViewSet):
    """CRUD back-office : /api/admin/reprise/demandes/"""
    queryset = DemandeReprise.objects.all().order_by("-created_at")
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return DemandeRepriseListeSerializer
        return DemandeRepriseDetailSerializer