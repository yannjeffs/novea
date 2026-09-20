from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from core.permissions import EstPersonnelInterne
from .models import Essai, Lead
from .serializers import EssaiSerializer, LeadCreationSerializer, LeadSerializer


class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.select_related("conseiller", "concession", "configuration")

    def get_serializer_class(self):
        if self.action == "create":
            return LeadCreationSerializer
        return LeadSerializer

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [IsAuthenticated(), EstPersonnelInterne()]


class EssaiViewSet(viewsets.ModelViewSet):
    queryset = Essai.objects.select_related("lead", "concession", "conseiller")
    serializer_class = EssaiSerializer
    permission_classes = [IsAuthenticated, EstPersonnelInterne]