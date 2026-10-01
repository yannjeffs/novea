# apps/catalogue/views.py
from rest_framework import viewsets, permissions
from .models import Carrosserie, Motorisation, Finition, Devis
from .serializers import (
    CarrosserieListeSerializer, CarrosseriePublicSerializer, CarrosserieAdminSerializer,
    MotorisationAdminSerializer, FinitionAdminSerializer, DevisSerializer,
)


class EstConseillerOuLectureSeule(permissions.BasePermission):
    """Lecture libre à tous, écriture réservée aux comptes authentifiés (conseillers/admin)"""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated


# ---------- Endpoints publics ----------

class CarrosseriePublicViewSet(viewsets.ReadOnlyModelViewSet):
    """GET /api/catalogue/carrosseries/  et  /api/catalogue/carrosseries/{id}/"""
    queryset = Carrosserie.objects.filter(publie=True).order_by("ordre_affichage")
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == "list":
            return CarrosserieListeSerializer
        return CarrosseriePublicSerializer


# ---------- Endpoints back-office ----------

class CarrosserieAdminViewSet(viewsets.ModelViewSet):
    """CRUD complet : /api/admin/catalogue/carrosseries/"""
    queryset = Carrosserie.objects.all().order_by("ordre_affichage")
    serializer_class = CarrosserieAdminSerializer
    permission_classes = [permissions.IsAuthenticated]


class MotorisationAdminViewSet(viewsets.ModelViewSet):
    queryset = Motorisation.objects.all()
    serializer_class = MotorisationAdminSerializer
    permission_classes = [permissions.IsAuthenticated]


class FinitionAdminViewSet(viewsets.ModelViewSet):
    queryset = Finition.objects.all()
    serializer_class = FinitionAdminSerializer
    permission_classes = [permissions.IsAuthenticated]


class DevisViewSet(viewsets.ModelViewSet):
    queryset = Devis.objects.all().order_by("-created_at")
    serializer_class = DevisSerializer
    permission_classes = [permissions.IsAuthenticated]