# apps/commercial/views.py
from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import Lead, EssaiPlanifie, Commande
from .serializers import LeadSerializer, EssaiPlanifieSerializer, CommandeSerializer


class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all().order_by("-created_at")
    serializer_class = LeadSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["statut", "source", "concession"]


class EssaiPlanifieViewSet(viewsets.ModelViewSet):
    queryset = EssaiPlanifie.objects.all().order_by("date_heure")
    serializer_class = EssaiPlanifieSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["concession", "statut", "date_heure"]


class CommandeViewSet(viewsets.ModelViewSet):
    queryset = Commande.objects.all().order_by("-created_at")
    serializer_class = CommandeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["etape", "concession", "type_financement"]