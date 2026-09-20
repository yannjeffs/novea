from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.permissions import EstProprietaireOuPersonnelInterne
from .models import Configuration
from .serializers import ConfigurationSerializer


class ConfigurationViewSet(viewsets.ModelViewSet):
    serializer_class = ConfigurationSerializer
    permission_classes = [IsAuthenticated, EstProprietaireOuPersonnelInterne]

    def get_queryset(self):
        user = self.request.user
        if user.est_personnel_interne:
            return Configuration.objects.all()
        return Configuration.objects.filter(client=user)

    def perform_create(self, serializer):
        configuration = serializer.save(client=self.request.user)
        configuration.calculer_prix_total()

    def perform_update(self, serializer):
        configuration = serializer.save()
        configuration.calculer_prix_total()