# apps/configurateur/views.py
from rest_framework import viewsets, permissions
from .models import ConfigurationVehicule
from .serializers import ConfigurationVehiculeSerializer


class ConfigurationVehiculeViewSet(viewsets.ModelViewSet):
    """
    POST /api/configurateur/configurations/        → créer une configuration
    PATCH /api/configurateur/configurations/{id}/   → modifier une sélection (recalcule le prix)
    GET /api/configurateur/configurations/{uuid}/   → retrouver une config partagée
    """
    queryset = ConfigurationVehicule.objects.all()
    serializer_class = ConfigurationVehiculeSerializer
    permission_classes = [permissions.AllowAny]   # pas de compte client, accès par UUID
    lookup_field = "uuid_public"