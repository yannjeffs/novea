from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.permissions import EstPersonnelInterne, EstProprietaireOuPersonnelInterne
from .models import Commande, Paiement, VehiculePhysique
from .serializers import CommandeSerializer, PaiementSerializer, VehiculePhysiqueSerializer


class VehiculePhysiqueViewSet(viewsets.ModelViewSet):
    queryset = VehiculePhysique.objects.select_related("modele", "finition", "concession")
    serializer_class = VehiculePhysiqueSerializer
    permission_classes = [IsAuthenticated, EstPersonnelInterne]


class CommandeViewSet(viewsets.ModelViewSet):
    serializer_class = CommandeSerializer
    permission_classes = [IsAuthenticated, EstProprietaireOuPersonnelInterne]

    def get_queryset(self):
        user = self.request.user
        qs = Commande.objects.select_related("client", "configuration", "concession").prefetch_related("paiements")
        return qs if user.est_personnel_interne else qs.filter(client=user)

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)


class PaiementViewSet(viewsets.ModelViewSet):
    serializer_class = PaiementSerializer
    permission_classes = [IsAuthenticated, EstPersonnelInterne]
    queryset = Paiement.objects.select_related("commande")