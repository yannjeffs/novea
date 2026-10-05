# apps/occasion/views.py
from rest_framework import viewsets, permissions
from .models import VehiculeOccasion
from .serializers import VehiculeOccasionDetailSerializer, VehiculeOccasionAdminSerializer


class VehiculeOccasionDetailViewSet(viewsets.ReadOnlyModelViewSet):
    """GET /api/occasions/{id}/ — fiche publique"""
    queryset = VehiculeOccasion.objects.filter(etape__in=["en_ligne", "reserve"])
    serializer_class = VehiculeOccasionDetailSerializer
    permission_classes = [permissions.AllowAny]


class VehiculeOccasionAdminViewSet(viewsets.ModelViewSet):
    """CRUD complet back-office : /api/admin/occasions/"""
    queryset = VehiculeOccasion.objects.all().order_by("-date_reception")
    serializer_class = VehiculeOccasionAdminSerializer
    permission_classes = [permissions.IsAuthenticated]